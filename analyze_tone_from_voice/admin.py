from django.contrib import admin
from .models import Depression, Stress, Person2, ADHD, PTSD
# Register your models here.

admin.site.register(Depression)
admin.site.register(Stress)
admin.site.register(Person2)
admin.site.register(ADHD)
admin.site.register(PTSD)