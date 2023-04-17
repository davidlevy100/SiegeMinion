#!/usr/bin/env python

from functools import partial
import json
import os
from datetime import datetime
import sys
from pathlib import Path

os.environ['KIVY_HOME'] = os.getcwd()
os.environ['KIVY_GL_BACKEND'] = 'sdl2'

from kivy import require
from kivy.app import App
from kivy.config import Config
import kivy.properties as kp
from kivy.logger import Logger

from configuration.dynamic_settings_with_sidebar import DynamicSettingsWithSidebar
from configuration.defaults import get_defaults

from ui.root_layout import RootLayout

from data.lcu_client.poller import TestLCUPollingDispatcher, LCUPollingDispatcher, RecordingLCUPollingDispatcher, DevLCUPollingDispatcher
from data.lcu_client.lcu_champ_select import LCUChampSelect

from data.esports.esports_poller import SyncDispatcher, ObserverUIDispatcher

from data.events.game_event_dispatch import GameEventDispatcher
from data.events.data_controller import DataController

from data.livestats.events import is_desired_event
from data.livestats.events import LivestatsEventDispatcher
from data.livestats.poller import LiveStatsPollingDispatcher, PlaybackPollingDispatcher
from data.livestats.history import LivestatsHistory
from data.livestats.defaults.stats_update import get_default_stats_update
from data.livestats.gold_tracker import GoldTracker
from data.livestats.store_tracker import StoreTracker

from data.sportradar.sportradar import Sportradar
from data.data_dragon.data_dragon import DataDragon
from data.vizrt.sender import DatapoolSender

from data.events.game_event_dispatch import GameEventDispatcher


#Overlay
from data.events.current.overlay.objectives import ElderDragon
from data.events.current.overlay.objectives import BaronPowerPlay
from data.events.current.overlay.inhibitors import Inhibitor
from data.events.current.overlay.top_bar import TopBar
from data.events.current.overlay.bottom_bar import BottomBar
from data.events.current.overlay.next_dragon import NextDragon
from data.events.current.overlay.players import OverlayPlayers

#Side Slabs
from data.events.current.side_slabs.gold import GoldSideSlab
from data.events.current.side_slabs.xp_level import XPLevelSideSlab
from data.events.current.side_slabs.vision import VisionSideSlab
from data.events.current.side_slabs.xp_level import XPLevelSideSlab

#Lower 3rds
from data.events.current.lower_3rds.damage_bar_chart import DamageBarChartL3
from data.events.current.lower_3rds.gold_bar_chart import GoldBarChartL3
from data.events.current.lower_3rds.live_gold_area_chart import LiveGoldAreaChartL3
from data.events.current.lower_3rds.whole_game_gold_area_chart import WholeGameGoldAreaChartL3
from data.events.current.lower_3rds.player_matchup import PlayerMatchupL3
from data.events.current.lower_3rds.player_stats import PlayerStatsL3
from data.events.current.lower_3rds.player_runes import PlayerRunesL3
from data.events.current.lower_3rds.special_baron_announce_event import SpecialBaronAnnounceEvent

from data.events.sponsor_event import SponsorEvent
from data.events.dragon_soul_event import DragonSoulEvent
from data.events.mythic_item_event import MythicItemEvent

from data.vizrt.mutator import VizMutator
from data.vizrt.top_bar_sender import TopBarVizSender
from data.vizrt.bottom_bar_sender import BottomBarVizSender
from data.vizrt.overlay_runes_sender import OverlayRunesVizSender
from data.vizrt.baron_sender import BaronVizSender
from data.vizrt.elder_sender import ElderVizSender
from data.vizrt.inhibitor_sender import InhibitorVizSender, InhibitorVizController
from data.vizrt.gold_side_slab_sender import GoldSideSlabVizSender
from data.vizrt.vision_side_slab_sender import VisionSideSlabVizSender
from data.vizrt.xp_level_side_slab_sender import XPLevelSideSlabVizSender
from data.vizrt.damage_bar_chart_l3_sender import DamageBarChartL3VizSender
from data.vizrt.gold_bar_chart_l3_sender import GoldBarChartL3VizSender
from data.vizrt.live_gold_area_chart_l3_sender import LiveGoldAreaChartL3VizSender
from data.vizrt.whole_game_gold_area_chart_l3_sender import WholeGameGoldAreaChartL3VizSender
from data.vizrt.item_callouts_sender import ItemCalloutsVizSender
from data.vizrt.level_sender import LevelCalloutsVizSender
from data.vizrt.sponsor_sender import SponsorSender
from data.vizrt.champ_select_sender import LCUVizSender
from data.vizrt.data_controller_sender import DataControllerVizSender
from data.vizrt.next_dragon_sender import NextDragonVizSender
from data.vizrt.player_matchup_l3_sender import PlayerMatchupL3VizSender
from data.vizrt.player_stats_l3_sender import PlayerStatsL3VizSender
from data.vizrt.player_runes_l3_sender import PlayerRunesL3VizSender
from data.vizrt.dragon_soul_sender import DragonSoulVizSender
from data.vizrt.mythic_item_sender import MythicItemVizSender
from data.vizrt.special_baron_announce_sender import SpecialBaronAnnounceVizSender


