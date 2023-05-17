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
from rasa_sdk.events import FollowupAction, SlotSet, UserUttered, ActionExecuted
from time import sleep
from typing import Any, Dict, List, Optional, Text

import collections
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


def check_session_not_done_before(cur, prolific_id):
    
    query = ("SELECT * FROM sessiondata WHERE prolific_id = %s")
    cur.execute(query, [prolific_id])
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

        try:
            conn = mysql.connector.connect(
                user=DATABASE_USER,
                password=DATABASE_PASSWORD,
                host=DATABASE_HOST,
                port=DATABASE_PORT,
                database='db'
            )
            cur = conn.cursor(prepared=True)
    
            session_loaded = check_session_not_done_before(cur, prolific_id)

        except mysql.connector.Error as error:
            logging.info("Error in loading first session: " + str(error))

        finally:
            if conn.is_connected():
                cur.close()
                conn.close()

        return [SlotSet("session_loaded", session_loaded)]

class ActionCheckNumberOfSlots(Action):

    def name(self) -> Text:
        return "action_check_number_of_slots"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # free times

        number_of_timeslots = bool(tracker.get_slot('monday_morning'))+ bool(tracker.get_slot('monday_midday'))+ bool(tracker.get_slot('monday_afternoon'))+ bool(tracker.get_slot('monday_evening')) + bool(tracker.get_slot('tuesday_morning'))+ bool(tracker.get_slot('tuesday_midday'))+ bool(tracker.get_slot('tuesday_afternoon'))+ bool(tracker.get_slot('tuesday_evening')) + bool(tracker.get_slot('wednesday_morning'))+ bool(tracker.get_slot('wednesday_midday'))+ bool(tracker.get_slot('wednesday_afternoon'))+ bool(tracker.get_slot('wednesday_evening')) + bool(tracker.get_slot('thursday_morning'))+ bool(tracker.get_slot('thursday_midday'))+ bool(tracker.get_slot('thursday_afternoon'))+ bool(tracker.get_slot('thursday_evening')) + bool(tracker.get_slot('friday_morning'))+ bool(tracker.get_slot('friday_midday'))+ bool(tracker.get_slot('friday_afternoon'))+ bool(tracker.get_slot('friday_evening')) + bool(tracker.get_slot('saturday_morning'))+ bool(tracker.get_slot('saturday_midday'))+ bool(tracker.get_slot('saturday_afternoon'))+ bool(tracker.get_slot('saturday_evening')) + bool(tracker.get_slot('sunday_morning'))+ bool(tracker.get_slot('sunday_midday'))+ bool(tracker.get_slot('sunday_afternoon'))+ bool(tracker.get_slot('sunday_evening'))  
        
        if number_of_timeslots < 4:

            dispatcher.utter_message(text=f"I'm afraid you would have to do a bit too much activity all at once if we were to plan with your current schedule in mind… Let's think again about the times when you are available. Even if you're free for only 30 minutes or so at that time, that should still be enough to take a short walk.")

            dispatcher.utter_message(text=f"Remember, you have to select at least four time slots when you are free. Also, you'll have to select the times when you are available again, even if you have told me before. I have a bit of a short memory, sorry about that... ")
                
            return [ActionExecuted("action_listen"), UserUttered(text="/retry_time_slots", parse_data={"intent": {"name": "retry_time_slots", "confidence": 1.0}}), 
            SlotSet("monday_morning", False), SlotSet("monday_midday", False), SlotSet("monday_afternoon", False), SlotSet("monday_evening", False),
            SlotSet("tuesday_morning", False), SlotSet("tuesday_midday", False), SlotSet("tuesday_afternoon", False), SlotSet("tuesday_evening", False),
            SlotSet("wednesday_morning", False), SlotSet("wednesday_midday", False), SlotSet("wednesday_afternoon", False), SlotSet("wednesday_evening", False),
            SlotSet("thursday_morning", False), SlotSet("thursday_midday", False), SlotSet("thursday_afternoon", False), SlotSet("thursday_evening", False),
            SlotSet("friday_morning", False), SlotSet("friday_midday", False), SlotSet("friday_afternoon", False), SlotSet("friday_evening", False),
            SlotSet("saturday_morning", False), SlotSet("saturday_midday", False), SlotSet("saturday_afternoon", False), SlotSet("saturday_evening", False),
            SlotSet("sunday_morning", False), SlotSet("sunday_midday", False), SlotSet("sunday_afternoon", False), SlotSet("sunday_evening", False)]

        else:
            dispatcher.utter_message(text=f"Thank you for letting me know when you are available.")
                
            return [ActionExecuted("action_listen"), UserUttered(text="/move_to_energy", parse_data={"intent": {"name": "move_to_energy", "confidence": 1.0}})]


