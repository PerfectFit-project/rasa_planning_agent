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
import mysql.connector


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

        monday_morning = tracker.get_slot('monday_morning')
        monday_midday = tracker.get_slot('monday_midday')
        monday_afternoon = tracker.get_slot('monday_afternoon')
        monday_evening = tracker.get_slot('monday_evening')

        tuesday_morning = tracker.get_slot('tuesday_morning')
        tuesday_midday = tracker.get_slot('tuesday_midday')
        tuesday_afternoon = tracker.get_slot('tuesday_afternoon')
        tuesday_evening = tracker.get_slot('tuesday_evening')

        wednesday_morning = tracker.get_slot('wednesday_morning')
        wednesday_midday = tracker.get_slot('wednesday_midday')
        wednesday_afternoon = tracker.get_slot('wednesday_afternoon')
        wednesday_evening = tracker.get_slot('wednesday_evening')

        thursday_morning = tracker.get_slot('thursday_morning')
        thursday_midday = tracker.get_slot('thursday_midday')
        thursday_afternoon = tracker.get_slot('thursday_afternoon')
        thursday_evening = tracker.get_slot('thursday_evening')

        friday_morning = tracker.get_slot('friday_morning')
        friday_midday = tracker.get_slot('friday_midday')
        friday_afternoon = tracker.get_slot('friday_afternoon')
        friday_evening = tracker.get_slot('friday_evening')

        saturday_morning = tracker.get_slot('saturday_morning')
        saturday_midday = tracker.get_slot('saturday_midday')
        saturday_afternoon = tracker.get_slot('saturday_afternoon')
        saturday_evening = tracker.get_slot('saturday_evening')

        sunday_morning = tracker.get_slot('sunday_morning')
        sunday_midday = tracker.get_slot('sunday_midday')
        sunday_afternoon = tracker.get_slot('sunday_afternoon')
        sunday_evening = tracker.get_slot('sunday_evening')

        free_times = [monday_morning, monday_midday, monday_afternoon, monday_evening,
        tuesday_morning, tuesday_midday, tuesday_afternoon, tuesday_evening,
        wednesday_morning, wednesday_midday, wednesday_afternoon, wednesday_evening,
        thursday_morning, thursday_midday, thursday_afternoon, thursday_evening,
        friday_morning, friday_midday, friday_afternoon, friday_evening,
        saturday_morning, saturday_midday, saturday_afternoon, saturday_evening,
        sunday_morning, sunday_midday, sunday_afternoon, sunday_evening]

        # energy levels

        weekdays_morning = tracker.get_slot('weekdays_morning')
        weekdays_day = tracker.get_slot('weekdays_day')
        weekdays_evening = tracker.get_slot('weekdays_evening')

        
        weekends_morning = tracker.get_slot('weekends_morning')
        weekends_day = tracker.get_slot('weekends_day')
        weekends_evening = tracker.get_slot('weekends_evening')

        energy_levels = [weekdays_morning, weekdays_day, weekdays_evening
        weekends_morning, weekends_day, weekends_evening]



        dispatcher.utter_message(text=f"Free slots: {free_times}")

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
