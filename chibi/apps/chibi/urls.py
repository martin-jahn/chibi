from django.urls import path

from . import views

app_name = 'chibi'


urlpatterns = [
    path('<slug>', views.redirect_view, name='short_url'),
    path('api/shorten/', views.AlarmSegmentView.as_view(), name='api_shorten'),
]
