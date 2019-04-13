from django.shortcuts import get_object_or_404
from django.utils.functional import cached_property
from django.views.generic import TemplateView, ListView
from django_context_decorator import context

from plum.core.models import Product, Category


class IndexView(TemplateView):
    template_name = 'front/index.html'

    @context
    def products(self):
        return Product.objects.filter(approved=True).select_related('vendor', 'category')


class CategoriesList(ListView):
    queryset = Category.objects.order_by('name')
    template_name = 'front/categories.html'
    context_object_name = 'categories'


class CategoryPage(ListView):
    queryset = Category.objects.order_by('name')
    template_name = 'front/category.html'
    context_object_name = 'products'

    def get_queryset(self):
        return self.category.product_set.filter(approved=True).select_related('vendor').order_by('name')

    @context
    @cached_property
    def category(self):
        return get_object_or_404(Category, pk=self.kwargs.get('cat'))
