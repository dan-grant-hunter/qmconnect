$(function() {
  console.log('Script loaded')

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
      'conversation_id': $('#conversation-span').text()
    },
    success: function(response) {
      console.log("Message sent successfully!")
      $('.messages').append(response['sender'] + " to " + response['receiver'] + ": " + response['text'])
      $('input[name=text]').val('')
    },
    error: function(xhr) {
      console.log($('.request-user').attr('id'))
      console.log(xhr)
    }
  });
}
