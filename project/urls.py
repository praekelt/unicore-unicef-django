from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'skeleton.views.home', name='home'),
    # url(r'^skeleton/', include('skeleton.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('jmbo.urls')),
    url(r'^', include('unicef.urls')),
    url(r'^ckeditor/', include('ckeditor.urls')),
    url(r'^likes/', include('likes.urls')),
    url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^djga/', include('google_analytics.urls')),
)
