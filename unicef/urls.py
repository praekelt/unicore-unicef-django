from django.views.generic import TemplateView
from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(
        r'^$',
        TemplateView.as_view(template_name="unicef/home.html"),
        name='home'
    ),
    url(
        r'^about/$',
        TemplateView.as_view(template_name="unicef/about.html"),
        name='about'
    ),
    url(
        r'^terms/$',
        TemplateView.as_view(template_name="unicef/terms.html"),
        name='terms'
    ),
    url(
        r'^hygiene/$',
        TemplateView.as_view(template_name="unicef/terms.html"),
        name='hygiene_list'
    ),
    url(
        r'^diarrhoea/$',
        TemplateView.as_view(template_name="unicef/terms.html"),
        name='diarrhoea_list'
    ),
    #url(r'^search/', cache_page(SearchView(results_per_page=5), 60 * 60), name='haystack_search'),
)

if settings.DEBUG:
    urlpatterns += patterns(
        '',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )
