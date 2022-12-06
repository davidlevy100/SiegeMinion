import kivy.properties as kp
from kivy.logger import Logger

from data.events.data_event_dispatch import DataEventDispatcher


class ActivatableDispatcher(DataEventDispatcher):

    active = kp.BooleanProperty(False)
    active_dispatcher = kp.ObjectProperty(allownone=True)
    active_title = kp.StringProperty("")

    """ Properties to detect if corresponding 
        screen is visible.  This allows us to
        to only sort data when screen is visible
        or when this has been activated
    """
    current_main_screen = kp.StringProperty()
    current_overlay_screen = kp.StringProperty()

    data_controller = kp.ObjectProperty()

    visible = kp.BooleanProperty(False)

    graphic_name = ""
    graphic_type = ""


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app.bind(current_main_screen=self.setter('current_main_screen'))
        self.app.bind(current_overlay_screen=self.setter('current_overlay_screen'))


    def on_active_dispatcher(self, *args):

        if self.active_dispatcher != self:
            self.active = False


    def on_current_main_screen(self, *args):
        self.check_visible()

    def on_current_overlay_screen(self, *args):
        self.check_visible()


    def on_data_controller(self, *args):

        if self.data_controller is not None:
            self.active_dispatcher = self.data_controller.active_dispatcher
            self.data_controller.bind(
                active_dispatcher=self.setter('active_dispatcher')
            )


    def on_game_reset(self, *args):
        self.active = False
        self.visible = False


    def on_visible(self, *args):

        if self.visible:
            self.update_properties()


    def set_active(self, is_active, *args):
        
        self.active = is_active

        new_dispatcher = None

        if self.active:
            new_dispatcher = self

        self.data_controller.set_active_dispatcher(new_dispatcher)


class L3Activatable(ActivatableDispatcher):

    current_l3_screen = kp.StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app.bind(current_l3_screen=self.setter('current_l3_screen'))

    def on_current_l3_screen(self, *args):
        self.check_visible()

    
    def check_visible(self, *args):
        
        if (self.current_main_screen == "overlay_screen" and
            self.current_overlay_screen == self.graphic_type and
            self.current_l3_screen == self.graphic_name
        ):
            self.visible = True

        else:
            self.visible = False


class SideSlabActivatable(ActivatableDispatcher):

    current_side_slab_screen = kp.StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app.bind(current_side_slab_screen=self.setter('current_side_slab_screen'))
    
    def on_current_side_slab_screen(self, *args):
        self.check_visible()

    
    def check_visible(self, *args):
        
        if (self.current_main_screen == "overlay_screen" and
            self.current_overlay_screen == self.graphic_type and
            self.current_side_slab_screen == self.graphic_name
        ):
            self.visible = True

        else:
            self.visible = False
