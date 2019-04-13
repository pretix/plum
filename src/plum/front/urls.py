from django.conf.urls import url

from .views.listings import IndexView, CategoriesList, CategoryPage

urlpatterns = [
    url(r'^$', IndexView.as_view(), name="index"),
    url(r'^categories/$', CategoriesList.as_view(), name="categories"),
    url(r'^categories/(?P<cat>\d+)/$', CategoryPage.as_view(), name="category"),
]
