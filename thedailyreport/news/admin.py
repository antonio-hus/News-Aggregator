# Imports Section
from django.contrib import admin
from .models import User, Media, Category, Tag, NewsSource, Article


# Display Customization
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title_preview', 'publish_date', 'publisher', 'likes_count', 'favorite_count')
    search_fields = ('title_preview', 'content_preview', 'writer')
    list_filter = ('publish_date', 'publisher', 'tags', 'categories')
    filter_horizontal = ('tags', 'categories', 'medias_full', 'medias_mailing', 'liked_by', 'favorited_by', 'read_later_by')


# Model Registration
admin.site.register(User)
admin.site.register(Media)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(NewsSource)
admin.site.register(Article, ArticleAdmin)
