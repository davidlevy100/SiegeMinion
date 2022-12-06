import io

from kivy.app import App
import kivy.properties as kp
from kivy.uix.gridlayout import GridLayout
from kivy.logger import Logger
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
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


    def on_source(self, *args):

        title_bar = BlackLabel(text=self.source.section)

        preview_btn = Button(text=PREVIEW_BTN_TEXT)
        preview_btn.bind(on_release=self.get_preview)

        slack_btn = Button(text=SLACK_BTN_TEXT)
        slack_btn.bind(on_release=self.source.send_to_slack)

        trio_btn = Button(text=TRIO_BTN_TEXT)
        trio_btn.bind(on_release=self.source.send_to_trio)

        trio_page_label = BlackLabel(text=self.source.trio_page_number)
        self.source.bind(trio_page_number=trio_page_label.setter('text'))

        body = GridLayout(rows=1, size_hint_y=0.5, padding=3, spacing=3)

        body.add_widget(preview_btn)
        body.add_widget(slack_btn)
        body.add_widget(trio_btn)
        body.add_widget(trio_page_label)

        self.add_widget(title_bar)
        self.add_widget(body)


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
