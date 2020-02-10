from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.stacklayout import StackLayout
from kivy.properties import ListProperty
from kivy.graphics import Color, Rectangle
from kivy.uix.camera import Camera
from kivy.uix.label import Label
import string

class RootWidget(StackLayout):
    def __init__(self, **kwargs):
        super(RootWidget, self).__init__(**kwargs)
        with self.canvas.before:
            Color(.75, .5, .5, 1)  # green; colors range from 0-1 instead of 0-255
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)
        self.orientation = "tb-lr"
        
        widget = Label(text="text")
#        self.add_widget(widget)
        x = 1
        for i in list(string.ascii_uppercase):
            btn = Button(text=str(x) + ". " + str(i), width=150, size_hint=(0.15, None))
            self.add_widget(btn)
            x += 1
        self.add_widget(Camera(play=True, resolution=(640,480)))
        
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

class TestApp(App):

    def build(self):
        self.root = root = RootWidget()
        with root.canvas.before:
            Color(1, 1, 0, 1)
        return root


if __name__ == '__main__':
    TestApp().run()