class ActionUtterCorrespondingStrategyForBarrier(Action):

    def name(self) -> Text:
        return "action_utter_corresponding_strategy_for_barrier"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        barrier_type = tracker.get_slot('identified_barrier')

        if barrier_type != "other":
            dispatcher.utter_message(text=f"Okay! Now, you have your approach to this barrier. Here is a strategy I thought about.")

        if barrier_type == "time":
            dispatcher.utter_message(text=f"If you lack the time to do go for regular walks, you could try taking a short walk when you have some free time (during your lunch break, for example)")
        elif barrier_type == "energy":
            dispatcher.utter_message(text=f"In terms of energy, think back to when we talked about when you feel most energetic during the day. Aim to schedule walks at those times, since it will be easier for you that way.")
        elif barrier_type == "people":
            dispatcher.utter_message(text=f"Try to go to the gym when it's a bit quieter if you don't like it when other people can see you doing physical activity. It is not absolutely necessary to go to a gym, especially if you're only taking walks. Try walking in a park nearby or simply on the sidewalk.")
        elif barrier_type == "equipment":
            dispatcher.utter_message(text=f"For walking in particular, the only thing you really need in terms of equipment are shoes that are comfortable for you, so putting aside some money for that can be a relatively simple strategy.")
        elif barrier_type == "family":
            dispatcher.utter_message(text=f"If you have to take care of someone in your family, it might be a good idea to take them on regular walks with you. That way you can fulfill your family obligations and make progress towards your goal.")
        elif barrier_type == "other":
            dispatcher.utter_message(text=f"Okay! Now, you have your approach to this barrier.")
                
        return []

class ActionUtterCorrespondingMessageForPlanningRelevance(Action):

    def name(self) -> Text:
        return "action_utter_corresponding_message_for_planning_relevance"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        relevance = tracker.get_slot('planning_relevance')

        if relevance == "motivation":
            dispatcher.utter_message(text=f"Ultimately, the plan is meant to help you take walks regularly. According to studies in planning for physical activity, rather than relying on spontaneous bursts motivation, having a plan can help give you the cue to start.")
        elif relevance == "habit":
            dispatcher.utter_message(text=f"By creating a plan that is consistent across different weeks, it will be easier for you to form a habit of when you should go for a walk. According to experts in health psychology, a habit can help you reach your goal more easily.")
        elif relevance == "road":
            dispatcher.utter_message(text=f"The plan shows you what you will be able to achieve in the end, so you have an idea of the goal you are working towards. This is helpful in terms of staying consistent with your walking schedule, according to experts in health psychology.")
        elif relevance == "obstacles":
            dispatcher.utter_message(text=f"According to several different studies, planning can help you identify and deal with obstacles that might prevent you from going on your walks.")
            dispatcher.utter_message(text=f"By anticipating these obstacles and devising strategies for overcoming them ahead of time, it will be easier to deal with them when they happen.")
                
        return []

def round_to_nearest_5(n):
    return 5 * round(n / 5)

def round_to_nearest_half(n):
    return round(n * 2.0) / 2.0


