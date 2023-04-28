// ========================== start session ========================
$(document).ready(function () {

	//get user ID
	const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const userid = urlParams.get('userid');
	user_id = userid;
	//get session number
	const session_num = 1;
	
	
	send('/start_session1{"session_num":"1"}');
	
})

//=====================================	user enter or sends the message =====================
$(".usrInput").on("keyup keypress", function (e) {
	var keyCode = e.keyCode || e.which;

	var text = $(".usrInput").val();
	if (keyCode === 13) {

		if (text == "" || $.trim(text) == "") {
			e.preventDefault();
			return false;
		} else {

			$("#paginated_cards").remove();
			$(".suggestions").remove();
			$(".usrInput").blur();
			setUserResponse(text);
			send(text);
			e.preventDefault();
			return false;
		}
	}
});

$("#sendButton").on("click", function (e) {
	var text = $(".usrInput").val();
	if (text == "" || $.trim(text) == "") {
		e.preventDefault();
		return false;
	}
	else {
		
		$(".suggestions").remove();
		$("#paginated_cards").remove();
		$(".usrInput").blur();
		setUserResponse(text);
		send(text);
		e.preventDefault();
		return false;
	}
})

//==================================== Set user response =====================================
function setUserResponse(message) {
	var UserResponse = '<img class="userAvatar" src=' + "/img/user_picture.png" + '><p class="userMsg">' + message + ' </p><div class="clearfix"></div>';
	$(UserResponse).appendTo(".chats").show("slow");

	$(".usrInput").val("");
	scrollToBottomOfResults();
	showBotTyping();
	$(".suggestions").remove();
}

//=========== Scroll to the bottom of the chats after new message has been added to chat ======
function scrollToBottomOfResults() {

	var terminalResultsDiv = document.getElementById("chats");
	terminalResultsDiv.scrollTop = terminalResultsDiv.scrollHeight;
}

//============== send the user message to rasa server =============================================
function send(message) {
	var url = document.location.protocol + "//" + document.location.hostname;
	$.ajax({

		url: url + "/rasa/webhooks/rest/webhook",
		type: "POST",
		contentType: "application/json",
		data: JSON.stringify({ message: message, sender: user_id }),
		success: function (botResponse, status) {
			console.log("Response from Rasa: ", botResponse, "\nStatus: ", status);

			setBotResponse(botResponse);

		},
		error: function (xhr, textStatus, errorThrown) {

			// if there is no response from rasa server
			setBotResponse("");
			console.log("Error from bot end: ", textStatus);
		}
	});
}

