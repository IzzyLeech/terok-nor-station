from django.contrib import admin
from .models import Season, Episode, EpisodeLog
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Season)
class SeasonAdmin(SummernoteModelAdmin):

    summernote_fields = ('summary')

admin.site.register(Episode)
admin.site.register(EpisodeLog)