class ActionCreateInitialPlan(Action):

    def name(self) -> Text:
        return "action_create_initial_plan"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # goal

        goal = f"{tracker.get_slot('goal')}"

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

        very_high_energy_timeslots = [[available, energy] for [available, energy] in available_timeslots if energy == '4']

        high_energy_timeslots = [[available, energy] for [available, energy] in available_timeslots if energy == '3']

        medium_energy_timeslots = [[available, energy] for [available, energy] in available_timeslots if energy == '2']

        low_energy_timeslots = [[available, energy] for [available, energy] in available_timeslots if energy == '1']

        very_low_energy_timeslots = [[available, energy] for [available, energy] in available_timeslots if energy == '0']

        number_of_very_high_energy_timeslots = len(very_high_energy_timeslots)

        number_of_high_energy_timeslots = len(high_energy_timeslots)

        number_of_medium_energy_timeslots = len(medium_energy_timeslots)

        number_of_low_energy_timeslots = len(low_energy_timeslots)

        number_of_very_low_energy_timeslots = len(very_low_energy_timeslots)

        minutes_week_1 = 120

        if goal == "10000":
            weekly_increase = 20
        elif goal == "11000":
            weekly_increase = 22
        elif goal == "12000":
            weekly_increase = 25
        
        if number_of_timeslots == 4:

            selected =  available_timeslots

        else: 

            select_slots = 4

            if number_of_very_high_energy_timeslots > select_slots:

                selected = random.sample(very_high_energy_timeslots, select_slots)

            else: 

                selected = very_high_energy_timeslots

                select_slots -= number_of_very_high_energy_timeslots

                if number_of_high_energy_timeslots > select_slots:

                    selected += random.sample(high_energy_timeslots, select_slots)

                else:

                    selected += high_energy_timeslots

                    select_slots -= number_of_high_energy_timeslots

                    if number_of_medium_energy_timeslots > select_slots:

                        selected += random.sample(medium_energy_timeslots, select_slots)

                    else:

                        selected += medium_energy_timeslots

                        select_slots -= number_of_medium_energy_timeslots

                        if number_of_low_energy_timeslots > select_slots:

                            selected += random.sample(low_energy_timeslots, select_slots)

                        else:

                            selected += low_energy_timeslots

                            select_slots -= number_of_low_energy_timeslots

                            if select_slots is not 0:
                            
                                selected += random.sample(very_low_energy_timeslots, select_slots)


        # dispatcher.utter_message(text=f"Available slots: {available_timeslots},  Selected slots: {selected}")

        duration_per_timeslot_week_1 = math.ceil(minutes_week_1/4)

        selected_times = [time_energy[0] for time_energy in selected]

        custom_order = {
            "monday_morning": 0, "monday_midday": 1, "monday_afternoon": 2, "monday_evening": 3,
            "tuesday_morning": 4, "tuesday_midday": 5, "tuesday_afternoon": 6, "tuesday_evening": 7,
            "wednesday_morning": 8, "wednesday_midday": 9, "wednesday_afternoon": 10, "wednesday_evening": 11,
            "thursday_morning": 12, "thursday_midday": 13, "thursday_afternoon": 14, "thursday_evening": 15,
            "friday_morning": 16, "friday_midday": 17, "friday_afternoon": 18, "friday_evening": 19,
            "saturday_morning": 20, "saturday_midday": 21, "saturday_afternoon": 22, "saturday_evening": 23,
            "sunday_morning": 24, "sunday_midday": 25, "sunday_afternoon": 26, "sunday_evening": 27
        }

        selected_times.sort(key=lambda x:custom_order[x])

        first = selected_times[0]

        message = f"""Plan 1: Week 1 - {round_to_nearest_5(duration_per_timeslot_week_1)} minutes at these time slots: {selected_times}. Week 2 - {round_to_nearest_5(math.ceil((minutes_week_1 + weekly_increase)/4))} minutes at these time slots: {selected_times}. Week 3 - Walking for {round_to_nearest_half((minutes_week_1 + 2* weekly_increase)/60.0)} hours, distributed across 4 time slots. Week 4 - Walking for {round_to_nearest_half((minutes_week_1 + 3* weekly_increase)/60.0)} hours, distributed across 4 time slots. Month 2 - Walking for up to {round_to_nearest_half((minutes_week_1 + 7* weekly_increase)/60.0)} hours per week, distributed across 5 time slots. Month 3 - Walking for up to {round_to_nearest_half((minutes_week_1 + 11* weekly_increase)/60.0)} hours per week, distributed across 6 time slots."""

        dispatcher.utter_message(text=message)

        return [SlotSet("plan_1", message), SlotSet("plan_check_week_3", f"{round_to_nearest_half((minutes_week_1 + 2* weekly_increase)/60.0)}"), SlotSet("plan_check_first_walk", first)]

    
    
