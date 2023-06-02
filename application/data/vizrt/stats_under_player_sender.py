from datetime import datetime

import kivy.properties as kp

from data.events.data_event_dispatch import DataEventDispatcher
from data.esports.stats import calculate_KDA, calculate_CSD, calculate_XPD, calculate_GD, string_VSM, string_KP, calculate_sum_of_team_damage, string_DMG_percent


class StatsUnderPlayerSender(DataEventDispatcher):

    current_stats_update = kp.DictProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(output=self.app.vizrt.setter('input_data'))
        self.app.livestats_history.bind(current_stats_update=self.setter('current_stats_update'))

    def on_game_reset(self, *args):
        output = {}

        self.app.vizrt.send_now(output)

    def on_current_stats_update(self, *args):
        output = {}
        if "participants" in self.current_stats_update and "gameTime" in self.current_stats_update:
            participant_list = self.current_stats_update["participants"]
            participant_map = self.map_participants(participant_list)
            if participant_map is None:
                return {}
            
            game_time_ms = self.current_stats_update["gameTime"]
            time_8_14, participant_map_8_14 = self.get_8_14_participant_data(game_time_ms)
            blue_kills, red_kills = self.get_team_kills()
            blue_dmg, red_dmg = calculate_sum_of_team_damage(participant_list)
            
            output.update(self.get_top_stats(1, 6, participant_map, participant_map_8_14, time_8_14, blue_dmg, self.current_stats_update["champion_kills"]))
            output.update(self.get_jungle_stats(2, 7, participant_map, participant_map_8_14, time_8_14, blue_kills))
            output.update(self.get_mid_bot_stats(3, 8, participant_map, participant_map_8_14, time_8_14, blue_dmg))
            output.update(self.get_mid_bot_stats(4, 9, participant_map, participant_map_8_14, time_8_14, blue_dmg))
            output.update(self.get_support_stats(5, 10, participant_map, participant_map_8_14, time_8_14, game_time_ms, blue_kills))
            output.update(self.get_top_stats(6, 1, participant_map, participant_map_8_14, time_8_14, red_dmg, self.current_stats_update["champion_kills"]))
            output.update(self.get_jungle_stats(7, 2, participant_map, participant_map_8_14, time_8_14, red_kills))
            output.update(self.get_mid_bot_stats(8, 3, participant_map, participant_map_8_14, time_8_14, red_dmg))
            output.update(self.get_mid_bot_stats(9, 4, participant_map, participant_map_8_14, time_8_14, red_dmg))
            output.update(self.get_support_stats(10, 5, participant_map, participant_map_8_14, time_8_14, game_time_ms, red_kills))

        print("sending output: ", output)
        self.send_data(**output)

    def get_8_14_participant_data(self, game_time_ms):
        """ returns a time and a map of participants at either game time 8 minutes, or 14 minutes
            result is empty between 0-8 minutes, 8 minute state between 8 and 14 minutes
            and 14 minute state from minute 14 on """
        game_state_idx = None
        game_time_8 = 8 * 60000
        game_time_14 = 14 * 60000
        time = ""
        if game_time_ms >= game_time_14:
            # Beyond minute 14
            game_state_idx = self.app.livestats_history.get_history_index(game_time_14)
            time = "14"
        elif game_time_ms >= game_time_8:
            # Between 8 and 14
            game_state_idx = self.app.livestats_history.get_history_index(game_time_8)
            time = "8"
        else:
            return "", None

        participant_map = {}
        if game_state_idx is not None:
            game_state = self.app.livestats_history.stats_update_history.values()[game_state_idx]

            if "participants" in game_state:
                participant_list = game_state["participants"]
                participant_map = self.map_participants(participant_list)

        if len(participant_map) != 10:
            return "", None
        
        return time, participant_map

    def get_team_kills(self):
        blue_kills = 0
        red_kills = 0
        if "teams" in self.current_stats_update and len(self.current_stats_update["teams"]) == 2:
            blue = self.current_stats_update["teams"][0]
            red = self.current_stats_update["teams"][1]
            blue_kills = blue["championsKills"] if "championsKills" in blue else 0
            red_kills = red["championsKills"] if "championsKills" in blue else 0
        return blue_kills, red_kills

    def map_participants(self, participants):
        m = {}
        for participant in participants:
            if "participantID" in participant and participant["participantID"] <= 10 and participant["participantID"] > 0:
                m[participant["participantID"]] = participant

        return None if len(m) != 10 else m


    def get_top_stats(self, participant_id, opponent_id, participant_map, participant_map_8_14, time_8_14, team_dmg, champ_kill_list):
        current_participant = participant_map[participant_id]

        solo_kills = 0
        for champ_kill in champ_kill_list:
            if "killer" in champ_kill and champ_kill["killer"] == participant_id:
                if "assistants" in champ_kill and len(champ_kill["assistants"]) == 0:
                    solo_kills+=1

        stat1 = self.solo_kills(solo_kills) if solo_kills > 0 else self.kda(current_participant)
        stat2 = self.creep_score_diff_8_14(participant_map_8_14, participant_id, opponent_id, time_8_14)
        stat3 = self.damage_percent(current_participant, team_dmg)
        return self.format_output(participant_id, stat1, stat2, stat3)

    def get_jungle_stats(self, participant_id, opponent_id, participant_map, participant_map_8_14, time_8_14, team_kills):
        current_participant = participant_map[participant_id]
        stat1 = self.gold_diff_8_14(participant_map_8_14, participant_id, opponent_id, time_8_14)
        stat2 = self.xp_diff_8_14(participant_map_8_14, participant_id, opponent_id, time_8_14)
        # TODO Stat3 CJ% if >= 10%, else kill participation   
        stat3 = self.kill_participation(current_participant, team_kills)
        return self.format_output(participant_id, stat1, stat2, stat3)

    def get_mid_bot_stats(self, participant_id, opponent_id, participant_map, participant_map_8_14, time_8_14, team_dmg):
        current_participant = participant_map[participant_id]
        stat1 = self.kda(current_participant)
        stat2 = self.creep_score_diff_8_14(participant_map_8_14, participant_id, opponent_id, time_8_14)
        stat3 = self.damage_percent(current_participant, team_dmg)
        return self.format_output(participant_id, stat1, stat2, stat3)

    def get_support_stats(self, participant_id, opponent_id, participant_map, participant_map_8_14, time_8_14, game_time_ms, team_kills):
        current_participant = participant_map[participant_id]
        stat1 = self.vision_score_per_minute(current_participant, game_time_ms)
        stat2 = self.gold_diff_8_14(participant_map_8_14, participant_id, opponent_id, time_8_14)
        stat3 = self.kill_participation(current_participant, team_kills)  
        return self.format_output(participant_id, stat1, stat2, stat3)

    def vision_score_per_minute(self, participant, game_time_ms):
        return f"VS/M {string_VSM(participant, game_time_ms)}"

    def gold_diff_8_14(self, participant_map, participant_id, opponent_id, time):
        if participant_map is not None:
            participant = participant_map[participant_id]
            opponent = participant_map[opponent_id]
            return f"GD@{time} {calculate_GD(participant, opponent)}"
        return "-1"
    
    def creep_score_diff_8_14(self, participant_map, participant_id, opponent_id, time):
        if participant_map is not None:
            participant = participant_map[participant_id]
            opponent = participant_map[opponent_id]
            return f"GD@{time} {calculate_CSD(participant, opponent)}"
        return "-1"
    
    def xp_diff_8_14(self, participant_map, participant_id, opponent_id, time):
        if participant_map is not None:
            participant = participant_map[participant_id]
            opponent = participant_map[opponent_id]
            return f"XPD@{time} {calculate_XPD(participant, opponent)}"
        return "-1"
    
    def damage_percent(self, participant, team_dmg):
        if team_dmg > 0:
            return f"DMG% {string_DMG_percent(participant, team_dmg)}"
        return "-1"

    def kill_participation(self, participant, team_kills):
        return f"KP {string_KP(participant, team_kills)}"
    
    def kda(self, participant):
        return f"KDA {calculate_KDA(participant)}"
    
    def solo_kills(self, solo_kills):
        return f"SOLO K {solo_kills}"

    def format_output(self, participant_id, *args):
        output = {}
        for idx, stat in enumerate(args):
            output[f"stats{participant_id}/{idx + 1}"] = stat
        return output