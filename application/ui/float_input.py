import re

import kivy.properties as kp
from kivy.uix.textinput import TextInput


class FloatInput(TextInput):

    pat = re.compile('[^0-9]')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.readonly = False
        self.multiline = False
        self.padding = [6, 1, 6, 0]
        self.write_tab = False
        self.size_hint_x = 1.5

    
    def insert_text(self, substring, from_undo=False):
        pat = self.pat
        
        if '.' in self.text:
            s = re.sub(pat, '', substring)
        
        else:
            s = '.'.join([re.sub(pat, '', s) for s in substring.split('.', 1)])
        
        return super().insert_text(s, from_undo=from_undo)

    
    def on_size(self, *args):
        self.font_size = self.size[1] * 0.8
