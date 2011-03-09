# -*- coding: utf-8 -*-
from datetime import datetime
from django.utils import simplejson
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
import logging, urllib
import feedparser

logging.getLogger().setLevel(logging.DEBUG)

class FeedomizerError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

# --- configure start ---
PUSH_HUB="http://pushub.appspot.com/"
SITE_URL="http://feedomizer.appspot.com"
SITE_NAME="Feed-o-mizer"
# --- configure end ---

class HomeHandler(webapp.RequestHandler):
  def get(self):
    hub_url, site_url, site_name  = PUSH_HUB, SITE_URL, SITE_NAME
    self.response.out.write(template.render('templates/index.html', locals()))

class FeedHandler(webapp.RequestHandler):
    def get(self,output='json'):
      try:
        feed_url = self.request.get("uri")
        if not feed_url:
            raise FeedomizerError("Please add uri={feed_url} parameter.")
        feed = feedparser.parse(feed_url)
        hub_url, site_url, site_name  = PUSH_HUB, SITE_URL, SITE_NAME
        now = datetime.today()
        if output == 'atom':
            if feed.has_key("dc_date"):
                latest = feed.dc_date
            else:
                latest = now
        response = []
        for entry in feed.entries:
            #logging.debug("entry: %s\n" % repr(entry))
            if entry.has_key("date_parsed"):
                p = entry.date_parsed
                date = datetime(p.tm_year, p.tm_mon, p.tm_mday, p.tm_hour, p.tm_min, p.tm_sec)
            else:
                date = now

            new          = {}
            new["title"] = entry.title
            new["link"]  = entry.link
            # entry GUID and date
            if output == 'atom':  
                new["date"] = date
                if entry.has_key("dc_identifier"):
                    new["guid"] = entry.dc_identifier
                elif  entry.has_key("guid"):    
                    new["guid"] = entry.guid
                else:
                    new["guid"] = urllib.quote_plus(entry.link)
            else:
                new["date"] = date.strftime("%Y-%m-%dT%H:%M:%SZ")
            # entry content
            if entry.has_key("summary"):
                new["content"] = entry.summary
            elif entry.has_key("description"):
                new["content"] = entry.description
            elif entry.has_key("content"):  
                new["content"] = entry.content
            else:    
                new["content"] = entry.title
            # entry author
            if entry.has_key("author_detail"):
                new["author"]         = {}
                new["author"]["name"] = entry.author_detail.name
            elif entry.has_key("author"):
                new["author"]         = {}
                new["author"]["name"] = entry.author
            response.append(new)

        if output == 'atom':
            self.response.headers['Content-Type'] = 'application/atom+xml'
            self.response.out.write(template.render('templates/feed.atom', locals()))
        else:
            self.response.headers['Content-Type'] = 'application/json; charset=UTF-8'
            self.response.out.write(simplejson.dumps(response))
      except Exception, e:
          logging.error('problem: %s' % repr(e))

if __name__ == "__main__":
    pages = []
    pages.append(("/", HomeHandler))
    pages.append(("/(json|atom)", FeedHandler))
    webapp.template.register_template_library('templatefilters')
    run_wsgi_app(webapp.WSGIApplication(pages, debug=True))
