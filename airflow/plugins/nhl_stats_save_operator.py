import logging
import requests
from airflow.models import BaseOperator
import uuid
import dataset
import os


class NhlStatsSaveOperator(BaseOperator):
    api_url = f'https://statsapi.web.nhl.com/api/v1/teams/'

    template_fields = ("team_id")

    def __init__(self, team_id: int = 10, **kwargs) -> None:
        super().__init__(**kwargs)
        self.team_id = team_id

    def parse_data(self, data: dict) -> (list, list, list):
        splits = []
        stats = []
        team_uid = str(uuid.uuid4())
        team = [{'uid': team_uid,
                 'id': self.team_id}]
        if data.get('stats'):
            for jsStat in data.get('stats'):
                stat_uid = str(uuid.uuid4())
                if jsStat.get('type'):
                    stat = {'team_uid': team_uid,
                            'uid': stat_uid,
                            'display_name': jsStat.get('type').get('displayName'),
                            'game_type': jsStat.get('type').get('gameType')}
                    stats.append(stat)
                for jsSplit in jsStat.get('splits'):
                    if jsSplit.get('stat'):
                        print(jsSplit.get('stat'))
                        split = {'stat_uid': stat_uid,
                                 'uid': str(uuid.uuid4()),
                                 'games_played': jsSplit.get('stat').get('gamesPlayed'),
                                 'wins': jsSplit.get('stat').get('wins'),
                                 'losses': jsSplit.get('stat').get('losses'),
                                 'ot': jsSplit.get('stat').get('ot'),
                                 'pts': jsSplit.get('stat').get('pts'),
                                 'ptpctg': jsSplit.get('stat').get('ptPctg'),
                                 'goals_pergame': jsSplit.get('stat').get('goalsPerGame'),
                                 'goals_against_pergame': jsSplit.get('stat').get('goalsAgainstPerGame'),
                                 'evgga_ratio': jsSplit.get('stat').get('evGGARatio'),
                                 'power_play_percentage': jsSplit.get('stat').get('powerPlayPercentage'),
                                 'power_play_goals': jsSplit.get('stat').get('powerPlayGoals'),
                                 'power_play_goals_against': jsSplit.get('stat').get('powerPlayGoalsAgainst'),
                                 'power_play_opportunities': jsSplit.get('stat').get('powerPlayOpportunities'),
                                 'penalty_kill_percentage': jsSplit.get('stat').get('penaltyKillPercentage'),
                                 'shots_pergame': jsSplit.get('stat').get('shotsPerGame'),
                                 'shots_allowed': jsSplit.get('stat').get('shotsAllowed'),
                                 'win_score_first': jsSplit.get('stat').get('winScoreFirst'),
                                 'win_opp_score_first': jsSplit.get('stat').get('winOppScoreFirst'),
                                 'win_lead_first_per': jsSplit.get('stat').get('winLeadFirstPer'),
                                 'win_lead_second_per': jsSplit.get('stat').get('winLeadSecondPer'),
                                 'win_out_shootopp': jsSplit.get('stat').get('winOutshootOpp'),
                                 'win_out_shotbyopp': jsSplit.get('stat').get('winOutshotByOpp'),
                                 'face_offs_taken': jsSplit.get('stat').get('faceOffsTaken'),
                                 'face_offs_won': jsSplit.get('stat').get('faceOffsWon'),
                                 'face_offs_lost': jsSplit.get('stat').get('faceOffsLost'),
                                 'face_off_win_percentage': jsSplit.get('stat').get('faceOffWinPercentage'),
                                 'shooting_pctg': jsSplit.get('stat').get('shootingPctg'),
                                 'save_pctg': jsSplit.get('stat').get('savePctg'),
                                 'penalty_kill_opportunities': jsSplit.get('stat').get('penaltyKillOpportunities'),
                                 'save_pct_rank': jsSplit.get('stat').get('savePctRank'),
                                 'shooting_pct_rank': jsSplit.get('stat').get('shootingPctRank')
                                 }
                        splits.append(split)
        return team, stats, splits

    def save_data(self, df: dict):
        uri = os.getenv("AIRFLOW_CONN_DWH_DB")
        (team, stats, splits) = self.parse_data(df)
        logging.info(f'Вставка team:{team}')
        logging.info(f'Вставка stats:{stats}')
        logging.info(f'Вставка splits:{splits}')
        db = dataset.connect(uri)
        db.begin()
        try:
            db['team'].insert_many(rows=team, chunk_size=10000)
            db['stats'].insert_many(rows=stats, chunk_size=10000)
            db['splits'].insert_many(rows=splits, chunk_size=10000)
            db.commit()
        except Exception as e:
            db.rollback()

    def execute(self, context):
        headers = {
            'accept': 'application/json',
            'content-type': 'application/json;charset=UTF-8'
        }
        response = requests.get(url=f'{self.api_url}{self.team_id}/stats', headers=headers)
        if response.status_code == 200:
            data = response.json()
            self.save_data(data)
        else:
            logging.error(f"Request failed with status code: {response.status_code}")