def save_sessiondata_entry(cur, conn, prolific_id, time, event):
    query = "INSERT INTO sessiondata(prolific_id, time, event) VALUES(%s, %s, %s)"
    cur.execute(query, [prolific_id, time, event])
    conn.commit()
    

class ActionSaveEventState(Action):
    def name(self):
        return "action_save_event_state"

    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        now = datetime.now()
        formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')

        try:
            conn = mysql.connector.connect(
                user=DATABASE_USER,
                password=DATABASE_PASSWORD,
                host=DATABASE_HOST,
                port=DATABASE_PORT,
                database='db'
            )
            cur = conn.cursor(prepared=True)
            
            prolific_id = tracker.current_state()['sender_id']

            ch = tracker.get_slot("changes_to_plan")

            c = tracker.get_slot("confidence")

            pu = tracker.get_slot("perceived_usefulness")

            a = tracker.get_slot("attitude")

            explain_planning = tracker.get_slot("explain_planning")

            identify_barriers = tracker.get_slot("identify_barriers")

            deal_with_barriers = tracker.get_slot("deal_with_barriers")

            show_testimonials = tracker.get_slot("show_testimonials")

            state = f"{ch}, {c}, {pu}, {a}, {explain_planning}, {identify_barriers}, {deal_with_barriers}, {show_testimonials}"

            save_sessiondata_entry(cur, conn, prolific_id, formatted_date, f"state: {state}")

        except mysql.connector.Error as error:
            logging.info("Error in saving event stateto db: " + str(error))

        finally:
            if conn.is_connected():
                cur.close()
                conn.close()
        
        return []

class ActionCheckDialogueDone(Action):
    def name(self):
        return "action_check_dialogue_done"

    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:


        # check how many actions have been done
        # after 2 actions, we can end the dialogue if states are good

        changes_to_plan = int(tracker.get_slot("changes_to_plan"))

        explain_planning = tracker.get_slot("explain_planning")

        identify_barriers = tracker.get_slot("identify_barriers")

        deal_with_barriers = tracker.get_slot("deal_with_barriers")

        show_testimonials = tracker.get_slot("show_testimonials")

        num_actions = changes_to_plan + explain_planning + identify_barriers + deal_with_barriers + show_testimonials

        if num_actions >= 2:

            c = tracker.get_slot("confidence")

            pu = tracker.get_slot("perceived_usefulness")

            a = tracker.get_slot("attitude")

            if c in ["medium", "high"] and (pu == "high" or a == "high"):
                
                end = True

            else:
                end = False
            
            if end:

                return [ActionExecuted("action_listen"), UserUttered(text="/confirm_actions_done", parse_data={"intent": {"name": "confirm_actions_done", "confidence": 1.0}})] 
        
        return[ActionExecuted("action_listen"), UserUttered(text="/confirm_continue_dialogue", parse_data={"intent": {"name": "confirm_continue_dialogue", "confidence": 1.0}})]

