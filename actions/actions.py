# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from datetime import datetime
from definitions import (DATABASE_HOST, DATABASE_PASSWORD, 
                         DATABASE_PORT, DATABASE_USER)
from rasa_sdk import Action, FormValidationAction, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import FollowupAction, SlotSet
from typing import Any, Dict, List, Optional, Text

import logging
import math
import mysql.connector
import random


class ActionEndDialog(Action):
    """Action to cleanly terminate the dialog."""
    # ATM this action just call the default restart action
    # but this can be used to perform actions that might be needed
    # at the end of each dialog
    def name(self):
        return "action_end_dialog"

    async def run(self, dispatcher, tracker, domain):

        return [FollowupAction('action_restart')]
    

class ActionDefaultFallbackEndDialog(Action):
    """Executes the fallback action and goes back to the previous state
    of the dialogue"""

    def name(self) -> Text:
        return "action_default_fallback_end_dialog"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(template="utter_default")
        dispatcher.utter_message(template="utter_default_close_session")

        # End the dialog, which leads to a restart.
        return [FollowupAction('action_end_dialog')]


def get_latest_bot_utterance(events) -> Optional[Any]:
    """
       Get the latest utterance sent by the VC.
        Args:
            events: the events list, obtained from tracker.events
        Returns:
            The name of the latest utterance
    """
    events_bot = []

    for event in events:
        if event['event'] == 'bot':
            events_bot.append(event)

    if (len(events_bot) != 0
            and 'metadata' in events_bot[-1]
            and 'utter_action' in events_bot[-1]['metadata']):
        last_utterance = events_bot[-1]['metadata']['utter_action']
    else:
        last_utterance = None

    return last_utterance


def check_session_not_done_before(cur, prolific_id, session_num):
    
    query = ("SELECT * FROM sessiondata WHERE prolific_id = %s and session_num = %s")
    cur.execute(query, [prolific_id, session_num])
    done_before_result = cur.fetchone()
    
    not_done_before = True

    # user has done the session before
    if done_before_result is not None:
        not_done_before = False
        
    return not_done_before
    


class ActionLoadSessionFirst(Action):
    
    def name(self) -> Text:
        return "action_load_session_first"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
    
        prolific_id = tracker.current_state()['sender_id']
        
        conn = mysql.connector.connect(
            user=DATABASE_USER,
            password=DATABASE_PASSWORD,
            host=DATABASE_HOST,
            port=DATABASE_PORT,
            database='db'
        )
        cur = conn.cursor(prepared=True)
        
        session_loaded = check_session_not_done_before(cur, prolific_id, 1)
        
        conn.close()

        return [SlotSet("session_loaded", session_loaded)]

def round_to_nearest_5(n):
    return 5 * round(n / 5)


