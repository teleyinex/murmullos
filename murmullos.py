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

import sys
import clutter
import urllib
import identica

class Murmullos:
    def __init__(self,service,tag):
        self.stage = clutter.Stage()
        self.stage.set_color(clutter.color_from_string('Black'))
        self.stage.set_size(800,600)
        self.stage.set_title("Murmullos")
        self.stage.connect('key-press-event',clutter.main_quit)
        self.stage.connect('destroy',clutter.main_quit)
        self.stage.connect('fullscreen',self.reposition,self)
        self.stage.hide_cursor()
        self.stage.set_fullscreen(True)

        self.color = clutter.Color(0xff,0xff,0xff,0xff)

        self.identica = identica.Identica(service,tag)

        # Code for the logo:
        self.logo = clutter.Texture()
        self.logo.set_from_file("img/logo.png")
        self.stage.add(self.logo)

        # Code for the avatar:
        self.avatar = clutter.Texture()

        # Code for the text:
        self.label = clutter.Text()
        self.label.set_color(self.color)
        self.label.set_font_name('Sans 16')
        self.label.set_line_wrap(True)

        # Grouping everything:
        self.group = clutter.Group()
        self.group.add(self.avatar,self.label)
        self.stage.add(self.group)

        # Creating the timeline:
        self.timeline = clutter.Timeline(8000)
        self.timeline.connect('completed',self.on_timeline_completed,self)
        self.timeline.set_loop(True)
        alpha = clutter.Alpha(self.timeline,clutter.LINEAR)
        self.behaviour = clutter.BehaviourOpacity(0xdd,0,alpha)
        self.behaviour.apply(self.group)
        self.behaviour.apply(self.logo)

        # Create the bubble if we are not in full screen mode
        if not self.stage.get_fullscreen():
            self.set_scene()


    def reposition(stage, frame_num, self):
        self.set_scene()

    def set_scene(self):
        # Obtain the size of the stage
        (x,y) = self.stage.get_size()

        # Size for the group: Rectangle, Texture and Label
        width = x - (x*40)/100
        height = y - (y*80)/100

        # Create the bubble
        width = round(width,-2)
        height = round(height,-2)
        if (height <= 100): height = 200
        self.new_bubble(width , height)
        self.bubble.hide()
        self.group.add(self.bubble)

        self.label.set_size(width-50, height-50)

        # Position for the logo
        sx = (x/2)-(self.logo.get_width()/2)
        sy= (y/2)-(self.logo.get_height()/2)

        self.logo.set_position(sx,sy)

        # Position for the group: Bubble, Texture and Label
        sx = (x/2)-(self.bubble.get_width()/2)
        sy = (y/2)-(self.bubble.get_height()/2)

        self.bubble.set_position(sx,sy)
        self.avatar.set_position(sx-48,sy+75)
        self.label.set_position(sx+60,sy+30)

        
       
    def IdenticaUpdate(self):
        self.identica.update()

    def post(self,avatar,message):
        # Avatar
        self.avatar.set_from_file(avatar)
        
        # Message
        self.label.set_text(message)

    def on_timeline_completed(timeline, frame_num, self):
        self.stage.remove(self.logo)
        self.bubble.show()
        try:
            item = self.identica.data['results'].pop()
            urllib.urlretrieve(item['profile_image_url'],"/tmp/avatar")
            self.post("/tmp/avatar",item['text'])
            print("Quedan %s elementos",len(self.identica.data['results']),item['text'])
            if (len(self.identica.data['results'])==0):
                self.IdenticaUpdate()
        except IndexError:
            self.post("default-avatar.png","Nothing found about your topic. Try another search ^_^")
        except AttributeError:
            self.post("default-avatar.png","Enable your Internet connection if you want to display dents or tweets ;)")

    def new_bubble(self, width=40, height=20):
        # First, we create the basic elements as textures
        self.corner_top_left = clutter.Texture()
        self.corner_top_right = clutter.Texture()
        self.corner_bottom_left = clutter.Texture()
        self.corner_bottom_right = clutter.Texture()
        self.border_top = clutter.Texture()
        self.border_bottom = clutter.Texture()
        self.border_left = clutter.Texture()
        self.border_right = clutter.Texture()
        self.nipple2 = clutter.Texture()

        # Now we load the textures for each item
        self.corner_top_left.set_from_file("img/bubble/corner_top_left.png")
        self.corner_top_right.set_from_file("img/bubble/corner_top_right.png")
        self.corner_bottom_left.set_from_file("img/bubble/corner_bottom_left.png")
        self.corner_bottom_right.set_from_file("img/bubble/corner_bottom_right.png")
        self.border_top.set_from_file("img/bubble/border_top.png")
        self.border_bottom.set_from_file("img/bubble/border_bottom.png")
        self.border_left.set_from_file("img/bubble/border_left.png")
        self.border_right.set_from_file("img/bubble/border_right.png")
        self.nipple2.set_from_file("img/bubble/nipple.png")

        # First, we create the top bar 
        tile_width = self.border_top.get_width()
        self.border_top.set_position(0,0)
        border_top_tiles = [self.border_top]
        for i in range(1,int(width/tile_width)):
            border_top_tiles.append(clutter.Clone(self.border_top))
            border_top_tiles[i].set_position(tile_width*i,0)

        self.bar_top = clutter.Group()
        for tile in border_top_tiles:
            self.bar_top.add(tile)

        # Secondly, we create the bottom bar 
        tile_width = self.border_bottom.get_width()
        self.border_bottom.set_position(0,height)
        border_bottom_tiles = [self.border_bottom]
        for i in range(1,int(width/tile_width)):
            border_bottom_tiles.append(clutter.Clone(self.border_bottom))
            border_bottom_tiles[i].set_position(tile_width*i,height)

        self.bar_bottom = clutter.Group()
        for tile in border_bottom_tiles:
            self.bar_bottom.add(tile)

        # Thirdly, we create the left bar
        tile_height = self.border_left.get_height()
        self.border_left.set_position(0,0)
        border_left_tiles = [self.border_left]
        # We have to add also the nipple
        self.nipple2.set_position(-36,49)
        border_left_tiles.append(self.nipple2)
        for i in range(2,int(height/tile_height)):
            border_left_tiles.append(clutter.Clone(self.border_left))
            border_left_tiles[i].set_position(0,tile_height*i)

        self.bar_left = clutter.Group()
        for tile in border_left_tiles:
            self.bar_left.add(tile)

        # Finally, we create the right bar
        tile_height = self.border_right.get_height()
        self.border_right.set_position(width,0)
        border_right_tiles = [self.border_right]
        for i in range(1,int(height/tile_height)):
            border_right_tiles.append(clutter.Clone(self.border_right))
            border_right_tiles[i].set_position(width,tile_height*i)

        self.bar_right = clutter.Group()
        for tile in border_right_tiles:
            self.bar_right.add(tile)

        # Now we create the whole bubble
        self.bubble = clutter.Group()
        self.corner_top_left.set_position(40,0)
        self.bar_top.set_position(self.corner_top_left.get_x()+self.corner_top_left.get_width(),0)
        self.corner_top_right.set_position(self.bar_top.get_width()+self.bar_top.get_x(),0)
        self.bar_left.set_position(40,self.corner_top_left.get_height())
        self.bar_right.set_position(self.corner_top_right.get_width()+self.corner_top_left.get_x(),self.corner_top_right.get_height())
        self.corner_bottom_left.set_position(40,self.bar_left.get_height()+self.corner_bottom_left.get_height())
        self.bar_bottom.set_position(self.corner_top_left.get_x()+self.corner_bottom_left.get_width(),self.corner_bottom_left.get_height()-4)
        self.corner_bottom_right.set_position(self.bar_bottom.get_width()+self.bar_bottom.get_x(),self.bar_right.get_height()+self.corner_bottom_right.get_height())

        self.bubble.add(self.corner_top_left,self.bar_top,self.corner_top_right,self.bar_left,self.bar_right,self.corner_bottom_left,self.bar_bottom,self.corner_bottom_right)

    def run (self):
        self.stage.show_all()
        self.IdenticaUpdate()
        self.timeline.start()

        clutter.main()

def main (args):
    if args:
        tag = args[0]
        service = args[1]
    else:
        tag = "gnu"
    
    app = Murmullos(service,tag)
    app.run()

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))


