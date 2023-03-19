from django.test import TestCase
from houselog.models import Houselog
from django.contrib.auth.models import User
import datetime


# Create your tests here.
# https://devblogs.microsoft.com/python/announcing-playwright-for-python-reliable-end-to-end-testing-for-the-web/

class TestModelParameters(TestCase):
    """
    Test field settings like note can be blank, etc
    """
    pass


class TestProperties(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(
            username="test_user",
            password="1234"
        )

        # id 1
        Houselog.objects.create(
            title="test",
            frequency="20",
            last_done=datetime.date.today(),
            user=user
        )

        # id 2
        Houselog.objects.create(
            title="test2",
            frequency="2",
            last_done=datetime.date.today(),
            user=user
        )

        # id 3
        Houselog.objects.create(
            title="test3",
            frequency="2",
            last_done="2023-01-01",
            user=user
        )

    def test_next_run(self):
        item = Houselog.objects.get(id=1)
        self.assertEqual(item.next_run, datetime.date.today() + datetime.timedelta(days=item.frequency))

    def test_status_ok(self):
        item = Houselog.objects.get(id=1)
        self.assertEqual(item.status, "ok")

    def test_status_soon(self):
        item = Houselog.objects.get(id=2)
        self.assertEqual(item.status, "soon")

    def test_status_late(self):
        item = Houselog.objects.get(id=3)
        self.assertEqual(item.status, "late")
