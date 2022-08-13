from games.models import StroopModel, SchulteModel


class Leaderboards:

    def __init__(self, game):
        self.game = game

    @staticmethod
    def _get_stroop_leaderboard():
        stroop_leaderboard = StroopModel.objects.raw(
                    """
                    WITH table1 AS (SELECT DISTINCT ON (user_id) user_id, games_stroop.id, score,record, date, username FROM games_stroop
                    INNER JOIN "Users" ON user_id = "Users"."id"
                    ORDER BY user_id, score DESC)
                    SELECT id, score, record, date, username FROM table1
                    ORDER BY score DESC
                    LIMIT 100
                    """
                )
        return stroop_leaderboard

    @staticmethod
    def _get_schulte_leaderboard():
        schulte_leaderboard = SchulteModel.objects.raw(
                    """
                    WITH table1 AS (SELECT DISTINCT ON (user_id) user_id, games_schulte.id, record, date, username FROM games_schulte
                    INNER JOIN "Users" ON user_id = "Users"."id"
                    ORDER BY user_id, record)
                    SELECT id, record, date, username FROM table1
                    ORDER BY record
                    LIMIT 100
                    """
                )
        return schulte_leaderboard

    def get_leaderboard(self):
        if self.game == 'schulte':
            return self._get_schulte_leaderboard()
        elif self.game == 'stroop':
            return self._get_stroop_leaderboard()
        else:
            return False


class Achievements:
    def __init__(self, game, user=None):
        self.game = game
        self.user = user

    def _get_schulte_achievements(self):
        records = SchulteModel.objects.order_by('date').values('record').filter(
                user_id=self.user.id).reverse().all()

        return records

    def _get_stroop_achievements(self):
        records = StroopModel.objects.order_by('date').values('record').filter(
            user_id=self.user.id).all().reverse()

        return records

    def get_achievements(self):
        if self.game == 'schulte':
            return self._get_schulte_achievements()
        elif self.game == 'stroop':
            return self._get_stroop_achievements()

    def _save_schulte_achievement(self, achievement):
        time = achievement.split(':')
        time = int(time[0]) * 60 * 100 + int(time[1]) * 100 + int(time[2])
        SchulteModel(record=time, user=self.user).save()

    def _save_stroop_achievement(self, achievement):
        StroopModel(record=achievement, user=self.user).save()

    def save_achievement(self, achievement):
        if self.game == 'schulte':
            return self._save_schulte_achievement(achievement)
        elif self.game == 'stroop':
            return self._save_stroop_achievement(achievement)
