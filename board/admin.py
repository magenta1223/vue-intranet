from django.contrib import admin
from .models import Post, Category

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name'] # 아래 register에서 함께 들어간 model DB에서 검색이 가능해짐

admin.site.register(Category, CategoryAdmin)