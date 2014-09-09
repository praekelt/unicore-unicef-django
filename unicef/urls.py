from django.views.generic import TemplateView
from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', 'unicef.views.home', name='home'),
    url(
        r'^about/$',
        TemplateView.as_view(template_name="unicef/about.html"),
        name='about'
    ),
    url(
        r'^credits/$',
        TemplateView.as_view(template_name="unicef/credits.html"),
        name='credits'
    ),
    url(
        r'^contact/$',
        TemplateView.as_view(template_name="unicef/contact.html"),
        name='contact'
    ),
    url(
        r'^about/hygiene/$',
        TemplateView.as_view(template_name="unicef/hygiene.html"),
        name='about_hygiene'
    ),
    url(
        r'^about/diarrhoea/$',
        TemplateView.as_view(template_name="unicef/diarrhoea.html"),
        name='about_diarrhoea'
    ),
    #url(r'^search/', cache_page(SearchView(results_per_page=5), 60 * 60), name='haystack_search'),
)

if settings.DEBUG:
    urlpatterns += patterns(
        '',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )
