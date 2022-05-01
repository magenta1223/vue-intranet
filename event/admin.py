from django.contrib import admin
from .models import *

# Register your models here.

class EventGroupAdmin(admin.ModelAdmin):
    search_fields = ['name'] # 아래 register에서 함께 들어간 model DB에서 검색이 가능해짐

class EventAdmin(admin.ModelAdmin):
    search_fields = ['name'] # 아래 register에서 함께 들어간 model DB에서 검색이 가능해짐



admin.site.register(Event, EventAdmin)
admin.site.register(EventGroup, EventGroupAdmin)