class ActionSelectAction(Action):
    def name(self):
        return "action_select_action"

    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:

            conn = mysql.connector.connect(
                user=DATABASE_USER,
                password=DATABASE_PASSWORD,
                host=DATABASE_HOST,
                port=DATABASE_PORT,
                database='db'
            )
            cur = conn.cursor(prepared=True)

            now = datetime.now()
            formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
            
            prolific_id = tracker.current_state()['sender_id']

            changes_to_plan = int(tracker.get_slot("changes_to_plan"))

            explain_planning = tracker.get_slot("explain_planning")

            identify_barriers = tracker.get_slot("identify_barriers")

            deal_with_barriers = tracker.get_slot("deal_with_barriers")

            show_testimonials = tracker.get_slot("show_testimonials")

            last_action = tracker.get_slot("last_action")

            number_actions = changes_to_plan + explain_planning + identify_barriers + deal_with_barriers + show_testimonials

            possible_actions = []

            # this corresponds to having done 3 actions, none of which were changes to the plan
            # if we do the 4th action that is not a change to the plan, then we have to do changes to plans in turns 5 and 6
            # that shouldn't happen, since we don't want to make changes to plans twice in a row
            if number_actions == 3 and changes_to_plan == 0:
                possible_actions = ["changes_to_plan"]
            else:
                # we want to make at most 2 changes to the initial plan and to not change the plan twice in a row
                if last_action != "changes_to_plan" and changes_to_plan<=1:
                    possible_actions.append("changes_to_plan")
                # we want to explain planning only once
                if explain_planning == False:
                    possible_actions.append("explain_planning")
                # we want to identify barriers only once
                if identify_barriers == False:
                    possible_actions.append("identify_barriers")
                # we can only deal with barriers after we have identified them and we want to do this only once
                if deal_with_barriers == False and identify_barriers == True:
                    possible_actions.append("deal_with_barriers")
                # we want to show testimonials only once
                if show_testimonials == False:
                    possible_actions.append("show_testimonials")

            # there are no actions that we cannot do
            # this means we have already done all the 6 possible actions
            if len(possible_actions) == 0:
                return [ActionExecuted("action_listen"), UserUttered(text="/confirm_actions_done", parse_data={"intent": {"name": "confirm_actions_done", "confidence": 1.0}}), SlotSet("actions_done", True)]

            # pick the action that was done the least for this state

            ch = tracker.get_slot("changes_to_plan")

            c = tracker.get_slot("confidence")

            pu = tracker.get_slot("perceived_usefulness")

            a = tracker.get_slot("attitude")

            # build current state
            state = f"{ch}, {c}, {pu}, {a}, {explain_planning}, {identify_barriers}, {deal_with_barriers}, {show_testimonials}"

            query = ("SELECT * FROM state_action_state WHERE state_before = %s")
            
            cur.execute(query, [state])
            
            # retrieve all database entries which have an action taken from this state
            result = cur.fetchall()

        # select only the actions in the database results
            actions = [f"{action}" for (userid,date,state,action,next_state) in result]

            # count how many times each action was done
            count = collections.Counter(actions)

            # order the count such that the most frequently done action is first
            ordered = list(count.most_common())

            cleaned = []

            # remove actions that cannot be done from this state (should never happen, but it's safer this way)
            for (ordered_action, frequency) in ordered:
                if ordered_action in possible_actions:
                    cleaned.append((ordered_action, frequency))      

            # if there are possible actions for this state that have never been done, add them to the list with them being done 0 times
            for possible_action in possible_actions:
                if not possible_action in [action for (action,frequency) in cleaned]:
                    cleaned.append((possible_action, 0))
            
            # figure out how many times he least frequent action was done
            least_frequent = min(cleaned, key = lambda x: x[1])[1]

            # pick a random action from the ones that have been done the least
            pick_from = [action for (action,frequency) in cleaned if frequency == least_frequent]

            picked = random.choice(pick_from)

            if picked == "explain_planning":

                return[ActionExecuted("action_listen"), UserUttered(text="/do_explain_planning", parse_data={"intent": {"name": "do_explain_planning", "confidence": 1.0}}), SlotSet("action", picked)]

            elif picked == "identify_barriers":

                return[ActionExecuted("action_listen"), UserUttered(text="/do_identify_barriers", parse_data={"intent": {"name": "do_identify_barriers", "confidence": 1.0}}), SlotSet("action", picked)]

            elif picked == "deal_with_barriers":

                return[ActionExecuted("action_listen"), UserUttered(text="/do_deal_with_barriers", parse_data={"intent": {"name": "do_deal_with_barriers", "confidence": 1.0}}), SlotSet("action", picked)]

            elif picked == "show_testimonials":

                return[ActionExecuted("action_listen"), UserUttered(text="/do_show_testimonials", parse_data={"intent": {"name": "do_show_testimonials", "confidence": 1.0}}), SlotSet("action", picked)]

            elif picked == "changes_to_plan":

                return[ActionExecuted("action_listen"), UserUttered(text="/do_changes_to_plan", parse_data={"intent": {"name": "do_changes_to_plan", "confidence": 1.0}}), SlotSet("action", picked)]

        except mysql.connector.Error as error:
            logging.info("Error in selecting action based on db data: " + str(error))
        
        finally:
            if conn.is_connected():
                cur.close()
                conn.close()
        
        return []