from data.osc.sender import OSCSender
from data.osc.champ_select_sender import LCUOSCSender
from data.osc.player_sender import AllPlayersOSCSender
from data.osc.objective_sender import ObjectiveOSCSender
from data.osc.dragon_sender import DragonOSCSender
from data.osc.game_end_sender import GameEndOSCSender
from data.osc.next_dragon_sender import NextDragonOSCSender
from data.osc.rift_herald_sender import RiftHeraldOSCSender
from data.osc.special_kill_sender import SpecialKillOSCSender

from data.slack.slack_game_info import GameInfoSlackDispatcher

from data.vizrt.vizcrank.caster_runes_sender import CasterRunesSender
from data.vizrt.vizcrank.item_build_sender import ItemBuildSender
from data.vizrt.vizcrank.pause_graphic_sender import PauseGraphicSender
from data.vizrt.vizcrank.post_game_breakdown_sender import PostGameBreakdownSender
from data.vizrt.vizcrank.post_game_gold_sender import PostGameGoldSender
from data.vizrt.vizcrank.team_pick_order_sender import TeamPickOrderSender
from data.vizrt.vizcrank.post_game_summary_sender import PostGameSummarySender
from data.vizrt.vizcrank.post_game_baron_sender import PostGameBaronSender
from data.vizrt.vizcrank.post_game_objectives_sender import PostGameObjectivesSender


from ui.screens.main_screen_manager import MainScreenManager
from ui.screens.overlay_screen_manager import OverlayScreenManager
from ui.screens.l3_screen_manager import L3ScreenManager
from ui.screens.side_slab_screen_manager import SideSlabScreenManager
from ui.screens.still_screen_manager import StillScreenManager

from ui.screens.overlay_screen import OverlayScreen
from ui.screens.side_slab_screen import SideSlabScreen
from ui.screens.gold_side_slab_screen import GoldSideSlabScreen
from ui.screens.xp_level_side_slab_screen import XPLevelSideSlabScreen
from ui.screens.vision_side_slab_screen import VisionSideSlabScreen
from ui.screens.l3_screen import L3Screen
from ui.screens.damage_bar_chart_l3_screen import DamageBarChartL3Screen
from ui.screens.gold_bar_chart_l3_screen import GoldBarChartL3Screen
from ui.screens.player_matchup_l3_screen import PlayerMatchupL3Screen
from ui.screens.player_stats_l3_screen import PlayerStatsL3Screen
from ui.screens.player_runes_l3_screen import PlayerRunesL3Screen
from ui.screens.live_gold_area_chart_l3_screen import LiveGoldAreaChartL3Screen
from ui.screens.whole_game_gold_area_chart_l3_screen import WholeGameGoldAreaChartL3Screen
from ui.screens.still_screen import StillScreen
from ui.screens.caster_runes_screen import CasterRunesScreen
from ui.screens.champ_select_screen import ChampSelectScreen
from ui.connector import DataButtonLayout

from ui.black_label import BlackLabel
from ui.storage_image import StorageImage

from ui.livestats.game_finder import GameFinderButton
from ui.livestats.game_finder_text_input import GameFinderTextInput
from ui.icons import BaronImage, ElderImage, DragonImage, TowerImage, GoldImage, KillImage, BlueInhibImage, RedInhibImage
from ui.data_label import NumericLabel, FormattedNumericLabel
from ui.clock_label import ClockLabel
from ui.delay_input import DelayInput
from ui.goto_time_input import GotoTimeInput
from ui.team_color_grid_layout import TeamColorGridLayout
from ui.game_images import ChampionImage, OverlayImage
from ui.team_bar import HorizontalTeamBar, RightHorizontalTeamBar
from ui.sponsor_layout import SponsorLayout
from ui.siege_spinner import SiegeSpinner
from ui.champ_select_tabbed_panel import ChampSelectTabbedPanel
from ui.warning_layout import GridWarningLayout
from ui.win_record_layout import WinRecordLayout
from ui.vizcrank.vizcrank_layout import VizcrankWidget
from ui.dragon_layout import DragonLayout
from ui.dragon_layout import ElderDragonLayout
from ui.resource_bars import HealthBar, ManaBar
from ui.dragon_soul_button import DragonSoulButton
from ui.mythic_item_button import MythicItemButton
from ui.baron_button import BaronButton


