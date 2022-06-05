from django.conf import settings
from django.core.cache import cache

from mainapp.models import Products, ProductCategory


def get_links_menu_category(category_id):
    if settings.LOW_CACHE:
        key = 'category_products'
        category_product = cache.get(key)
        if category_product is None:
            category_product = Products.objects.filter(category=category_id).select_related('category')
            cache.set(key, category_product)
        return category_product
    else:
        return Products.objects.filter(category=category_id).select_related('category')

def get_links_menu():
    if settings.LOW_CACHE:
        key = 'all_products'
        all_products = cache.get(key)
        if all_products is None:
            all_products = Products.objects.all()
            cache.set(key, all_products)
        return all_products
    return Products.objects.all()


def get_categories():
    if settings.LOW_CACHE:
        key = 'all_cats'
        all_cats = cache.get(key)
        if all_cats is None:
            all_cats = ProductCategory.objects.all()
            cache.set(key, all_cats)
        return all_cats
    return ProductCategory.objects.all()


def get_product_detail(pk):
    if settings.LOW_CACHE:
        key = 'product'
        product = cache.get(key)
        if product is None:
            product = Products.objects.filter(pk=pk).select_related('category')
            cache.set(key, product)
        return product
    else:
        return Products.objects.filter(pk=pk)