class ActionSaveAction(Action):
    def name(self):
        return "action_save_action"

    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        
        try:
            conn = mysql.connector.connect(
                user=DATABASE_USER,
                password=DATABASE_PASSWORD,
                host=DATABASE_HOST,
                port=DATABASE_PORT,
                database='db'
            )
            cur = conn.cursor(prepared=True)

            now = datetime.now()
            formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')

            prolific_id = tracker.current_state()['sender_id']

            changes_to_plan = int(tracker.get_slot("changes_to_plan"))

            action = tracker.get_slot("action")

            save_sessiondata_entry(cur, conn, prolific_id, formatted_date, f"action: {action}")

            conn.close()

            # check how many actions have been done
            # after actions 2 and 4, show a meta utterance saying that we repeat the state questions

            changes_to_plan = int(tracker.get_slot("changes_to_plan"))

            explain_planning = tracker.get_slot("explain_planning")

            identify_barriers = tracker.get_slot("identify_barriers")

            deal_with_barriers = tracker.get_slot("deal_with_barriers")

            show_testimonials = tracker.get_slot("show_testimonials")

            num_actions = changes_to_plan + explain_planning + identify_barriers + deal_with_barriers + show_testimonials

            if num_actions == 2:

                dispatcher.utter_message(text="I am going to ask the three questions regarding your situation again.")

            elif num_actions == 4:

                dispatcher.utter_message(text="I will once again ask you three questions about your situation.")
            


            if action == "changes_to_plan":
                
                changes_to_plan += 1

                return [ActionExecuted("action_listen"), UserUttered(text="/confirm_state", parse_data={"intent": {"name": "confirm_state", "confidence": 1.0}}),SlotSet("changes_to_plan", f"{changes_to_plan}"), SlotSet("last_action", "changes_to_plan")]

            else:

                return [SlotSet(action, True), SlotSet("last_action", action)]

        except mysql.connector.Error as error:
            logging.info("Error in saving action to db: " + str(error))

        finally:
            if conn.is_connected():
                cur.close()
                conn.close()

        return []


def save_goal_plans_and_reward_to_db(cur, conn, prolific_id, time, goal, plan_1, plan_2, plan_3, reward):
    query = "INSERT INTO users(prolific_id, time, goal, plan_1, plan_2, plan_3, reward) VALUES(%s, %s, %s, %s, %s, %s, %s)"
    cur.execute(query, [prolific_id, time, goal, plan_1, plan_2, plan_3, reward])
    conn.commit()

class ActionSaveGoalPlansAndReward(Action):
    def name(self):
        return "action_save_goal_plans_and_reward"

    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        now = datetime.now()
        formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')

        try:

            conn = mysql.connector.connect(
                user=DATABASE_USER,
                password=DATABASE_PASSWORD,
                host=DATABASE_HOST,
                port=DATABASE_PORT,
                database='db'
            )
            cur = conn.cursor(prepared=True)
            
            prolific_id = tracker.current_state()['sender_id']

            goal = tracker.get_slot("goal")

            plan_1 = tracker.get_slot("plan_1")

            plan_2 = tracker.get_slot("plan_2")

            plan_3 = tracker.get_slot("plan_3")

            satisfaction = tracker.get_slot("satisfaction")

            commitment_1 = tracker.get_slot("commitment_1")

            commitment_f = tracker.get_slot("commitment_f")

            confidence_goal = tracker.get_slot("confidence_goal")

            reward = f"Reward: satifaction = {satisfaction}, commitment_1 = {commitment_1}, commitment_f = {commitment_f}, confidence_goal = {confidence_goal}"

            save_goal_plans_and_reward_to_db(cur, conn, prolific_id, formatted_date, goal, plan_1, plan_2, plan_3, reward)

        except mysql.connector.Error as error:
            logging.info("Error in saving name to db: " + str(error))

        finally:
            if conn.is_connected():
                cur.close()
                conn.close()

        return []

