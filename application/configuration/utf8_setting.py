from kivy.uix.settings import SettingString
from kivy.compat import string_types, text_type

class UTF8String(SettingString):

    def on_value(self, instance, value):

        if not self.section or not self.key:
            return
        # get current value in config
        panel = self.panel
        if not isinstance(value, string_types):
            value = str(value, encoding='utf-8')
        panel.set_value(self.section, self.key, value)
