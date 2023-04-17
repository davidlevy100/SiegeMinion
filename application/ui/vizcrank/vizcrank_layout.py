import io

from kivy.app import App
import kivy.properties as kp
from kivy.uix.gridlayout import GridLayout
from kivy.logger import Logger
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from ui.siege_spinner import SiegeSpinner
from kivy.uix.settings import SettingSpacer
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp
from kivy.core.image import Image as CoreImage

from ui.constants.text import PREVIEW_BTN_TEXT
from ui.constants.text import SLACK_BTN_TEXT
from ui.constants.text import TRIO_BTN_TEXT
from ui.constants.text import CLOSE_BTN_TEXT
from ui.constants.text import POPUP_TEXT

from ui.constants.images import LOADING_IMG_PATH

from ui.black_label import BlackLabel
from ui.black_grid_layout import BlackGridLayout

class VizTextInput(TextInput):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.padding = (6, 1 ,6 , 0)
        self.multiline = False
        self.write_tab = False


    def on_size(self, *args):
        self.font_size = self.size[1] * 0.8


class VizcrankWidget(BlackGridLayout):

    source = kp.ObjectProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()

        # LayoutCode
        self.cols = 1


        # Popup code
        self.popup_content = GridLayout(cols=1, spacing='5dp')

        self.preview_layout = GridLayout(cols=1)
        self.preview_image = Image(
            source=LOADING_IMG_PATH,
            nocache=True
        )
        
        self.popup_content.add_widget(self.preview_layout)
        self.popup_content.add_widget(SettingSpacer())

        self.popup = Popup(
            title = POPUP_TEXT,
            content = self.popup_content,
            size_hint=(0.9, 0.9)
        )

        self.popup.bind(on_dismiss=self.clear_popup)

        buttons = GridLayout(
            rows=1,
            size_hint_y = 0.08
        )

        close_btn = Button(
            text=CLOSE_BTN_TEXT
        )
        close_btn.bind(on_release=self.popup.dismiss)

        buttons.add_widget(close_btn)
        
        self.popup_content.add_widget(buttons)

    def get_button_row(self, *args):
        preview_btn = Button(text=PREVIEW_BTN_TEXT)
        preview_btn.bind(on_release=self.get_preview)

        slack_btn = Button(text=SLACK_BTN_TEXT)
        slack_btn.bind(on_release=self.source.send_to_slack)

        trio_btn = Button(text=TRIO_BTN_TEXT)
        trio_btn.bind(on_release=self.source.send_to_trio)

        trio_page_label = BlackLabel(text=self.source.trio_page_number)
        self.source.bind(trio_page_number=trio_page_label.setter('text'))

        button_row = GridLayout(rows=1, size_hint_y=0.5, padding=3, spacing=3)
        button_row.add_widget(preview_btn)
        button_row.add_widget(slack_btn)
        button_row.add_widget(trio_btn)
        button_row.add_widget(trio_page_label)
        return button_row
    
    def get_title_row(self, *args):
        return BlackLabel(text=self.source.section)

    def on_source(self, *args):
        self.add_widget(self.get_title_row())
        self.add_widget(self.get_button_row())

    def clear_popup(self, *args):
        self.preview_layout.clear_widgets()


    def get_preview(self, *args):
        
        self.preview_layout.clear_widgets()
        self.preview_layout.add_widget(self.preview_image)
        self.popup.open()

        self.source.get_preview(self.preview_handler)


    def preview_handler(self, request, result, *args):
        finished_data = self.source.process_game_data(result)
        self.source.get_preview_image(finished_data, self.got_preview_image)


    def got_preview_image(self, request, result, **kwargs):

        try:

            data = io.BytesIO(result)

            new_image = Image()
            new_image.texture = CoreImage(data, ext='png').texture        

            self.preview_layout.clear_widgets()
            self.preview_layout.add_widget(new_image)

        except Exception as e:
            Logger.exception(e)


class PlayerSelectVizcrankWidget(VizcrankWidget):
    def on_source(self, *args):
        spinner_row = GridLayout(rows=1, size_hint_y=0.5, padding=3, spacing=3)

        default_text = "No Players Available"
        spinner = SiegeSpinner(
            text=default_text,
            values=[])
        
        spinner.bind(text=self.update_selected_player)
        
        def update_values(self, values):
            spinner.values = values
            spinner.text = values[0] if len(values) > 0 else default_text
        self.source.bind(sorted_player_names=update_values)
        
        spinner_row.add_widget(spinner)
        
        self.add_widget(super().get_title_row())
        self.add_widget(spinner_row)
        self.add_widget(super().get_button_row())

    def update_selected_player(self, spinner, value):
        self.source.selected_player_name=value