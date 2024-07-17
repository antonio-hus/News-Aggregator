###################
# IMPORTS SECTION #
###################
# Django Libraries
from django.contrib import admin
# Project Libraries
from .models import User, Media, Category, Tag, NewsSource, Article


######################
# MODEL REGISTRATION #
######################
# User Class
admin.site.register(User)
# Media Class
admin.site.register(Media)
# Category Class
admin.site.register(Category)
# Tag Class
admin.site.register(Tag)
# News Source Class
admin.site.register(NewsSource)


#########################
# DISPLAY CUSTOMIZATION #
#########################
# Article Class
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):

    # Display Options
    # Display Fields
    list_display = ('title', 'publish_date', 'publisher', 'likes_count', 'favorite_count')
    # Display Filters
    list_filter = ('publish_date', 'publisher', 'tags', 'category')
    # Display Search Fields
    search_fields = ('title', 'content', 'writer')
    # Display Filter ( Useful for ManyToMany Relation Mappings )
    filter_horizontal = ('tags', 'liked_by', 'favorited_by', 'read_later_by')

    # Custom Fields
    # Likes Counts
    def likes_count(self, obj):
        return obj.likes_count()
    # Favourites Count
    def favorite_count(self, obj):
        return obj.favorite_count()

