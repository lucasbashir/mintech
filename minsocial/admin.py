from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Post)
admin.site.register(User)
admin.site.register(Follow)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Love)
admin.site.register(Shock)
admin.site.register(Haha)
admin.site.register(Sad)

