from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class TestUserCreate:
    def test_returns_201(self, client, db):
        url = reverse('user-list')
        response = client.post(url, {
            'name': 'João Silva',
            'email': 'joao@email.com',
            'password': 'senha1234',
        })
        assert response.status_code == 201

    def test_returns_tokens_on_create(self, client, db):
        url = reverse('user-list')
        response = client.post(url, {
            'name': 'João Silva',
            'email': 'joao@email.com',
            'password': 'senha1234',
        })
        assert 'access' in response.data
        assert 'refresh' in response.data

    def test_password_is_hashed(self, client, db):
        url = reverse('user-list')
        client.post(url, {
            'name': 'João Silva',
            'email': 'joao@email.com',
            'password': 'senha1234',
        })
        user = User.objects.get(email='joao@email.com')
        assert user.password != 'senha1234'

    def test_invalid_name_returns_400(self, client, db):
        url = reverse('user-list')
        response = client.post(url, {
            'name': 'João123',
            'email': 'joao@email.com',
            'password': 'senha1234',
        })
        assert response.status_code == 400

    def test_password_with_spaces_returns_400(self, client, db):
        url = reverse('user-list')
        response = client.post(url, {
            'name': 'João Silva',
            'email': 'joao@email.com',
            'password': 'senha 1234',
        })
        assert response.status_code == 400

    def test_short_password_returns_400(self, client, db):
        url = reverse('user-list')
        response = client.post(url, {
            'name': 'João Silva',
            'email': 'joao@email.com',
            'password': '123',
        })
        assert response.status_code == 400

    def test_duplicate_email_returns_400(self, client, user):
        url = reverse('user-list')
        response = client.post(url, {
            'name': 'João Silva',
            'email': 'joao@email.com',
            'password': 'senha1234',
        })
        assert response.status_code == 400

    def test_does_not_require_authentication(self, client, db):
        url = reverse('user-list')
        response = client.post(url, {
            'name': 'João Silva',
            'email': 'joao@email.com',
            'password': 'senha1234',
        })
        assert response.status_code == 201


class TestUserList:
    def test_returns_200_for_admin(self, admin_client, user):
        url = reverse('user-list')
        response = admin_client.get(url)
        assert response.status_code == 200

    def test_returns_403_for_user(self, auth_client):
        url = reverse('user-list')
        response = auth_client.get(url)
        assert response.status_code == 403

    def test_returns_401_for_unauthenticated(self, client):
        url = reverse('user-list')
        response = client.get(url)
        assert response.status_code == 401

    def test_returns_all_users(self, admin_client, user):
        url = reverse('user-list')
        response = admin_client.get(url)
        assert response.data['count'] == 2  # user + admin


class TestUserRetrieve:
    def test_returns_200_for_admin(self, admin_client, user):
        url = reverse('user-detail', kwargs={'pk': str(user.id)})
        response = admin_client.get(url)
        assert response.status_code == 200

    def test_returns_403_for_user(self, auth_client, user):
        url = reverse('user-detail', kwargs={'pk': str(user.id)})
        response = auth_client.get(url)
        assert response.status_code == 403

    def test_returns_401_for_unauthenticated(self, client, user):
        url = reverse('user-detail', kwargs={'pk': str(user.id)})
        response = client.get(url)
        assert response.status_code == 401


class TestUserMe:
    def test_returns_200(self, auth_client):
        url = reverse('user-me')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_returns_own_data(self, auth_client, user):
        url = reverse('user-me')
        response = auth_client.get(url)
        assert response.data['email'] == user.email
        assert response.data['name'] == user.name

    def test_returns_401_for_unauthenticated(self, client):
        url = reverse('user-me')
        response = client.get(url)
        assert response.status_code == 401

    def test_update_name(self, auth_client):
        url = reverse('user-me')
        response = auth_client.patch(url, {'name': 'Novo Nome'})
        assert response.status_code == 200
        assert response.data['name'] == 'Novo Nome'

    def test_update_password(self, auth_client, user):
        url = reverse('user-me')
        response = auth_client.patch(url, {'password': 'novasenha1234'})
        assert response.status_code == 200
        user.refresh_from_db()
        assert user.check_password('novasenha1234')

    def test_delete_user(self, auth_client, user):
        url = reverse('user-me')
        response = auth_client.delete(url)
        assert response.status_code == 204
        assert not User.objects.filter(id=user.id).exists()

    def test_delete_returns_401_for_unauthenticated(self, client):
        url = reverse('user-me')
        response = client.delete(url)
        assert response.status_code == 401


class TestUserPartialUpdate:
    def test_returns_405_for_admin(self, admin_client, user):
        url = reverse('user-detail', kwargs={'pk': str(user.id)})
        response = admin_client.patch(url, {'name': 'Novo Nome'})
        assert response.status_code == 405

    def test_returns_405_for_user(self, auth_client, user):
        url = reverse('user-detail', kwargs={'pk': str(user.id)})
        response = auth_client.patch(url, {'name': 'Novo Nome'})
        assert response.status_code == 405

    def test_returns_401_for_unauthenticated(self, client, user):
        url = reverse('user-detail', kwargs={'pk': str(user.id)})
        response = client.patch(url, {'name': 'Novo Nome'})
        assert response.status_code == 401


class TestUserDelete:
    def test_returns_405_for_admin(self, admin_client, user):
        url = reverse('user-detail', kwargs={'pk': str(user.id)})
        response = admin_client.delete(url)
        assert response.status_code == 405

    def test_returns_405_for_user(self, auth_client, user):
        url = reverse('user-detail', kwargs={'pk': str(user.id)})
        response = auth_client.delete(url)
        assert response.status_code == 405

    def test_returns_401_for_unauthenticated(self, client, user):
        url = reverse('user-detail', kwargs={'pk': str(user.id)})
        response = client.delete(url)
        assert response.status_code == 401
