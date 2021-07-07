# -*- coding: utf-8 -*-
from django.conf.urls import url, patterns, include
from django.core.urlresolvers import reverse_lazy
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import RedirectView
from django.contrib import admin
from .views import BroadcastChatView,index,user_login,user_logout,register
from django.conf import settings
from django.conf.urls.static import static

admin.autodiscover()

urlpatterns = patterns('',
                        url(r'^register/$', register, name='register'),
                        url(r'^$',index,name='index'),
                        url(r'^logout/$',user_logout, name='logout'),
                       url(r'^user_login/',user_login,name='user_login'),
                       url(r'^chat/$', BroadcastChatView.as_view(), name='chat'),
                       url(r'^admin/', include(admin.site.urls)),
                       ) + staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
handler404 = 'chatserver.views.handler404'
