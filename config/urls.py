from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from apiv1 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html')),
    path('create/', TemplateView.as_view(template_name='gacha.html')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/', include('apiv1.urls')),
    path('api/v1/result/', views.GachaViewSet.as_view()),
    path('api/', include('accounts.urls')),
    path('register/', TemplateView.as_view(template_name='create.html'), name="register"),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns
