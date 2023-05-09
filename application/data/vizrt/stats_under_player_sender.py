from datetime import datetime

import kivy.properties as kp

from data.events.data_event_dispatch import DataEventDispatcher
from data.esports.stats import calculate_KDA, calculate_CSD, calculate_XPD, calculate_GD, calculate_vision, calculate_KP, calculate_sum_of_team_damage, calculate_DMG_percent


class StatsUnderPlayerSender(DataEventDispatcher):

    current_stats_update = kp.DictProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bind(output=self.app.vizrt.setter('input_data'))

        self.app.livestats_history.bind(
            current_stats_update=self.setter('current_stats_update')
        )


    def on_game_reset(self, *args):

        output = {
            "dragon/anim": 0,
            "dragon/cd": "---",
            "dragon/type": 0
        }

        self.app.vizrt.send_now(output)


    def on_current_stats_update(self, *args):
        print("stats under player stats updated...")
        output = {}
        if "participants" in self.current_stats_update and "gameTime" in self.current_stats_update:
            participant_list = self.current_stats_update["participants"]
            participant_map = self.map_participants(participant_list)
            if len(participant_map) != 10:
                return {}
            
            game_time_ms = self.current_stats_update["gameTime"]

            game_state_idx = None
            if game_time_ms >= 14000:
                # Beyond minute 14
                game_state_idx = self.app.livestats_history.get_history_index(14000)
            elif game_time_ms >= 8000:
                # Between 8 and 14
                game_state_idx = self.app.livestats_history.get_history_index(8000)

            key_time_participant_map = {}
            if game_state_idx is not None:
                game_state = self.app.livestats_history.stats_update_history.values()[game_state_idx]

                if "participants" in game_state:
                    participant_list = self.current_stats_update["participants"]
                    key_time_participant_map = self.map_participants(participant_list)

            blue_kills = 0
            red_kills = 0
            if "teams" in self.current_stats_update and len(self.current_stats_update["teams"] == 2):
                blue = self.current_stats_update["teams"][0]
                red = self.current_stats_update["teams"][1]
                blue_kills = blue["championKills"] if "championKills" in blue else 0
                red_kills = red["championKills"] if "championKills" in blue else 0

            blue_dmg, red_dmg = calculate_sum_of_team_damage(participant_list)
            
            output.update(self.get_top_stats(1, 6, participant_map, key_time_participant_map, blue_dmg))
            output.update(self.get_jungle_stats(2, 7, participant_map, key_time_participant_map, blue_kills))
            output.update(self.get_mid_stats(3, 8, participant_map, key_time_participant_map, blue_dmg))
            output.update(self.get_bot_stats(4, 9, participant_map, key_time_participant_map))
            output.update(self.get_support_stats(5, 10, participant_map, key_time_participant_map))
            output.update(self.get_top_stats(6, 1, participant_map, key_time_participant_map, red_dmg))
            output.update(self.get_jungle_stats(7, 2, participant_map, key_time_participant_map, red_kills))
            output.update(self.get_mid_stats(8, 3, participant_map, key_time_participant_map, red_dmg))
            output.update(self.get_bot_stats(9, 4, participant_map, key_time_participant_map))
            output.update(self.get_support_stats(10, 5, participant_map, key_time_participant_map))

        self.send_data(**output)
            


    def map_participants(participants):
        m = {}
        for participant in participants:
            if "participantID" in participant and participant["participantID"] <= 10 and participant["participantID"] > 0:
                m[participant["participantID"]] = participant
        return m


    def get_top_stats(self, participant_id, opponent_id, current_map, key_time_map, team_dmg):
        current_participant = current_map[participant_id]
        output = {
            f"stats{participant_id}/1": calculate_KDA(current_participant), # TODO SOLO K if > 1
        }
        if len(key_time_map) == 10:
            key_time_participant = key_time_map[participant_id]
            key_time_opponent = key_time_map[opponent_id]
            output[f"stats{participant_id}/2"] = calculate_CSD(key_time_participant, key_time_opponent)

        if team_dmg > 0:
            output[f"stats{participant_id}/3"] = calculate_DMG_percent(current_participant, team_dmg)
        return output
    
    def get_jungle_stats(self, participant_id, opponent_id, current_map, key_time_map, team_kills):
        current_participant = current_map[participant_id]
        output = {}
        if len(key_time_map) == 10:
            key_time_participant = key_time_map[participant_id]
            key_time_opponent = key_time_map[opponent_id]
            output[f"stats{participant_id}/1"] = calculate_XPD(key_time_participant, key_time_opponent)
            output[f"stats{participant_id}/2"] = calculate_GD(key_time_participant, key_time_opponent)

        # TODO CJ% if >= 10%, else kill participation   
        output[f"stats{participant_id}/3"] = calculate_KP(current_participant, team_kills)  

        return output
    
    def get_mid_stats(self, participant_id, opponent_id, current_map, key_time_map, team_dmg):
        current_participant = current_map[participant_id]
        output = {
            f"stats{participant_id}/1": calculate_KDA(current_participant)
        }
        if len(key_time_map) == 10:
            key_time_participant = key_time_map[participant_id]
            key_time_opponent = key_time_map[opponent_id]
            output[f"stats{participant_id}/2"] = calculate_CSD(key_time_participant, key_time_opponent)

        if team_dmg > 0:
            output[f"stats{participant_id}/3"] = calculate_DMG_percent(current_participant, team_dmg)

        return output
    
    def get_bot_stats(self, participant, opponent):
        return {
            f"stats{id}/1": calculate_KDA(participant),
            f"stats{id}/2": calculate_CSD(participant, opponent), # TODO needs to be 8/14
            f"stats{id}/3": 0 # TODO DMG%
        }
    
    def get_support_stats(self, participant, opponent):
        return { 
            f"stats/{id}/1": calculate_vision(participant), # TODO needs to be VS per minute
            f"stats/{id}/2": calculate_GD(participant, opponent), # TODO needs to be 8/14
            f"stats/{id}/3": 0 # TODO kill participation
        }