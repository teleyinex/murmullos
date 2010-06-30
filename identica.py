#!/usr/bin/env python 
# -*- coding: utf-8 -*-

import urllib, simplejson

class Identica:
    def __init__(self, tag = None):
        if (tag != None):
            self.url = "http://identi.ca/api/search.json?q=" + tag
        else:
            self.url = "http://identi.ca/api/statuses/public_timeline.json"

    def update(self):
        self.data = simplejson.load(urllib.urlopen(self.url))
    
