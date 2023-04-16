from django.urls import path

from .views import auth, account, listings, vendor

urlpatterns = [
    path('', listings.IndexView.as_view(), name="index"),
    path('categories/', listings.CategoriesList.as_view(), name="categories"),
    path('categories/<int:cat>/', listings.CategoryPage.as_view(), name="category"),
    path('products/<str:product>/', listings.ProductDetail.as_view(), name="product"),
    path('products/<str:product>/pricing', listings.ProductPricing.as_view(), name="product.pricing"),
    path('products/<str:product>/versions', listings.ProductVersions.as_view(), name="product.versions"),
    path('products/<str:product>/instructions', listings.ProductInstructions.as_view(), name="product.instructions"),
    path('products/<str:product>/buy', listings.ProductBuy.as_view(), name="product.buy"),
    path('vendors/<int:pk>/', listings.VendorPage.as_view(), name="vendor"),
    path('auth/login', auth.Login.as_view(), name="auth.login"),
    path('auth/logout', auth.Logout.as_view(), name="auth.logout"),
    path('auth/forgot', auth.PasswordReset.as_view(), name="auth.reset"),
    path('auth/forgot/confirm/<str:uidb64>/<str:token>/', auth.PasswordResetConfirm.as_view(), name="auth.reset.confirm"),
    path('auth/register', auth.register, name="auth.register"),
    path('account/', auth.UserIndex.as_view(), name="user.index"),
    path('account/user/password', auth.PasswordChange.as_view(), name="user.password"),
    path('account/business/create', account.Create.as_view(), name="account.create"),
    path('account/business/<int:pk>/', account.Detail.as_view(), name="account.index"),
    path('account/business/<int:pk>/edit', account.Edit.as_view(), name="account.edit"),
    path('account/business/<int:account>/servers/create', account.CreateServer.as_view(), name="account.server.create"),
    path('account/vendor/create', vendor.Create.as_view(), name="vendor.create"),
    path('account/vendor/<int:pk>/', vendor.Detail.as_view(), name="vendor.index"),
    path('account/vendor/<int:pk>/edit', vendor.Edit.as_view(), name="vendor.edit"),
    path('account/vendor/<int:vendor>/products/create', vendor.CreateProduct.as_view(), name="vendor.product.create"),
    path('account/vendor/<int:pk>/products/create_paid', vendor.CreatePaidProduct.as_view(), name="vendor.product.create.paid"),
    path('account/vendor/<int:vendor>/products/<int:pk>/edit', vendor.UpdateProduct.as_view(), name="vendor.product.edit"),
]
