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
        weekdays_day = tracker.get_slot('weekdays_day')
        weekdays_evening = tracker.get_slot('weekdays_evening')

        
        weekends_morning = tracker.get_slot('weekends_morning')
        weekends_day = tracker.get_slot('weekends_day')
        weekends_evening = tracker.get_slot('weekends_evening')

        # "day_time" : [free_at_time, energetic_at_time]
        days = {
        "monday_morning" : [monday_morning, weekdays_morning],
        "monday_midday" : [monday_midday, weekdays_day],
        "monday_afternoon" : [monday_afternoon, weekdays_day],
        "monday_evening" : [monday_evening, weekdays_evening],

        "tuesday_morning" : [tuesday_morning, weekdays_morning],
        "tuesday_midday" : [tuesday_midday, weekdays_day],
        "tuesday_afternoon" : [tuesday_afternoon, weekdays_day],
        "tuesday_evening" : [tuesday_evening, weekdays_evening],

        "wednesday_morning" : [wednesday_morning, weekdays_morning],
        "wednesday_midday" : [wednesday_midday, weekdays_day],
        "wednesday_afternoon" : [wednesday_afternoon, weekdays_day],
        "wednesday_evening" : [wednesday_evening, weekdays_evening],

        "thursday_morning" : [thursday_morning, weekdays_morning],
        "thursday_midday" : [thursday_midday, weekdays_day],
        "thursday_afternoon" : [thursday_afternoon, weekdays_day],
        "thursday_evening" : [thursday_evening, weekdays_evening],

        "friday_morning" : [friday_morning, weekdays_morning],
        "friday_midday" : [friday_midday, weekdays_day],
        "friday_afternoon" : [friday_afternoon, weekdays_day],
        "friday_evening" : [friday_evening, weekdays_evening],

        "saturday_morning" : [saturday_morning, weekends_morning],
        "saturday_midday" : [saturday_midday, weekends_day],
        "saturday_afternoon" : [saturday_afternoon, weekends_day],
        "saturday_evening" : [saturday_evening, weekends_evening],

        "sunday_morning" : [sunday_morning, weekends_morning],
        "sunday_midday" : [sunday_midday, weekends_day],
        "sunday_afternoon" : [sunday_afternoon, weekends_day],
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


        dispatcher.utter_message(text=f"Available slots: {available_timeslots},  Selected slots: {selected}")

        duration_per_timeslot_week_1 = minutes_week_1/4

        selected_times = [time_energy[0] for time_energy in selected]


        dispatcher.utter_message(text=f"""Plan: week 1 - {duration_per_timeslot_week_1} minutes at these time slots: {selected_times} \n week 2 - {math.ceil((minutes_week_1 + weekly_increase)/4)} minutes at these time slots: {selected_times} 
        week 3 - Walking for {(minutes_week_1 + 2* weekly_increase)} minutes across 4 days. \n week 4 - Walking for {(minutes_week_1 + 3* weekly_increase))} minutes across 4 days. 
        Month 2 - Walking for up to {math.ceil((minutes_week_1 + 7* weekly_increase))} minutes per week across 5 days. \n Month 3 - Walking for up to {(minutes_week_1 + 11* weekly_increase)} minutes per week across 6 days.""")

        return []


# class ActionLoadSessionNotFirst(Action):

#     def name(self) -> Text:
#         return "action_load_session_not_first"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
#         prolific_id = tracker.current_state()['sender_id']
#         session_num = tracker.get_slot("session_num")
        
#         session_loaded = True
#         mood_prev = ""
        
#         conn = mysql.connector.connect(
#             user=DATABASE_USER,
#             password=DATABASE_PASSWORD,
#             host=DATABASE_HOST,
#             port=DATABASE_PORT,
#             database='db'
#         )
#         cur = conn.cursor(prepared=True)
        
#         # get user name from database
#         query = ("SELECT name FROM users WHERE prolific_id = %s")
#         cur.execute(query, [prolific_id])
#         user_name_result = cur.fetchone()
        
#         if user_name_result is None:
#             session_loaded = False
            
#         else:
#             user_name_result = user_name_result[0]
            
#             # check if user has done previous session before '
#             # (i.e., if session data is saved from previous session)
#             query = ("SELECT * FROM sessiondata WHERE prolific_id = %s and session_num = %s and response_type = %s")
#             cur.execute(query, [prolific_id, str(int(session_num) - 1), "state_1"])
#             done_previous_result = cur.fetchone()
            
#             if done_previous_result is None:
#                 session_loaded = False
                
#             else:
#                 # check if user has not done this session before
#                 # checks if some data on this session is already saved in database
#                 # this basically means that it checks whether the user has already 
#                 # completed the session part until the dropout question before,
#                 # since that is when we first save something to the database
#                 session_loaded = check_session_not_done_before(cur, prolific_id, 
#                                                                session_num)
                
#                 if session_loaded:
#                     # Get mood from previous session
#                     query = ("SELECT response_value FROM sessiondata WHERE prolific_id = %s and session_num = %s and response_type = %s")
#                     cur.execute(query, [prolific_id, str(int(session_num) - 1), "mood"])
#                     mood_prev = cur.fetchone()[0]
                    
        
#         conn.close()

        
#         return [SlotSet("user_name_slot_not_first", user_name_result),
#                 SlotSet("mood_prev_session", mood_prev),
#                 SlotSet("session_loaded", session_loaded)]
        
        
    
# class ActionSaveNameToDB(Action):

#     def name(self) -> Text:
#         return "action_save_name_to_db"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
#         now = datetime.now()
#         formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')

#         conn = mysql.connector.connect(
#             user=DATABASE_USER,
#             password=DATABASE_PASSWORD,
#             host=DATABASE_HOST,
#             port=DATABASE_PORT,
#             database='db'
#         )
#         cur = conn.cursor(prepared=True)
#         query = "INSERT INTO users(prolific_id, name, time) VALUES(%s, %s, %s)"
#         queryMatch = [tracker.current_state()['sender_id'], 
#                       tracker.get_slot("user_name_slot"),
#                       formatted_date]
#         cur.execute(query, queryMatch)
#         conn.commit()
#         conn.close()

#         return []
    

class ActionSaveActivityExperience(Action):
    def name(self):
        return "action_save_activity_experience"

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
        session_num = tracker.get_slot("session_num")
        
        slots_to_save = ["effort", "activity_experience_slot",
                         "activity_experience_mod_slot",
                         "dropout_response"]
        for slot in slots_to_save:
        
            save_sessiondata_entry(cur, conn, prolific_id, session_num,
                                   slot, tracker.get_slot(slot),
                                   formatted_date)

        conn.close()
    
    
def save_sessiondata_entry(cur, conn, prolific_id, session_num, response_type,
                           response_value, time):
    query = "INSERT INTO sessiondata(prolific_id, session_num, response_type, response_value, time) VALUES(%s, %s, %s, %s, %s)"
    cur.execute(query, [prolific_id, session_num, response_type,
                        response_value, time])
    conn.commit()
    

class ActionSaveSession(Action):
    def name(self):
        return "action_save_session"

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
        session_num = tracker.get_slot("session_num")
        
        slots_to_save = ["mood", "state_1"]
        for slot in slots_to_save:
        
            save_sessiondata_entry(cur, conn, prolific_id, session_num,
                                   slot, tracker.get_slot(slot),
                                   formatted_date)

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
