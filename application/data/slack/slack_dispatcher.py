import imghdr
import json

from datetime import datetime
from urllib.parse import urlencode

from kivy.event import EventDispatcher
import kivy.properties as kp
from kivy.logger import Logger
from kivy.network.urlrequest import UrlRequest
from kivy.app import App

from requests_toolbelt import MultipartEncoder


SLACK_MESSAGE_URL = 'https://slack.com/api/chat.postMessage'
SLACK_IMAGE_URL = 'https://slack.com/api/files.upload'


class SlackDispatcher(EventDispatcher):

    #Input Data
    section = kp.StringProperty()
    text_message = kp.StringProperty(None, allownone=True)
    image = kp.ObjectProperty(None, allownone=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()


    def on_text_message(self, *args):

        if (self.text_message is not None and
            len(self.text_message) > 0
        ):
            self.send_message(self.text_message)


    def basic_block_builder(self, *args):

        json_block = []

        divider = {"type": "divider"}

        json_block.append(divider)

        for this_message in args:

            this_context = {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": f"{this_message}"
                    }
                ]
            }

            json_block.append(this_context)

        return json.dumps(json_block)


    def get_token_and_channels(self, *args):

        token = self.app.config.get('Slack', "api_token")
        channels = self.app.config.get(self.section, "slack_channels")

        return token, channels


    def send_message(self, text, blocks="", *args):

        token, channels = self.get_token_and_channels()

        querystring = {
            "channel": channels,
            "text": text
        }

        if len(blocks) > 0:
            querystring["blocks"] = blocks


        headers = {
            'Authorization': f"Bearer {token}"
        }

        slack_query = urlencode(querystring)
        
        url = f"{SLACK_MESSAGE_URL}?{slack_query}"

        self.post_data(url=url, headers=headers)


    def send_image(self, image, *args):

        try:

            token, channels = self.get_token_and_channels()

            filename = self.section

            image_extension = imghdr.what(None, h=image)
            #image_extension = "png"

            mime_type = f"image/{image_extension}"

            payload = MultipartEncoder(
                fields={
                    'file': (
                        f"{filename}.{image_extension}", 
                        image,
                        mime_type
                    )
                }
            )

            headers = {
                'Authorization': f"Bearer {token}",
                'Content-Type': payload.content_type
            }

            querystring = {"channels": f"{channels}"}
            slack_query = urlencode(querystring)

            url = f"{SLACK_IMAGE_URL}?{slack_query}"

            UrlRequest(
                url, 
                on_success = self.got_success, 
                on_redirect = self.got_redirect,
                on_failure = self.got_fail,
                on_error = self.got_error,
                req_headers = headers,
                req_body=payload,
                verify = False
            )

        except Exception as e:

            Logger.exception(e)


    def post_data(self, **kwargs):

        """ Single Function to POST data
            Expects full URL(url), 
            headers(headers) """

        try:

            url = kwargs["url"]
            headers = kwargs["headers"]

            UrlRequest(
                url, 
                on_success = self.got_success, 
                on_redirect = self.got_redirect,
                on_failure = self.got_fail,
                on_error = self.got_error,
                req_headers = headers,
                verify = False
            )

        except Exception as e:
            Logger.exception(f"Error: {e}")

    
    def got_success(self, req, *args):
        Logger.info(f"Slack Post: {datetime.now().strftime('%r')} {req.url}, {args}")
        return


    def got_error(self, req, *args):
        Logger.exception(f"Slack Error: {datetime.now().strftime('%r')} {req.url}, {args}")
        return


    def got_fail(self, req, *args):
        Logger.exception(f"Slack Fail: {datetime.now().strftime('%r')} {req.url}, {args}")
        return


    def got_redirect(self, req, *args):
        Logger.exception(f"Slack Redirect: {datetime.now().strftime('%r')} {req.url}, {args}")
        return