DEFAULT_STATS_UPDATE = get_default_stats_update()
require('1.11.1')


class SiegeMinion(App):

    connected = kp.BooleanProperty(False)
    platform_game_id = kp.StringProperty("")
    game_reset = kp.StringProperty("")

    #Screen Managers State
    current_main_screen = kp.StringProperty()
    current_overlay_screen = kp.StringProperty()
    current_l3_screen = kp.StringProperty()
    current_side_slab_screen = kp.StringProperty()
    current_still_screen = kp.StringProperty()

    current_visible_screen = kp.StringProperty()


    def on_current_main_screen(self, *args):
        Logger.info(f"Main Screen Change: {args[1]}")

    def on_current_overlay_screen(self, *args):
        Logger.info(f"Overlay Screen Change: {args[1]}")

    def on_current_l3_screen(self, *args):
        Logger.info(f"L3 Screen Change: {args[1]}")

    def on_current_side_slab_screen(self, *args):
        Logger.info(f"Side Slab Screen Change: {args[1]}")

    def on_current_still_screen(self, *args):
        Logger.info(f"Still Screen Change: {args[1]}")
    

    def build(self):
        self.settings_cls = DynamicSettingsWithSidebar
        self.use_kivy_settings = False
        Config.write()

        self.build_data()

        return RootLayout()

    
    def build_config(self, config):

        defaults = get_defaults()

        for key, value in defaults.items():
            config.setdefaults(key, value)


    def build_settings(self, settings):

        settings_map = {
            'Data Dragon': 'data_dragon.json',
            'Livestats': 'livestats.json',
            'Observer UI': 'observer_ui.json',
            'OSC': 'osc.json',
            'Slack': 'slack.json',
            'Sponsors': 'sponsor.json',
            'Sportradar': 'sportradar.json',
            'Sync': 'sync.json',
            'User Game Data': 'user_game_data.json',
            'VizRT': 'vizrt.json',
            'VizRT Still Graphics': 'vizcrank.json',
            'Caster Runes': 'caster_runes.json',
            'Item Build': 'item_build.json',
            'Pause Graphic': 'pause_graphic.json',
            'Post-Game Baron': 'post_game_baron.json',
            'Post-Game Breakdown': 'post_game_breakdown.json',
            'Post-Game Gold': 'post_game_gold.json',
            'Post-Game Objectives': 'post_game_objectives.json',
            'Post-Game Summary': 'post_game_summary.json',
            'Team Pick Order': 'team_pick_order.json'
        }

        config_path = Path.cwd().joinpath('configuration')

        for section, filename in settings_map.items():

            settings.add_json_panel(
                section,
                self.config,
                f"{config_path.joinpath(filename)}"
            )

    
    def build_data(self, *args):

        test_mode = bool(self.config.getint("User Game Data", "test_mode"))
        record_mode = bool(self.config.getint("User Game Data", "record_mode"))
        dev_mode = bool(self.config.getint("User Game Data", "dev_mode"))

        if test_mode:
            self.livestats_poller = PlaybackPollingDispatcher()
            self.lcu_poller = TestLCUPollingDispatcher()

        elif dev_mode:
            self.livestats_poller = LiveStatsPollingDispatcher()
            self.lcu_poller = DevLCUPollingDispatcher()

        else:
            self.livestats_poller = LiveStatsPollingDispatcher()

            if record_mode: 
                self.lcu_poller = RecordingLCUPollingDispatcher()
            else:
                self.lcu_poller = LCUPollingDispatcher()

        

        self.live_data = LivestatsEventDispatcher()
        self.sync_poller = SyncDispatcher()
        self.observer_ui_poller = ObserverUIDispatcher()
        self.livestats_history = LivestatsHistory()

        self.gold_tracker = GoldTracker()
        self.store_tracker = StoreTracker()
         
        self.data_dragon = DataDragon()
        self.sportradar = Sportradar()
        self.vizrt = DatapoolSender()
        self.osc = OSCSender()

        ## Champ Select
        self.lcu_champ_select = LCUChampSelect()


        ## In-Game
        self.game_data = GameEventDispatcher()

        self.elder_dragon = ElderDragon()
        self.baron_power_play = BaronPowerPlay()
        self.top_bar = TopBar()

        self.side_slab_controller = DataController()

        self.gold_side_slab = GoldSideSlab(data_controller=self.side_slab_controller)
        self.xp_level_side_slab = XPLevelSideSlab(data_controller=self.side_slab_controller)
        self.vision_side_slab = VisionSideSlab(data_controller=self.side_slab_controller)
        
        self.blue_top_inhib = Inhibitor(lane_teamID="top_100")
        self.blue_mid_inhib = Inhibitor(lane_teamID="mid_100")
        self.blue_bot_inhib = Inhibitor(lane_teamID="bot_100")
        
        self.red_top_inhib = Inhibitor(lane_teamID="top_200")
        self.red_mid_inhib = Inhibitor(lane_teamID="mid_200")
        self.red_bot_inhib = Inhibitor(lane_teamID="bot_200")

        self.l3_controller = DataController()

        self.mythic_item = MythicItemEvent()
        self.special_baron_announce_event = SpecialBaronAnnounceEvent()

        self.overlay_players = OverlayPlayers()
        
        self.damage_bar_chart_l3 = DamageBarChartL3(data_controller=self.l3_controller)
        self.gold_bar_chart_l3 = GoldBarChartL3(data_controller=self.l3_controller)
        self.live_gold_area_chart_l3 = LiveGoldAreaChartL3(data_controller=self.l3_controller)
        self.whole_game_gold_area_chart_l3 = WholeGameGoldAreaChartL3(data_controller=self.l3_controller)
        self.player_matchup_l3 = PlayerMatchupL3(data_controller=self.l3_controller)
        self.player_stats_l3 = PlayerStatsL3(data_controller=self.l3_controller)
        self.player_runes_l3 = PlayerRunesL3(data_controller=self.l3_controller)
        self.bottom_bar = BottomBar()
        self.next_dragon = NextDragon(elder_dragon=self.elder_dragon)

        self.sponsor_1 = SponsorEvent(section="Sponsors", prefix="sponsor1")
        self.sponsor_2 = SponsorEvent(section="Sponsors", prefix="sponsor2")
        self.sponsor_3 = SponsorEvent(section="Sponsors", prefix="sponsor3")
        self.sponsor_4 = SponsorEvent(section="Sponsors", prefix="sponsor4")
        self.sponsor_5 = SponsorEvent(section="Sponsors", prefix="sponsor5")
        self.sponsor_6 = SponsorEvent(section="Sponsors", prefix="sponsor6")
        self.sponsor_7 = SponsorEvent(section="Sponsors", prefix="sponsor7")
        self.sponsor_8 = SponsorEvent(section="Sponsors", prefix="sponsor8")

        self.dragon_soul = DragonSoulEvent()

        self.game_info_slack = GameInfoSlackDispatcher()


        # VizRT Senders
        self.viz_mutator = VizMutator()
        self.lcu_viz_sender = LCUVizSender()
        self.l3_controller_viz_sender = DataControllerVizSender(
            source=self.l3_controller,
            key="l3/l3"
        )
        self.side_slab_controller_viz_sender = DataControllerVizSender(
            source=self.side_slab_controller,
            key="ss/anim"
        )
        self.top_bar_viz_sender = TopBarVizSender()
        self.bottom_bar_viz_sender = BottomBarVizSender()
        self.overlay_runes_viz_sender = OverlayRunesVizSender()
        self.baron_viz_sender = BaronVizSender()
        self.elder_viz_sender = ElderVizSender()
        self.next_dragon_viz_sender = NextDragonVizSender()

        self.inhib_left_viz_sender = InhibitorVizSender(
            side="blue",
            top_source=self.blue_top_inhib,
            mid_source=self.blue_mid_inhib,
            bot_source=self.blue_bot_inhib
        )

        self.inhib_right_viz_sender = InhibitorVizSender(
            side="red",
            top_source=self.red_top_inhib,
            mid_source=self.red_mid_inhib,
            bot_source=self.red_bot_inhib
        )
        
        self.inhib_viz_controller = InhibitorVizController()

        self.gold_side_slab_viz_sender = GoldSideSlabVizSender(
            source=self.gold_side_slab
        )
        self.vision_side_slab_viz_sender = VisionSideSlabVizSender(
            source=self.vision_side_slab
        )
        self.xp_level_side_slab_viz_sender = XPLevelSideSlabVizSender(
            source=self.xp_level_side_slab
        )
        
        self.damage_bar_chart_l3_viz_sender = DamageBarChartL3VizSender(
            source=self.damage_bar_chart_l3
        )
        self.live_gold_area_chart_l3_viz_sender = LiveGoldAreaChartL3VizSender(
            source=self.live_gold_area_chart_l3
        )
        self.whole_game_gold_area_chart_l3_viz_sender = WholeGameGoldAreaChartL3VizSender(
            source=self.whole_game_gold_area_chart_l3
        )
        self.gold_bar_chart_l3_viz_sender = GoldBarChartL3VizSender(
            source=self.gold_bar_chart_l3
        )
        self.player_matchup_l3_viz_sender = PlayerMatchupL3VizSender(
            source=self.player_matchup_l3
        )
        self.player_stats_l3_viz_sender = PlayerStatsL3VizSender(
            source=self.player_stats_l3
        )
        self.player_runes_l3_viz_sender = PlayerRunesL3VizSender(
            source=self.player_runes_l3
        )

        self.item_callouts_viz_sender = ItemCalloutsVizSender()
        self.level_callouts_viz_sender = LevelCalloutsVizSender()

        self.sponsor_viz_sender_1 = SponsorSender(target=self.sponsor_1, key="sponsor1")
        self.sponsor_viz_sender_2 = SponsorSender(target=self.sponsor_2, key="sponsor2")
        self.sponsor_viz_sender_3 = SponsorSender(target=self.sponsor_3, key="sponsor3")
        self.sponsor_viz_sender_4 = SponsorSender(target=self.sponsor_4, key="sponsor4")
        self.sponsor_viz_sender_5 = SponsorSender(target=self.sponsor_5, key="sponsor5")
        self.sponsor_viz_sender_6 = SponsorSender(target=self.sponsor_6, key="sponsor6")
        self.sponsor_viz_sender_7 = SponsorSender(target=self.sponsor_7, key="sponsor7")
        self.sponsor_viz_sender_8 = SponsorSender(target=self.sponsor_8, key="sponsor8")

        self.dragon_soul_viz_sender = DragonSoulVizSender()
        self.mythic_item_viz_sender = MythicItemVizSender()
        self.special_baron_announce_viz_sender = SpecialBaronAnnounceVizSender()


        # OSC Senders

        champ_select_enabled = bool(self.config.getint("OSC", "champ_select_enabled"))
        in_game_enabled = bool(self.config.getint("OSC", "in_game_enabled"))

        if champ_select_enabled:
            self.lcu_osc_sender = LCUOSCSender()

        if in_game_enabled:

            self.all_players_osc_sender = AllPlayersOSCSender()
            self.baron_osc_sender = ObjectiveOSCSender(
                source=self.baron_power_play,
                state_path="/BaronState/Team",
                buff_timer_path="/BaronState/Timer",
                killer_path="/BaronState/Killer"
            )

            self.elder_osc_sender = ObjectiveOSCSender(
                source=self.elder_dragon,
                state_path="/ElderState/Team",
                buff_timer_path="/ElderState/Timer",
                killer_path="/ElderState/Killer"
            )

            self.rift_herald_osc_sender = RiftHeraldOSCSender()
            self.special_kill_osc_sender = SpecialKillOSCSender()

            self.dragon_osc_sender = DragonOSCSender()
            self.next_dragon_osc_sender = NextDragonOSCSender()
            self.game_end_osc_sender = GameEndOSCSender()


        #Still Graphics Senders
        self.caster_runes_sender = CasterRunesSender()
        self.pause_graphic_sender = PauseGraphicSender()
        self.item_build_sender = ItemBuildSender()
        self.post_game_breakdown_sender = PostGameBreakdownSender()
        self.post_game_gold_sender = PostGameGoldSender()
        self.team_pick_order_sender = TeamPickOrderSender()
        self.post_game_summary_sender = PostGameSummarySender()
        self.post_game_baron_sender = PostGameBaronSender()
        self.post_game_objectives_sender = PostGameObjectivesSender()
        
        self.initialize()


    def on_config_change(
        self, 
        config, 
        section,
        key, 
        value
    ):
        Logger.info(f"Settings Change: Section {section} | Key {key} | Value {value}")

    
    def initialize(self):

        self.game_reset = str(datetime.now())
        self.current = 'overlay_screen'

        LogMessage = (
            f"Event: {datetime.now().strftime('%r')} "
            f"Resetting Siege Minion"
        )
        Logger.info(LogMessage)

    
    def set_sending(self, state, *args):
        if state == "normal":
            self.sending = False
        else:
            self.sending = True

        LogMessage = (
            f"Engine: sending enabled is {self.sending}"
        )
        Logger.info(LogMessage)


if __name__ == "__main__":

    SiegeMinion().run()
