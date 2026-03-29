import pytest
from django.urls import reverse
from orders.models import Order, OrderItem
from products.models import Product

@pytest.fixture
def product(db):
    return Product.objects.create(name='Cartela de ovos', price='8.50')

@pytest.fixture
def order(db, user, product):
    order = Order.objects.create(user=user)
    OrderItem.objects.create(
        order=order,
        product=product,
        quantity=2,
        unit_price=product.price,
    )
    order.calculate_total()
    return order

@pytest.fixture
def completed_order(db, user, product):
    order = Order.objects.create(user=user, status=Order.Status.COMPLETED)
    OrderItem.objects.create(
        order=order,
        product=product,
        quantity=1,
        unit_price=product.price,
    )
    order.calculate_total()
    return order


class TestOrderList:
    def test_returns_200(self, auth_client, order):
        url = reverse('order-list')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_user_sees_only_own_orders(self, auth_client, order, admin):
        Order.objects.create(user=admin)
        url = reverse('order-list')
        response = auth_client.get(url)
        assert response.data['count'] == 1

    def test_admin_sees_all_orders(self, admin_client, order, admin):
        Order.objects.create(user=admin)
        url = reverse('order-list')
        response = admin_client.get(url)
        assert response.data['count'] == 2

    def test_returns_401_for_unauthenticated(self, client):
        url = reverse('order-list')
        response = client.get(url)
        assert response.status_code == 401


class TestOrderRetrieve:
    def test_returns_200(self, auth_client, order):
        url = reverse('order-detail', kwargs={'pk': str(order.id)})
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_returns_correct_order(self, auth_client, order):
        url = reverse('order-detail', kwargs={'pk': str(order.id)})
        response = auth_client.get(url)
        assert str(order.id) == response.data['id']

    def test_user_cannot_access_other_user_order(self, auth_client, admin, completed_order):
        other_order = Order.objects.create(user=admin)
        url = reverse('order-detail', kwargs={'pk': str(other_order.id)})
        response = auth_client.get(url)
        assert response.status_code == 404

    def test_admin_can_access_any_order(self, admin_client, order):
        url = reverse('order-detail', kwargs={'pk': str(order.id)})
        response = admin_client.get(url)
        assert response.status_code == 200

    def test_returns_401_for_unauthenticated(self, client, order):
        url = reverse('order-detail', kwargs={'pk': str(order.id)})
        response = client.get(url)
        assert response.status_code == 401


class TestOrderCreate:
    def test_returns_201(self, auth_client, product):
        url = reverse('order-list')
        response = auth_client.post(url, {
            'items': [{'product': str(product.id), 'quantity': 2}]
        }, format='json')
        assert response.status_code == 201

    def test_calculates_total_correctly(self, auth_client, product):
        url = reverse('order-list')
        response = auth_client.post(url, {
            'items': [{'product': str(product.id), 'quantity': 2}]
        }, format='json')
        assert response.data['total'] == '17.00'

    def test_empty_items_returns_400(self, auth_client):
        url = reverse('order-list')
        response = auth_client.post(url, {'items': []}, format='json')
        assert response.status_code == 400

    def test_returns_401_for_unauthenticated(self, client, product):
        url = reverse('order-list')
        response = client.post(url, {
            'items': [{'product': str(product.id), 'quantity': 1}]
        }, format='json')
        assert response.status_code == 401


class TestOrderUpdateStatus:
    def test_returns_200_for_admin(self, admin_client, order):
        url = reverse('order-update-status', kwargs={'pk': str(order.id)})
        response = admin_client.patch(url, {'status': 'completed'}, format='json')
        assert response.status_code == 200

    def test_updates_status_correctly(self, admin_client, order):
        url = reverse('order-update-status', kwargs={'pk': str(order.id)})
        admin_client.patch(url, {'status': 'completed'}, format='json')
        order.refresh_from_db()
        assert order.status == Order.Status.COMPLETED

    def test_updates_updated_at(self, admin_client, order):
        previous_updated_at = order.updated_at
        url = reverse('order-update-status', kwargs={'pk': str(order.id)})
        admin_client.patch(url, {'status': 'completed'}, format='json')
        order.refresh_from_db()
        assert order.updated_at > previous_updated_at

    def test_returns_403_for_user(self, auth_client, order):
        url = reverse('order-update-status', kwargs={'pk': str(order.id)})
        response = auth_client.patch(url, {'status': 'completed'}, format='json')
        assert response.status_code == 403

    def test_returns_401_for_unauthenticated(self, client, order):
        url = reverse('order-update-status', kwargs={'pk': str(order.id)})
        response = client.patch(url, {'status': 'completed'}, format='json')
        assert response.status_code == 401


class TestOrderDelete:
    def test_returns_204(self, auth_client, order):
        url = reverse('order-detail', kwargs={'pk': str(order.id)})
        response = auth_client.delete(url)
        assert response.status_code == 204

    def test_completed_order_cannot_be_deleted(self, auth_client, completed_order):
        url = reverse('order-detail', kwargs={'pk': str(completed_order.id)})
        response = auth_client.delete(url)
        assert response.status_code == 403

    def test_user_cannot_delete_other_user_order(self, auth_client, admin, product):
        other_order = Order.objects.create(user=admin)
        url = reverse('order-detail', kwargs={'pk': str(other_order.id)})
        response = auth_client.delete(url)
        assert response.status_code == 404

    def test_returns_401_for_unauthenticated(self, client, order):
        url = reverse('order-detail', kwargs={'pk': str(order.id)})
        response = client.delete(url)
        assert response.status_code == 401
