from django.contrib import admin
from .models import User, Listing, Category, Comment

admin.site.register(User)
admin.site.register(Listing)
admin.site.register(Category)
admin.site.register(Comment)

