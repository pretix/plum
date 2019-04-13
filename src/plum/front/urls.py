from django.conf.urls import url

from .views import listings

urlpatterns = [
    url(r'^$', listings.IndexView.as_view(), name="index"),
    url(r'^categories/$', listings.CategoriesList.as_view(), name="categories"),
    url(r'^categories/(?P<cat>\d+)/$', listings.CategoryPage.as_view(), name="category"),
    url(r'^products/(?P<product>\d+)/$', listings.ProductDetail.as_view(), name="product"),
    url(r'^products/(?P<product>\d+)/pricing$', listings.ProductPricing.as_view(), name="product.pricing"),
    url(r'^products/(?P<product>\d+)/versions$', listings.ProductVersions.as_view(), name="product.versions"),
]
