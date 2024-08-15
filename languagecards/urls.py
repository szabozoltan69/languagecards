from django.urls import path
from .views import IndexView, UnfilteredView, JndexView, User2View, User3View, User4View


urlpatterns = [
    path('', IndexView.as_view()),
    path('0', JndexView.as_view()),
    path('all', UnfilteredView.as_view()),
    path('2', User2View.as_view()),
    path('3', User3View.as_view()),
    path('4', User4View.as_view()),
# Also add in vite.config.js
]
