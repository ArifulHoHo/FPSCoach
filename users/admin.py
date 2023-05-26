from django.contrib import admin
from .models import Profile,ValorantData, Skill, Review, CoachProfile, BookSession, Message, NewsPortalPost, Tag
# Register your models here.

admin.site.register(Profile)
admin.site.register(Skill)
admin.site.register(Review)
admin.site.register(CoachProfile)
admin.site.register(ValorantData)
admin.site.register(BookSession)
admin.site.register(Message)
admin.site.register(NewsPortalPost)
admin.site.register(Tag)