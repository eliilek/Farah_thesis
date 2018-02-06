from django.contrib import admin

# Register your models here.
from models import *

class StimulusAdmin(admin.ModelAdmin):
    exclude = ('video_id',)

# Register your models here.
admin.site.register(Stimulus, StimulusAdmin)
admin.site.register(Subject)
