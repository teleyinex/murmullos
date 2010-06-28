#!/usr/bin/env python 
# -*- coding: utf-8 -*-

import urllib, simplejson

class Identica:
    def __init__(self, query = None):
        if (query != None):
            self.url = "http://identi.ca/api/search.json?q=" + query
        else:
            self.url = "http://identi.ca/api/statuses/public_timeline.json"

    def update(self):
        self.data = simplejson.load(urllib.urlopen(self.url))
    
