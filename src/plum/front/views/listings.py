from django.db.models import Q, Count
from django.shortcuts import get_object_or_404
from django.utils.functional import cached_property
from django.views.generic import TemplateView, ListView, DetailView
from django_context_decorator import context

from plum.core.models import Product, Category, Vendor


class IndexView(TemplateView):
    template_name = 'front/index.html'

    @context
    def products(self):
        return Product.objects.filter(approved=True, unlisted=False).exclude(stability='discontinued').select_related('vendor', 'category').order_by('-certified', 'name')


class CategoriesList(ListView):
    queryset = Category.objects.annotate(c=Count('products')).order_by('name')
    template_name = 'front/categories.html'
    context_object_name = 'categories'


class CategoryPage(ListView):
    template_name = 'front/category.html'
    context_object_name = 'products'

    def get_queryset(self):
        return self.category.products.filter(approved=True, unlisted=False).exclude(stability='discontinued').select_related('vendor').order_by('name')

    @context
    @cached_property
    def category(self):
        return get_object_or_404(Category, pk=self.kwargs.get('cat'))


class VendorPage(ListView):
    template_name = 'front/vendor.html'
    context_object_name = 'products'

    def get_queryset(self):
        return self.vendor.products.filter(approved=True, unlisted=False).select_related('vendor').order_by('name')

    @context
    @cached_property
    def vendor(self):
        return get_object_or_404(Vendor, pk=self.kwargs.get('pk'))


class ProductDetail(DetailView):
    context_object_name = 'product'
    slug_url_kwarg = 'product'
    template_name = 'front/product.html'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Product.objects.filter(
                Q(approved=True) | Q(vendor__users__pk__in=[self.request.user.pk])
            ).distinct()
        else:
            return Product.objects.filter(
                Q(approved=True)
            ).distinct()


class ProductPricing(ProductDetail):
    template_name = 'front/product_pricing.html'


class ProductVersions(ProductDetail):
    template_name = 'front/product_versions.html'


class ProductInstructions(ProductDetail):
    template_name = 'front/product_instructions.html'


class ProductBuy(ProductDetail):
    template_name = 'front/product_buy.html'
