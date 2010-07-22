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

        # Create the bubble
        self.new_bubble(400, 200)

       
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

        # Now we load the textures for each item
        self.corner_top_left.set_from_file("img/bubble/corner_top_left.png")
        self.corner_top_right.set_from_file("img/bubble/corner_top_right.png")
        self.corner_bottom_left.set_from_file("img/bubble/corner_bottom_left.png")
        self.corner_bottom_right.set_from_file("img/bubble/corner_bottom_right.png")
        self.border_top.set_from_file("img/bubble/border_top.png")
        self.border_bottom.set_from_file("img/bubble/border_bottom.png")
        self.border_left.set_from_file("img/bubble/border_left.png")
        self.border_right.set_from_file("img/bubble/border_right.png")

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
        for i in range(1,int(height/tile_height)):
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
        self.corner_top_left.set_position(0,0)
        self.bar_top.set_position(self.corner_top_left.get_width(),0)
        self.corner_top_right.set_position(self.bar_top.get_width()+self.bar_top.get_x(),0)
        self.bar_left.set_position(0,self.corner_top_left.get_height())
        self.bar_right.set_position(self.corner_top_right.get_width(),self.corner_top_right.get_height())
        self.corner_bottom_left.set_position(0,self.bar_left.get_height()+self.corner_bottom_left.get_height())
        self.bar_bottom.set_position(self.corner_bottom_left.get_width(),self.corner_bottom_left.get_height())
        self.corner_bottom_right.set_position(self.bar_bottom.get_width()+self.corner_bottom_right.get_width(),self.bar_right.get_height()+self.corner_bottom_right.get_height())

        self.bubble.add(self.corner_top_left,self.bar_top,self.corner_top_right,self.bar_left,self.bar_right,self.corner_bottom_left,self.bar_bottom,self.corner_bottom_right)
        self.stage.add(self.bubble)





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


