# Salon Management System

Sistema de gestão para salão de beleza, com área pública para clientes agendarem
serviços e uma área administrativa para gerenciar serviços, horários de
funcionamento, clientes e agendamentos.

O projeto é dividido em dois módulos principais — **backend** (API REST) e
**frontend** (SPA) — orquestrados via Docker Compose junto a um banco MySQL e ao
phpMyAdmin.

## Tecnologias

### Backend (`/backend`)
- **Python 3.11+** com **FastAPI** — framework web para a API REST
- **Uvicorn** — servidor ASGI
- **Tortoise ORM** — ORM assíncrono
- **asyncmy** — driver assíncrono para MySQL
- **Pydantic / pydantic-settings** — validação de dados e configurações via `.env`
- **PyJWT** + **passlib[bcrypt]** — autenticação JWT e hash de senhas
- **Poetry** — gerenciamento de dependências

Arquitetura em módulos (`auth`, `services`, `business_hours`, `appointments`,
`customers`), cada um com controller, service e repository.

### Frontend (`/frontend`)
- **Vue 3** (Composition API) com **Vite** — build e dev server
- **Vue Router** — roteamento SPA
- **Pinia** — gerenciamento de estado
- **Axios** — cliente HTTP
- **ESLint + Prettier** — lint e formatação

### Infraestrutura
- **Docker / Docker Compose** — orquestração dos serviços
- **MySQL 8.4** — banco de dados
- **phpMyAdmin 5.2** — administração visual do banco

## Estrutura do projeto

```
salon-management-system/
├── docker-compose.yml
├── .env.example          # variáveis do banco (serviço db)
├── backend/
│   ├── .env.example      # variáveis da API
│   ├── Dockerfile
│   └── app/
└── frontend/
    ├── .env.example      # variáveis do frontend
    ├── Dockerfile
    └── src/
```

## Como rodar o projeto

### Pré-requisitos
- [Docker](https://docs.docker.com/get-docker/) e Docker Compose

### 1. Clonar o repositório

```bash
git clone https://github.com/AlmirRogerio/salon-management-system.git
cd salon-management-system
```

### 2. Configurar as variáveis de ambiente

Cada módulo tem o seu próprio `.env`, e o Docker Compose carrega o arquivo de
cada projeto via `env_file`. Copie os arquivos de exemplo e ajuste os valores
conforme necessário:

**Linux / macOS:**
```bash
cp .env.example .env
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

**Windows (PowerShell):**
```powershell
Copy-Item .env.example .env
Copy-Item backend/.env.example backend/.env
Copy-Item frontend/.env.example frontend/.env
```

O que cada arquivo controla:

| Arquivo             | Serviço      | Conteúdo                                                              |
| ------------------- | ------------ | -------------------------------------------------------------------- |
| `./.env`            | `db` (MySQL) | Nome do banco, usuário, senha e senha de root                        |
| `./backend/.env`    | `api`        | Config da app, `DATABASE_URL`, JWT e credenciais do admin do seed    |
| `./frontend/.env`   | `web`        | `VITE_API_BASE_URL` (URL base da API)                                |

> **Importante:** as credenciais em `backend/.env` (`DATABASE_URL`) precisam
> ser consistentes com as definidas em `./.env` (`MYSQL_USER` / `MYSQL_PASSWORD`
> / `MYSQL_DATABASE`). Se alterar o usuário ou a senha do banco, atualize a
> `DATABASE_URL` também.

### 3. Subir os containers

```bash
docker compose up -d --build
```

Na primeira execução, a API roda os *seeds* (usuário admin, serviços e horários
de funcionamento) antes de iniciar o servidor.

### 4. Acessar os serviços

| Serviço            | URL                              |
| ------------------ | -------------------------------- |
| Frontend (SPA)     | http://localhost:5173            |
| API (FastAPI)      | http://localhost:8000            |
| Docs da API (Swagger) | http://localhost:8000/docs    |
| Health check       | http://localhost:8000/health     |
| phpMyAdmin         | http://localhost:8080            |

### Credenciais padrão do admin

Definidas em `backend/.env` (valores de exemplo):

- **E-mail:** `leila@salao.com`
- **Senha:** `leila12345`
