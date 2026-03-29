import pytest
import uuid
from django.urls import reverse
from products.models import Product


@pytest.fixture
def product(db):
    return Product.objects.create(name='Cartela de ovos', price='8.50')

@pytest.fixture
def product_list(db):
    Product.objects.bulk_create([
        Product(name='Produto A', price='10.00'),
        Product(name='Produto B', price='20.00'),
        Product(name='Produto C', price='30.00'),
    ])


class TestProductList:
    def test_return_200(self, client, product_list):
        url = reverse('product-list')
        response = client.get(url)
        assert response.status_code == 200

    def test_return_products_list(self, client, product_list):
        url = reverse('product-list')
        response = client.get(url)
        assert response.data['count'] == 3

    def test_return_products_ordered_by_name(self, client, product_list):
        url = reverse('product-list')
        response = client.get(url)
        nomes = [p['name'] for p in response.data['results']]
        assert nomes == sorted(nomes)

    def test_pagination(self, client, db):
        Product.objects.bulk_create([
            Product(name=f'Produto {i}', price='10.00') for i in range(15)
        ])
        url = reverse('product-list')
        response = client.get(url)
        assert len(response.data['results']) == 10
        assert response.data['next'] is not None

    def test_auth_not_required(self, client, product_list):
        url = reverse('product-list')
        response = client.get(url)
        assert response.status_code == 200


class TestProductDetail:
    def test_return_200(self, client, product):
        url = reverse('product-detail', kwargs={'pk': str(product.id)})
        response = client.get(url)
        assert response.status_code == 200

    def test_return_correct_product(self, client, product):
        url = reverse('product-detail', kwargs={'pk': str(product.id)})
        response = client.get(url)
        assert response.data['name'] == 'Cartela de ovos'
        assert response.data['price'] == '8.50'

    def test_invalid_id_return_400(self, client, db):
        url = reverse('product-detail', kwargs={'pk': 'id-invalido'})
        response = client.get(url)
        assert response.status_code == 400

    def test_product_not_found_return_404(self, client, db):
        url = reverse('product-detail', kwargs={'pk': str(uuid.uuid4())})
        response = client.get(url)
        assert response.status_code == 404

    def test_auth_not_required(self, client, product):
        url = reverse('product-detail', kwargs={'pk': str(product.id)})
        response = client.get(url)
        assert response.status_code == 200
