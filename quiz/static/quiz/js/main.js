let main = function(){
	//enable csrf post ajax

	//This function gets cookie with a given name
	function getCookie(name) {
		var cookieValue = null;
		if (document.cookie && document.cookie != '') {
			var cookies = document.cookie.split(';');
			for (var i = 0; i < cookies.length; i++) {
				var cookie = jQuery.trim(cookies[i]);
				// Does this cookie string begin with the name we want?
				if (cookie.substring(0, name.length + 1) == (name + '=')) {
				 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				 break;
				}
			}
		}
		return cookieValue;
	}
	var csrftoken = getCookie('csrftoken');

	/*
	The functions below will create a header with csrftoken
	*/

	function csrfSafeMethod(method) {
	 // these HTTP methods do not require CSRF protection
	 return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	}

	$.ajaxSetup({
	 beforeSend: function(xhr, settings) {
		 if (!csrfSafeMethod(settings.type) && !this.crossDomain &&
			(!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url)))) {
		 // Only send the token to relative URLs i.e. locally.
		 xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
		 }
	 }
	});

	let level = 50;
	let diff = document.getElementById('difficulty');
	diff.onclick = function(event){
		var target = event.target;
		while (target != this) {
			if (target.tagName == 'BUTTON') {
				let content = target.textContent;
				switch (content){
					case 'Easy':
						level = 50;
						break;
					case 'Medium':
						level = 70;
						break;
					case 'Hard':
						level = 90;
						break;
				}
				return;
			}
			target = target.parentNode;
		}
	};

	let answered = false;
	let quiz = document.getElementById('quiz');
	console.log(quiz);
	quiz.onclick = function(event) {
		if(!answered){
			console.log('a');
			var target = event.target;
			while (target != this) {
				if (target.classList.contains("answer")) {
					answered = true;
					sendAnswer(target);
					return;
				}
				target = target.parentNode;
			}
		}
	};
	function sendAnswer(elem){
		elem.classList.add('human-answer');

		let request = $.ajax({
			type: "POST",
			url: handleAnswerUrl,
			data: JSON.stringify({answer: elem.id, level})
		});
		request.done(function(data){
			handleCorrectAnswer(data);
		});
		request.fail(function(){
			alert('fail to csrf-protect');
		})
	}

	function handleCorrectAnswer(data){
		try{
			for(let key in data){
				if(data.hasOwnProperty(key))
					console.log(key + ' ' + data[key]);
			}
			let computerAnswerDiv = document.getElementById(data['computer_answer']);
			computerAnswerDiv.classList.add('computer-answer');

			let correctAnswerDiv = document.getElementById(data['correct_answer']);
			correctAnswerDiv.classList.add('correct-answer');

			if(data['is_user_correct'] === false){
				let userAnswerDiv = document.getElementById(data['user_answer']);
				console.log(userAnswerDiv);
				userAnswerDiv.classList.add('incorrect-user-answer');
			}

			let nextButton = document.getElementById('next');
			nextButton.disabled = false;
			nextButton.addEventListener('click', getNextQuestion);

			changeScore(data);
		} catch (e){
			throw new Error('cannot read json');
		}
	}

	function changeScore(data){
		let userScoreElem = document.getElementById("user-score-left");
		let computerScoreElem = document.getElementById("computer-score-right");
		userScoreElem.innerHTML = data['user_score'];
		computerScoreElem.innerHTML = data['computer_score'];
	}

	function getNextQuestion(jsonQuestion){
		window.location = questionUrl;
	}

	$('[data-mobile-app-toggle] .button').click(function () {
		$(this).siblings().removeClass('is-active');
		$(this).addClass('is-active');
	});


}();


