import uuid, pytest
from django.urls import reverse
from news.models import News
from orders.models import Order, OrderItem
from products.models import Product

@pytest.fixture
def product(db):
    return Product.objects.create(name='Cartela de ovos', price='8.50')

@pytest.fixture
def news_list(db):
    News.objects.bulk_create([
        News(title='Notícia A', description='Descrição A'),
        News(title='Notícia B', description='Descrição B'),
        News(title='Notícia C', description='Descrição C'),
    ])


class TestNewsList:
    def test_returns_200(self, client, news_list):
        url = reverse('news-list')
        response = client.get(url)
        assert response.status_code == 200

    def test_returns_correct_count(self, client, news_list):
        url = reverse('news-list')
        response = client.get(url)
        assert response.data['count'] == 3

    def test_does_not_require_authentication(self, client, news_list):
        url = reverse('news-list')
        response = client.get(url)
        assert response.status_code == 200

    def test_ordered_by_most_recent(self, client, news_list):
        url = reverse('news-list')
        response = client.get(url)
        dates = [n['created_at'] for n in response.data['results']]
        assert dates == sorted(dates, reverse=True)


class TestNewsRetrieve:
    def test_returns_200(self, client, news_list):
        news = News.objects.first()
        url = reverse('news-detail', kwargs={'pk': str(news.id)})
        response = client.get(url)
        assert response.status_code == 200

    def test_returns_correct_news(self, client, news_list):
        news = News.objects.first()
        url = reverse('news-detail', kwargs={'pk': str(news.id)})
        response = client.get(url)
        assert response.data['title'] == news.title

    def test_invalid_id_returns_400(self, client, db):
        url = reverse('news-detail', kwargs={'pk': 'id-invalido'})
        response = client.get(url)
        assert response.status_code == 400

    def test_not_found_returns_404(self, client, db):
        url = reverse('news-detail', kwargs={'pk': str(uuid.uuid4())})
        response = client.get(url)
        assert response.status_code == 404

    def test_does_not_require_authentication(self, client, news_list):
        news = News.objects.first()
        url = reverse('news-detail', kwargs={'pk': str(news.id)})
        response = client.get(url)
        assert response.status_code == 200


class TestNewsSignals:
    def test_creates_news_on_order_create(self, auth_client, product, db):
        url = reverse('order-list')
        auth_client.post(url, {
            'items': [{'product': str(product.id), 'quantity': 1}]
        }, format='json')
        assert News.objects.filter(title='Novo pedido criado').exists()

    def test_creates_news_on_order_status_update(self, admin_client, user, product, db):
        order = Order.objects.create(user=user)
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=1,
            unit_price=product.price,
        )
        url = reverse('order-update-status', kwargs={'pk': str(order.id)})
        admin_client.patch(url, {'status': 'completed'}, format='json')
        assert News.objects.filter(title='Status de pedido atualizado').exists()

    def test_creates_news_on_order_delete(self, auth_client, user, product, db):
        order = Order.objects.create(user=user)
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=1,
            unit_price=product.price,
        )
        url = reverse('order-detail', kwargs={'pk': str(order.id)})
        auth_client.delete(url)
        assert News.objects.filter(title='Pedido cancelado').exists()
