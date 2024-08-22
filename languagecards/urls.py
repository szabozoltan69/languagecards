from django.urls import path
from .views import (IndexView, UnfilteredView, JndexView, CategoryView,
                    User2View, User3View, User4View, robots_txt)


urlpatterns = [
    path('', IndexView.as_view()),
    path('0', JndexView.as_view()),
    path('all', UnfilteredView.as_view()),
    path('2', User2View.as_view()),
    path('3', User3View.as_view()),
    path('4', User4View.as_view()),
    path("categ/<int:category>", CategoryView.as_view()),
    path("robots.txt", robots_txt),
# Also add in vite.config.js
]
