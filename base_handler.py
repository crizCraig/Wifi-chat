import base64
import hashlib
import os
import json
import uuid
from datetime import datetime, timedelta
import re

import webapp2
from webapp2_extras import sessions
import logging
import jinja2

from models import Person

import models

jinja_environment = jinja2.Environment(
  loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

QUOTE_SURROUND = re.compile('"(.*)"')

class BaseHandler(webapp2.RequestHandler):
  """Base class to be used for most request handlers."""

  # For stuff accessible across all handlers.
  def out(self, data):
    self.response.out.write(data)

  def json_out(self, data):
    self.response.headers['Content-Type'] = 'application/json'
    self.out(json.dumps(data))

  def get_checkbox(self, name):
    return self.request.get(name) == 'on'

  def set_checkbox(self, checked):
    return 'checked' if checked else ''

  def template_out(self, filename, template_values=None):
    if template_values is None:
      template_values = {}
    return self.out(self.render_template(filename, template_values))

  def jsonp(self, obj):
    self.response.headers['Content-Type'] = 'text/javascript'
    self.out('%s(%s);' % (self.request.get('callback'), json.dumps(obj)))

  def jsonp_template_out(self, file_path, template_values=None):
    """Return HTML body with JSONP so we can XSS in browser during dev."""
    self.response.headers['Content-Type'] = 'text/javascript'
    if template_values is None:
      template_values = {}
    body = self.render_template(file_path, template_values)\
      .replace('\r','')\
      .replace('\n', '')\
      .replace("'", '&#39;')

    self.out(self.request.get('callback') + '( {"body": \'%s\'});' % body)

  def render_template(self, filename, template_values=None):
    if template_values is None:
      template_values = {}
    all_template_values = {
      'APP_VERSION': os.environ['CURRENT_VERSION_ID'],
      'HOST': self.request.host,
      'PAGE_URL_FULL': self.request.path_url,
      'QUERY_STRING': self.request.query_string,
      'URL': self.request.url,
      'PATH': self.request.path
    }

    all_template_values.update(template_values)
    template = jinja_environment.get_template(filename)
    return template.render(all_template_values)

  def set_cookie(self, name, value):
    expires = datetime.utcnow() + timedelta(weeks=9999)
    expires_rfc822 = expires.strftime('%a, %d %b %Y %H:%M:%S GMT')
    protocol = os.environ['wsgi.url_scheme']
    logging.info('wazaaa')
    logging.info('protocol ' + protocol)
    secure = ' Secure; ' if protocol == 'https' >= 0 else ''
    self.response.headers.add_header(
      'Set-Cookie',
      '{name}={value}; path=/; expires={expires}; {secure} HttpOnly'.format(
        name=name,
        value=value,
        secure=secure,
        expires=expires_rfc822))
    pass

  def get_cookie(self, name='chatbyip2'):
    if name and self.request.cookies.has_key(name):
      return self.request.cookies[name], False
    else:
      val = rand_str(10)
      self.set_cookie(name, val)
      return val, True

  def person(self):
    cookie, is_new_cookie = self.get_cookie()
    if is_new_cookie:
      person = Person.create(cookie)
    else:
      person = Person.get_by_cookie(cookie)

    return person

def rand_str(length):
  """Create random string of certain length.

  Good up to 38 characters, whatever that means.
  CQ: I did some sort of randomness or speed test to get that number. :)
  """
  h = hashlib.sha224()
  h.update(str(uuid.uuid4()).replace('-', ''))
  b64 = base64.b64encode(h.digest(), altchars=['h', 'c', 'd', '9', '3'])
  return b64[0:length]