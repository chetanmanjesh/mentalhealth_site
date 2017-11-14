from django.contrib import admin
from .models import Depression, Stress, Person2
# Register your models here.

admin.site.register(Depression)
admin.site.register(Stress)
admin.site.register(Person2)