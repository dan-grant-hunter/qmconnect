$(function() {
  console.log('Script loaded')

  $('.conversation-partner').on('click', function() {
    conversation_id = this.id
    showMessage(conversation_id)
    $('#message-form').show()
  });

  $('#message-submit').on('click', function() {
    //receiver_id = $('.receiver-id').attr('id')
    sendMessage(8)
  });
});

/*
  This function returns the conversation with
  a particular user.
*/
function showMessage(conversation_id) {
  $.ajax({
    url: "/conversation/" + conversation_id,
    type: "GET",
    success: function(response) {
      console.log('success')
      $('.messages').html('')
      $('.messages').append(response + "</br>")
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
      'request.user': $('.request-user').attr('id')
    },
    success: function(response) {
      console.log("Message sent successfully!")
      console.log(response)
      //$('.messages').append(response['sender'] + " to " + response['receiver'] + ": " + response['text'])
    },
    error: function(xhr) {
      console.log($('.request-user').attr('id'))
      console.log(xhr)
    }
  });
}
