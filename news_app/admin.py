from django.contrib import admin
from .models import Category, Post, Comment
from modeltranslation.admin import TranslationAdmin


class CategoryAdmin(TranslationAdmin):
    model = Category

class MyModelAdmin(TranslationAdmin):
    model = Post

class PostAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    list_display = ('title', 'text', 'type', 'author', 'created_at', 'rating')  # оставляем только имя и цену товара
    list_filter = ('title', 'categories', 'text', 'type', 'author', 'created_at', 'rating')  # добавляем примитивные фильтры в нашу админку
    search_fields = ('title', 'text')  # тут всё очень похоже на фильтры из запросов в базу


admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)

