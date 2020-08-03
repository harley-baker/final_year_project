from django.contrib import admin
from .models import TwitterUser, Search

admin.site.register(TwitterUser)
admin.site.register(Search)