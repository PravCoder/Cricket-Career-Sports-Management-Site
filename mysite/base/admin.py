from django.contrib import admin
from.models import *

# Register your models here.

admin.site.register(Player)
admin.site.register(Team)
admin.site.register(Game)
admin.site.register(GameInvite)
admin.site.register(TeamInvite)

admin.site.register(PlayerGameStat)
admin.site.register(Organization)
admin.site.register(OrganizationInvite)

admin.site.register(Chat)
admin.site.register(Message)