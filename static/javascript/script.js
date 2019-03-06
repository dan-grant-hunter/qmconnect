$(function() {
  console.log('Script loaded')

  // retrieve the conversation
  $('.conversation-partner').on('click', function() {
    // this refers to the a tag
    // this.id retrieve the id from the a tag
    conversation_id = this.id

    // this.text refers to the value of the anchor tag
    // it is the receiver of the message
    receiver = this.classList[1]

    // display the form that allows the users to send messages
    // hidden initially
    $('#message-form').show()

    // call the showMessage function with the id of the convo
    showMessage(conversation_id, receiver)
  });

  // send message in the current conversation
  $('#message-submit').on('click', function() {
    receiver_id = $('#receiver-span').text()
    sendMessage(receiver_id)
  });

  // answer a question
  // https://stackoverflow.com/questions/23393076/jquery-ajax-call-only-works-once
  $(document).on('click', '#answer-submit', function() {
    topic_id = $('#topic_pk').text()
    question_id = $('#question_pk').text()
    page_number = $('#page_number').text()

    leave_reply(topic_id, question_id, page_number)
  });

  ///////////////////////////////////////////////////////////////
  ////////////////////  NETWORK PAGE ///////////////////////////
  /////////////////////////////////////////////////////////////
  // Allows the logged in user to filter the registered users
  $(document).on('click', '#submitFiltering', function(event) {
    filter(event)
  });

  // Allows the users to reset the filters
  $(document).on('click', '#reset-btn', function(event) {
    reset(event)
  });
  ///////////////////////////////////////////////////////////////
});

/*
  This function returns the conversation with
  a particular user.
*/
function showMessage(conversation_id, receiver) {
  $.ajax({
    url: "/conversation/" + conversation_id,
    type: "GET",
    success: function(response) {
      console.log('success')
      $('.messages').html('')
      $('.messages').append(response + "</br>")
      // attach the receiver and conversation IDs to the webpage so they can be retrieved by the other function - sendMessage
      $('.messages').append('<span style="display:none;" id="receiver-span">' + receiver + '</span>')
      $('.messages').append('<span style="display:none;" id="conversation-span">' + conversation_id + '</span>')
    },
    error: function(xhr) {
      console.log(xhr)
    }
  });
}

/*
  This function allows users to send messages
*/
function sendMessage(receiver_id) {
  $.ajax({
    url: "/messages/" + receiver_id + "/send_message/",
    type: "POST",
    data: {
      'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
      'text': $('input[name=text]').val(),
      'request.user': $('.request-user').attr('id'),
      // send the conversation id so the new message can be attached to the proper conversation
      'conversation_id': $('#conversation-span').text()
    },
    success: function(response) {
      console.log("Message sent successfully!")
      $('.messages').append(response['sender'] + " to " + response['receiver'] + ": " + response['text'] + "</br>")
      // clear the input after sending the message
      $('input[name=text]').val('')
    },
    error: function(xhr) {
      console.log(xhr)
    }
  });
}

/*
  This functions allows users to leave replies on questions
*/
function leave_reply(topic_id, question_id, page_number) {
  $.ajax({
    url: "/topics/" + topic_id + "/questions/" + question_id + "/reply/" + "?page=" + page_number,
    type: "POST",
    data: {
      'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
      'message': $('#textarea_answerquestion').val(),
      'pk': topic_id,
      'question_pk': question_id
    },
    success: function(response) {
      $("#whole").load(document.URL + " #whole");
    },
    error: function(xhr) {
      console.log(xhr.responseText)
    }
  });
}

/*
  Filter the data in the network page
*/
function filter(event) {
  var form = $('#formFiltering');
  $.ajax({
    url: "/network/",
    type: "GET",
    data: form.serialize(),
    success: function(response) {
      $('#main-part').replaceWith($('#main-part', response));
    },
    error: function(xhr) {
      console.log(xhr.responseText)
    }
  });
  event.preventDefault();
}

/*
  Reset the filtering in the network page
  Display all users registered
*/
function reset(event) {
  $.ajax({
    url: "/network/",
    type: "GET",
    success: function(response) {
      $('#main-part').replaceWith($('#main-part', response));
      $('#reset-filters').replaceWith($('#reset-filters', response));
    },
    error: function(xhr) {
      console.log(xhr.responseText)
    }
  });
  event.preventDefault();
}
