from kivy.uix.settings import SettingsWithSidebar

from configuration.data_dragon import DDragonSettingOptions
from configuration.password_settings import PasswordString
from configuration.vizcrank import VizcrankSettingOptions
from configuration.utf8_setting import UTF8String

class DynamicSettingsWithSidebar(SettingsWithSidebar):
    
    """ Settings panel that can dynamically update """

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.register_type('password', PasswordString)
        self.register_type('ddragon_options', DDragonSettingOptions)
        self.register_type('vizcrank_options', VizcrankSettingOptions)
        self.register_type('utf8_string', UTF8String)
