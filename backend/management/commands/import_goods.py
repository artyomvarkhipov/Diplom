import yaml
from django.core.management.base import BaseCommand
from backend.models import Shop, Category, Product, ProductInfo, Parameter, ProductParameter


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str)

    def handle(self, *args, **options):
        file_path = options['file_path']
        with open(file_path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)

        shop, created = Shop.objects.get_or_create(name=data['shop'])

        for category in data['categories']:
            category_object, created = Category.objects.get_or_create(
                id=category['id'],
                name=category['name']
            )
            category_object.shops.add(shop.id)
            category_object.save()

        ProductInfo.objects.filter(shop_id=shop.id).delete()

        for item in data['goods']:
            product, created = Product.objects.get_or_create(
                name=item['name'],
                category_id=item['category']
            )
            product_info = ProductInfo.objects.create(
                product_id=product.id,
                external_id=item['id'],
                model=item['model'],
                price=item['price'],
                price_rrc=item['price_rrc'],
                quantity=item['quantity'],
                shop_id=shop.id
            )
            for name, value in item['parameters'].items():
                parameter_object, created = Parameter.objects.get_or_create(name=name)
                ProductParameter.objects.create(
                    product_info_id=product_info.id,
                    parameter_id=parameter_object.id,
                    value=value
                )

        print('Товары успешно загружены!')