class ActionCreateInitialPlan(Action):

    def name(self) -> Text:
        return "action_create_initial_plan"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # goal

        goal = tracker.get_slot('goal')

        # free times

        monday_morning = bool(tracker.get_slot('monday_morning'))
        monday_midday = bool(tracker.get_slot('monday_midday'))
        monday_afternoon = bool(tracker.get_slot('monday_afternoon'))
        monday_evening = bool(tracker.get_slot('monday_evening'))

        tuesday_morning = bool(tracker.get_slot('tuesday_morning'))
        tuesday_midday = bool(tracker.get_slot('tuesday_midday'))
        tuesday_afternoon = bool(tracker.get_slot('tuesday_afternoon'))
        tuesday_evening = bool(tracker.get_slot('tuesday_evening'))

        wednesday_morning = bool(tracker.get_slot('wednesday_morning'))
        wednesday_midday = bool(tracker.get_slot('wednesday_midday'))
        wednesday_afternoon = bool(tracker.get_slot('wednesday_afternoon'))
        wednesday_evening = bool(tracker.get_slot('wednesday_evening'))

        thursday_morning = bool(tracker.get_slot('thursday_morning'))
        thursday_midday = bool(tracker.get_slot('thursday_midday'))
        thursday_afternoon = bool(tracker.get_slot('thursday_afternoon'))
        thursday_evening = bool(tracker.get_slot('thursday_evening'))

        friday_morning = bool(tracker.get_slot('friday_morning'))
        friday_midday = bool(tracker.get_slot('friday_midday'))
        friday_afternoon = bool(tracker.get_slot('friday_afternoon'))
        friday_evening = bool(tracker.get_slot('friday_evening'))

        saturday_morning = bool(tracker.get_slot('saturday_morning'))
        saturday_midday = bool(tracker.get_slot('saturday_midday'))
        saturday_afternoon = bool(tracker.get_slot('saturday_afternoon'))
        saturday_evening = bool(tracker.get_slot('saturday_evening'))

        sunday_morning = bool(tracker.get_slot('sunday_morning'))
        sunday_midday = bool(tracker.get_slot('sunday_midday'))
        sunday_afternoon = bool(tracker.get_slot('sunday_afternoon'))
        sunday_evening = bool(tracker.get_slot('sunday_evening'))

        # energy levels

        weekdays_morning = tracker.get_slot('weekdays_morning')
        weekdays_midday = tracker.get_slot('weekdays_midday')
        weekdays_afternoon = tracker.get_slot('weekdays_afternoon')
        weekdays_evening = tracker.get_slot('weekdays_evening')

        
        weekends_morning = tracker.get_slot('weekends_morning')
        weekends_midday = tracker.get_slot('weekends_midday')
        weekends_afternoon = tracker.get_slot('weekends_afternoon')
        weekends_evening = tracker.get_slot('weekends_evening')

        # "day_time" : [free_at_time, energetic_at_time]
        days = {
        "monday_morning" : [monday_morning, weekdays_morning],
        "monday_midday" : [monday_midday, weekdays_midday],
        "monday_afternoon" : [monday_afternoon, weekdays_afternoon],
        "monday_evening" : [monday_evening, weekdays_evening],

        "tuesday_morning" : [tuesday_morning, weekdays_morning],
        "tuesday_midday" : [tuesday_midday, weekdays_midday],
        "tuesday_afternoon" : [tuesday_afternoon, weekdays_afternoon],
        "tuesday_evening" : [tuesday_evening, weekdays_evening],

        "wednesday_morning" : [wednesday_morning, weekdays_morning],
        "wednesday_midday" : [wednesday_midday, weekdays_midday],
        "wednesday_afternoon" : [wednesday_afternoon, weekdays_afternoon],
        "wednesday_evening" : [wednesday_evening, weekdays_evening],

        "thursday_morning" : [thursday_morning, weekdays_morning],
        "thursday_midday" : [thursday_midday, weekdays_midday],
        "thursday_afternoon" : [thursday_afternoon, weekdays_afternoon],
        "thursday_evening" : [thursday_evening, weekdays_evening],

        "friday_morning" : [friday_morning, weekdays_morning],
        "friday_midday" : [friday_midday, weekdays_midday],
        "friday_afternoon" : [friday_afternoon, weekdays_afternoon],
        "friday_evening" : [friday_evening, weekdays_evening],

        "saturday_morning" : [saturday_morning, weekends_morning],
        "saturday_midday" : [saturday_midday, weekends_midday],
        "saturday_afternoon" : [saturday_afternoon, weekends_afternoon],
        "saturday_evening" : [saturday_evening, weekends_evening],

        "sunday_morning" : [sunday_morning, weekends_morning],
        "sunday_midday" : [sunday_midday, weekends_midday],
        "sunday_afternoon" : [sunday_afternoon, weekends_afternoon],
        "sunday_evening" : [sunday_evening, weekends_evening]
        }

        available_timeslots = [[day, days[day][1]] for day in days if days[day][0] == True]

        number_of_timeslots = len(available_timeslots) 

        high_energy_timeslots = [[available, energy] for [available, energy] in available_timeslots if energy == '3']

        medium_energy_timeslots = [[available, energy] for [available, energy] in available_timeslots if energy == '2']

        low_energy_timeslots = [[available, energy] for [available, energy] in available_timeslots if energy == '1']

        number_of_high_energy_timeslots = len(high_energy_timeslots)

        number_of_medium_energy_timeslots = len(medium_energy_timeslots)

        number_of_low_energy_timeslots = len(low_energy_timeslots)

        minutes_week_1 = 120

        if goal == "low":
            weekly_increase = 20
        elif goal == "medium":
            weekly_increase = 22
        elif goal == "high":
            weekly_increase = 25

        if number_of_timeslots < 4:
            
            dispatcher.utter_message(text=f"I'm afraid you would have to do a bit too much activity all at once if we were to plan with your current schedule in mind… Let's think again about the times when you are available. Even if you're free for only 30 minutes or so at that time, that should still be enough to take a short walk.  [Handle this case later by going back to selecting time slots].")
            
            return []

        elif number_of_timeslots == 4:

            selected =  available_timeslots

        else: 

            select_slots = 4

            if number_of_high_energy_timeslots > select_slots:

                selected = random.sample(high_energy_timeslots, select_slots)

            else: 

                selected = high_energy_timeslots

                select_slots -= number_of_high_energy_timeslots

                if number_of_medium_energy_timeslots > select_slots:

                    selected += random.sample(medium_energy_timeslots, select_slots)

                else:

                    selected += medium_energy_timeslots

                    select_slots -= number_of_medium_energy_timeslots

                    if select_slots is not 0:
                        
                        selected += random.sample(low_energy_timeslots, select_slots)


        # dispatcher.utter_message(text=f"Available slots: {available_timeslots},  Selected slots: {selected}")

        duration_per_timeslot_week_1 = math.ceil(minutes_week_1/4)

        selected_times = [time_energy[0] for time_energy in selected]


        dispatcher.utter_message(text=f"""Plan: Week 1 - {round_to_nearest_5(duration_per_timeslot_week_1)} minutes at these time slots: {selected_times}. Week 2 - {round_to_nearest_5(math.ceil((minutes_week_1 + weekly_increase)/4))} minutes at these time slots: {selected_times}. Week 3 - Walking for {round_to_nearest_5(minutes_week_1 + 2* weekly_increase)} minutes across 4 days. Week 4 - Walking for {round_to_nearest_5(minutes_week_1 + 3* weekly_increase)} minutes across 4 days. Month 2 - Walking for up to {round_to_nearest_5(minutes_week_1 + 7* weekly_increase)} minutes per week across 5 days. Month 3 - Walking for up to {round_to_nearest_5(minutes_week_1 + 11* weekly_increase)} minutes per week across 6 days.""")

        return []

    
    