//=================== set bot response in the chats ===========================================
function setBotResponse(response) {

	//display bot response after the number of miliseconds caputred by the variable 'delay_first_message'
	var delay_first_message = 500;
	if (response.length >=1) {
		// delay_first_message = Math.min(Math.max(response[0].text.length * 45, 800), 5000);
		delay_first_message = 20;
	}
	setTimeout(function () {
		hideBotTyping();
		if (response.length < 1) {
			//if there is no response from Rasa, send  fallback message to the user
			var fallbackMsg = "I am facing some issues, please try again later!!!";

			var BotResponse = '<img class="botAvatar" src="/img/chatbot_picture.png"/><p class="botMsg">' + fallbackMsg + '</p><div class="clearfix"></div>';

			$(BotResponse).appendTo(".chats").hide().fadeIn(1000);
			scrollToBottomOfResults();
		}
		//if we get response from Rasa
		else {
			//check if the response contains "text"
			if (response[0].hasOwnProperty("text")) {
				var response_text = response[0].text.split("\n")
				for (j = 0; j < response_text.length; j++){
					// display the plan when it is available
					if(response_text[j].includes("Plan: Week 1 - ")){
						const week_1 = response_text[j].split("Plan: Week 1 - ")[1].split(" ")[0];

						const week_2 = response_text[j].split(" Week 2 - ")[1].split(" ")[0];
						
						const week_3 = response_text[j].split(" Week 3 - Walking for ")[1].split(" ")[0];
						
						const week_4 = response_text[j].split(" Week 4 - Walking for ")[1].split(" ")[0];
						
						const month_2 = response_text[j].split(" Month 2 - Walking for up to ")[1].split(" ")[0];
					
						const month_3 = response_text[j].split(" Month 3 - Walking for up to ")[1].split(" ")[0];

						const slots = response_text[j].split(" minutes at these time slots: [")[1].split("]")[0].split(", ");
    
						var clean_slots = slots.map(function(e) { 
							e = e.replace(/^'(.*)'$/, '$1'); 
							return e;
						});

						clean_slots.forEach(e => document.getElementById(e + "_1").innerHTML = "Walk " + week_1 + " minutes");

						clean_slots.forEach(e => document.getElementById(e + "_2").innerHTML = "Walk " + week_2 + " minutes");

						document.getElementById("week_3").innerHTML = "Walking for up to " + week_3 + " minutes across 4 days";

						document.getElementById("week_4").innerHTML = "Walking for up to " + week_4 + " minutes across 4 days";

						document.getElementById("month_2").innerHTML = "Walking for up to " + month_2 + " minutes per week across 5 days each week";

						document.getElementById("month_3").innerHTML = "Walking for up to " + month_3 + " minutes per week across 5 days each week";

						$(".plan_table").toggle();
					}
					else if(response_text[j].includes("placeholder changes to plan")){

						var button = document.getElementById("submit_plan_button");
  						
						button.style.display = "table";

						const days = [	"monday_morning_1", "monday_midday_1", "monday_afternoon_1", "monday_evening_1",
										"tuesday_morning_1", "tuesday_midday_1", "tuesday_afternoon_1", "tuesday_evening_1",
										"wednesday_morning_1", "wednesday_midday_1", "wednesday_afternoon_1", "wednesday_evening_1",
										"thursday_morning_1", "thursday_midday_1", "thursday_afternoon_1", "thursday_evening_1",
										"friday_morning_1", "friday_midday_1", "friday_afternoon_1", "friday_evening_1",
										"saturday_morning_1", "saturday_midday_1", "saturday_afternoon_1", "saturday_evening_1",
										"sunday_morning_1", "sunday_midday_1", "sunday_afternoon_1", "sunday_evening_1",
										"monday_morning_2", "monday_midday_2", "monday_afternoon_2", "monday_evening_2",
										"tuesday_morning_2", "tuesday_midday_2", "tuesday_afternoon_2", "tuesday_evening_2",
										"wednesday_morning_2", "wednesday_midday_2", "wednesday_afternoon_2", "wednesday_evening_2",
										"thursday_morning_2", "thursday_midday_2", "thursday_afternoon_2", "thursday_evening_2",
										"friday_morning_2", "friday_midday_2", "friday_afternoon_2", "friday_evening_2",
										"saturday_morning_2", "saturday_midday_2", "saturday_afternoon_2", "saturday_evening_2",
										"sunday_morning_2", "sunday_midday_2", "sunday_afternoon_2", "sunday_evening_2"
									]

						days.forEach(element => document.getElementById(element).classList.add("toggleable"));

					}
					// otherwise, display the message
					else{
						var BotResponse = '<img class="botAvatar" src="/img/chatbot_picture.png"/><p class="botMsg">' + response_text[j] + '</p><div class="clearfix"></div>';
						$(BotResponse).appendTo(".chats").hide().fadeIn(1000);
					}
				}
			}

			//check if the response contains "buttons" 
			if (response[0].hasOwnProperty("buttons")) {
				addSuggestion(response[0].buttons);
			}

		scrollToBottomOfResults();
		}
	}, delay_first_message);
	

	//if there is more than 1 message from the bot
	if (response.length > 1){
		//show typing symbol again
		// var delay_typing = 600 + delay_first_message;
		var delay_typing = 20;
		setTimeout(function () {
		showBotTyping();
		}, delay_typing)
		
		//send remaining bot messages if there are more than 1
		var summed_timeout = delay_typing;
		for (var i = 1; i < response.length; i++){
			
			//Add delay based on the length of the next message
			// summed_timeout += Math.min(Math.max(response[i].text.length * 45, 800), 5000);
			doScaledTimeout(i, response, summed_timeout)
			
		}
	}
	
}


//====================================== Scaled timeout for showing messages from bot =========
// See here for an explanation on timeout functions in javascript: https://stackoverflow.com/questions/5226285/settimeout-in-for-loop-does-not-print-consecutive-values.
function doScaledTimeout(i, response, summed_timeout) {
	
	setTimeout(function() {
		hideBotTyping();
			
		//check if the response contains "text"
		if (response[i].hasOwnProperty("text")) {
			var response_text = response[i].text.split("\n")
			for (j = 0; j < response_text.length; j++){
				var BotResponse = '<img class="botAvatar" src="/img/chatbot_picture.png"/><p class="botMsg">' + response_text[j] + '</p><div class="clearfix"></div>';
				$(BotResponse).appendTo(".chats").hide().fadeIn(1000);
			}
		}

		//check if the response contains "buttons" 
		if (response[i].hasOwnProperty("buttons")) {
			addSuggestion(response[i].buttons);
		}
		
		scrollToBottomOfResults();
		
		if (i < response.length - 1){
			showBotTyping();
		}
	}, summed_timeout);
}


//====================================== Toggle chatbot =======================================
$("#profile_div").click(function () {
	$(".profile_div").toggle();
	$(".widget").toggle();
});

//====================================== Toggle time slots =======================================
// a bit hacky since I'm not passing the "real" values, but it turns out that regardless of what the goal is,
// these are always 30 minutes in the first week and 35 in the second week since we round to the nearest 5
function toggle_table_cell_1(clicked_id){
	var time_slot = document.getElementById(clicked_id)
	if(time_slot.classList.contains("toggleable")){
		if (time_slot.innerHTML == "Walk 30 minutes") {
			time_slot.innerHTML = "";
		  } else {
			time_slot.innerHTML = "Walk 30 minutes";
		  }
	}
}

