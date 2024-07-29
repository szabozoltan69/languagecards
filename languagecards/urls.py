from django.urls import path
from .views import IndexView, BriefView, UnfilteredView


urlpatterns = [
    path('', IndexView.as_view()),
    path('2', BriefView.as_view()),
    path('all', UnfilteredView.as_view()),
# Also add in vite.config.js
]
