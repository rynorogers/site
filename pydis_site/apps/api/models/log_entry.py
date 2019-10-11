import textwrap

from django.db import models
from django.utils import timezone

from pydis_site.apps.api.models.utils import ModelReprMixin


# Used to shorten the timestamp length in the Django Admin.
TIMESTAMP_WITH_SECONDS_LENGTH = len('YYYY-MM-DD HH:MM:SS')


class LogEntry(ModelReprMixin, models.Model):
    """A log entry generated by one of the PyDis applications."""

    application = models.CharField(
        max_length=20,
        help_text="The application that generated this log entry.",
        choices=(
            ('bot', 'Bot'),
            ('seasonalbot', 'Seasonalbot'),
            ('site', 'Website')
        )
    )
    logger_name = models.CharField(
        max_length=100,
        help_text="The name of the logger that generated this log entry."
    )
    timestamp = models.DateTimeField(
        default=timezone.now,
        help_text="The date and time when this entry was created."
    )
    level = models.CharField(
        max_length=8,  # 'critical'
        choices=(
            ('debug', 'Debug'),
            ('info', 'Info'),
            ('warning', 'Warning'),
            ('error', 'Error'),
            ('critical', 'Critical')
        ),
        help_text=(
            "The logger level at which this entry was emitted. The levels "
            "correspond to the Python `logging` levels."
        )
    )
    module = models.CharField(
        max_length=100,
        help_text="The fully qualified path of the module generating this log line."
    )
    line = models.PositiveSmallIntegerField(
        help_text="The line at which the log line was emitted."
    )
    message = models.TextField(
        help_text="The textual content of the log line."
    )

    def __str__(self) -> str:
        timestamp = str(self.timestamp)[:TIMESTAMP_WITH_SECONDS_LENGTH]
        message = textwrap.shorten(self.message, width=140)
        level = self.level[:4].upper()

        return f'{timestamp} | {self.application} | {level} | {message}'
