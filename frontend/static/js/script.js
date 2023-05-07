var number_plan = 0;

var current_takeaway = 0;

var first_walk = "";

var week_3_time = "";

var check_first_walk = false;

var check_week_3 = false;

$('.usrInput').attr("disabled",true);

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

			if(current_takeaway == 1){
				var message = "/confirm_takeaway_1";
				setUserResponse(text);
				send(message);

				$('.usrInput').attr("disabled",true);
			}
			else if(current_takeaway == 2){
				var message = "/confirm_takeaway_2";
				setUserResponse(text);
				send(message);

				$('.usrInput').attr("disabled",true);
			}
			else if(check_first_walk){

				console.log(text);

				console.log(first_walk);

				if(text==first_walk){
					var message = "/first_walk_correct";
				}
				else{
					var message = "/first_walk_incorrect";
				}

				console.log(message);

				setUserResponse(text);
				send(message);

				$('.usrInput').attr("disabled",true);
			}
			else if(check_week_3){

				console.log(text);

				console.log(week_3_time);

				if(text==week_3_time){
					var message = "/week_3_correct";
				}
				else{
					var message = "/week_3_incorrect";
				}

				console.log(message);
				
				setUserResponse(text);
				send(message);

				$('.usrInput').attr("disabled",true);
			}
			else{
				setUserResponse(text);
				send(text);
			}

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
					
					if(response_text[j].includes("Nice! Before we can get started, let's see when you have free time.")){
						$(".timeslots_table").toggle();


						var BotResponse = '<img class="botAvatar" src="/img/chatbot_picture.png"/><p class="botMsg">' + response_text[j] + '</p><div class="clearfix"></div>';
						$(BotResponse).appendTo(".chats").hide().fadeIn(1000);
					}

					else if(response_text[j].includes("Now, I want to ask when you are usually energetic.")){
						$(".energy_levels_table").toggle();


						var BotResponse = '<img class="botAvatar" src="/img/chatbot_picture.png"/><p class="botMsg">' + response_text[j] + '</p><div class="clearfix"></div>';
						$(BotResponse).appendTo(".chats").hide().fadeIn(1000);
					}

					// display the plan when it is available
					else if(response_text[j].includes("Plan 1: Week 1 - ")){

						console.log(response_text[j]);

						const week_1 = response_text[j].split("Plan 1: Week 1 - ")[1].split(" ")[0];

						const week_2 = response_text[j].split(" Week 2 - ")[1].split(" ")[0];
						
						const week_3 = response_text[j].split(" Week 3 - Walking for ")[1].split(" ")[0];
						
						const week_4 = response_text[j].split(" Week 4 - Walking for ")[1].split(" ")[0];
						
						const month_2 = response_text[j].split(" Month 2 - Walking for up to ")[1].split(" ")[0];
					
						const month_3 = response_text[j].split(" Month 3 - Walking for up to ")[1].split(" ")[0];

						const slots = response_text[j].split(" minutes at these time slots: [")[1].split("]")[0].split(", ");

						week_3_time = String(week_3);

    
						var clean_slots = slots.map(function(e) { 
							e = e.replace(/^'(.*)'$/, '$1'); 
							return e;
						});

						first_walk = String(clean_slots[0]);

						clean_slots.forEach(e => document.getElementById(e + "_1").innerHTML = "Walk " + week_1 + " minutes");

						clean_slots.forEach(e => document.getElementById(e + "_2").innerHTML = "Walk " + week_2 + " minutes");

						document.getElementById("week_3").innerHTML = "Walking for " + week_3 + " hours, distributed across 4 time slots";

						document.getElementById("week_4").innerHTML = "Walking for " + week_4 + " hours, distributed across 4 time slots";

						document.getElementById("month_2").innerHTML = "Walking for up to " + month_2 + " hours per week, distributed across 5 time slots each week";

						document.getElementById("month_3").innerHTML = "Walking for up to " + month_3 + " hours per week, distributed across 6 time slots each week";

						$(".plan_table").toggle();

						number_plan = 1;
					}
					else if(response_text[j].includes("this is a message for javascript: enable the buttons")){

						var button = document.getElementById("submit_plan_button");

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

						button.style.display = "table";

					}
					else if(response_text[j].includes("What can you take away from this example for yourself? Please type this in the chat.")){
						var BotResponse = '<img class="botAvatar" src="/img/chatbot_picture.png"/><p class="botMsg">' + response_text[j] + '</p><div class="clearfix"></div>';
						$(BotResponse).appendTo(".chats").hide().fadeIn(1000);
						
						$('.usrInput').attr("disabled",false);
						$(".usrInput").prop('placeholder', "Type something...");
						current_takeaway = 1;
					}
					else if(response_text[j].includes("How about this example? What can you take away for yourself? Please type this in the chat.")){
						var BotResponse = '<img class="botAvatar" src="/img/chatbot_picture.png"/><p class="botMsg">' + response_text[j] + '</p><div class="clearfix"></div>';
						$(BotResponse).appendTo(".chats").hide().fadeIn(1000);
						
						$('.usrInput').attr("disabled",false);
						$(".usrInput").prop('placeholder', "Type something...");
						current_takeaway = 2;
					}

					else if(response_text[j].includes("To check that you understand what the plan signifies, let's do a quick pop quiz!")){
						var BotResponse = '<img class="botAvatar" src="/img/chatbot_picture.png"/><p class="botMsg">' + response_text[j] + '</p><div class="clearfix"></div>';
						$(BotResponse).appendTo(".chats").hide().fadeIn(1000);
						
						$('.usrInput').attr("disabled",false);
						$(".usrInput").prop('placeholder', "Type something...");
						check_week_3 = true;
					}
					else if(response_text[j].includes("You can see the first two weeks planned in detail. When is the first time you have to take a walk?")){
						var BotResponse = '<img class="botAvatar" src="/img/chatbot_picture.png"/><p class="botMsg">' + response_text[j] + '</p><div class="clearfix"></div>';
						$(BotResponse).appendTo(".chats").hide().fadeIn(1000);
						
						$('.usrInput').attr("disabled",false);
						$(".usrInput").prop('placeholder', "Type something...");
						check_first_walk = true;
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


function toggle_slot(clicked_id){
	var time_slot = document.getElementById(clicked_id)
	if (time_slot.innerHTML == "Selected") {
		time_slot.innerHTML = "";
		time_slot.style.backgroundColor = "white";
		} else {
		time_slot.innerHTML = "Selected";
		time_slot.style.backgroundColor = "#82e876";
		}
}

function toggle_slot_energy(clicked_id){
	var time_slot = document.getElementById(clicked_id)

	if (time_slot.innerHTML == "Selected") {
		time_slot.innerHTML = "";
		time_slot.style.backgroundColor = "white";
		} else {

		var time = clicked_id.substring(0, clicked_id.length - 9);

		var times = [];

		for(var i = 0; i<=4; i++){
			times.push(`${time}_energy_${i}`);
		}

		var index = times.indexOf(clicked_id);

		times.splice(index, 1);

		times.forEach(function(element) {
			document.getElementById(element).innerHTML = "";
			document.getElementById(element).style.backgroundColor = "white";
		});

		time_slot.innerHTML = "Selected";
		time_slot.style.backgroundColor = "#82e876";
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

	var selected_slots_1 = [];
	var selected_slots_2 = [];

	days_1.forEach(element_id => selected_slots_1.push(slots_selected(element_id)));
	days_2.forEach(element_id => selected_slots_2.push(slots_selected(element_id)));

	var filtered_1 = selected_slots_1.filter(function (el) {
		return el != "";
	});

	var filtered_2 = selected_slots_2.filter(function (el) {
		return el != "";
	});

	const week_3 = document.getElementById("week_3").innerHTML;
	const week_4 = document.getElementById("week_4").innerHTML;

	const month_2 = document.getElementById("month_2").innerHTML;
	const month_3 = document.getElementById("month_3").innerHTML;

	if(count_1 == 4 && count_2 == 4){
		button.style.display = "none";
		days_1.forEach(element => document.getElementById(element).classList.remove("toggleable"));
		days_2.forEach(element => document.getElementById(element).classList.remove("toggleable"));

		if(number_plan == 1){
			var message = `/plan_modified{"plan_2":"Plan 2: Week 1 - 30 minutes at these time slots: [${filtered_1}]. Week 2 - 35 minutes at these time slots: [${filtered_2}]. Week 3 - Walking for ${week_3} hours, distributed across 4 time slots. Week 4 - Walking for ${week_4} hours, distributed across 4 time slots. Month 2 - Walking for up to ${month_2} hours per week, distributed across 5 time slots. Month 3 - Walking for up to ${month_3} hours per week, distributed across 6 time slots."}`;

			send(message);

			number_plan = 2;
	
		}
		else{
			var message = `/plan_modified{"plan_3":"Plan 3: Week 1 - 30 minutes at these time slots: [${filtered_1}]. Week 2 - 35 minutes at these time slots: [${filtered_2}]. Week 3 - Walking for ${week_3} hours, distributed across 4 time slots. Week 4 - Walking for ${week_4} hours, distributed across 4 time slots. Month 2 - Walking for up to ${month_2} hours per week, distributed across 5 time slots. Month 3 - Walking for up to ${month_3} hours per week, distributed across 6 time slots."}`;

			send(message);
		}
	}
	else{
		window.alert("You cannot submit the plan as it is currently. Each week should have exactly four time slots selected.");
	}
}

function check_selected_timeslots_initial(){

	var button = document.getElementById("submit_timeslots_button");

	var table = document.getElementById("timeslots_table");

	const days = ["monday_morning_slot", "monday_midday_slot", "monday_afternoon_slot", "monday_evening_slot",
	"tuesday_morning_slot", "tuesday_midday_slot", "tuesday_afternoon_slot", "tuesday_evening_slot",
	"wednesday_morning_slot", "wednesday_midday_slot", "wednesday_afternoon_slot", "wednesday_evening_slot",
	"thursday_morning_slot", "thursday_midday_slot", "thursday_afternoon_slot", "thursday_evening_slot",
	"friday_morning_slot", "friday_midday_slot", "friday_afternoon_slot", "friday_evening_slot",
	"saturday_morning_slot", "saturday_midday_slot", "saturday_afternoon_slot", "saturday_evening_slot",
	"sunday_morning_slot", "sunday_midday_slot", "sunday_afternoon_slot", "sunday_evening_slot"
	]


	var count = 0;

	days.forEach(element_id => count+= check_inner_HTML(element_id));

	var selected_slots = [];

	days.forEach(element_id => selected_slots.push(slots_selected_initial(element_id)));

	var selected_slots = selected_slots.filter(function (el) {
		return el != "";
	});


	if(count >= 4){
		button.style.display = "none";
		table.style.display = "none";

		var message = `/move_to_energy{`;

		selected_slots.forEach(function(slot) {
			message = message.concat(`"${slot.substring(1,slot.length-1)}":"True",`);
		});

		message = message.substring(0, message.length - 1);

		message = message.concat(`}`);

		send(message);
		
	}
	else{
		window.alert("Please select at least four time slots.");
	}
}


function check_energy(){

	var button = document.getElementById("submit_energy_button");

	var table = document.getElementById("energy_levels_table");

	times_weekdays = [ "weekdays_morning_energy", "weekdays_midday_energy", "weekdays_afternoon_energy", "weekdays_evening_energy"]

	times_weekends = [ "weekends_morning_energy", "weekends_midday_energy", "weekends_afternoon_energy", "weekends_evening_energy"]

	var alerted_1 = false;

	selected = [];

	times_weekdays.forEach(function(time) {

		slots = [];

		for(var i = 0; i<=4; i++){
			slots.push(`${time}_${i}`);
		}

		count = 0;
		
		slots.forEach(function(element_id) {
			var value = check_inner_HTML(element_id);
			count += value;

			if(value==1){
				selected.push(element_id);
			}
		});

		if(count != 1 && !alerted_1){
			alerted_1 = true;
		}
		
	});

	var alerted_2;

	times_weekends.forEach(function(time) {

		slots = [];

		for(var i = 0; i<=4; i++){
			slots.push(`${time}_${i}`);
		}

		count = 0;
		
		slots.forEach(function(element_id) {
			var value = check_inner_HTML(element_id);
			count += value;

			if(value==1){
				selected.push(element_id);
			}
		});

		if(count != 1 && !alerted_2){
			alerted_2 = true;
			
		}
		
	});

	if(alerted_1 && alerted_2){
		window.alert("Please select an option for each of the time periods for both weekdays and weekends.");
	}
	else if(alerted_1 && !alerted_2){
		window.alert("Please select an option for each of the time periods for weekdays.");
	}
	else if(!alerted_1 && alerted_2){
		window.alert("Please select an option for each of the time periods for weekends.");
	}
	else if(!alerted_1 && !alerted_2){

		button.style.display = "none";
		table.style.display = "none";

		var message = `/confirm_energy_levels{`;

		selected.forEach(function(level) {
			message = message.concat(`"${level.substring(0,level.length-9)}":"${level.slice(-1)}",`);
		});

		message = message.substring(0, message.length - 1);

		message = message.concat(`}`);

		console.log(message);
	
		send(message);
	}
}

function check_inner_HTML(element_id){
	var element =  document.getElementById(element_id);

	if(element.innerHTML == ""){
		return 0;
	}
	else return 1;
}

function slots_selected(element_id){
	var element = document.getElementById(element_id);

	if(element.innerHTML == ""){
		return "";
	}
	// remove the _1 or _2 from the id
	else return `'${element_id.substring(0, element_id.length - 2)}'`;
}

function slots_selected_initial(element_id){
	var element = document.getElementById(element_id);

	if(element.innerHTML == ""){
		return "";
	}
	// remove the _slot from the id
	else return `'${element_id.substring(0, element_id.length - 5)}'`;
}


//====================================== Suggestions ===========================================

function addSuggestion(textToAdd) {
	setTimeout(function () {

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
	// $('.usrInput').attr("disabled",false);
	$(".usrInput").prop('placeholder', "Use the buttons to communicate with Jamie.");
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


