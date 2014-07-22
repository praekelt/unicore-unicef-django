from django.contrib import admin
from django.contrib.admin.sites import NotRegistered

from post.models import Post
from jmbo.admin import ModelBaseAdmin

from unicef.models import HygienePost, DiarrhoeaPost


class PostAdmin(ModelBaseAdmin):
    raw_id_fields = ('owner', )
    inlines = ModelBaseAdmin.inlines
    list_display = (
        'title', 'primary_category', 'publish_on', 'retract_on',
        '_get_absolute_url', 'is_featured', 'created', '_actions',
        '_view_comments'
    )
    ordering = ('-publish_on', '-created')
    list_per_page = 10

    def is_featured(self, obj, *args, **kwargs):
        return obj.categories.filter(slug='featured').exists()
    is_featured.boolean = True

    def _view_comments(self, article):
        return '<a href="/admin/post/%s/%s/moderate/">View (%s)</a>' % (
            article._meta.module_name,
            article.pk, article.comment_count)

    _view_comments.short_description = 'Comments'
    _view_comments.allow_tags = True


class UnicefPostAdmin(PostAdmin):

    def queryset(self, request):
        qs = super(UnicefPostAdmin, self).queryset(request)
        return qs.filter(
            primary_category__slug=self.model.primary_category_slug)


try:
    admin.site.unregister(Post)
except NotRegistered:
    pass

admin.site.register(Post, PostAdmin)
admin.site.register(HygienePost, UnicefPostAdmin)
admin.site.register(DiarrhoeaPost, UnicefPostAdmin)
