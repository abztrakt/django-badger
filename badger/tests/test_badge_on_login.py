import badger

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User, Permission

#Need to finish writing the following unit tests

#Should also be unit test for:
#Award Badge manually that has 1 prereq
#Award Badge manually that has 0 prereq
#Award Badge to someone that doesn have the prereqs
#Award a milestone badge automatically
#Award badge with claim code
#Nominate person for badge

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
        pass

    def test_userWithNoBadges:
        #A user that has not yet earned any badges
        #No badges should be awarded
        return Award.objects.create(user=awardee, badge=self,creator=awarder,description=description)
        pass

    def test_userWithBadgesNoNew:
        #A user that has badged but has not earned any new badges
        #No badges should be awarded
        pass

    def test_userWithBadgesNew:
        #A user that has badges and has earned new badges
        #Badge(s) should be awarded
        pass
