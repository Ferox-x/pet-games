from django.core.management import call_command
from django.test import TestCase

from games.models import SchulteModel, StroopModel
from services.games_services import Leaderboards, Achievements
from users.models import Users


class LeaderboardsAchievementsTests(TestCase):
    """Класс тестирования класса Leaderboards и Achievements."""

    @classmethod
    def setUpTestData(cls):
        """Загружает фикстуры в тестовую базу данных."""
        call_command('makefixtures')
        call_command('loaddata', 'fixtures/user.json')
        call_command('loaddata', 'fixtures/stroop_leaderboard.json')
        call_command('loaddata', 'fixtures/schulte_leaderboard.json')

    def setUp(self) -> None:
        """Создание экземпляров."""
        self.user: Users = Users.objects.get(id=1)
        self.leaderboard_schulte: Leaderboards = Leaderboards('schulte')
        self.leaderboard_stroop: Leaderboards = Leaderboards('stroop')
        self.achievements_schulte: Achievements = Achievements('schulte',
                                                               self.user)
        self.achievements_stroop: Achievements = Achievements('stroop',
                                                              self.user)

    def test_get_leaderboards_schulte(self) -> None:
        """Тест проверяющий на количество записей в таблице games_schulte."""
        len_schulte_leaderboard = len(
            self.leaderboard_schulte.get_leaderboard())
        self.assertEqual(
            len_schulte_leaderboard, 100,
            'Неверное количество записей, должно быть 100'
        )

    def test_get_leaderboards_stroop(self) -> None:
        """Тест проверяющий на количество записей в таблице games_stroop."""
        leaderboard_stroop = len(
            self.leaderboard_schulte.get_leaderboard())
        self.assertEqual(
            leaderboard_stroop, 100,
            'Неверное количество записей, должно быть 100'
        )

    def test_get_leaderboards_wrong_game(self) -> None:
        """Тест проверяющий на отсутствие таблицы лидеров."""
        leaderboard = Leaderboards('1111111').get_leaderboard()
        self.assertEqual(leaderboard, False)

    def test_get_leaderboard_with_paginator(self) -> None:
        """Тест проверяющий работу пагинатора, на первой странице должно быть 25 записей."""
        paginator = self.leaderboard_schulte.get_leaderboard_with_paginator()
        len_first_page = len(paginator.page(1))
        self.assertEqual(
            len_first_page, 25, 'Неверное количество записей, должно быть 25'
        )

    def test_get_leaderboard_with_paginator_wrong_game(self):
        """Тест проверяющий на отсутствие таблицы лидеров с пагинатором."""
        leaderboard = Leaderboards('1111111').get_leaderboard_with_paginator()
        self.assertEqual(leaderboard, False)

    def test_get_achievements_schulte(self) -> None:
        achievements = self.achievements_schulte.get_achievements()[0].get('record')
        queryset = SchulteModel.objects.order_by('date').values(
            'record').filter(
            user_id=self.user.id).reverse().all()[0].get('record')
        self.assertEqual(achievements, queryset, 'Неверный QuerySet')

    def test_get_achievements_stroop(self) -> None:
        achievements = self.achievements_stroop.get_achievements()[0].get('record')
        queryset = StroopModel.objects.order_by('date').values('record').filter(
            user_id=self.user.id).all().reverse()[0].get('record')
        self.assertEqual(achievements, queryset, 'Неверный QuerySet')

    def test_save_achievement_schulte(self) -> None:
        self.achievements_schulte.save_achievement('00:09:00')
        achievement = SchulteModel.objects.filter(user_id=self.user.id, record=900).first()
        self.assertEqual(achievement.record, 900)

    def test_save_achievement_stroop(self) -> None:
        self.achievements_stroop.save_achievement('999 - 0 - 1', 15000)
        achievement = StroopModel.objects.filter(user_id=self.user.id, score=15000).first()
        self.assertEqual(achievement.record, '999 - 0 - 1')
