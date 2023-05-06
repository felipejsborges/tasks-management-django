from datetime import datetime, timedelta

from django.test import TestCase

from .models import Task


class TaskModelTests(TestCase):
    def test_was_completed_recently_with_future_task(self):
        """
        was_completed_recently() returns False for tasks whose completed_at
        is in the future.
        """
        time = datetime.now() + timedelta(days=30)
        future_task = Task(completed_at=time)
        self.assertIs(future_task.was_completed_recently(), False)

    def test_was_completed_recently_with_old_task(self):
        """
        was_completed_recently() returns False for tasks whose completed_at
        is older than 1 day.
        """
        time = datetime.now() - timedelta(days=1, seconds=1)
        old_task = Task(completed_at=time)
        self.assertIs(old_task.was_completed_recently(), False)

    def test_was_completed_recently_with_recent_task(self):
        """
        was_completed_recently() returns True for tasks whose completed_at
        is within the last day.
        """
        time = datetime.now() - timedelta(hours=23, minutes=59, seconds=59)
        recent_task = Task(completed_at=time)
        self.assertIs(recent_task.was_completed_recently(), True)
