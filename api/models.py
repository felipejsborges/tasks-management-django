from datetime import datetime, timedelta

from django.contrib import admin
from django.db import models


class Task(models.Model):
    owner = models.ForeignKey(
        "auth.User", related_name="tasks", on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    title = models.CharField(max_length=100)
    description = models.TextField()

    effort = models.IntegerField()

    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-updated_at", "created_at"]

    def __str__(self):
        return str(self.title)

    @admin.display(
        boolean=True,
        ordering="completed_at",
        description="Completed recently?",
    )
    def was_completed_recently(self):
        now = datetime.now()
        return now - timedelta(days=1) <= self.completed_at <= now
