from google.appengine.ext import ndb
import logging
from google.appengine.api import channel
import random_name
import json

class Person(ndb.Model):
  token = ndb.StringProperty()
  name = ndb.StringProperty()
  chat_room_id = ndb.StringProperty()

  @staticmethod
  def get_by_cookie(cookie):
    return Person.get_or_insert(cookie)

  def in_chat_room(self, chat_room):
    return self.key.id() in chat_room.people_ids

  def remove_from_old_chat_room(self):
    if self.chat_room_id and self.chat_room_id != '':
      remove_person_from_chat_room(self)

  def channel_token(self):
    return channel.create_channel(self.key.id(), 1440)

  def send_message_to_chat_room(self, message, chat_room):
    if message != '':
      data = {
        'name': self.name,
        'message': message
      }
      self.send_data_to_chat_room(data, chat_room)

  def send_sign_on_to_chat_room(self, chat_room):
    data = {
      'signOn': True,
      'name': self.name,
      'numPeople': chat_room.num_people()
    }
    self.send_data_to_chat_room(data, chat_room)

  def send_sign_off_to_chat_room(self):
    chat_room = get_chat_room_by_id(self.chat_room_id)
    data = {
      'signOff': True,
      'name': self.name,
      'numPeople': chat_room.num_people()
    }
    self.send_data_to_chat_room(data, chat_room)

  def send_data_to_chat_room(self, data, chat_room):
    for person_id in chat_room.people_ids:
      logging.info('SENDING %s TO PERSON: %s' % (data, person_id))
      channel.send_message(person_id, json.dumps(data))

  @staticmethod
  def create(cookie):
    person = Person(id=cookie)
    person.name = random_name.generate()
    return person


class ChatRoom(ndb.Model):
  people_ids = ndb.StringProperty(repeated=True)
  names = ndb.StringProperty(repeated=True)

  @staticmethod
  def get_by_ip(ip):
    logging.info(ip)
    return ChatRoom.get_or_insert(ip)

  def remove_person(self, person):
    self.people_ids.remove(person.key.id())
    self.put()

  def add(self, person):
    self.people_ids.append(person.key.id())
    self.put()
    while person.name in self.names:
      person.name = random_name.generate()
    person.chat_room_id = self.key.id()
    person.put()

  def remove(self, person):
    if person.key.id() in self.people_ids:
      self.people_ids.remove(person.key.id())
      self.put()

  def size(self):
    return len(self.people_ids)

  def num_people(self):
    num_people = self.size() - 1
    if num_people == 1:
      num_people = '1 person'
    else:
      num_people = '%d people' % num_people
    return num_people

def remove_person_from_chat_room(person):
  # Had to put below both models to parse.
  old_chat_room = ChatRoom.get_by_id(person.chat_room_id)
  old_chat_room.remove(person)

def get_chat_room_by_id(chat_room_id):
  return ChatRoom.get_by_id(chat_room_id)