#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# Copyright 2010 Daniel Lombraña González <teleyinex AT gmail DOT com>
# 
# This file is part of Murmullos.
# 
# Murmullos is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Murmullos is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Murmullos.  If not, see <http://www.gnu.org/licenses/>.


import urllib, simplejson

class Identica:
    def __init__(self, service="identica", tag = None):
        # Service parameter choses Identica (by default) or Twitter
        if (service == "identica"):
            if (tag != None):
                self.url = "http://identi.ca/api/search.json?q=" + tag + "&rpp=25"
            else:
                self.url = "http://identi.ca/api/statuses/public_timeline.json"
        else:
            if (tag != None):
                self.url = "http://search.twitter.com/search.json?q=" + tag + "&rpp=25"
            else:
                self.url = "http://search.twitter.com/search.json?q=" + tag


    def update(self):
        self.data = simplejson.load(urllib.urlopen(self.url))
    
