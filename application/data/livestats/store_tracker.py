from sortedcontainers import SortedDict

import kivy.properties as kp

from data.events.data_event_dispatch import DataEventDispatcher


class StoreTracker(DataEventDispatcher):

    local_time = kp.NumericProperty(0)

    item_destroyed_event = kp.DictProperty()
    item_purchased_event = kp.DictProperty()
    item_sold_event = kp.DictProperty()
    item_undo_event = kp.DictProperty()

    sales = kp.DictProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app.livestats_history.bind(local_time=self.setter('local_time'))

        self.app.live_data.bind(item_destroyed_event=self.setter('item_destroyed_event'))
        self.app.live_data.bind(item_purchased_event=self.setter('item_purchased_event'))
        self.app.live_data.bind(item_sold_event=self.setter('item_sold_event'))
        self.app.live_data.bind(item_undo_event=self.setter('item_undo_event'))

        self.reset_sales()


    def on_game_reset(self, *args):

        self.reset_sales()


    def on_item_destroyed_event(self, *args):

        return

        if ("itemID" in self.item_destroyed_event and
            "participantID" in self.item_destroyed_event
        ):

            index = self.item_destroyed_event["participantID"]
            item_id = self.item_destroyed_event["itemID"]

            if item_id in self.sales[index]:
                self.sales[index].pop(item_id)


    def on_item_purchased_event(self, *args):

        if ("itemID" in self.item_purchased_event and
            "participantID" in self.item_purchased_event and
            "gameTime" in self.item_purchased_event and
            self.item_purchased_event["participantID"] in self.sales
        ):

            self.add_item(
                self.item_purchased_event["participantID"],
                self.item_purchased_event["itemID"],
                self.item_purchased_event["gameTime"]
            )


    def on_item_sold_event(self, *args):

        if ("itemID" in self.item_sold_event and
            "participantID" in self.item_sold_event
        ):

            index = self.item_sold_event["participantID"]
            item_id = self.item_sold_event["itemID"]

            if item_id in self.sales[index]:
                self.sales[index].pop(item_id)


    def on_item_undo_event(self, *args):

        if ("itemID" in self.item_undo_event and
            "participantID" in self.item_undo_event
        ):

            index = self.item_undo_event["participantID"]
            item_id = self.item_undo_event["itemID"]

            if item_id in self.sales[index]:
                self.sales[index].pop(item_id)

                if ("itemsAdded" in self.item_undo_event and
                    "gameTime" in self.item_undo_event
                ):

                    for this_item in self.item_undo_event["itemsAdded"]:
                        self.add_item(index, this_item, self.item_undo_event["gameTime"])


    def add_item(self, participantID, itemID, gameTime):

        self.sales[participantID][itemID] = {"gameTime": gameTime}



    def did_purchase(self, participantID, itemID):
        
        result = False

        if (participantID in self.sales and
            itemID in self.sales[participantID] and
            "gameTime" in self.sales[participantID][itemID] and
            self.sales[participantID][itemID]["gameTime"] <= self.local_time
        ):
            result = True

        return result

    def reset_sales(self):
        self.sales = {x:{} for x in range(1, 11)}
