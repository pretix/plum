from django.conf.urls import url

from .views import auth, listings

urlpatterns = [
    url(r'^$', listings.IndexView.as_view(), name="index"),
    url(r'^categories/$', listings.CategoriesList.as_view(), name="categories"),
    url(r'^categories/(?P<cat>\d+)/$', listings.CategoryPage.as_view(), name="category"),
    url(r'^products/(?P<product>[^/]+)/$', listings.ProductDetail.as_view(), name="product"),
    url(r'^products/(?P<product>[^/]+)/pricing$', listings.ProductPricing.as_view(), name="product.pricing"),
    url(r'^products/(?P<product>[^/]+)/versions$', listings.ProductVersions.as_view(), name="product.versions"),
    url(r'^products/(?P<product>[^/]+)/instructions$', listings.ProductInstructions.as_view(), name="product.instructions"),
    url(r'^products/(?P<product>[^/]+)/buy$', listings.ProductBuy.as_view(), name="product.buy"),
    url(r'^auth/login$', auth.Login.as_view(), name="auth.login"),
    url(r'^auth/logout$', auth.Logout.as_view(), name="auth.logout"),
    url(r'^auth/forgot$', auth.PasswordReset.as_view(), name="auth.reset"),
    url(r'^auth/forgot/confirm/(?P<uidb64>[^/]+)/(?P<token>[^/]+)/$', auth.PasswordResetConfirm.as_view(), name="auth.reset.confirm"),
    url(r'^user/', auth.UserIndex.as_view(), name="user.index"),
    url(r'^user/password$', auth.PasswordChange.as_view(), name="user.password"),
]
