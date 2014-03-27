from google.appengine.api import users
from google.appengine.api import memcache
from google.appengine.ext import db

import webapp2
import jinja2
import cgi
import cStringIO
import datetime
import logging
import urllib
import os

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)



class Greeting(db.Model):
    """Models an individual Guestbook entry with author, content, and date."""
    author = db.StringProperty()
    content = db.StringProperty(multiline=True)
    date = db.DateTimeProperty(auto_now_add=True)



def guestbook_key(guestbook_name=None):
    """Constructs a Datastore key for a Guestbook entity with guestbook_name."""
    return db.Key.from_path('Guestbook', guestbook_name or 'default_guestbook');



class MainPage(webapp2.RequestHandler):

    def get(self):
        self.response.write('<html><body>')
        guestbook_name = self.request.get('guestbook_name')

        greetings = self.get_greetings(guestbook_name)
        stats = memcache.get_stats()

        self.response.out.write('<b>Cache Hits: %s</b><br />' % stats['hits'])
        self.response.out.write('<b>Cache Misses: %s</b><br /><br />' % stats['misses'])
        self.response.out.write(greetings)

        self.response.out.write("""
          <form action="/sign?%s" method="post">
            <div><textarea name="content" rows="3" cols="60"></textarea></div>
            <div><input type="submit" value="Sign Guestbook"></div>
          </form>
          <hr>
          <form>Guestbook name: <input value="%s" name="guestbook_name">
          <input type="submit" value="switch"></form>
        </body>
      </html>""" % (urllib.urlencode({'guestbook_name': guestbook_name}),
                          cgi.escape(guestbook_name)))


    def get_greetings(self, guestbook_name):
        """get_greetings()

        Checks the cache to see if there are cached greetings.
        If not, call render_greetings and set the cache.

        Args:
          guestbook_name: Guestbook entity group key (string)

        Returns:
          A string of HTML containing greetings.
        """

        greetings = memcache.get('%s:greetings' % guestbook_name)
        if greetings is not None:
            return greetings
        else:
            greetings = self.render_greetings(guestbook_name)
            if not memcache.add('%s:greetings' % guestbook_name, greetings, 10):
                logging.error('Memcache set failed.')
            return greetings


    def render_greetings(self, guestbook_name):
        """render_greetings()

        Queries the database for greetings, iterate through the
        results and create the HTML.

        Args:
          guestbook_name: Guestbook entity group key (string)

        Returns:  
          A string of HTML containing greetings.
        """

        greetings = db.GqlQuery('SELECT * '
                                'FROM Greeting '
                                'WHERE ANCESTOR IS :1 '
                                'ORDER BY date DESC LIMIT 10',
                                guestbook_key(guestbook_name))
        output = cStringIO.StringIO()
        
        for greeting in greetings:
            if greeting.author:
                output.write('<b>%s</b> wrote:' % greeting.author)
            else:
                output.write('An anonymous person wrote:')
            output.write('<blockquote>%s</blockquote>' % cgi.escape(greeting.content))

        return output.getvalue()


class Guestbook(webapp2.RequestHandler):

    def post(self):
        guestbook_name = self.request.get('guestbook_name')
        greeting = Greeting(parent=guestbook_key(guestbook_name))

        if users.get_current_user():
            greeting.author = users.get_current_user().nickname()

        greeting.content = self.request.get('content')
        greeting.put()
        memcache.flush_all()

        self.redirect('/?' + urllib.urlencode({'guestbook_name': guestbook_name}))




application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/sign', Guestbook),
], debug=True)