class ActionConvertDBToStateActionNextState(Action):
    def name(self):
        return "action_rearrange_db"

    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            conn = mysql.connector.connect(
                user=DATABASE_USER,
                password=DATABASE_PASSWORD,
                host=DATABASE_HOST,
                port=DATABASE_PORT,
                database='db'
            )
            cur = conn.cursor(prepared=True)
            
            prolific_id = tracker.current_state()['sender_id']

            query = ("SELECT * FROM sessiondata WHERE prolific_id = %s")
            
            cur.execute(query, [prolific_id])
            
            result = cur.fetchall()

            for row in result[:-1:2]:
        
                i = result.index(row)
                
                state_before = row[2].split("state: ")[1]
                
                action = result[i+1][2].split("action: ")[1]
                
                state_after = result[i+2][2].split("state: ")[1]

                time = result[i+2][1]

                query = "INSERT INTO state_action_state(prolific_id, time, state_before, action, state_after) VALUES(%s, %s, %s, %s, %s)"
                cur.execute(query, [prolific_id, time, state_before, action, state_after])
                conn.commit()

        except mysql.connector.Error as error:
            logging.info("Error in saving name to db: " + str(error))

        finally:
            if conn.is_connected():
                cur.close()
                conn.close()

        return []

class ActionShowTestimonials(Action):
    def name(self):
        return "action_show_testimonials"

    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            testimonials = ["Here is how this person introduces themselves: 'Hello. I know I'm thin, but I have great stamina. I'm a big Pokémon go fan. I walk for 2 hours every day to collect as many virtual Pokémon as possible.' This person achieved the following goal: 'I think the best sport for me is walking. I walked 3.000 km last year. I played games and did sports. I achieved this by walking every day for 2 hours, that's about 8 km a day.' ",
                            "Here is how this person introduces themselves: 'Hi, I am very interested in exchanging our experiences. I run to increase my resistance.' This person achieved the following goal: 'I ran every day for 30 minutes. I achieved this by running every day for 30 minutes at least.' ",
                            "Here is how this person introduces themselves: 'I had been a bit of a couch potato before early retirement, however, during the last year I have taken up walking.' This person achieved the following goal: 'I reached over 10.000 steps in 24 hours. I achieved this by walking daily along beaches and in forests.' ",
                            "Here is how this person introduces themselves: 'I really like cycling on the weekends. I don't always feel like running so I try to sprint every time. If I'm able to I always walk to my destination.' This person achieved the following goal: 'I ran 100m in 12 seconds. I achieved this by sprinting 3 times a week.' ",
                            "Here is how this person introduces themselves: 'I really like to run and be active. I like going to the gym as well. I like challenges.' This person achieved the following goal: 'My goal was to run 10 km in under 40 minutes. I achieved this by training every day for a year.' ",
                            "Here is how this person introduces themselves: 'I'm 51, not really physically fit but trying. I've set myself walking and jogging goals through lockdown which I've achieved.' This person achieved the following goal: 'I walked and ran more during lockdown. I achieved this by walking more through lockdown, especially in the morning.' ",
                            "Here is how this person introduces themselves: 'I like to walk for an hour every day. I am looking to get back into table tennis weekly.' This person achieved the following goal: 'I have walked for an hour every day. I achieved this by writing a schedule every day and making sure to incorporate it into the framework.' ",
                            "Here is how this person introduces themselves: 'Hello, my name is Joseph and I'm a 29-year-old man who loves to run. I like outdoor running and I exercise 3-5 times per week.' This person achieved the following goal: 'I pushed myself to be able to run for a longer time with fewer pauses. I achieved this by keeping up with my running schedule. I ran faster to push myself. I ate better food and tried to eat at good times.' "
                            ]

            testimonials_to_show = random.sample(testimonials, 2)

            split_on =" This person achieved the following goal:"

            testimonial_1_intro = testimonials_to_show[0].split(split_on)[0]

            testimonial_1_body = f"This person achieved the following goal:{testimonials_to_show[0].split(split_on)[1]}"

            testimonial_2_intro = testimonials_to_show[1].split(split_on)[0]

            testimonial_2_body = f"This person achieved the following goal:{testimonials_to_show[1].split(split_on)[1]}"

            return [SlotSet("testimonial_1_intro", testimonial_1_intro), SlotSet("testimonial_1_body", testimonial_1_body), SlotSet("testimonial_2_intro", testimonial_2_intro), SlotSet("testimonial_2_body", testimonial_2_body)]