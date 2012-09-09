import os
import webapp2
import logging
from google.appengine.api import channel
from models import ChatRoom, Person
import json
import urllib

from base_handler import BaseHandler

# TODO: Deal with expired tokens
# TODO: Deal with failed connections.

class HomeHandler(BaseHandler):
  def get(self):
    ip = self.request.remote_addr
    chat_room = ChatRoom.get_by_ip(ip)
    person = self.person()

    if not person.in_chat_room(chat_room):
      person.remove_from_old_chat_room()
      chat_room.add(person)

    self.template_out('templates/home.html', template_values={
      'token': person.channel_token(),
      'num_people': chat_room.num_people()
    })

class MessageHandler(BaseHandler):
  @staticmethod
  def sanitize_html(s):
    replacements = [
      ('&', '&amp;'),
      ('<', '&lt;'),
      ('>', '&gt;'),
    ]
    for before, after in replacements:
      s = s.replace(before, after)
    return s

  def get_message(self):
    message = json.loads(urllib.unquote_plus(self.request.body))['message']
    return self.sanitize_html(message)


  def post(self):
    chat_room = ChatRoom.get_by_ip(self.request.remote_addr)
    message = self.get_message()
    person = self.person()

#    if message == 'connected':
#      person.send_sign_on_to_chat_room(chat_room)
#    else:
    person.send_message_to_chat_room(message, chat_room)

class ConnectedHandler(BaseHandler):
  def post(self):
    # TODO: notify users on the same IP by changing number and putting name in list
    pass
#    chat_room = ChatRoom.get_by_ip(self.request.remote_addr)
#    person = self.person()
#    person.send_sign_on_to_chat_room(chat_room)

class DisconnectedHandler(BaseHandler):
  def post(self):
    # TODO: notify users on the same IP by changing number and putting name in list
    person_id = self.request.get('from')
    person = Person.get_by_id(person_id)
    person.send_sign_off_to_chat_room()

class RobotsTextHandler(BaseHandler):
  def get(self):
    allow = os.environ['HTTP_HOST'] == 'chatbyip.appspot.com'
    self.template_out('html/robots.txt', {'allow': allow})

app = webapp2.WSGIApplication([
  ('/', HomeHandler),
  ('/message', MessageHandler),
  ('/_ah/channel/connected/', ConnectedHandler),
  ('/_ah/channel/disconnected/', DisconnectedHandler),

], debug=os.environ.get('SERVER_SOFTWARE', '').startswith('Dev'))