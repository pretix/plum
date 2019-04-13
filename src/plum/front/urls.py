from django.conf.urls import url

from .views.listings import IndexView, CategoriesList, CategoryPage, ProductDetail, ProductPricing

urlpatterns = [
    url(r'^$', IndexView.as_view(), name="index"),
    url(r'^categories/$', CategoriesList.as_view(), name="categories"),
    url(r'^categories/(?P<cat>\d+)/$', CategoryPage.as_view(), name="category"),
    url(r'^products/(?P<product>\d+)/$', ProductDetail.as_view(), name="product"),
    url(r'^products/(?P<product>\d+)/pricing$', ProductPricing.as_view(), name="product.pricing"),
]
