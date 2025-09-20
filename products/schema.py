import graphene
from graphene_django import DjangoObjectType
from .models import Product
from .models import ProductImage


class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = ('id', 'name', 'slug', 'description', 'price', 'stock_quantity', 'is_active', 'created_at', 'updated_at', 'images')


class ProductImageType(DjangoObjectType):
    class Meta:
        model = ProductImage
        fields = ('id', 'image', 'order', 'alt_text')


class Query(graphene.ObjectType):
    products = graphene.List(ProductType, search=graphene.String(), first=graphene.Int(), skip=graphene.Int())
    product = graphene.Field(ProductType, id=graphene.Int(), slug=graphene.String())

    def resolve_products(self, info, search=None, first=None, skip=None):
        qs = Product.objects.filter(is_active=True).order_by('-created_at')
        if search:
            qs = qs.filter(name__icontains=search)
        if skip:
            qs = qs[skip:]
        if first:
            qs = qs[:first]
        return qs

    def resolve_product(self, info, id=None, slug=None):
        if id:
            return Product.objects.filter(is_active=True).filter(pk=id).first()
        if slug:
            return Product.objects.filter(is_active=True).filter(slug=slug).first()
        return None
