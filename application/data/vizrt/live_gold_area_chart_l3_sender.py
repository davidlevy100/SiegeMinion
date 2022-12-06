import kivy.properties as kp
from kivy.logger import Logger

from data.events.data_event_dispatch import DataEventDispatcher

THIS_TEMPLATE_ID = 5

class LiveGoldAreaChartL3VizSender(DataEventDispatcher):

    active = kp.BooleanProperty(False)

    mode = kp.OptionProperty(
        "5 Minutes", options=["5 Minutes", "10 Minutes"]
    )

    start_time = kp.NumericProperty(0)
    end_time = kp.NumericProperty(0)

    active_title = kp.StringProperty("")

    tricode_left = kp.StringProperty()
    tricode_right = kp.StringProperty()

    chart_data = kp.ListProperty()
    chart_min = kp.NumericProperty(0)
    chart_max = kp.NumericProperty(0)

    source = kp.ObjectProperty()

    #Viz formatting variables

    col_offset = kp.NumericProperty(0)
    bar_pos_x = kp.NumericProperty(0)
    x_bar_mask = kp.BooleanProperty(False)
    zero_line_pos = kp.NumericProperty(0)
    show_zero = kp.BooleanProperty(False)
    num_cols = kp.NumericProperty(20)

    chart_width = kp.NumericProperty(1200)
    chart_interval = kp.NumericProperty(300000)
    max_chart_time = kp.NumericProperty(6000000)
    max_displacement = kp.NumericProperty(-22800)


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app.game_data.bind(tricode_left=self.setter('tricode_left'))
        self.app.game_data.bind(tricode_right=self.setter('tricode_right'))

        self.bind(output=self.app.vizrt.setter('input_data'))


    def on_game_reset(self, *args):

        self.col_offset = 0
        self.bar_pos_x = 0
        self.x_bar_mask = False
        self.zero_line_pos = 0
        self.show_zero = False
        self.num_cols = 20

        output = {
            "l3/templateb": 0,
            "l3/titleb": "",
            "l3/goldgraph": "",
            "l3/numCols": self.num_cols,
            "l3/colOffset": self.col_offset,
            "l3/yMax": "",
            "l3/yMin": "",
            "l3/showZero": int(self.show_zero),
            "l3/barPosX": self.bar_pos_x,
            "l3/XBarMask": int(self.x_bar_mask),
            "l3/ZeroLinePos": self.zero_line_pos
        }

        self.app.vizrt.send_now(output)



    def on_active(self, *args):

        if self.active:
            self.format_viz_graph()
            self.update_vizrt()


    def on_source(self, *args):

        self.active = self.source.active
        self.source.bind(active=self.setter('active'))

        self.active_title = self.source.active_title
        self.source.bind(active_title=self.setter('active_title'))
        
        self.source.bind(start_time=self.setter('start_time'))
        self.source.bind(end_time=self.setter('end_time'))
        self.source.bind(chart_data=self.setter('chart_data'))
        self.source.bind(chart_min=self.setter('chart_min'))
        self.source.bind(chart_max=self.setter('chart_max'))
        self.source.bind(mode=self.setter('mode'))
        

    def on_end_time(self, *args):

        if not(self.active):
            return

        self.format_viz_graph()
        self.update_vizrt()


    def on_mode(self, *args):

        if self.mode == "5 Minutes":
            self.chart_width = 1200
            self.chart_interval = 300000
            self.max_chart_time = 6000000
            self.max_displacement = -22800

        elif self.mode == "10 Minutes":
            self.chart_width = 600
            self.chart_interval = 600000
            self.max_chart_time = 6000000
            self.max_displacement = -10800


    def format_viz_graph(self, *args):

        time_delta = self.end_time - self.start_time

        #Time delta compared to calibrated 10 min interval
        time_percent = time_delta / self.chart_interval

        if time_delta > 0:
            self.col_offset = self.chart_width / time_percent
            self.bar_pos_x = (self.start_time / (self.max_chart_time - time_delta)) * (self.max_displacement / time_percent)

        else:
            self.col_offset = 600
            self.bar_pos_x = 0

        self.x_bar_mask = True

        if self.chart_max >= 0 and self.chart_min >= 0:
            self.zero_line_pos = 0

        elif self.chart_max < 0 and self.chart_min < 0:
            self.zero_line_pos = 100

        else:
            total = abs(self.chart_min) + abs(self.chart_max)
            self.zero_line_pos = abs(self.chart_min) / total * 100

        if self.zero_line_pos > 80 or self.zero_line_pos < 20:
            self.show_zero = False

        else:
            self.show_zero = True


    def update_vizrt(self, *args):

        string_data = ",".join([str(x) for x in self.chart_data])
        chart_max_string = f"{abs(self.chart_max):,d}"
        chart_min_string = f"{abs(self.chart_min):,d}"

        output = {
            "l3/templateb": THIS_TEMPLATE_ID,
            "l3/titleb": self.active_title,
            "l3/goldgraph": f'\"\"{string_data}\"\"',
            "l3/numCols": self.num_cols,
            "l3/colOffset": self.col_offset,
            "l3/yMax": f'\"\"{chart_max_string}\"\"',
            "l3/yMin": f'\"\"{chart_min_string}\"\"',
            "l3/showZero": int(self.show_zero),
            "l3/barPosX": self.bar_pos_x,
            "l3/XBarMask": int(self.x_bar_mask),
            "l3/ZeroLinePos": self.zero_line_pos
        }

        self.send_data(**output)