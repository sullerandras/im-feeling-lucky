#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import urllib2
from google.appengine.api import images
import logging
import re

from webapp2_extras import sessions

class BaseHandler(webapp2.RequestHandler):
    def dispatch(self):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)

        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session()

class MainHandler(BaseHandler):
    def get(self, path = None):
        origin = self.session.get('origin', '')
        if not origin:
            self.redirect('/im-feeling-lucky/index.html')
            return
        # self.response.out.write('path: %s, origin: %s' % (path, origin))
        src = origin + path
        logging.info('getting content: %s', src)
        response = urllib2.urlopen(src)
        headers = response.headers
        logging.info('headers: %s' % headers)
        ct = headers.get('content-type', '')
        if ct in IMAGE_TYPES:
            self.luckify_image(ct, response.read())
        else:
            self.response.headers['content-type'] = ct
            self.response.out.write(response.read())

    def luckify_image(self, contentType, data):
        #apply the I'm feeling lucky filter
        img = images.Image(data)
        img.im_feeling_lucky()
        luckied = img.execute_transforms(output_encoding=images.JPEG)

        self.response.headers['content-type'] = contentType
        # self.response.out.write(response.headers)
        self.response.out.write(luckied)

IMAGE_TYPES = ['image/jpeg']

class ImFeelingLuckyHandler(BaseHandler):
    def get(self):
        src = self.request.GET.get('src', '')
        r = re.search('^(https?://[^/]+)(/.*)?$', src)
        if not r:
            self.session['origin'] = None
            self.redirect('/im-feeling-lucky/index.html')
            return
        origin = r.group(1)
        path = r.group(2) or '/'
        logging.info('origin: %s, path: %s', origin, path)
        self.session['origin'] = origin
        return self.redirect(path)

config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'd;fkhpiohw eonsdlkgvmad s ;glke gosdgdsojgads ;hglsdhweoi;ds ;fkjlsdng;oiew ;duvbdns;fjk,'
}
app = webapp2.WSGIApplication([('/im-feeling-lucky', ImFeelingLuckyHandler), ('(.*)', MainHandler)],
                              debug=True, config=config)
