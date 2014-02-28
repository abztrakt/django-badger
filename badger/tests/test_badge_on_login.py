import badger

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User, Permission

class LoginBadgeTest(TestCase):
    def setUp(self):
        """
        Preps the test db for permissions testing
        """
        self.dawg = User.objects.create_user('Dawg', 'dawg@test.com', 'pass')
        self.dawg.save()

        c = Client()
        resp = c.get('/chronos/')
        c.login(username="Dawg", password='pass')

    def test_login:
        #Ensure a user is logged in
        self.assertEqual(resp1.status_code, 200)  # successfully logged in

    def testUserWithNoBadges:
        #A user that has not yet earned any badges
        #No badges should be awarded
        pass

    def testUserWithBadgesNoNew:
        #A user that has badged but has not earned any new badges
        #No badges should be awarded
        pass

    def testUserWithBadgesNew:
        #A user that has badges and has earned new badges
        #Badge(s) should be awarded
        pass
