#!/usr/bin/env python 
# -*- coding: utf-8 -*-

import sys
import clutter
import urllib
import identica

class Murmullos:
    def __init__(self,tag):
        self.stage = clutter.Stage()
        self.stage.set_color(clutter.color_from_string('Black'))
        self.stage.set_size(800,600)
        self.stage.set_title("Murmullos")
        self.stage.connect('key-press-event',clutter.main_quit)
        self.stage.set_fullscreen(True)

        self.color = clutter.Color(0xff,0xff,0xff,0xff)

        self.identica = identica.Identica(tag)

        # Code for the avatar:
        self.texture = clutter.Texture()
        self.texture.set_position(300,300)

        # Code for the text:
        self.label = clutter.Text()
        self.label.set_size(600,900)
        self.label.set_color(self.color)
        self.label.set_font_name('Sans 16')
        self.label.set_line_wrap(True)
        label_x = self.stage.get_width()/2 
        label_y = self.stage.get_height()/2 
        self.label.set_position(label_x, label_y)

        # Grouping everything:
        self.group = clutter.Group()
        self.group.add(self.texture,self.label)
        self.stage.add(self.group)

        # Creating the timeline:
        self.timeline = clutter.Timeline(4000)
        self.timeline.connect('completed',self.on_timeline_completed,self)
        self.timeline.set_loop(True)
        alpha = clutter.Alpha(self.timeline,clutter.LINEAR)
        self.behaviour = clutter.BehaviourOpacity(0xdd,0,alpha)
        self.behaviour.apply(self.group)
       
    def IdenticaUpdate(self):
        self.identica.update()

    def post(self,avatar,message):
        # Avatar
        self.texture.set_from_file(avatar)

        # Message
        self.label.set_text(message)

    def on_timeline_completed(timeline, frame_num, self):
        item = self.identica.data['results'].pop()
        urllib.urlretrieve(item['profile_image_url'],"avatar")
        self.post("avatar",item['text'])
        print("Quedan %s elementos",len(self.identica.data['results']),item['text'])
        if (len(self.identica.data['results'])==0):
            self.IdenticaUpdate()

    def run (self):
        self.stage.show_all()
        self.IdenticaUpdate()
        self.timeline.start()

        clutter.main()

def main (args):
    if args:
        tag = args[0]
    else:
        tag = "murmullos"
    
    app = Murmullos(tag)
    app.run()

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))


