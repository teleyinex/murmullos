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
        self.stage.connect('fullscreen',self.reposition,self)
        self.stage.set_fullscreen(True)

        self.color = clutter.Color(0xff,0xff,0xff,0xff)

        self.identica = identica.Identica(tag)

        # Code for the bacground rectangle
        self.rectangle = clutter.Rectangle()
        self.rectangle.set_border_width(3)
        self.rectangle.set_color(clutter.Color(0x00,0x00,0x00,0x00))
        self.rectangle.set_border_color(clutter.Color(0xff,0xff,0xff,0xff))
        self.rectangle.hide()

        # Code for the avatar:
        self.avatar = clutter.Texture()

        # Code for the nipple
        self.nipple = clutter.Texture()

        # Code for the text:
        self.label = clutter.Text()
        self.label.set_color(self.color)
        self.label.set_font_name('Sans 16')
        self.label.set_line_wrap(True)

        # Grouping everything:
        self.group = clutter.Group()
        self.group.add(self.avatar,self.label,self.nipple,self.rectangle)
        self.stage.add(self.group)

        # Creating the timeline:
        self.timeline = clutter.Timeline(8000)
        self.timeline.connect('completed',self.on_timeline_completed,self)
        self.timeline.set_loop(True)
        alpha = clutter.Alpha(self.timeline,clutter.LINEAR)
        self.behaviour = clutter.BehaviourOpacity(0xdd,0,alpha)
        self.behaviour.apply(self.group)

    def reposition(stage, frame_num, self):
        # Obtain the size of the fullscreen stage
        (x,y) = self.stage.get_size()

        # Size for the group: Rectangle, Texture and Label
        width = x - (x*40)/100
        height = y - (y*80)/100
        self.rectangle.set_size(width, height)
        self.label.set_size(width-50, height-50)

        # Position for the group: Rectangle, Texture and Label
        sx = (x/2)-(self.rectangle.get_width()/2)
        sy = (y/2)-(self.rectangle.get_height()/2)

        self.avatar.set_position(sx,sy)
        self.rectangle.set_position(sx+48+5+23,sy-5)
        self.nipple.set_position(sx+48+5,sy)
        self.label.set_position(sx+48+5+27+5,sy)

       
    def IdenticaUpdate(self):
        self.identica.update()

    def post(self,avatar,message):
        # Avatar
        self.avatar.set_from_file(avatar)
        
        # Nipple
        self.nipple.set_from_file("img/nipple.png")

        # Message
        self.label.set_text(message)

    def on_timeline_completed(timeline, frame_num, self):
        self.rectangle.show()
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
        tag = "gnu"
    
    app = Murmullos(tag)
    app.run()

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))