function toggle_table_cell_2(clicked_id){
	var time_slot = document.getElementById(clicked_id)
	if(time_slot.classList.contains("toggleable")){
		if (time_slot.innerHTML == "Walk 35 minutes") {
			time_slot.innerHTML = "";
		  } else {
			time_slot.innerHTML = "Walk 35 minutes";
		  }
	}
}

//====================================== Check selected time slots =======================================
function check_selected_timeslots(){

	var button = document.getElementById("submit_plan_button");

	const days_1 = [	"monday_morning_1", "monday_midday_1", "monday_afternoon_1", "monday_evening_1",
	"tuesday_morning_1", "tuesday_midday_1", "tuesday_afternoon_1", "tuesday_evening_1",
	"wednesday_morning_1", "wednesday_midday_1", "wednesday_afternoon_1", "wednesday_evening_1",
	"thursday_morning_1", "thursday_midday_1", "thursday_afternoon_1", "thursday_evening_1",
	"friday_morning_1", "friday_midday_1", "friday_afternoon_1", "friday_evening_1",
	"saturday_morning_1", "saturday_midday_1", "saturday_afternoon_1", "saturday_evening_1",
	"sunday_morning_1", "sunday_midday_1", "sunday_afternoon_1", "sunday_evening_1"
	]

	const days_2 = ["monday_morning_2", "monday_midday_2", "monday_afternoon_2", "monday_evening_2",
	"tuesday_morning_2", "tuesday_midday_2", "tuesday_afternoon_2", "tuesday_evening_2",
	"wednesday_morning_2", "wednesday_midday_2", "wednesday_afternoon_2", "wednesday_evening_2",
	"thursday_morning_2", "thursday_midday_2", "thursday_afternoon_2", "thursday_evening_2",
	"friday_morning_2", "friday_midday_2", "friday_afternoon_2", "friday_evening_2",
	"saturday_morning_2", "saturday_midday_2", "saturday_afternoon_2", "saturday_evening_2",
	"sunday_morning_2", "sunday_midday_2", "sunday_afternoon_2", "sunday_evening_2"
	]

	var count_1 = 0;

	days_1.forEach(element_id => count_1+= check_inner_HTML(element_id));

	var count_2 = 0;

	days_2.forEach(element_id => count_2+= check_inner_HTML(element_id));

	if(count_1 == 4 && count_2 == 4){
		button.style.display = "none";
		days_1.forEach(element => document.getElementById(element).classList.remove("toggleable"));
		days_2.forEach(element => document.getElementById(element).classList.remove("toggleable"));
	}
	else{
		window.alert("You cannot submit the plan as it is currently. Each week should have exactly four time slots selected.");
	}
}

function check_inner_HTML(element_id){
	var element =  document.getElementById(element_id);

	if(element.innerHTML == ""){
		return 0;
	}
	else return 1;
}


//====================================== Suggestions ===========================================

function addSuggestion(textToAdd) {
	setTimeout(function () {
		$('.usrInput').attr("disabled",true);
		$(".usrInput").prop('placeholder', "Use one of the buttons to answer.");
		var suggestions = textToAdd;
		var suggLength = textToAdd.length;
		$(' <div class="singleCard"> <div class="suggestions"><div class="menu"></div></div></diV>').appendTo(".chats").hide().fadeIn(1000);
		// Loop through suggestions
		for (i = 0; i < suggLength; i++) {
			$('<div class="menuChips" data-payload=\'' + (suggestions[i].payload) + '\'>' + suggestions[i].title + "</div>").appendTo(".menu");
		}
		scrollToBottomOfResults();
	}, 1000);
}

// on click of suggestions, get the value and send to rasa
$(document).on("click", ".menu .menuChips", function () {
	$('.usrInput').attr("disabled",false);
	$(".usrInput").prop('placeholder', "Type a message...");
	var text = this.innerText;
	var payload = this.getAttribute('data-payload');
	console.log("payload: ", this.getAttribute('data-payload'))
	setUserResponse(text);
	send(payload);

	//delete the suggestions once user click on it
	$(".suggestions").remove();

});


//======================================bot typing animation ======================================
function showBotTyping() {

	var botTyping = '<img class="botAvatar" id="botAvatar" src="/img/chatbot_picture.png"/><div class="botTyping">' + '<div class="bounce1"></div>' + '<div class="bounce2"></div>' + '<div class="bounce3"></div>' + '</div>'
	$(botTyping).appendTo(".chats");
	$('.botTyping').show();
	scrollToBottomOfResults();
}

function hideBotTyping() {
	$('#botAvatar').remove();
	$('.botTyping').remove();
}


