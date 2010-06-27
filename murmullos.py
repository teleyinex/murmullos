#!/usr/bin/env python 
# -*- coding: utf-8 -*-

import sys
import clutter

class Murmullos:
    def __init__(self,message):
        self.stage = clutter.Stage()
        self.stage.set_color(clutter.color_from_string('Black'))
        self.stage.set_size(800,600)
        self.stage.set_title("Murmullos")
        self.stage.connect('key-press-event',clutter.main_quit)
        self.stage.set_fullscreen(True)

        color = clutter.Color(0xff,0xff,0xff,0xff)

        self.label = clutter.Text()
        self.label.set_text(message)
        self.label.set_color(color)
        self.label.set_font_name('Sans 32')
        (label_width,label_height) = self.label.get_size()
        label_x = self.stage.get_width() - label_width - 50
        label_y = self.stage.get_height() - label_height
        self.label.set_position(label_x, label_y)
        self.stage.add(self.label)

        self.timeline = clutter.Timeline(4000)
        self.timeline.set_loop(True)
        alpha = clutter.Alpha(self.timeline,clutter.LINEAR)
        self.behaviour = clutter.BehaviourOpacity(0xdd,0,alpha)
        self.behaviour.apply(self.label)


    def run (self):
        self.stage.show_all()
        self.timeline.start()
        clutter.main()


def main (args):
    if args:
        message = args[0]
    else:
        message = "Hellow Murmullos"
    
    app = Murmullos(message)
    app.run()

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))