def save_sessiondata_entry(cur, conn, prolific_id, time, event, session_num):
    query = "INSERT INTO sessiondata(prolific_id, time, event, session_num) VALUES(%s, %s, %s, %s, %s, %s)"
    cur.execute(query, [prolific_id, time, event, session_num])
    conn.commit()
    

class ActionSaveEventState(Action):
    def name(self):
        return "action_save_event_state"

    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        now = datetime.now()
        formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')

        conn = mysql.connector.connect(
            user=DATABASE_USER,
            password=DATABASE_PASSWORD,
            host=DATABASE_HOST,
            port=DATABASE_PORT,
            database='db'
        )
        cur = conn.cursor(prepared=True)
        
        prolific_id = tracker.current_state()['sender_id']

        c = tracker.get_slot("confidence")

        pu_1 = tracker.get_slot("perceived")

        a = tracker.get_slot("attitude")

        state = f"{c}, {pu}, {a}"

        dispatcher.utter_message(text="I am going to save the state to the database.")

        save_sessiondata_entry(cur, conn, prolific_id, formatted_date, state, 1)

        dispatcher.utter_message(text="I have saved the state to the database.")

        conn.close()
        
        return []
    
class ActionSaveEventAction(Action):
    def name(self):
        return "action_save_event_action"

    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        now = datetime.now()
        formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')

        conn = mysql.connector.connect(
            user=DATABASE_USER,
            password=DATABASE_PASSWORD,
            host=DATABASE_HOST,
            port=DATABASE_PORT,
            database='db'
        )
        cur = conn.cursor(prepared=True)
        
        prolific_id = tracker.current_state()['sender_id']

        action = "placeholder"

        dispatcher.utter_message(text="I am going to save the action to the database.")

        save_sessiondata_entry(cur, conn, prolific_id, formatted_date, action, 1)

        dispatcher.utter_message(text="I have saved the action to the database.")

        conn.close()
        
        return []

# class ValidateActivityExperienceForm(FormValidationAction):
#     def name(self) -> Text:
#         return 'validate_activity_experience_form'

#     def validate_activity_experience_slot(
#             self, value: Text, dispatcher: CollectingDispatcher,
#             tracker: Tracker, domain: Dict[Text, Any]) -> Dict[Text, Any]:
#         # pylint: disable=unused-argument
#         """Validate activity_experience_slot input."""
#         last_utterance = get_latest_bot_utterance(tracker.events)

#         if last_utterance != 'utter_ask_activity_experience_slot':
#             return {"activity_experience_slot": None}

#         # people should either type "none" or say a bit more
#         if not (len(value) >= 10 or "none" in value.lower()):
#             dispatcher.utter_message(response="utter_provide_more_detail")
#             return {"activity_experience_slot": None}

#         return {"activity_experience_slot": value}
    

# class ValidateActivityExperienceModForm(FormValidationAction):
#     def name(self) -> Text:
#         return 'validate_activity_experience_mod_form'

#     def validate_activity_experience_mod_slot(
#             self, value: Text, dispatcher: CollectingDispatcher,
#             tracker: Tracker, domain: Dict[Text, Any]) -> Dict[Text, Any]:
#         # pylint: disable=unused-argument
#         """Validate activity_experience_mod_slot input."""
#         last_utterance = get_latest_bot_utterance(tracker.events)

#         if last_utterance != 'utter_ask_activity_experience_mod_slot':
#             return {"activity_experience_mod_slot": None}

#         # people should either type "none" or say a bit more
#         if not (len(value) >= 5 or "none" in value.lower()):
#             dispatcher.utter_message(response="utter_provide_more_detail")
#             return {"activity_experience_mod_slot": None}

#         return {"activity_experience_mod_slot": value}
