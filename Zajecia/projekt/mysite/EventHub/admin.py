from django.contrib import admin
from .models import User, Category, Event, Enrollment, Comment

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Event)
admin.site.register(Enrollment)
admin.site.register(Comment)