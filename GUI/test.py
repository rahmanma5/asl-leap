from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.config import Config
import string

class KivyButton(App):

    def build(self):
        Window.clearcolor = (0.75, 0.75, 1, 1)
        self.img = Image(source='logo.png')
        self.img.allow_stretch = True
        self.img.keep_ratio = False
        self.img.size_hint_x = 1
        self.img.size_hint_y = 1
        self.img.pos = (1500, 1080)
        self.img.opacity = 1
        s = Widget()
        s.add_widget(self.img)
        
        self.btn1 = Button(text="sentance 1", width=200, pos=(500, 500))
        self.btn2 = Button(text="sentance 2", width=200, pos=(700, 500))
        self.btn3 = Button(text="sentance 3", width=200, pos=(900, 500))

        s.add_widget(self.btn1)
        s.add_widget(self.btn2)
        s.add_widget(self.btn3)
        
#        self.l = Label(text="text", color=[0, 0, 0, 1])
#        self.l.pos =(398.0, 301.0)
#        self.l.font_size = '100dp'
#        s.add_widget(self.l)
        return s

KivyButton().run()
