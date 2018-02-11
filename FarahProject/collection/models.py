from __future__ import unicode_literals

from django.db import models
import re
from django.utils import timezone

# Create your models here.
class Subject(models.Model):
    subject_id = models.CharField(max_length=5, primary_key=True)

    def __unicode__(self):
        return "Subject " + str(self.subject_id)

class Stimulus(models.Model):
    class Meta:
        verbose_name_plural = "Stimuli"

    url = models.CharField(max_length=500)
    video_id = models.CharField(max_length=50)
    start_time = models.PositiveSmallIntegerField()
    subjects = models.ManyToManyField(Subject)
    active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if "&" in self.url:
            temp = self.url.split("&", 1)[0]
        else:
            temp = self.url
        result = re.search('v=(.*)', temp)
        self.video_id = result.group(1)
        return super(Stimulus, self).save(*args, **kwargs)

class PairedStimulusResultsBlock(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    session_number = models.PositiveSmallIntegerField()
    created = models.DateTimeField(editable=False)
    completed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        return super(PairedStimulusResultsBlock, self).save(*args, **kwargs)

    def date_time(self):
        return self.created

class PairedStimulusResult(models.Model):
    block = models.ForeignKey(PairedStimulusResultsBlock, on_delete=models.CASCADE)
    video_left = models.ForeignKey(Stimulus, on_delete=models.CASCADE, related_name="LeftStimResult")
    video_right = models.ForeignKey(Stimulus, on_delete=models.CASCADE, related_name="RightStimResult")
    video_selected = models.NullBooleanField(choices=((False, "Left"), (True, "Right")))

class ConjugateStimulusResultsBlock(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    created = models.DateTimeField(editable=False)
    completed = models.BooleanField(default=False)
    session_number = models.PositiveSmallIntegerField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        return super(ConjugateStimulusResultsBlock, self).save(*args, **kwargs)

    def date_time(self):
        return self.created

class ConjugateStimulusResult(models.Model):
    block = models.ForeignKey(ConjugateStimulusResultsBlock, on_delete=models.CASCADE)
    video = models.ForeignKey(Stimulus, on_delete=models.CASCADE)
    response_number = models.PositiveSmallIntegerField(null=True)
    play_time = models.DurationField(null=True)

    def response_rate(self):
        return self.response_number/self.play_time.seconds
