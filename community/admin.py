from django.contrib import admin
from .models import CommunitySection, Post, Comment
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):

    summernote_fields = ('description')


admin.site.register(CommunitySection)
admin.site.register(Comment)
