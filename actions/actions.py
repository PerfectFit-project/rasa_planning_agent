version: "3.1"

intents:
### Session
- start_session1
- confirm_purpose
- confirm_usage
- confirm_intro_session


### dropout
- confirm_dropout


### states
- confirm_state_pa


# propose new activity
- confirm_activity_read


# end session
- confirm_goodbye


entities:


- state_pa:
    influence_conversation: false


- dropout_response:
    influence_conversation: false


slots:
  ### intro/general
  session_loaded:
    type: bool
    influence_conversation: true
    mappings:
    - type: custom


  user_name:
    type: text
    initial_value: ''
    influence_conversation: false
    mappings:
    - type: from_text
      conditions:
        - active_loop: user_name_form


  ### states
  state_pa:
    type: text
    initial_value: ''
    influence_conversation: false
    mappings:
    - type: from_entity
      entity: state_pa


  ### activity experience
  # dropout
  dropout_response:
    type: text
    initial_value: ''
    influence_conversation: false
    mappings:
    - type: from_entity
      entity: dropout_response


responses:


  ### Intro first session
  utter_greet_first_time:
  - text: "Hey there, I'm your virtual coach."


  utter_ask_user_name:
  - text: "How may I call you?"


  utter_confirm_name:
  - text: "Hi {user_name}, it's nice to meet you."


  utter_purpose_1:
  - text: "I have mentioned my name, but let me also tell you bit about what I do: My goal is to help people prepare for quitting smoking. And since becoming more physically active may make it easier to quit smoking, I also want to prepare people for becoming more physically active."


  utter_purpose_2:
  - text: "Why prepare to quit? Because proper preparation can help to quit successfully."


  utter_purpose_3:
  - text: "And how do I prepare people? I propose activities that help build the competencies needed for quitting."


  utter_purpose_4:
  - text: "Ultimately, I want to be able to propose activities that match the situation a person is in."


  utter_purpose_5:
  - buttons:
    - payload: /confirm_purpose
      title: "I'm ready"
    text: "And this is why you are here, {user_name}: I want to learn how an activity I propose helps you in your specific situation.\nLet me know when you have read what my purpose is and are ready to continue."

  utter_explain_purpose:
  - text: "Okay! Before we start, let me explain how you can communicate with me."


  utter_prompt_usage:
  - text: "Okay! Before we start, let me explain how you can communicate with me."


  utter_explain_usage:
  - buttons:
    - payload: /confirm_usage
      title: "Yes, that's clear"
    - payload: /confirm_usage
      title: "Nice, sounds easy enough!"
    text: "Most of the time, you can just click on one of the buttons like you already did. If no buttons appear, just make use of the text field below."


  utter_intro_session_1:
  - text: "Now, let me tell you what we will do in this session."


  utter_intro_session_2:
  - text: "First, I'll ask you a few questions to learn about your current situation with regard to preparing for quitting smoking."


  utter_intro_session_3:
  - text: "Next, I'll recommend you a preparatory activity to do after this and before the next session, which you'll get invited to about 2 days from now."


  utter_intro_session_4:
  - text: "And in the end, I'll briefly tell you about our next session."


  utter_intro_session_5:
  - text: "And don't worry, I'll also send you your activity in a message on Prolific right after this session ends."


  utter_intro_session_6:
  - text: "Please note that doing your recommended activity after this session is voluntary and does not impact your payment."


  utter_intro_session_7:
  - buttons:
    - payload : /confirm_intro_session
      title: "Now"
    text: "Let me know when you've finished reading our plan for today's session."


  ### Ask state questions
  utter_state_pa_question_intro:
  - text: "Now I will ask you a question about your current situation regarding preparing for being more physically active."


  utter_state_question:
  - buttons:
    - payload: /confirm_state_pa{"state_pa":"-5"}
      title: "-5 (make it a lot harder)"
    - payload: /confirm_state_pa{"state_pa":"-4"}
      title: "-4"
    - payload: /confirm_state_pa{"state_pa":"-3"}
      title: "-3"
    - payload: /confirm_state_pa{"state_pa":"-2"}
      title: "-2"
    - payload: /confirm_state_pa{"state_pa":"-1"}
      title: "-1"
    - payload: /confirm_state_pa{"state_pa":"0"}
      title: "0 (neutral)"
    - payload: /confirm_state_pa{"state_pa":"1"}
      title: "1"
    - payload: /confirm_state_pa{"state_pa":"2"}
      title: "2"
    - payload: /confirm_state_pa{"state_pa":"3"}
      title: "3"
    - payload: /confirm_state_pa{"state_pa":"4"}
      title: "4"
    - payload: /confirm_state_pa{"state_pa":"5"}
      title: "5 (make it a lot easier)"
    text: "How do you think do self-confidence and motivation affect quitting smoking?"


  ### Propose activity
  # utter_transition_new_activity:
  #   - text: "Now let's turn our attention to an activity that can benefit your current situation."
  #   - text: "Let's move on to an activity that can support you in your efforts to prepare for quitting smoking."
  #   - text: "Next, we'll take a closer look at an activity that can assist you in preparing to quit smoking."


  # utter_propose_new_activity_intro:
  #   - text: "I think that this activity would be useful for you:"


  # utter_activity:
  #   - text: "I suggest you visualize your desired future self."


  # utter_activity_read:
  #     - text: "I'll continue when you're done reading about your first activity."
  #       buttons:
  #       - payload: /confirm_activity_read
  #         title: "I'm done"

  #   - text: "Use the button below once you've finished reading, then I'll continue."
  #     buttons:
  #     - payload: /confirm_activity_read
  #       title: "Finished!"
  #   - text: "Let me know when you've finished reading the description and we can continue."
  #     buttons:
  #     - payload: /confirm_activity_read
  #       title: "Let's continue"


  # utter_ask_dropout:
  # - text: "Currently you are taking part in a paid experiment. Imagine this was an unpaid smoking cessation program.\nHow likely would you then have quit the program or returned to this session?"
  #   buttons:
  #   - payload: /confirm_dropout{"dropout_response":"-5"}
  #     title: "-5 (definitely would have quit the program)"
  #   - payload: /confirm_dropout{"dropout_response":"-4"}
  #     title: "-4"
  #   - payload: /confirm_dropout{"dropout_response":"-3"}
  #     title: "-3"
  #   - payload: /confirm_dropout{"dropout_response":"-2"}
  #     title: "-2"
  #   - payload: /confirm_dropout{"dropout_response":"-1"}
  #     title: "-1"
  #   - payload: /confirm_dropout{"dropout_response":"0"}
  #     title: "0 (neutral)"
  #   - payload: /confirm_dropout{"dropout_response":"1"}
  #     title: "1"
  #   - payload: /confirm_dropout{"dropout_response":"2"}
  #     title: "2"
  #   - payload: /confirm_dropout{"dropout_response":"3"}
  #     title: "3"
  #   - payload: /confirm_dropout{"dropout_response":"4"}
  #     title: "4"
  #   - payload: /confirm_dropout{"dropout_response":"5"}
  #     title: "5 (definitely would have returned to this session)"


  ### End session
  utter_email_reminder:
    - text: "That's all for this session. I'll be sending you a message with your activity on Prolific right after this session."


  utter_prolific_link:
    - text: "Alright! Then here is your completion link: ... ."


  utter_goodbye:
    - text: "Bye!"
      buttons:
      - payload: /confirm_goodbye
        title: "Goodbye!"


  utter_final_close_session:
  - text: "THIS IS THE END OF THIS SESSION. PLEASE CLOSE THIS WINDOW.\nANY FURTHER TYPING IN THIS CHAT RENDERS THIS SESSION INVALID. IF YOU HAVE QUESTIONS, CONTACT THE RESEARCHER PER MESSAGE ON PROLIFIC."


  ### General
  utter_great:
  - text: Great!
  - text: Perfect!
  - text: Awesome!


  utter_cool:
  - text: Nice!
  - text: Cool!
  - text: Perfect!


  utter_thanks:
  - text: "Thanks!"
  - text: "Thanks for letting me know!"
  - text: "Okay thanks!"
  - text: "Thanks for sharing that with me!"


  utter_provide_more_detail:
  - text: "Hmm, can you describe this in a bit more detail?"
  - text: "I see, could you elaborate a little more on this?"
  - text: "I'd like to understand better, can you give me more details on this?"
  - text: "I'm not quite following, could you provide more details?"


  utter_default:
  - text: "There is a problem with this session."


  utter_default_close_session:
  - text: "PLEASE CLOSE THIS WINDOW AND CONTACT THE RESEARCHER ON PROLIFIC."


  utter_error_close_session:
  - text: "PLEASE CLOSE THIS WINDOW. ANY FURTHER TYPING IN THIS CHAT RENDERS THIS SESSION INVALID."


session_config:
  session_expiration_time: 5  # these are minutes
  carry_over_slots_to_new_session: false


# Needed so that slots can be set via buttons
config:
  store_entities_as_slots: true


forms:
  user_name_form:
    required_slots:
        - user_name


actions:
- action_load_session_first
- validate_user_name_form
- action_end_dialog
- action_default_fallback_end_dialog