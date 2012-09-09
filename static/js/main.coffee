$ ->
  $('input').focus()
  channel = new goog.appengine.Channel(window.chatByIpToken)
  socket = channel.open()

  connect = ->
    channel = new goog.appengine.Channel(window.chatByIpToken)
    socket = channel.open()

  socket.onerror = ->
    connect()

  socket.onclose = ->
    connect()

  sendMessage = (msg) ->
    $.ajax(
      url: "/message?message="
      type: "POST"
      data: JSON.stringify(message: msg)
    ).done (response) ->
      console.log response
      $("input").val('')

  printMessage = (data) ->
    message = urlize(data.message, {target: '_blank'})
    $(".messages").append(
      "<table class='message-line'>
        <tr>
          <td class='name'>#{data.name}: </td>
          <td class='message'>#{message}</td>
        </tr>
      </table>"
    )
#    $('body').scrollTop($('body')[0].scrollHeight)

  $("form").submit (e) ->
    e.preventDefault()
    sendMessage($('input').val())

  socket.onopen = ->
    connected = true
    sendMessage "connected"

  chatlog = JSON.parse(localStorage['chatlog'] or '[]')

#  $.each chatlog, (i, data) ->
#    printMessage(data)

  socket.onmessage = (msg) ->
    data = JSON.parse(msg.data)
    if data.signOn or data.signOff
      $('.num-people').text(data.numPeople)
    else
      #chatlog.push(data)
      localStorage['chatlog'] = JSON.stringify(chatlog)
      printMessage(data)