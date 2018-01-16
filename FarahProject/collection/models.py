from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Subject(models.Model):
    subject_id = models.CharField(max_length=5, primary_key=True)

class Stimulus(models.Model):
    url = models.CharField(max_length=500)
    start_time = models.PositiveSmallIntegerField()
    subjects = models.ManyToManyField(Subject)
    active = models.BooleanField(default=True)

class PairedStimulusResultsBlock(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
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
    response_number = models.PositiveSmallIntegerField()
    play_time = models.DurationField()

    def response_rate(self):
        return self.response_number/self.play_time.seconds
