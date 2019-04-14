from django.conf.urls import url

from .views import auth, account, listings, vendor

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
    url(r'^auth/register$', auth.register, name="auth.register"),
    url(r'^user/$', auth.UserIndex.as_view(), name="user.index"),
    url(r'^user/password$', auth.PasswordChange.as_view(), name="user.password"),
    url(r'^account/create$', account.Create.as_view(), name="account.create"),
    url(r'^account/(?P<pk>\d+)/$', account.Detail.as_view(), name="account.index"),
    url(r'^account/(?P<pk>\d+)/edit$', account.Edit.as_view(), name="account.edit"),
    url(r'^account/(?P<account>\d+)/servers/create$', account.CreateServer.as_view(), name="account.server.create"),
    url(r'^vendor/create$', vendor.Create.as_view(), name="vendor.create"),
    url(r'^vendor/(?P<pk>\d+)/$', vendor.Detail.as_view(), name="vendor.index"),
    url(r'^vendor/(?P<pk>\d+)/edit$', vendor.Edit.as_view(), name="vendor.edit"),
    url(r'^vendor/(?P<vendor>\d+)/products/create$', vendor.CreateProduct.as_view(), name="vendor.product.create"),
    url(r'^vendor/(?P<pk>\d+)/products/create_paid$', vendor.CreatePaidProduct.as_view(), name="vendor.product.create.paid"),
    url(r'^vendor/(?P<vendor>\d+)/products/(?P<pk>\d+)/edit$', vendor.UpdateProduct.as_view(), name="vendor.product.edit"),
]
