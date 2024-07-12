# Imports Section
from django.contrib import admin
from .models import User, Media, Category, Tag, NewsSource, Article


# Display Customization
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'publish_date', 'publisher', 'likes_count', 'favorite_count')
    list_filter = ('publish_date', 'publisher', 'tags', 'categories')
    search_fields = ('title', 'content', 'writer')
    filter_horizontal = ('tags', 'categories', 'medias_full', 'liked_by', 'favorited_by', 'read_later_by')

    def likes_count(self, obj):
        return obj.liked_by.count()

    def favorite_count(self, obj):
        return obj.favorited_by.count()


# Model Registration
admin.site.register(User)
admin.site.register(Media)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(NewsSource)
