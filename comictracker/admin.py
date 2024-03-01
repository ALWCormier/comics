from django.contrib import admin
from .models import Comic, Series, Artist

# Register your models here.
admin.site.register(Comic)
admin.site.register(Series)
admin.site.register(Artist)