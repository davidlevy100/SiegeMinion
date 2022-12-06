from kivy.uix.settings import SettingString
from kivy.uix.label import Label


class PasswordString(SettingString):

    # Change textinput in the popup into a password field
    def _create_popup(self, instance):
        super()._create_popup(instance)
        self.textinput.password=True
        self.textinput.allow_copy=False

    # If widget is a Label, replace it's text
    def add_widget(self, widget, *largs):
        
        if isinstance(widget, Label):

            star_text = "********"

            widget = Label(
                text=f"[color=808080]{star_text}[/color]",
                markup = True
            )

        super().add_widget(widget, *largs)
