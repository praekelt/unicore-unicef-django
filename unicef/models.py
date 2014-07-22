from post.models import Post
from category.models import Category


class HygienePost(Post):
    primary_category_slug = 'hygiene'

    class Meta:
        app_label = 'post'
        proxy = True

    def save(self, *args, **kwargs):
        if not self.primary_category:
            self.primary_category = Category.objects.get(
                slug=self.primary_category_slug)
        super(HygienePost, self).save(*args, **kwargs)


class DiarrhoeaPost(Post):
    primary_category_slug = 'diarrhoea'

    class Meta:
        app_label = 'post'
        proxy = True

    def save(self, *args, **kwargs):
        if not self.primary_category:
            self.primary_category = Category.objects.get(
                slug=self.primary_category_slug)
        super(DiarrhoeaPost, self).save(*args, **kwargs)
