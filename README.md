# rasa_example_project
Example for setting up a conversational agent based on Rasa Open Source on a Google Compute Engine instance. The conversational agent in this example interacts with people in 5 conversational sessions.

Based on this Github repository (https://github.com/AmirStudy/Rasa_Deployment) as well as the work by Tom Jacobs (https://github.com/TomJ-EU/rasa/tree/dev).


## Components

This virtual coach consists of a backend based on Rasa Open Source (backend), a custom action server (actions), a frontend (frontend), a database (db), an SQLTrackerStore, and Nginx.


## Setup on Google Compute Engine

To run this project on a Google Compute Engine, I followed these steps:

   - Create a Google Compute Engine instance:
	  - Use Ubuntu 20.04.
	  - Make sure that the location is in Europe.
	  - Enable http and https traffic.
	  - Choose a small instance for the start, since you have to pay more for larger instances. I started with an e2-medium machine type and 100GB for the boot disk.
	  - The first 3 months you have some free credit.
      - Follow the instructions from [here](https://github.com/AmirStudy/Rasa_Deployment) in the sense that you “allow full access to all cloud APIs” on the Google Compute Engine instance. This is shown in this video: https://www.youtube.com/watch?v=qOHszxJsuGs&ab_channel=JiteshGaikwad. Also see this screenshot:
   
      <img src = "Readme_images/allow_full_access.PNG" width = "500" title="Allowing full access to all cloud APIs.">
   
   - Open port 5005 for tcp on the Compute Engine instance:
	
   <img src = "Readme_images/firewall_rule.PNG" width = "500" title="Creating a firewall rule.">
	
   <img src = "Readme_images/firewall_rule_0.PNG" width = "250" title="Creating a firewall rule 0.">
	
   <img src = "Readme_images/firewall_rule_1.PNG" width = "500" title="Creating a firewall rule 1.">
	
   <img src = "Readme_images/firewall_rule_2.PNG" width = "250" title="Creating a firewall rule 2.">
   
   <img src = "Readme_images/firewall_rule_3.PNG" width = "250" title="Creating a firewall rule 3.">
	
   - Follow the instructions from [here](https://github.com/AmirStudy/Rasa_Deployment) for installing Docker on the Google Compute Engine instance. You can do this via the command line that opens after you click on "SSH":
   
   <img src = "Readme_images/ssh.PNG" width = "250" title="Connect via SSH.">
	
   - Install docker-compose on the instance:
	  - I followed the steps described [here](https://levelup.gitconnected.com/the-easiest-docker-docker-compose-setup-on-compute-engine-ec171c09a29a):
	     - `curl -L "https://github.com/docker/compose/releases/download/1.26.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose`
	     - `chmod +x /usr/local/bin/docker-compose`
	     - You might need to add `sudo` in front of the commands to make them work.
   - I suggest getting a static IP address for your Google Compute Engine instance:
      - Follow the instructions here: https://cloud.google.com/compute/docs/ip-addresses/reserve-static-external-ip-address.
	  - You have to pay for every month, but it is rather cheap.
   - Make sure you turn off your instance whenever you do not need it, as you are charged for the time that it is up.
   - Create your own branch/fork from this project.
   - If you are NOT using Nginx, set the IP address of your Google Compute Engine instance in the function `send(message)` in the file frontend/static/js/script.js: `url: "http://<your_instance_IP>:5005/webhooks/rest/webhook"`.
      - When you run the project locally, use `url: "http://localhost:5005/webhooks/rest/webhook"`.
   - Clone your project from Github on the Google Compute Engine instance.
   - Navigate to your project folder on the Compute Engine instance and start your project with `docker-compose up`.
   - Check if all your containers are running on your Google Compute Engine instance via `docker container ls`.
   - You can access the frontend from your browser via `http://<your_instance_IP>/?userid=<some_user_id>&n=1`. `n` determines which session is started (1-5). Earlier sessions need to be completed by a user to be able to access later ones.
      - If you are not using Nginx, you also need to specify the port number: `http://<your_instance_IP>:3000/?userid=<some_user_id>&n=1`.
	  - And if you are not using Nginx, you also need to open port 3000 on your Google Compute Engine instance for tcp.
   - Open the chat here:
   
      <img src = "Readme_images/open_chat.PNG" width = "250" title="Open chat.">
   
      - The button can be very small on your phone.
   
   - The chat should look something like this:
   
   <img src = "Readme_images/chat.PNG" width = "500" title="Chat.">
   
   - Right now I have set the code in frontend/static/css/style.css such that the chat is always opened in fullscreen. See this code:
     
	 ```css
	 .widget {
	 display: none;
	 width: 98%;
	 right: 1%;
	 left: 1%;
	 height: 98%;
	 bottom: 2%;
	 position: fixed;
	 background: #f7f7f7;
	 border-radius: 10px 10px 10px 10px;
	 box-shadow: 0px 2px 10px 1px #b5b5b5;
     }
	 ```
      - The code by Tom Jacobs (https://github.com/TomJ-EU/rasa/tree/dev) instead first opens the chat as a smaller window and adds a "fullscreen"-option to the drop-down used in [the code by Jitesh Gaikwad](https://github.com/AmirStudy/Rasa_Deployment). For example, like this in script.js:
   
		```js
		//fullscreen function to toggle fullscreen.
		$("#fullscreen").click(function () {
		   if ($('.widget').width() == 350) {
		      $('.widget').css("width" , "98%");
			  $('.widget').css("height" , "100%");
		   } else {
			  $('.widget').css("width" , "350px");
			  $('.widget').css("height" , "500px");
		   }
		});
		```
      - But then you also need to make sure to add the drop-down to the file index.html:
	  
	    ```html
		<div class="chat_header">

           <!--Add the name of the bot here -->
		   <span class="chat_header_title">Virtual Coach Mel</span>
		   <span class="dropdown-trigger" href='#' data-target='dropdown1'>
			  <i class="material-icons">
				 more_vert
			  </i>
		   </span>
        </div>
		```
		
		```html
		<!-- Dropdown menu-->
        <ul id='dropdown1' class='dropdown-content'>
           <li><a href="#" id="fullscreen">Fullscreen</a></li>
        </ul>
		```
		
	  - And further adapt script.js by adding code to `(document).ready(function ()`:
	  
	    ```js
		//drop down menu
	    $('.dropdown-trigger').dropdown();
	    ```

This project uses an SQLTrackerStore (https://rasa.com/docs/rasa/tracker-stores/) to store the conversation history in a database:
   - A nice way to see the contents of this database is using the program DBeaver.
      - First also open port 5432 on your Google Compute Engine instance for tcp. There is no need to restart the instance after opening the port.
      - To configure DBeaver, add a new database connection:
   
      <img src = "Readme_images/dbeaver_1.PNG" width = "250" title="DBeaver 1.">
   
      - Select a "PostgresSQL" connection.
      - Enter your instance's IP address as the "Host", keep the "Port" set to 5432, enter the username and password used in docker-compose.yml, and set the "Database" to "rasa".
      - After connecting, you can inspect the database content by clicking on the "events" table:
   
      <img src = "Readme_images/dbeaver_2.PNG" width = "500" title="DBeaver 2.">
   
      - After clicking on "Data," you can see the table content. The "sender_id" is the "<some_user_id>" you used when accessing your frontend:
   
      <img src = "Readme_images/dbeaver_3.PNG" width = "500" title="DBeaver 3.">
   
      - To refresh the view, you can click on File > Refresh in DBeaver.
	  - You can also export the data in the database:
	  
	  <img src = "Readme_images/dbeaver_4.PNG" width = "500" title="DBeaver 4.">

   - The database is persistent because of the "volumes" we specified in docker-compose.yml for postgres. Read more about this here: https://medium.com/codex/how-to-persist-and-backup-data-of-a-postgresql-docker-container-9fe269ff4334.
      - So you can run `docker-compose down --volumes` and `docker-compose up --build` and the database content is still there. Check for yourself using DBeaver.
	  - To delete the database content, just remove the "data"-folder.


The project further uses an mysql database to store specific data from the conversations:
   - The database is also persistent. The folder "data_mysql" is used for this, as set up in docker-compose.yml.
   - To inspect the database content content with DBeaver, first open port 3306 on your instance for tcp. Again, there is no need to restart your instance after opening this port.
   - When setting up the connection, use "db" for "Database", "root" for "Username", and the password specified in docker-compose.yml. Keep "Port" to 3306. The "Server Host" is the IP address of your instance.
      - You might have to set "allowPublicKeyRetrieval" to "true" in "Driver properties." 
   - To delete the database content, just delete the folder "data_mysql" on your Google Compute Engine instance.
   - Make sure to use a secure password. This needs to be set in both docker-compose.yml and actions/definitions.py. For example, see [this post](https://www.akamai.com/blog/security/btc-strikes-back-now-attacking-mysql-databases).


Some errors I got during the setup:
   - "Couldn't connect to Docker daemon at http+docker://localhost - is it running? If it's at a non-standard location, specify the URL with the DOCKER_HOST environment variable“ when running `docker-compose up –-build`.
      - I followed the steps suggested here: https://forums.docker.com/t/couldnt-connect-to-docker-daemon-at-http-docker-localhost-is-it-running/87257/2.
	  - These 2 steps fixed the issue for me:
	     
		 <img src = "Readme_images/error_build.PNG" width = "500" title="docker-compose up --build error.">
		 
		 - Run `sudo docker-compose up –-build`. 
		 
   - When running the project locally on Windows:
      - I got an error for the SQLTrackerStore when running `docker-compose up –-build`. Just removing the information on `volumes` in docker-compose.yml helped. This removes the persistence though.
	  - Since adding nginx, nginx does not work out of the box. To just quickly get the project to work locally, I ignored the nginx part. So I accessed the frontend via "localhost:3000/?..." and changed the url in the file script.js to `url: "http://localhost:5005/webhooks/rest/webhook",`.
	
		 
## Frontend Styling

Check the file frontend/static/css/style.css to adapt the styling of the frontend:
   - .chats defines the chat area within the window in fullscreen mode. I tuned the height and width of this.
   - .chat_header_title defines the chat header title. I set the color to #f7f7f7 so that the title is not visible in fullscreen mode. Change the margin-left to align the title to the center. Right now I have fully removed the title though. If you want to add the title again, your file frontend/index.html should contain `chat_header_title`:
   
     ```html
	 <!--chatbot widget -->
	 <div class="widget">
		 <div class="chat_header">

		    <!--Add the name of the bot here -->
		    <span class="chat_header_title">Your Bot Name</span>
		   
		 </div>
		   
	     <!--Chatbot contents goes here -->
	     <div class="chats" id="chats">
		    <div class="clearfix"></div>
	     </div>

	     <!--keypad for user to type the message -->
	     <div class="keypad">
		    <textarea id="userInput" placeholder="Type a message..." class="usrInput"></textarea>
		    <div id="sendButton"><i class="fa fa-paper-plane" aria-hidden="true"></i></div>
	     </div>

	 </div>
     ```
	
   - If you want to change the way that buttons are displayed, adapt `.menu` and `.menuChips` in the file style.css.
      - For example, you may want to display the buttons like this:
	   
	     <img src = "Readme_images/buttons_wrapped.PNG" width = "500" title="Wrapped buttons.">
		  
	  - This can be done with this code:

	    ```css
	    .menu {
			padding: 5px;
			display: flex;
			flex-wrap: wrap;
		}

		.menuChips {
			display: inline-block;
			background: #2c53af;
			color: #fff;
			padding: 5px;
			margin-bottom: 5px;
			cursor: pointer;
			border-radius: 15px;
			font-size: 14px;
		}
	    ```

      - Important is that `display: flex` and `flex-wrap: wrap` in `.menu`.
	  - To further remove the background of the buttons and add a shadow to the individual buttons instead, set `box-shadow: 2px 5px 5px 1px #dbdade` for `.menuChips` and use this code for `.suggestions` in the file style.css:
	  
	    ```css
		.suggestions {
			padding: 5px;
			width: 80%;
			border-radius: 10px;
			background: #f7f7f7;
		}
		```

	  - Then buttons are displayed like this:
	  
	     <img src = "Readme_images/buttons_wrapped_noback.PNG" width = "500" title="Wrapped buttons no background.">
		
	  - See [this post](https://stackoverflow.com/questions/73533611/how-to-put-two-chips-divs-next-to-each-other) for some other ideas for displaying buttons next to each other.
	  - Note that by default, buttons are displayed like this:
		
	     <img src = "Readme_images/buttons_below.PNG" width = "500" title="Buttons below each other.">
		
	  - The corresponding code in the file style.css looks like this:
		
		```css
		.menu {
			padding: 5px;
		}

		.menuChips {
			display: block;
			background: #2c53af;
			color: #fff;
			text-align: center;
			padding: 5px;
			margin-bottom: 5px;
			cursor: pointer;
			border-radius: 15px;
			font-size: 14px;
			word-wrap: break-word;
		}
		```

The files in frontend/static/img are used to display the chatbot and the user inside the chat, as well as to display the chatbot when the chat is still closed at the start.

You can use "\n" in your utterances in domain.yml to display a single utterance as two (or more) separate messages. The resulting messages are not treated as separate messages when it comes to displaying the typing symbol though.


## HTTPS

You might want to allow also for https traffic:
   - I recommend looking at [this tutorial](https://datahive.ai/deploying-rasa-chatbot-on-google-cloud-with-docker/). Compared to allowing only http-traffic, you have to make changes in nginx.conf and docker-compose.yml and create an SSL certificate.
   - For example, this is what the entry for nginx in docker-compose.yml may look like when allowing https traffic:
     
	 ```yml
	 nginx:
      container_name: "nginx"
      image: nginx
      volumes:
        - ./nginx.conf:/etc/nginx/nginx.conf
        - ./certs:/etc/certs
      ports:
        - 80:80
        - 443:443
	  depends_on: 
        - rasa
        - action-server
        - chatbotui
     ```
	 
      - The folder "certs" on the Google compute engine instance stores the SSL certificate files in this example.

   - See [this post](https://adamtheautomator.com/https-nodejs/) for how to create a self-signed SSL certificate.
      - If you use a self-signed SSL certificate and access your frontend via https, you may see a warning like this in your browser (here Google Chrome):
   
        <img src = "Readme_images/https.PNG" width = "250" title="https warning browser">
 
      - This might scare participants off. So I would recommend to either stick to http or to go all the way and get a proper certificate.
	 
   - See [this page](https://cloud.google.com/load-balancing/docs/ssl-certificates/self-managed-certs) for more information on certificates on Google cloud.
      - Info on registering a domain: https://cloud.google.com/dns/docs/tutorials/create-domain-tutorial#register-domain.
	     - Registering a domain for a year is quite cheap (you can get one for about 8 euros).
      - Cloud DNS pricing info: https://cloud.google.com/dns/pricing. You need this if you get a domain and want to use it.


## Getting the user name
- It is not a good idea to just get and use the user name as in this example project. This is because many people reply with things such as "Hi, my name is Mary" when being asked about their name.
- So it might be a good idea to not ask for and use the name at all.
- Some steps to try to improve getting the name:
   - Use an entity and an intent for getting the entity in domain.yml:
   
     ```yml
	 intents:
     - user_name_intent

	 entities:
     - user_name_entity:
	     influence_conversation: false

	 slots:
	   user_name_slot:
		 type: text
		 initial_value: ''
		 influence_conversation: false
		 mappings:
		 - type: from_entity
		   entity: user_name_entity
		   conditions:
			 - active_loop: user_name_form
     ```
	 
   - Create some training data for the intent in the file nlu.yml (remember to create a lot of training data):
   
     ```yml
	 nlu:

	 - intent: user_name_intent
	   examples: |
		 - "Hi Mel, I'm [PERSON](user_name_entity)"
		 - "My name is [PERSON](user_name_entity)"
		 - "I'm [PERSON](user_name_entity)"
		 - "[PERSON](user_name_entity)"
     ```
   
   - Use spacy in config.yml. See [here](https://spacy.io/models/en) for different English language models.
   
     ```yml
	 language: en
	 pipeline:
	 - name: SpacyNLP
	   model: en_core_web_lg
	   case_sensitive: false
	 - name: SpacyTokenizer
	 - name: SpacyFeaturizer
	   pooling: mean
	 - name: SpacyEntityExtractor
	   dimensions:
	   - PERSON
	 - name: RegexFeaturizer
	 - name: LexicalSyntacticFeaturizer
	 - name: CountVectorsFeaturizer
     ```
	 
   - Now that you use spacy, you also need to adapt the Dockerfile for your backend:
   
     ```
     USER root

	 COPY requirements.txt .
	 RUN pip install -r requirements.txt

	 # Spacy language model
	 RUN python -m spacy download en_core_web_lg

	 USER 1001
	 ```
	 
   - And backend/requirements.txt needs to list `spacy` as a requirement.
   - When rasa does not succeed in extracting a slot in the `user_name_form` (e.g., when you try a not-so-typical English name such as "Priyanka"), then an ActionExecutionRejected event is thrown.
   - A work-around is to then just store the last user utterance as `user_name_slot`.
   - To do this, you might create a rule like this one:
     
	 ```yml
	 - rule: name session 1 failed fallback
	   condition:
		 - active_loop: user_name_form
	   steps:
	   - intent: nlu_fallback
	   - action: action_get_name_from_last_utterance
	   - action: utter_confirm_name
	   - action: action_deactivate_loop
	   - active_loop: null
	   - action: utter_ask_for_mood_session1
	 ```

   - The action `action_get_name_from_last_utterance` just gets the text from the last user utterance via `last_user_utterance = tracker.latest_message['text']` and stores this in the slot `user_name_slot`.
   - Since you are using spacy, you also need to have spacy installed where you train your rasa model. To do this in an anaconda environment, use `conda install -c conda-forge spacy`.
   - And then you also need to download the language model you use.
   - I personally got package version conflicts with rasa 3.2.8, so I used rasa 3.5.3 for the training.
      - This also means that I updated the Dockerfile for the custom actions to use `FROM rasa/rasa-sdk:3.3.0` and the Dockerfile for the backend to use `FROM rasa/rasa:3.5.3-full`.
   - Now this setup MIGHT allow you to correctly handle responses such as "My name is John" or "Priyanka":
      - It is quite difficult to get this setup to work well in all cases:
	     - For example, the DietClassifier may also extract (wrong) entities, in which case you may need to look through all entities in `tracker.latest_message['entities']` in a custom action and choose the entity for which `entity["extractor"] == "SpacyEntityExtractor"`.
	     - Sometimes, rasa recognizes "user_name_intent" for "Priyanka" but cannot extract an entity.
		 - If the user uses the chatbot name in their message, sometimes the chatbot name is extracted as the user name.
   - Unless you are confident that the user has a common English (or whichever language model you use) name and/or types only their name, I would suggest to not use the user name. In my pilot study, 3 out of 8 people typed more than their name.
   - You could of course also play back to the user what you got as their name and ask them for confirmation, but this might make the virtual coach look rather stupid if what they play back as the user name is "My name is Priyanka".


## Other Notes
- The frontend is not fully cleaned up yet (i.e., still contains quite some components that are not used by this project).
- The repository by Jitesh Gaikwad (https://github.com/AmirStudy/Rasa_Deployment) also contains code for displaying charts, drop-downs, and images in frontend/static/js/script.js (see the function `setBotResponse` for displaying responses from the rasa bot). I have removed this code in this example project, but if you need to send such kinds of messages, take a look.
- `"--debug"` in backend/Dockerfile prints a lot of debugging statements (e.g., for the action prediction). This is handy while you are still developing your agent, but can be removed.
- The Developer tools in Google Chrome show the logs from script.js (i.e., the result of `console.log()`)if you access the frontend via Google Chrome.
- Think carefully about how you deal with timed out sessions. You may want to customize the `action_session_start`: https://rasa.com/docs/rasa/default-actions#customization.
- If you have made changes and they do not reflect on your Google Compute Engine instance, check if you have run `docker-compose down --volumes` and `docker-compose up --build`.
- If you do not see the result of retraining your rasa model, it can sometimes help to delete all models and retrain from scratch.
- You might want to prevent people from typing while the chatbot is still sending more messages. You can adapt the file script.js to allow for this using statements such as `$('.usrInput').attr("disabled",true);` and `$(".usrInput").prop('placeholder', "Wait for Mel's response.");`
- Before running the chatbot on a Google Compute Engine instance for your experiment, make sure to get a paid account. Once the trial period ends or you have used up your free credit your instance will stop. And a billing account will also help to prevent Google from stopping your project when it thinks that you are mining crypto currencies (e.g., see [here](https://groups.google.com/g/gce-discussion/c/5prZHD3DEnQ)).
- When using the db, pay attention to closing connections. Also pay attention to the kind of cursor you use when you use fetchone(). It may be good to use a buffered cursor then (e.g., see [here](https://stackoverflow.com/questions/29772337/python-mysql-connector-unread-result-found-when-using-fetchone)).
- You might want to get more detailed logs for your mysql database. See [here](https://stackoverflow.com/questions/39708213/enable-logging-in-docker-mysql-container) for a useful discussion. 
   - You can add `- ./mysql_log:/var/log/mysql` to your mysql volumes in docker-compose.yml.
   - Create a file called mysql.log in /var/log/mysql in your mysql container after running `docker exec -it [mysql_container_id] /bin/bash` (e.g., via `cat > mysql.log`).
   - Give sufficient permissions to this newly created file (e.g., via `chmod a+crw mysql.log`).
   - Run `SET global general_log = 1;`, `SET global general_log_file='/var/log/mysql/mysql.log';` and `SET global log_output = 'file';` (e.g., via the console in DBeaver under SQL Editor > Open SQL console).
   - Now you can see the logs on your Google Compute Engine instance in mysql_log/mysql.log.
- Viewing google activity logs: https://cloud.google.com/compute/docs/logging/activity-logs.
- Listing sessions/active connections on mysql server: https://dataedo.com/kb/query/mysql/list-database-sessions (e.g., can execute a query in DBeaver).


## License

Copyright (C) 2023 Delft University of Technology.

Licensed under the Apache License, version 2.0. See LICENSE for details.
