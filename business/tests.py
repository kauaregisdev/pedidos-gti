import pytest
from django.urls import reverse
from business.models import Business

@pytest.fixture
def business(db):
    return Business.objects.create(
        name='Minha Empresa',
        description='Descrição da empresa.',
        email='contato@empresa.com',
        phone='+55 85 99999-9999',
        founded_at='2020-01-01',
    )


class TestBusiness:
    def test_returns_200(self, client, business):
        url = reverse('business')
        response = client.get(url)
        assert response.status_code == 200

    def test_returns_correct_data(self, client, business):
        url = reverse('business')
        response = client.get(url)
        assert response.data['name'] == 'Minha Empresa'
        assert response.data['email'] == 'contato@empresa.com'

    def test_returns_404_when_no_business(self, client, db):
        url = reverse('business')
        response = client.get(url)
        assert response.status_code == 404

    def test_does_not_require_authentication(self, client, business):
        url = reverse('business')
        response = client.get(url)
        assert response.status_code == 200

    def test_completed_orders_are_empty(self, client, business):
        url = reverse('business')
        response = client.get(url)
        assert response.data['completed_orders']['results'] == []

    def test_invalid_page_returns_empty_results(self, client, business):
        url = reverse('business')
        response = client.get(url, {'page': 999})
        assert response.status_code == 200
        assert response.data['completed_orders']['results'] == []
