# 🛒 GTi Pedidos - Django REST API

API RESTful desenvolvida com Django e Django REST Framework, com autenticação JWT, painel administrativo customizado e deploy automatizado via CI/CD.

🌐 **Deploy:** https://pedidos-gti.onrender.com

📄 **Documentação:** https://documenter.getpostman.com/view/45024278/2sBXinFpa2

---

## 🚀 Tecnologias

- **Python** + **Django**
- **Django REST Framework** — API REST
- **Simple JWT** — autenticação por tokens
- **PostgreSQL** — banco de dados
- **django-unfold** — painel admin customizado
- **pytest** + **pytest-cov** — testes e cobertura
- **GitHub Actions** — CI/CD
- **Render** — deploy

---

## 📁 Estrutura do Projeto

```
pedidos-gti/
├── core/           # configurações, urls e exceções globais
├── users/          # autenticação e gerenciamento de usuários
├── products/       # catálogo de produtos
├── orders/         # pedidos e itens de pedido
├── business/       # dados da empresa
├── news/           # notícias geradas automaticamente por signals
├── conftest.py     # fixtures globais de testes
├── pytest.ini      # configuração do pytest
├── build.sh        # script de build para produção
└── requirements.txt
```

---

## ⚙️ Configuração Local

### 1. Clone o repositório

```bash
git clone https://github.com/kauaregisdev/pedidos-gti.git
cd pedidos-gti
```

### 2. Crie e ative o ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure o `.env`

```env
SECRET_KEY=sua-chave-secreta
DEBUG=True
DATABASE_URL=postgres://usuario:senha@localhost:5432/nome_do_banco
ALLOWED_HOSTS=localhost
```

### 5. Rode as migrations e crie o superusuário

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 6. Inicie o servidor

```bash
python manage.py runserver
```

---

## 🔐 Autenticação

A API utiliza autenticação JWT via `djangorestframework-simplejwt`.

| Método | Rota | Descrição |
|---|---|---|
| `POST` | `/api/token/` | Login — retorna `access` e `refresh` |
| `POST` | `/api/token/refresh/` | Renova o `access` token |

**Exemplo de login:**
```json
POST /api/token/
{
    "email": "user@email.com",
    "password": "senha1234"
}
```

---

## 📌 Endpoints

### Usuários `/api/users/`

| Método | Rota | Permissão | Descrição |
|---|---|---|---|
| `POST` | `/api/users/` | Público | Cria usuário e retorna tokens |
| `GET` | `/api/users/` | Admin | Lista todos os usuários |
| `GET` | `/api/users/<uuid>/` | Admin | Detalha um usuário |
| `GET` | `/api/users/me/` | Autenticado | Retorna dados do próprio usuário |
| `PATCH` | `/api/users/me/` | Autenticado | Atualiza dados do próprio usuário |
| `DELETE` | `/api/users/me/` | Autenticado | Deleta o próprio usuário |

### Produtos `/api/products/`

| Método | Rota | Permissão | Descrição |
|---|---|---|---|
| `GET` | `/api/products/` | Público | Lista produtos com paginação |
| `GET` | `/api/products/<uuid>/` | Público | Detalha um produto |

### Pedidos `/api/orders/`

| Método | Rota | Permissão | Descrição |
|---|---|---|---|
| `GET` | `/api/orders/` | Autenticado | Lista pedidos do usuário (admin vê todos) |
| `POST` | `/api/orders/` | Autenticado | Cria um pedido |
| `GET` | `/api/orders/<uuid>/` | Autenticado | Detalha um pedido (admin pode detalhar qualquer pedido) |
| `PATCH` | `/api/orders/<uuid>/status/` | Admin | Atualiza status do pedido |
| `DELETE` | `/api/orders/<uuid>/` | Autenticado | Exclui um pedido pendente (admin pode deletar qualquer pedido pendente) |

### Empresa `/api/business/`

| Método | Rota | Permissão | Descrição |
|---|---|---|---|
| `GET` | `/api/business/` | Público | Dados da empresa e pedidos concluídos |

### Notícias `/api/news/`

| Método | Rota | Permissão | Descrição |
|---|---|---|---|
| `GET` | `/api/news/` | Público | Lista notícias com paginação |
| `GET` | `/api/news/<id>/` | Público | Detalha uma notícia |

---

## 🔔 Notícias Automáticas

Notícias são geradas automaticamente via **Django Signals** nos seguintes eventos:

| Evento | Notícia gerada |
|---|---|
| Criação de pedido | `"Novo pedido criado"` |
| Atualização de status | `"Status de pedido atualizado"` |
| Exclusão de pedido | `"Pedido cancelado"` |

---

## 🧪 Testes

```bash
# rodar todos os testes
pytest

# rodar testes de um app específico
pytest products/tests.py
pytest users/tests.py
pytest orders/tests.py
pytest business/tests.py
pytest news/tests.py
```

A cobertura de testes é exibida automaticamente no terminal via configuração do `pytest.ini`.

---

## 🚢 Deploy

O deploy é realizado na plataforma **Render** com PostgreSQL gerenciado.

### Variáveis de ambiente em produção

| Variável | Descrição |
|---|---|
| `SECRET_KEY` | Chave secreta do Django |
| `DEBUG` | `False` em produção |
| `DATABASE_URL` | URL do banco PostgreSQL |
| `ALLOWED_HOSTS` | Host do app no Render |
| `DJANGO_SUPERUSER_NAME` | Nome do superusuário |
| `DJANGO_SUPERUSER_EMAIL` | Email do superusuário |
| `DJANGO_SUPERUSER_PASSWORD` | Senha do superusuário |

### Build

O arquivo `build.sh` é executado automaticamente pelo Render a cada deploy:

```bash
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate
# criação do superusuário (apenas na primeira vez)
```

---

## 🔄 CI/CD

O pipeline de CI/CD é gerenciado pelo **GitHub Actions**:

| Evento | Branch | Testes | Deploy |
|---|---|---|---|
| push | `master` | ✅ | ✅ |
| push | `dev` | ✅ | ❌ |
| pull request | `master` | ✅ | ❌ |
| pull request | `dev` | ✅ | ❌ |

O deploy só é disparado após todos os testes passarem em pushes na branch `master`.

---

## 🖥️ Painel Administrativo

O painel admin utiliza o tema **django-unfold** e está disponível em `/admin/`.

| Model | Visualizar | Adicionar | Editar | Deletar |
|---|---|---|---|---|
| `Product` | ✅ | ✅ | ✅ | ✅ |
| `Order` | ✅ | ❌ | Só status | ❌ |
| `OrderItem` | ✅ | ❌ | ❌ | ❌ |
| `User` | ✅ | ❌ | ❌ | ❌ |
| `Business` | ✅ | Só 1 | ✅ | ✅ |
| `News` | ✅ | ❌ | ❌ | ❌ |
