# MANUAL CANÔNICO DO BACKEND - HB TRACKING

**Versão:** 1.0
**Projeto:** HB Tracking - Sistema de Gestão de Handebol
**Stack:** FastAPI + PostgreSQL (Neon) + Alembic + SQLAlchemy
**Regras:** [regras-sistema-v1.1_Version2.md](regras-sistema-v1.1_Version2.md)

---

## 📚 SUMÁRIO

- [Introdução](#introdução)
- [Pré-requisitos](#pré-requisitos)
- [Arquitetura do Sistema](#arquitetura-do-sistema)
- [FASE 0 - Preparação do Ambiente](#fase-0---preparação-do-ambiente)
- [FASE 1 - Infraestrutura de Banco de Dados](#fase-1---infraestrutura-de-banco-de-dados)
- [FASE 2 - Núcleo do Backend](#fase-2---núcleo-do-backend)
- [FASE 3 - Contrato da API](#fase-3---contrato-da-api)
- [FASE 4 - FastAPI Mínimo](#fase-4---fastapi-mínimo)
- [FASE 5 - CRUDs por Recurso](#fase-5---cruds-por-recurso)
- [FASE 6 - Endurecimento e Segurança](#fase-6---endurecimento-e-segurança)
- [FASE 7 - Preparação para Produção](#fase-7---preparação-para-produção)
- [FASE 8 - Validação Production-Ready](#fase-8---validação-production-ready)
- [Apêndices](#apêndices)

---

## 🎯 INTRODUÇÃO

### Objetivo do Manual

Este manual é o **guia canônico oficial** para desenvolvimento do backend do HB Tracking. Cada fase contém:

- ✅ **Configurações detalhadas** com comandos exatos
- ✅ **Implementações** seguindo as regras RDB, R, RF, RD, RP
- ✅ **Testes obrigatórios** com exemplos de código
- ✅ **Seeds e fixtures** para cada entidade
- ✅ **Checklist de validação** (Definition of Done)
- ✅ **Troubleshooting** para problemas comuns

### Princípios de Desenvolvimento

1. **Conformidade Total com RAG**: Toda implementação deve referenciar regras específicas
2. **Zero Retrabalho**: Seguir o manual elimina necessidade de refatoração
3. **Testes Obrigatórios**: Nenhuma funcionalidade é considerada pronta sem testes
4. **Auditoria por Padrão**: Ações críticas sempre geram logs (R31, R32, RDB5)
5. **Soft Delete Sempre**: Exclusão física bloqueada por triggers (R29, RDB4)

### Estrutura de Pastas Final

```
Hb Traking - neon database/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                    # FastAPI app
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── config.py              # Configurações (BaseSettings)
│   │   │   ├── database.py            # Engine, SessionLocal, get_db
│   │   │   ├── context.py             # Contexto de execução (R6, R33)
│   │   │   ├── security.py            # JWT, autenticação
│   │   │   └── logging.py             # Logging estruturado
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── base.py                # Base declarativa
│   │   │   ├── person.py              # R1
│   │   │   ├── user.py                # R2, R3
│   │   │   ├── organization.py        # R34
│   │   │   ├── role.py                # R4
│   │   │   ├── membership.py          # R6, R7, RDB9
│   │   │   ├── season.py              # R8, RF5, RDB8
│   │   │   ├── category.py            # R15, RDB11
│   │   │   ├── team.py                # RF6
│   │   │   ├── team_registration.py   # R17, RDB10
│   │   │   ├── athlete.py             # R12, R13, R14
│   │   │   ├── athlete_state.py       # R13 histórico
│   │   │   ├── training_session.py    # R18
│   │   │   ├── match.py               # R19, RDB13
│   │   │   ├── match_event.py         # RD, estatísticas
│   │   │   └── audit_log.py           # R35, RDB5
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── error.py               # ErrorResponse padrão
│   │   │   ├── person.py
│   │   │   ├── user.py
│   │   │   ├── membership.py
│   │   │   └── ...
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── person_service.py
│   │   │   ├── user_service.py
│   │   │   ├── membership_service.py
│   │   │   └── ...
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── v1/
│   │   │       ├── __init__.py
│   │   │       ├── deps/
│   │   │       │   ├── __init__.py
│   │   │       │   ├── database.py    # get_db dependency
│   │   │       │   ├── auth.py        # get_current_user
│   │   │       │   └── permissions.py # check_permissions
│   │   │       └── routers/
│   │   │           ├── __init__.py
│   │   │           ├── health.py
│   │   │           ├── persons.py
│   │   │           ├── users.py
│   │   │           ├── memberships.py
│   │   │           └── ...
│   │   └── tests/
│   │       ├── __init__.py
│   │       ├── conftest.py            # Fixtures globais
│   │       ├── unit/
│   │       │   ├── services/
│   │       │   └── schemas/
│   │       └── integration/
│   │           ├── test_RDB9_membership_exclusivity.py
│   │           ├── test_RDB10_team_registrations.py
│   │           ├── test_R13_athlete_state_dispense.py
│   │           └── ...
│   ├── db_migrations/
│   │   ├── alembic/
│   │   │   ├── env.py
│   │   │   └── versions/
│   │   │       └── *.py               # 33+ migrations
│   │   ├── alembic.ini
│   │   └── seeds/
│   │       ├── 001_seed_roles.py
│   │       ├── 002_seed_superadmin.py
│   │       ├── 003_seed_categories.py
│   │       └── ...
│   ├── .env
│   ├── .env.example
│   ├── requirements.txt
│   └── pytest.ini
├── docs/
│   ├── regras-sistema-v1.1_Version2.md
│   ├── MANUAL_BACKEND_CANONICO.md     # Este arquivo
│   └── API_CONTRACT.md                # Gerado na Fase 3
├── .gitignore
└── README.md
```

---

## 🔧 PRÉ-REQUISITOS

### Software Obrigatório

| Software | Versão Mínima | Comando de Verificação |
|----------|---------------|------------------------|
| **Python** | 3.11+ | `python --version` |
| **pip** | 23.0+ | `pip --version` |
| **Git** | 2.30+ | `git --version` |
| **PostgreSQL Client** | 15+ | `psql --version` |
| **VS Code** | Última | `code --version` |

### Extensões do VS Code Recomendadas

```json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.vscode-pylance",
    "ms-python.black-formatter",
    "charliermarsh.ruff",
    "GitHub.copilot",
    "mtxr.sqltools",
    "mtxr.sqltools-driver-pg"
  ]
}
```

### Conta Neon Database

1. Criar conta em https://neon.tech
2. Criar projeto "hb-tracking"
3. Copiar `DATABASE_URL` com formato:
   ```
   postgresql://USER:PASSWORD@HOST/DATABASE?sslmode=require
   ```

---

## 🏗️ ARQUITETURA DO SISTEMA

### Camadas de Enforcement (Seção 7 do RAG)

```
┌─────────────────────────────────────────────────────┐
│  7.1 - Apenas no DB                                 │
│  └─ Triggers, Constraints, Índices                  │
│     Regras: R4, R20, R29, R35, RDB1-RDB14           │
└─────────────────────────────────────────────────────┘
              ↓ valida ↓
┌─────────────────────────────────────────────────────┐
│  7.2 - DB + Backend                                 │
│  └─ Validações de negócio em Services              │
│     Regras: R1-R3, R5-R8, R11-R13, R15-R17, etc.   │
└─────────────────────────────────────────────────────┘
              ↓ expõe via ↓
┌─────────────────────────────────────────────────────┐
│  7.3 - Apenas Backend                               │
│  └─ Lógica de cálculo, derivação, agregação        │
│     Regras: R10, R21, R22, R26, R27, R36, RD1-RD91 │
└─────────────────────────────────────────────────────┘
              ↓ serve ↓
┌─────────────────────────────────────────────────────┐
│  7.4 - Backend + Frontend                           │
│  └─ APIs REST, validação de entrada, UI/UX         │
│     Regras: R9, R14, R18, RF1-RF31, RP1-RP20        │
└─────────────────────────────────────────────────────┘
```

### Fluxo de Dados

```
Cliente (Frontend)
    ↓ HTTP Request
FastAPI Router (api/v1/routers/)
    ↓ Depends(get_db, get_current_user)
Service Layer (services/)
    ↓ Validações de negócio (R, RF, RD, RP)
SQLAlchemy Models (models/)
    ↓ ORM
PostgreSQL + Triggers (RDB)
    ↓ Auditoria
audit_logs (imutável)
```

---

## 📦 FASE 0 - PREPARAÇÃO DO AMBIENTE

**Status:** ✅ Cumprida (referência)
**Duração Estimada:** 30 minutos
**Objetivo:** Configurar ambiente local para desenvolvimento

### 0.1 - Criar e Ativar Ambiente Virtual

**Windows:**
```powershell
cd "c:\Users\davis\OneDrive\Área de Trabalho\SISTEMA HANDEBOL\Hb Traking - neon database"
python -m venv .venv
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
cd ~/hb-tracking
python3 -m venv .venv
source .venv/bin/activate
```

**Validação:**
```bash
which python  # Deve apontar para .venv/bin/python ou .venv\Scripts\python.exe
```

### 0.2 - Instalar Dependências Base

**Criar `requirements.txt`:**
```txt
# Core
fastapi==0.109.0
uvicorn[standard]==0.27.0
python-dotenv==1.0.0
pydantic==2.5.3
pydantic-settings==2.1.0

# Database
sqlalchemy==2.0.25
alembic==1.13.1
psycopg2-binary==2.9.9

# Security
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6

# Testing
pytest==7.4.4
pytest-cov==4.1.0
pytest-asyncio==0.23.3
httpx==0.26.0

# Dev Tools
ruff==0.1.14
black==24.1.1
isort==5.13.2
```

**Instalar:**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 0.3 - Configurar Variáveis de Ambiente

**Criar `.env`:**
```bash
# Environment
ENV=local

# Database (Neon)
DATABASE_URL=postgresql://neondb_owner:npg_Dn0WbLMkO7Zo@ep-plain-voice-a4omihun.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require

# Security (gerar com: openssl rand -hex 32)
JWT_SECRET=your-secret-key-here-change-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRES_MINUTES=30

# API
API_VERSION=v1
API_TITLE=HB Tracking API
API_DESCRIPTION=Sistema de Gestão de Handebol

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# Logging
LOG_LEVEL=INFO
```

**Criar `.env.example`:**
```bash
cp .env .env.example
# Editar .env.example e remover valores sensíveis
```

### 0.4 - Configurar .gitignore

**Criar/Atualizar `.gitignore`:**
```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
.venv/
venv/
ENV/
env/

# IDEs
.vscode/
.idea/
*.swp
*.swo

# Environment
.env
.env.local
.env.*.local

# Alembic
review.sql
review_*.sql

# Testing
.coverage
htmlcov/
.pytest_cache/
.tox/

# OS
.DS_Store
Thumbs.db
```

### 0.5 - Configurar pytest

**Criar `pytest.ini`:**
```ini
[pytest]
testpaths = backend/app/tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
    -v
    --strict-markers
    --tb=short
    --cov=backend/app
    --cov-report=html
    --cov-report=term-missing:skip-covered
markers =
    unit: Unit tests
    integration: Integration tests with database
    slow: Slow running tests
    rdb: Tests for RDB rules (database)
    r: Tests for R rules (structural)
    rf: Tests for RF rules (operational)
    rd: Tests for RD rules (sports domain)
    rp: Tests for RP rules (participation)
```

### ✅ CHECKLIST FASE 0

- [x] Ambiente virtual criado e ativado
- [x] `requirements.txt` instalado sem erros
- [x] `.env` configurado com DATABASE_URL válido
- [x] `.env.example` criado (sem secrets)
- [x] `.gitignore` configurado
- [x] `pytest.ini` criado
- [x] Conexão com Neon testada: `psql $DATABASE_URL -c "SELECT version();"`

---

## 🗄️ FASE 1 - INFRAESTRUTURA DE BANCO DE DADOS

**Status:** ✅ Cumprida (com melhorias aplicadas)
**Duração Estimada:** 1 hora
**Objetivo:** Validar e aplicar migrations no banco Neon

### 1.1 - Diagnóstico Não-Destrutivo

**Executar comandos de diagnóstico:**
```bash
cd backend/db_migrations

# 1. Verificar HEAD do repositório
alembic heads
# Saída esperada: 4af09f9d46a0 (add_season_status_view_and_trigger_docs)

# 2. Verificar revisão atual do banco
alembic current
# Saída esperada: 3e2898989f01 ou d021c0ffee21

# 3. Listar últimas 5 migrations
ls -lt alembic/versions/*.py | head -5  # Linux/Mac
# ou
Get-ChildItem alembic/versions/*.py | Sort-Object LastWriteTime -Descending | Select-Object -First 5  # Windows
```

### 1.2 - Gerar Dry-Run para Revisão

**Gerar SQL sem aplicar:**
```bash
# Windows (usar script batch)
../../generate_review.bat

# Linux/Mac
export DATABASE_URL="postgresql://..." && \
alembic upgrade head --sql > ../../review_with_improvements.sql
```

**Revisar arquivo gerado:**
```bash
# Verificar tamanho (deve ter ~111KB)
ls -lh ../../review_with_improvements.sql

# Revisar primeiras linhas
head -100 ../../review_with_improvements.sql

# Procurar por VIEW criada
grep -A 30 "v_seasons_with_status" ../../review_with_improvements.sql

# Procurar por COMMENT ON FUNCTION
grep "COMMENT ON FUNCTION" ../../review_with_improvements.sql | wc -l
# Saída esperada: 16
```

### 1.3 - Aplicar Migrations

⚠️ **ATENÇÃO:** Este comando **altera o banco de produção**!

```bash
# Backup manual antes de aplicar (recomendado)
# Via Neon Console: Project > Backups > Create Snapshot

# Aplicar migrations
alembic upgrade head

# Validar aplicação
alembic current
# Saída esperada: 4af09f9d46a0 (head)
```

### 1.4 - Validar Estrutura Criada

**Conectar ao banco:**
```bash
psql $DATABASE_URL
```

**Executar validações SQL:**
```sql
-- 1. Verificar tabelas principais
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
  AND table_type = 'BASE TABLE'
ORDER BY table_name;
-- Espera-se: ~25 tabelas

-- 2. Validar VIEW v_seasons_with_status
\d+ v_seasons_with_status
-- Deve mostrar: todas colunas de seasons + status_derivado + flags booleanos

-- 3. Verificar triggers documentados
SELECT p.proname,
       pg_catalog.obj_description(p.oid, 'pg_proc') as documentation
FROM pg_proc p
JOIN pg_namespace n ON p.pronamespace = n.oid
WHERE n.nspname = 'public'
  AND pg_catalog.obj_description(p.oid, 'pg_proc') IS NOT NULL
ORDER BY p.proname;
-- Espera-se: 16 funções com documentação

-- 4. Validar RDB10 (team_registrations)
\d+ team_registrations
-- Deve ter: start_at (NOT NULL), end_at, EXCLUDE constraint

-- 5. Validar auditoria imutável (RDB5)
SELECT tgname, tgtype, tgenabled
FROM pg_trigger
WHERE tgrelid = 'audit_logs'::regclass;
-- Deve ter: trg_audit_logs_immutable (BEFORE UPDATE OR DELETE)

-- 6. Validar super admin único (R3, RDB6)
SELECT indexname, indexdef
FROM pg_indexes
WHERE tablename = 'users'
  AND indexname = 'idx_users_superadmin_unique';
-- Deve retornar: índice parcial único em is_superadmin

-- 7. Sair
\q
```

### 1.5 - Seeds Iniciais

**Criar estrutura de seeds:**
```bash
mkdir -p backend/db_migrations/seeds
```

**Seed 1: Roles (R4)**

**Arquivo:** `backend/db_migrations/seeds/001_seed_roles.py`
```python
"""
Seed: Papéis do sistema (R4)
Regras: dirigente, coordenador, treinador, atleta
"""
from sqlalchemy import text
from sqlalchemy.orm import Session
from backend.app.core.database import engine

def seed_roles():
    with Session(engine) as session:
        # Verificar se já existem roles
        result = session.execute(text("SELECT COUNT(*) FROM roles"))
        if result.scalar() > 0:
            print("❌ Roles já existem. Pulando seed.")
            return

        # Inserir roles (R4)
        session.execute(text("""
            INSERT INTO roles (code, name) VALUES
            ('dirigente', 'Dirigente'),
            ('coordenador', 'Coordenador'),
            ('treinador', 'Treinador'),
            ('atleta', 'Atleta')
            ON CONFLICT (code) DO NOTHING;
        """))
        session.commit()
        print("✅ Roles criados com sucesso!")

if __name__ == "__main__":
    seed_roles()
```

**Executar:**
```bash
python backend/db_migrations/seeds/001_seed_roles.py
```

**Seed 2: Super Administrador (R3, RDB6)**

**Arquivo:** `backend/db_migrations/seeds/002_seed_superadmin.py`
```python
"""
Seed: Super Administrador único (R3, RDB6)
Seed inicial deve criar EXATAMENTE 1 superadmin
"""
from sqlalchemy import text
from sqlalchemy.orm import Session
from backend.app.core.database import engine
import uuid

def seed_superadmin():
    with Session(engine) as session:
        # Verificar se já existe superadmin (RDB6)
        result = session.execute(text(
            "SELECT COUNT(*) FROM users WHERE is_superadmin = true"
        ))
        if result.scalar() > 0:
            print("❌ Super Admin já existe. Pulando seed.")
            return

        # Criar pessoa
        person_id = uuid.uuid4()
        session.execute(text("""
            INSERT INTO persons (id, full_name, birth_date)
            VALUES (:id, 'Super Administrador', NULL)
        """), {"id": person_id})

        # Criar usuário superadmin
        session.execute(text("""
            INSERT INTO users (person_id, email, full_name, is_superadmin, status)
            VALUES (:person_id, 'admin@hbtracking.com', 'Super Administrador', true, 'ativo')
        """), {"person_id": person_id})

        # Criar organização (R34 - clube único na V1)
        org_id = uuid.uuid4()
        session.execute(text("""
            INSERT INTO organizations (id, name, owner_user_id, status)
            SELECT :org_id, 'Clube HB Tracking', id, 'ativo'
            FROM users WHERE is_superadmin = true
        """), {"org_id": org_id})

        session.commit()
        print("✅ Super Administrador criado!")
        print(f"   Email: admin@hbtracking.com")
        print(f"   Person ID: {person_id}")

if __name__ == "__main__":
    seed_superadmin()
```

**Executar:**
```bash
python backend/db_migrations/seeds/002_seed_superadmin.py
```

**Seed 3: Categorias Globais (R15, RDB11)**

**Arquivo:** `backend/db_migrations/seeds/003_seed_categories.py`
```python
"""
Seed: Categorias globais de handebol (R15, RDB11)
Categorias definidas exclusivamente por idade
"""
from sqlalchemy import text
from sqlalchemy.orm import Session
from backend.app.core.database import engine

def seed_categories():
    with Session(engine) as session:
        # Verificar se já existem categorias
        result = session.execute(text("SELECT COUNT(*) FROM categories"))
        if result.scalar() > 0:
            print("❌ Categorias já existem. Pulando seed.")
            return

        # Inserir categorias padrão (handebol feminino brasileiro)
        session.execute(text("""
            INSERT INTO categories (code, label, min_age, max_age) VALUES
            ('SUB12', 'Sub-12', 10, 12),
            ('SUB14', 'Sub-14 (Mirim)', 13, 14),
            ('SUB16', 'Sub-16 (Infantil)', 15, 16),
            ('SUB18', 'Sub-18 (Cadete)', 17, 18),
            ('SUB20', 'Sub-20 (Juvenil)', 19, 20),
            ('ADULTO', 'Adulto', 21, NULL)
            ON CONFLICT (code) DO NOTHING;
        """))
        session.commit()
        print("✅ Categorias criadas!")

if __name__ == "__main__":
    seed_categories()
```

**Executar:**
```bash
python backend/db_migrations/seeds/003_seed_categories.py
```

### 1.6 - Validar Seeds

```sql
-- Conectar ao banco
psql $DATABASE_URL

-- Validar roles (R4)
SELECT * FROM roles ORDER BY id;
-- Espera-se: 4 linhas (dirigente, coordenador, treinador, atleta)

-- Validar superadmin (R3, RDB6)
SELECT u.email, u.is_superadmin, p.full_name
FROM users u
JOIN persons p ON u.person_id = p.id
WHERE u.is_superadmin = true;
-- Espera-se: 1 linha (admin@hbtracking.com)

-- Validar organização (R34)
SELECT * FROM organizations;
-- Espera-se: 1 linha (Clube HB Tracking)

-- Validar categorias (R15, RDB11)
SELECT * FROM categories ORDER BY min_age;
-- Espera-se: 6 linhas (SUB12, SUB14, SUB16, SUB18, SUB20, ADULTO)

\q
```

### ✅ CHECKLIST FASE 1

- [ ] `alembic current` retorna `4af09f9d46a0`
- [ ] VIEW `v_seasons_with_status` criada
- [ ] 16 triggers documentados com `COMMENT ON FUNCTION`
- [ ] `team_registrations` tem `start_at`, `end_at` e EXCLUDE constraint
- [ ] `audit_logs` tem trigger de imutabilidade
- [ ] `users` tem índice único para `is_superadmin`
- [ ] Roles seedados (4 linhas)
- [ ] Super Admin seedado (1 linha)
- [ ] Organização seedada (1 linha)
- [ ] Categorias seedadas (6 linhas)
- [ ] `review_with_improvements.sql` adicionado ao `.gitignore`

---

## 🎯 FASE 2 - NÚCLEO DO BACKEND

**Status:** ⬜ Pendente
**Duração Estimada:** 3 horas
**Objetivo:** Implementar core do backend (config, database, context, auth mock)

### 2.1 - Estrutura de Diretórios

```bash
mkdir -p backend/app/core
mkdir -p backend/app/models
mkdir -p backend/app/schemas
mkdir -p backend/app/services
mkdir -p backend/app/api/v1/routers
mkdir -p backend/app/api/v1/deps
mkdir -p backend/app/tests/unit
mkdir -p backend/app/tests/integration

# Criar __init__.py
touch backend/app/__init__.py
touch backend/app/core/__init__.py
touch backend/app/models/__init__.py
touch backend/app/schemas/__init__.py
touch backend/app/services/__init__.py
touch backend/app/api/__init__.py
touch backend/app/api/v1/__init__.py
touch backend/app/api/v1/routers/__init__.py
touch backend/app/api/v1/deps/__init__.py
touch backend/app/tests/__init__.py
touch backend/app/tests/unit/__init__.py
touch backend/app/tests/integration/__init__.py
```

### 2.2 - Implementar Config (BaseSettings)

**Arquivo:** `backend/app/core/config.py`

```python
"""
Configurações do sistema usando Pydantic Settings
Todas as configurações via variáveis de ambiente (12-factor app)
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal


class Settings(BaseSettings):
    """
    Configurações globais do HB Tracking Backend

    Referências RAG:
    - R34: Clube único na V1
    - RDB1: PostgreSQL 17 (Neon)
    """

    # Environment
    ENV: Literal["local", "staging", "production"] = "local"

    # API
    API_VERSION: str = "v1"
    API_TITLE: str = "HB Tracking API"
    API_DESCRIPTION: str = "Sistema de Gestão de Handebol"
    API_VERSION_NUMBER: str = "1.0.0"

    # Database (RDB1)
    DATABASE_URL: str
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10
    DB_POOL_PRE_PING: bool = True

    # Security
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRES_MINUTES: int = 30

    # CORS
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]

    # Logging
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

    @property
    def is_production(self) -> bool:
        return self.ENV == "production"

    @property
    def is_local(self) -> bool:
        return self.ENV == "local"


# Singleton instance
settings = Settings()
```

**Teste:** `backend/app/tests/unit/test_config.py`

```python
"""Testes unitários para configurações"""
import pytest
from backend.app.core.config import Settings, settings


def test_settings_singleton():
    """Valida que settings é singleton"""
    from backend.app.core.config import settings as settings2
    assert settings is settings2


def test_settings_required_fields():
    """Valida campos obrigatórios"""
    assert settings.DATABASE_URL is not None
    assert settings.JWT_SECRET is not None
    assert settings.API_TITLE == "HB Tracking API"


def test_settings_env_detection():
    """Valida detecção de ambiente"""
    assert settings.ENV in ["local", "staging", "production"]

    if settings.ENV == "local":
        assert settings.is_local is True
        assert settings.is_production is False


def test_settings_cors_origins_is_list():
    """Valida que CORS_ORIGINS é lista"""
    assert isinstance(settings.CORS_ORIGINS, list)
    assert len(settings.CORS_ORIGINS) > 0
```

**Executar teste:**
```bash
pytest backend/app/tests/unit/test_config.py -v
```

### 2.2 - Implementar Database (Engine + SessionLocal)

**Arquivo:** `backend/app/core/database.py`

```python
"""
Gerenciamento de conexão com PostgreSQL (Neon)

Referências RAG:
- RDB1: PostgreSQL 17 com pgcrypto
- RDB3: timestamptz em UTC
- R33: Nada acontece fora de um vínculo
"""
from sqlalchemy import create_engine, text, event
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import NullPool
from backend.app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# Engine com pool configurado (RDB1)
engine = create_engine(
    settings.DATABASE_URL,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_pre_ping=settings.DB_POOL_PRE_PING,
    echo=settings.LOG_LEVEL == "DEBUG",
    future=True,
    # Garantir timezone UTC (RDB3)
    connect_args={
        "options": "-c timezone=utc"
    }
)

# SessionLocal para dependency injection
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    future=True,
    expire_on_commit=False
)


def get_db() -> Session:
    """
    Dependency para obter sessão de banco

    Uso: Depends(get_db) nos routers

    Garantias:
    - Commit automático se não houver exceção
    - Rollback automático em caso de erro
    - Sessão sempre fechada (finally)

    Referência RAG:
    - RF21: Em conflito, integridade prevalece
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        logger.error(f"Database error: {e}")
        raise
    finally:
        db.close()


def healthcheck_db() -> dict:
    """
    Healthcheck do banco de dados

    Verifica:
    - Conexão ativa
    - Versão do PostgreSQL
    - Extensão pgcrypto (RDB1)

    Returns:
        dict: Status da conexão
    """
    try:
        with engine.connect() as conn:
            # Testar conexão
            result = conn.execute(text("SELECT version()"))
            pg_version = result.scalar()

            # Verificar pgcrypto (RDB1)
            result = conn.execute(text(
                "SELECT COUNT(*) FROM pg_extension WHERE extname = 'pgcrypto'"
            ))
            has_pgcrypto = result.scalar() > 0

            # Verificar alembic_version
            result = conn.execute(text(
                "SELECT version_num FROM alembic_version LIMIT 1"
            ))
            alembic_version = result.scalar()

            return {
                "status": "healthy",
                "pg_version": pg_version.split()[1] if pg_version else "unknown",
                "pgcrypto_enabled": has_pgcrypto,
                "alembic_version": alembic_version
            }
    except Exception as e:
        logger.error(f"Database healthcheck failed: {e}")
        return {
            "status": "unhealthy",
            "error": str(e)
        }
```

**Teste:** `backend/app/tests/unit/test_database.py`

```python
"""Testes para database core"""
import pytest
from sqlalchemy import text
from backend.app.core.database import engine, get_db, healthcheck_db


def test_engine_created():
    """Valida que engine foi criado"""
    assert engine is not None
    assert engine.url.database is not None


def test_get_db_yields_session():
    """Valida que get_db retorna sessão"""
    gen = get_db()
    db = next(gen)
    assert db is not None
    assert hasattr(db, "execute")
    assert hasattr(db, "commit")
    assert hasattr(db, "rollback")
    # Fechar sessão
    try:
        next(gen)
    except StopIteration:
        pass


def test_healthcheck_db_success():
    """Valida healthcheck do banco"""
    health = healthcheck_db()
    assert health["status"] == "healthy"
    assert health["pgcrypto_enabled"] is True  # RDB1
    assert health["alembic_version"] is not None


@pytest.mark.integration
def test_database_timezone_utc():
    """Valida que timezone é UTC (RDB3)"""
    with engine.connect() as conn:
        result = conn.execute(text("SHOW timezone"))
        timezone = result.scalar()
        assert timezone.upper() == "UTC"


@pytest.mark.integration
def test_database_can_generate_uuid():
    """Valida que gen_random_uuid() funciona (RDB1, RDB2)"""
    with engine.connect() as conn:
        result = conn.execute(text("SELECT gen_random_uuid()"))
        uuid_value = result.scalar()
        assert uuid_value is not None
        assert len(str(uuid_value)) == 36  # UUID v4 format
```

**Executar testes:**
```bash
# Apenas unit
pytest backend/app/tests/unit/test_database.py -v -m "not integration"

# Com integration
pytest backend/app/tests/unit/test_database.py -v
```

### 2.3 - Implementar Context (Contexto de Execução)

**Arquivo:** `backend/app/core/context.py`

```python
"""
Contexto de execução para rastreabilidade e auditoria

Referências RAG:
- R6: Vínculo organizacional (pessoa, papel, clube, temporada)
- R33: Nada acontece fora de um vínculo
- R31: Ações críticas auditáveis
- R32: Log obrigatório (quem, quando, o quê)
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID


@dataclass
class ExecutionContext:
    """
    Contexto de execução de uma requisição

    Usado para:
    - Auditoria (R31, R32)
    - Validação de permissões (R25, R26)
    - Enforcement de vínculos (R6, R33)

    Attributes:
        user_id: ID do usuário autenticado
        person_id: ID da pessoa (R1)
        membership_id: ID do vínculo ativo (R6)
        organization_id: ID da organização (R34 - único na V1)
        role_code: Código do papel (R4: dirigente, coordenador, treinador, atleta)
        is_superadmin: Se é Super Administrador (R3)
        request_id: ID único da requisição (para correlação de logs)
        timestamp: Timestamp da execução
    """
    user_id: UUID
    person_id: UUID
    membership_id: Optional[UUID]  # None apenas para superadmin (R2)
    organization_id: UUID
    role_code: str
    is_superadmin: bool
    request_id: str
    timestamp: datetime

    def can_bypass_rules(self) -> bool:
        """
        Verifica se pode ignorar travas operacionais

        Referência RAG:
        - R3: Super Administrador pode ignorar travas, mas é auditado
        """
        return self.is_superadmin

    def has_active_membership(self) -> bool:
        """
        Verifica se tem vínculo ativo

        Referência RAG:
        - R42: Usuários sem vínculo não operam (exceto superadmin)
        - RF3: Vínculo ativo obrigatório
        """
        return self.is_superadmin or self.membership_id is not None

    def to_audit_dict(self) -> dict:
        """
        Converte contexto para dict de auditoria

        Usado em audit_logs (R31, R32, RDB5)
        """
        return {
            "actor_user_id": str(self.user_id),
            "actor_person_id": str(self.person_id),
            "actor_membership_id": str(self.membership_id) if self.membership_id else None,
            "actor_organization_id": str(self.organization_id),
            "actor_role": self.role_code,
            "is_superadmin": self.is_superadmin,
            "request_id": self.request_id,
            "timestamp": self.timestamp.isoformat()
        }


# Contexto mock para desenvolvimento (FASE 2)
def get_mock_context() -> ExecutionContext:
    """
    Contexto mock para testes e desenvolvimento inicial

    ATENÇÃO: Substituir por get_current_context() real na FASE 6
    """
    from uuid import uuid4
    from datetime import datetime

    return ExecutionContext(
        user_id=uuid4(),
        person_id=uuid4(),
        membership_id=uuid4(),
        organization_id=uuid4(),
        role_code="coordenador",  # Mock como coordenador (acesso total - R26)
        is_superadmin=False,
        request_id=str(uuid4()),
        timestamp=datetime.utcnow()
    )
```

**Teste:** `backend/app/tests/unit/test_context.py`

```python
"""Testes para contexto de execução"""
import pytest
from uuid import uuid4, UUID
from datetime import datetime
from backend.app.core.context import ExecutionContext, get_mock_context


def test_execution_context_creation():
    """Valida criação de contexto"""
    ctx = ExecutionContext(
        user_id=uuid4(),
        person_id=uuid4(),
        membership_id=uuid4(),
        organization_id=uuid4(),
        role_code="coordenador",
        is_superadmin=False,
        request_id=str(uuid4()),
        timestamp=datetime.utcnow()
    )
    assert isinstance(ctx.user_id, UUID)
    assert ctx.role_code == "coordenador"
    assert ctx.is_superadmin is False


def test_superadmin_can_bypass_rules():
    """Valida que superadmin pode ignorar travas (R3)"""
    ctx_super = ExecutionContext(
        user_id=uuid4(),
        person_id=uuid4(),
        membership_id=None,  # Superadmin pode não ter membership (R2)
        organization_id=uuid4(),
        role_code="dirigente",
        is_superadmin=True,
        request_id=str(uuid4()),
        timestamp=datetime.utcnow()
    )
    assert ctx_super.can_bypass_rules() is True

    ctx_normal = ExecutionContext(
        user_id=uuid4(),
        person_id=uuid4(),
        membership_id=uuid4(),
        organization_id=uuid4(),
        role_code="treinador",
        is_superadmin=False,
        request_id=str(uuid4()),
        timestamp=datetime.utcnow()
    )
    assert ctx_normal.can_bypass_rules() is False


def test_has_active_membership():
    """Valida verificação de vínculo ativo (R42, RF3)"""
    # Superadmin sem membership (ok)
    ctx_super = ExecutionContext(
        user_id=uuid4(),
        person_id=uuid4(),
        membership_id=None,
        organization_id=uuid4(),
        role_code="dirigente",
        is_superadmin=True,
        request_id=str(uuid4()),
        timestamp=datetime.utcnow()
    )
    assert ctx_super.has_active_membership() is True

    # Usuário normal com membership (ok)
    ctx_with_membership = ExecutionContext(
        user_id=uuid4(),
        person_id=uuid4(),
        membership_id=uuid4(),
        organization_id=uuid4(),
        role_code="treinador",
        is_superadmin=False,
        request_id=str(uuid4()),
        timestamp=datetime.utcnow()
    )
    assert ctx_with_membership.has_active_membership() is True

    # Usuário normal sem membership (NÃO ok - violaria R42)
    ctx_without_membership = ExecutionContext(
        user_id=uuid4(),
        person_id=uuid4(),
        membership_id=None,
        organization_id=uuid4(),
        role_code="treinador",
        is_superadmin=False,
        request_id=str(uuid4()),
        timestamp=datetime.utcnow()
    )
    assert ctx_without_membership.has_active_membership() is False


def test_to_audit_dict():
    """Valida conversão para dict de auditoria (R31, R32)"""
    ctx = get_mock_context()
    audit_dict = ctx.to_audit_dict()

    assert "actor_user_id" in audit_dict
    assert "actor_person_id" in audit_dict
    assert "actor_role" in audit_dict
    assert "request_id" in audit_dict
    assert "timestamp" in audit_dict
    assert isinstance(audit_dict["timestamp"], str)  # ISO format


def test_get_mock_context():
    """Valida contexto mock para desenvolvimento"""
    ctx = get_mock_context()
    assert ctx.role_code == "coordenador"  # Acesso total (R26)
    assert ctx.has_active_membership() is True
```

**Executar:**
```bash
pytest backend/app/tests/unit/test_context.py -v
```

### 2.4 - Implementar Auth Mock (FASE 2 - Temporário)

**Arquivo:** `backend/app/api/v1/deps/auth.py`

```python
"""
Dependências de autenticação

FASE 2: Mock temporário
FASE 6: Implementação real com JWT
"""
from fastapi import Depends, Header, HTTPException, status
from backend.app.core.context import ExecutionContext, get_mock_context


# MOCK para FASE 2 (substituir na FASE 6)
async def get_current_context(
    x_request_id: str = Header(default=None)
) -> ExecutionContext:
    """
    Obtém contexto de execução atual

    FASE 2 (MOCK): Retorna contexto fixo para desenvolvimento
    FASE 6 (REAL): Valida JWT, busca usuário, valida vínculo ativo

    Referências RAG:
    - R42: Usuários sem vínculo não operam
    - RF3: Vínculo ativo obrigatório
    - R3: Super Admin pode operar sem vínculo
    """
    # TODO FASE 6: Implementar autenticação JWT real
    ctx = get_mock_context()

    # Adicionar request_id do header se fornecido
    if x_request_id:
        ctx.request_id = x_request_id

    return ctx


# MOCK para FASE 2 (substituir na FASE 6)
async def require_role(allowed_roles: list[str]):
    """
    Dependency para validar papel do usuário

    FASE 2 (MOCK): Sempre autoriza
    FASE 6 (REAL): Valida papel conforme R25, R26

    Args:
        allowed_roles: Lista de papéis permitidos
            - "dirigente" (R26: acesso administrativo)
            - "coordenador" (R26: acesso total operacional)
            - "treinador" (R26: acesso às suas equipes)
            - "atleta" (R26: acesso restrito aos próprios dados)

    Raises:
        HTTPException 403: Se papel não autorizado
    """
    async def dependency(ctx: ExecutionContext = Depends(get_current_context)):
        # MOCK: sempre autoriza
        # TODO FASE 6: Implementar validação real
        if ctx.is_superadmin:
            return ctx  # Superadmin bypassa (R3)

        # TODO FASE 6: Validar ctx.role_code in allowed_roles
        return ctx

    return dependency
```

### ✅ CHECKLIST FASE 2

- [ ] `backend/app/core/config.py` implementado e testado
- [ ] `backend/app/core/database.py` implementado e testado
- [ ] `backend/app/core/context.py` implementado e testado
- [ ] `backend/app/api/v1/deps/auth.py` (mock) implementado
- [ ] Healthcheck `healthcheck_db()` retorna `healthy`
- [ ] Timezone do banco confirmado como UTC
- [ ] Todos os testes unitários passando: `pytest backend/app/tests/unit/ -v`
- [ ] Nenhum import error ao executar: `python -c "from backend.app.core.config import settings; print(settings.API_TITLE)"`

---

## 📝 FASE 3 - CONTRATO DA API

**Status:** ⬜ Pendente
**Duração Estimada:** 2 horas
**Objetivo:** Definir contratos de API (endpoints, schemas, error codes)

### 3.1 - Definição de Endpoints

**Criar:** `docs/API_CONTRACT.md`

```markdown
# CONTRATO DA API - HB TRACKING V1

## Convenções Gerais

- **Base URL**: `/api/v1`
- **Formato**: JSON (Content-Type: application/json)
- **Timezone**: UTC (RDB3)
- **IDs**: UUID v4 (RDB1, RDB2)
- **Paginação**: `?skip=0&limit=100` (padrão: 100 itens)
- **Autenticação**: Bearer Token (FASE 7)

## Códigos de Status HTTP

| Código | Uso | Exemplo |
|--------|-----|---------|
| **200** | Sucesso (GET, PUT, PATCH) | Dados retornados |
| **201** | Criado (POST) | Recurso criado |
| **204** | Sem conteúdo (DELETE lógico) | Soft delete executado |
| **400** | Requisição inválida | Dados malformados |
| **401** | Não autenticado | Token ausente/inválido |
| **403** | Não autorizado | Papel sem permissão (R25, R26) |
| **404** | Não encontrado | Recurso inexistente |
| **409** | Conflito | Violação de constraint (RDB9, RDB10) |
| **422** | Erro de validação | Falha em regra de negócio (R, RF, RD) |
| **500** | Erro interno | Falha não tratada |

## Estrutura de Erro Padrão

```json
{
  "error_code": "MEMBERSHIP_OVERLAP",
  "message": "Vínculo sobrepõe período existente",
  "details": {
    "field": "start_date",
    "constraint": "RDB9",
    "existing_membership_id": "uuid"
  },
  "timestamp": "2025-12-24T10:30:00Z",
  "request_id": "uuid"
}
```

## Endpoints por Recurso

### 🔐 Autenticação (FASE 7)

| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| POST | `/auth/login` | Login com credenciais | Público |
| POST | `/auth/logout` | Logout (invalidar token) | Requer token |
| GET | `/auth/me` | Dados do usuário autenticado | Requer token |

### 👤 Persons (R1)

| Método | Endpoint | Descrição | Papéis | Regras |
|--------|----------|-----------|--------|--------|
| GET | `/persons` | Listar pessoas | coordenador, dirigente | - |
| GET | `/persons/{id}` | Buscar pessoa | coordenador, dirigente | - |
| POST | `/persons` | Criar pessoa | coordenador, dirigente | R1 |
| PUT | `/persons/{id}` | Atualizar pessoa | coordenador, dirigente | R1 |
| DELETE | `/persons/{id}` | Soft delete | coordenador, dirigente | RDB4 |

### 👥 Users (R2, R3)

| Método | Endpoint | Descrição | Papéis | Regras |
|--------|----------|-----------|--------|--------|
| GET | `/users` | Listar usuários | dirigente | - |
| GET | `/users/{id}` | Buscar usuário | dirigente | - |
| POST | `/users` | Criar usuário | dirigente | R2 |
| PUT | `/users/{id}` | Atualizar usuário | dirigente | R3 (superadmin imutável) |
| DELETE | `/users/{id}` | Soft delete | dirigente | R3 (superadmin não deletável) |

### 🤝 Memberships (R6, R7, RDB9)

| Método | Endpoint | Descrição | Papéis | Regras |
|--------|----------|-----------|--------|--------|
| GET | `/memberships` | Listar vínculos | coordenador, dirigente | - |
| GET | `/memberships/active` | Vínculos ativos | coordenador, dirigente | R7 |
| GET | `/memberships/{id}` | Buscar vínculo | coordenador, dirigente | - |
| POST | `/memberships` | Criar vínculo | dirigente | RDB9 (sem overlap) |
| PUT | `/memberships/{id}` | Atualizar vínculo | dirigente | RDB9 |
| POST | `/memberships/{id}/end` | Encerrar vínculo | dirigente | R7 |

### 📅 Seasons (R8, RF5, RDB8)

| Método | Endpoint | Descrição | Papéis | Regras |
|--------|----------|-----------|--------|--------|
| GET | `/seasons` | Listar temporadas | todos | - |
| GET | `/seasons/active` | Temporada ativa | todos | VIEW v_seasons_with_status |
| GET | `/seasons/{id}` | Buscar temporada | todos | - |
| POST | `/seasons` | Criar temporada | dirigente | RDB8 (sem overlap) |
| PUT | `/seasons/{id}` | Atualizar temporada | dirigente | RDB8 |
| POST | `/seasons/{id}/cancel` | Cancelar temporada | dirigente | RF5.1 |
| POST | `/seasons/{id}/interrupt` | Interromper temporada | dirigente | RF5.2 |

### 🏃 Athletes (R12, R13, R14)

| Método | Endpoint | Descrição | Papéis | Regras |
|--------|----------|-----------|--------|--------|
| GET | `/athletes` | Listar atletas | coordenador, treinador | - |
| GET | `/athletes/{id}` | Buscar atleta | coordenador, treinador | - |
| POST | `/athletes` | Criar atleta | coordenador | R12 |
| PUT | `/athletes/{id}` | Atualizar atleta | coordenador | R12 |
| POST | `/athletes/{id}/state` | Alterar estado | coordenador | R13 (ativa, lesionada, dispensada) |
| GET | `/athletes/{id}/states` | Histórico de estados | coordenador, treinador | R13 |

### 🏆 Team Registrations (R17, RDB10)

| Método | Endpoint | Descrição | Papéis | Regras |
|--------|----------|-----------|--------|--------|
| GET | `/team-registrations` | Listar inscrições | coordenador, treinador | - |
| GET | `/teams/{team_id}/registrations` | Inscrições por equipe | coordenador, treinador | - |
| POST | `/team-registrations` | Inscrever atleta | coordenador | RDB10, RD2, RD3 (validação etária) |
| PUT | `/team-registrations/{id}/end` | Encerrar inscrição | coordenador | RDB10 |

### ⚽ Matches (R19, RDB13)

| Método | Endpoint | Descrição | Papéis | Regras |
|--------|----------|-----------|--------|--------|
| GET | `/matches` | Listar jogos | todos | - |
| GET | `/matches/{id}` | Buscar jogo | todos | - |
| POST | `/matches` | Criar jogo | treinador, coordenador | R19 |
| PUT | `/matches/{id}` | Atualizar jogo | treinador, coordenador | RDB13 |
| POST | `/matches/{id}/finalize` | Finalizar jogo | treinador, coordenador | RD8 |
| POST | `/matches/{id}/reopen` | Reabrir jogo | coordenador | RF15 |
| DELETE | `/matches/{id}` | Soft delete | coordenador | R29 |

### 📊 Match Events (RD, estatísticas)

| Método | Endpoint | Descrição | Papéis | Regras |
|--------|----------|-----------|--------|--------|
| GET | `/matches/{match_id}/events` | Eventos do jogo | todos | - |
| POST | `/matches/{match_id}/events` | Adicionar evento | treinador, coordenador | RD (validações por tipo) |
| PUT | `/matches/{match_id}/events/{id}` | Corrigir evento | coordenador | R23, R24 (admin_note obrigatório) |
| DELETE | `/matches/{match_id}/events/{id}` | Soft delete evento | coordenador | RDB4 |

## Schemas Pydantic (Exemplos)

### PersonCreate (R1)

```python
class PersonCreate(BaseModel):
    full_name: str = Field(..., min_length=3, max_length=200)
    birth_date: Optional[date] = None
    cpf: Optional[str] = Field(None, pattern=r"^\d{11}$")
```

### MembershipCreate (R6, RDB9)

```python
class MembershipCreate(BaseModel):
    person_id: UUID
    role_id: UUID
    organization_id: UUID
    season_id: UUID
    start_date: date
    end_date: Optional[date] = None

    @model_validator(mode='after')
    def validate_dates(self):
        if self.end_date and self.end_date <= self.start_date:
            raise ValueError("end_date deve ser posterior a start_date")
        return self
```

### AthleteStateCreate (R13)

```python
class AthleteStateCreate(BaseModel):
    athlete_id: UUID
    state: Literal["ativa", "lesionada", "dispensada"]
    started_at: date
    reason: Optional[str] = Field(None, max_length=500)
    admin_note: Optional[str] = None  # Obrigatório para "dispensada"

    @model_validator(mode='after')
    def validate_dispense_note(self):
        if self.state == "dispensada" and not self.admin_note:
            raise ValueError("admin_note obrigatório para dispensa (R13)")
        return self
```

## Erros de Negócio (Error Codes)

### RDB Rules

| Error Code | HTTP | Descrição | Regra |
|------------|------|-----------|-------|
| `MEMBERSHIP_OVERLAP` | 409 | Vínculo sobrepõe período existente | RDB9 |
| `TEAM_REG_OVERLAP` | 409 | Inscrição sobrepõe período existente | RDB10 |
| `SEASON_OVERLAP` | 409 | Temporada sobrepõe período existente | RDB8 |
| `SOFT_DELETE_REASON_REQUIRED` | 422 | deleted_reason obrigatório | RDB4 |

### R Rules

| Error Code | HTTP | Descrição | Regra |
|------------|------|-----------|-------|
| `SUPERADMIN_IMMUTABLE` | 403 | Super Admin não pode ser modificado | R3 |
| `SUPERADMIN_REQUIRED` | 409 | Deve existir 1 Super Admin | R3, RDB6 |
| `NO_ACTIVE_MEMBERSHIP` | 403 | Usuário sem vínculo ativo | R42, RF3 |
| `ATHLETE_DISPENSE_NO_UNDO` | 422 | Dispensa não pode ser revertida | R13 |

### RD Rules

| Error Code | HTTP | Descrição | Regra |
|------------|------|-----------|-------|
| `AGE_BELOW_CATEGORY` | 422 | Atleta abaixo da idade mínima | RD2, RD3 |
| `MATCH_ALREADY_FINALIZED` | 409 | Jogo já finalizado | RD8 |
| `CORRECTION_NOTE_REQUIRED` | 422 | admin_note obrigatório na correção | R23, R24 |

---

## Validações de Regras por Endpoint

Consultar seção 7 do RAG ([regras-sistema-v1.1_Version2.md](regras-sistema-v1.1_Version2.md)) para enforcement:

- **7.1 - Apenas no DB**: Triggers bloqueiam violações (RDB1-RDB14, R4, R20, R29, R35)
- **7.2 - DB + Backend**: Services validam regras (R1-R3, R5-R8, R11-R13, R15-R17, etc.)
- **7.3 - Apenas Backend**: Cálculos, derivações, agregações (R10, R21, R22, R26, R27, R36, RD1-RD91)
- **7.4 - Backend + Frontend**: APIs REST, validação de entrada (R9, R14, R18, RF1-RF31, RP1-RP20)
```

### 3.2 - Schemas de Erro

**Arquivo:** `backend/app/schemas/error.py`

```python
"""
Schemas de erro padrão da API

Referências RAG:
- Seção 8: Códigos de erro estruturados
"""
from pydantic import BaseModel, Field
from typing import Optional, Any
from datetime import datetime


class ErrorDetail(BaseModel):
    """
    Detalhes adicionais do erro

    Campos dinâmicos conforme contexto:
    - field: campo que causou o erro
    - constraint: regra violada (ex: RDB9, R13, RD2)
    - existing_id: ID de recurso conflitante
    """
    field: Optional[str] = None
    constraint: Optional[str] = None
    value: Optional[Any] = None

    model_config = {"extra": "allow"}  # Permite campos adicionais


class ErrorResponse(BaseModel):
    """
    Resposta padrão de erro da API

    Exemplo:
    ```json
    {
      "error_code": "MEMBERSHIP_OVERLAP",
      "message": "Vínculo sobrepõe período existente",
      "details": {
        "field": "start_date",
        "constraint": "RDB9",
        "existing_membership_id": "uuid"
      },
      "timestamp": "2025-12-24T10:30:00Z",
      "request_id": "uuid"
    }
    ```
    """
    error_code: str = Field(..., description="Código único do erro")
    message: str = Field(..., description="Mensagem legível")
    details: Optional[ErrorDetail] = Field(None, description="Detalhes adicionais")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    request_id: Optional[str] = Field(None, description="ID da requisição para rastreio")

    model_config = {
        "json_schema_extra": {
            "example": {
                "error_code": "AGE_BELOW_CATEGORY",
                "message": "Atleta com 13 anos não pode atuar em categoria SUB12 (min 10 anos)",
                "details": {
                    "field": "category_id",
                    "constraint": "RD2",
                    "athlete_age": 13,
                    "category_min_age": 10
                },
                "timestamp": "2025-12-24T10:30:00Z",
                "request_id": "550e8400-e29b-41d4-a716-446655440000"
            }
        }
    }


# Códigos de erro padrão
class ErrorCode:
    """Enum de códigos de erro do sistema"""

    # RDB (Database)
    MEMBERSHIP_OVERLAP = "MEMBERSHIP_OVERLAP"
    TEAM_REG_OVERLAP = "TEAM_REG_OVERLAP"
    SEASON_OVERLAP = "SEASON_OVERLAP"
    SOFT_DELETE_REASON_REQUIRED = "SOFT_DELETE_REASON_REQUIRED"

    # R (Structural)
    SUPERADMIN_IMMUTABLE = "SUPERADMIN_IMMUTABLE"
    SUPERADMIN_REQUIRED = "SUPERADMIN_REQUIRED"
    NO_ACTIVE_MEMBERSHIP = "NO_ACTIVE_MEMBERSHIP"
    ATHLETE_DISPENSE_NO_UNDO = "ATHLETE_DISPENSE_NO_UNDO"

    # RD (Sports Domain)
    AGE_BELOW_CATEGORY = "AGE_BELOW_CATEGORY"
    MATCH_ALREADY_FINALIZED = "MATCH_ALREADY_FINALIZED"
    CORRECTION_NOTE_REQUIRED = "CORRECTION_NOTE_REQUIRED"

    # Generic
    VALIDATION_ERROR = "VALIDATION_ERROR"
    NOT_FOUND = "NOT_FOUND"
    UNAUTHORIZED = "UNAUTHORIZED"
    FORBIDDEN = "FORBIDDEN"
    INTERNAL_ERROR = "INTERNAL_ERROR"
```

### 3.3 - Base Schemas Comuns

**Arquivo:** `backend/app/schemas/base.py`

```python
"""
Schemas base para herança
"""
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from uuid import UUID
from typing import Optional


class TimestampMixin(BaseModel):
    """Mixin para campos temporais (RDB3)"""
    created_at: datetime
    updated_at: datetime


class SoftDeleteMixin(BaseModel):
    """Mixin para soft delete (RDB4)"""
    deleted_at: Optional[datetime] = None
    deleted_reason: Optional[str] = None


class BaseSchema(BaseModel):
    """Schema base com configurações padrão"""
    model_config = ConfigDict(
        from_attributes=True,  # ORM mode
        use_enum_values=True,
        json_encoders={
            datetime: lambda v: v.isoformat()
        }
    )


class BaseResponseSchema(BaseSchema, TimestampMixin):
    """Schema base para responses (inclui id, timestamps)"""
    id: UUID = Field(..., description="ID único (UUID v4)")


class PaginatedResponse(BaseModel):
    """Response paginado genérico"""
    items: list
    total: int
    skip: int
    limit: int

    @property
    def has_more(self) -> bool:
        return self.skip + self.limit < self.total
```

### ✅ CHECKLIST FASE 3

- [ ] `docs/API_CONTRACT.md` criado com todos os endpoints
- [ ] `backend/app/schemas/error.py` implementado
- [ ] `backend/app/schemas/base.py` implementado
- [ ] ErrorResponse testado: `pytest backend/app/tests/unit/test_schemas_error.py -v`
- [ ] Todos os error codes mapeados conforme RAG seção 8
- [ ] Validações de regra documentadas por endpoint

---

## ⚡ FASE 4 - FASTAPI MÍNIMO

**Status:** ⬜ Pendente
**Duração Estimada:** 2 horas
**Objetivo:** Criar aplicação FastAPI mínima com health endpoint

### 4.1 - Implementar main.py

**Arquivo:** `backend/app/main.py`

```python
"""
Aplicação principal FastAPI - HB Tracking

Referências RAG:
- R34: Clube único na V1
- R42: Modo somente leitura sem vínculo ativo
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from backend.app.core.config import settings
from backend.app.api.v1 import api_router
import logging

# Configurar logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Criar app FastAPI
app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION_NUMBER,
    docs_url=f"/api/{settings.API_VERSION}/docs",
    redoc_url=f"/api/{settings.API_VERSION}/redoc",
    openapi_url=f"/api/{settings.API_VERSION}/openapi.json"
)

# CORS (FASE 7: restringir em produção)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS if not settings.is_production else [],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(api_router, prefix=f"/api/{settings.API_VERSION}")

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint - redirect para docs"""
    return JSONResponse(
        content={
            "message": "HB Tracking API",
            "version": settings.API_VERSION_NUMBER,
            "docs": f"/api/{settings.API_VERSION}/docs"
        }
    )


# Startup/Shutdown events
@app.on_event("startup")
async def startup_event():
    logger.info(f"🚀 HB Tracking API {settings.API_VERSION_NUMBER} iniciada")
    logger.info(f"📊 Ambiente: {settings.ENV}")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("🛑 HB Tracking API encerrada")
```

### 4.2 - Router de Health

**Arquivo:** `backend/app/api/v1/routers/health.py`

```python
"""
Health check endpoint

Referências RAG:
- RDB1: PostgreSQL + pgcrypto
- RDB5: audit_logs imutável
"""
from fastapi import APIRouter, status
from backend.app.core.database import healthcheck_db
from backend.app.core.config import settings

router = APIRouter(tags=["Health"])


@router.get("/health", status_code=status.HTTP_200_OK)
async def health():
    """
    Health check completo

    Verifica:
    - Database connection
    - PostgreSQL version
    - pgcrypto extension (RDB1)
    - Alembic migration version

    Returns:
        dict: Status de saúde do sistema
    """
    db_health = healthcheck_db()

    return {
        "status": "healthy" if db_health["status"] == "healthy" else "unhealthy",
        "version": settings.API_VERSION_NUMBER,
        "environment": settings.ENV,
        "database": db_health
    }


@router.get("/health/liveness", status_code=status.HTTP_200_OK)
async def liveness():
    """
    Liveness probe (Kubernetes)

    Retorna 200 se a aplicação está rodando
    """
    return {"status": "alive"}


@router.get("/health/readiness", status_code=status.HTTP_200_OK)
async def readiness():
    """
    Readiness probe (Kubernetes)

    Retorna 200 se a aplicação está pronta para receber tráfego
    """
    db_health = healthcheck_db()

    if db_health["status"] != "healthy":
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "not_ready", "reason": "database_unavailable"}
        )

    return {"status": "ready"}
```

### 4.3 - Main Router (v1)

**Arquivo:** `backend/app/api/v1/__init__.py`

```python
"""
Router principal da API v1
"""
from fastapi import APIRouter
from backend.app.api.v1.routers import health

api_router = APIRouter()

# Incluir routers
api_router.include_router(health.router)

# TODO FASE 5: Adicionar routers de recursos
# api_router.include_router(persons.router, prefix="/persons", tags=["Persons"])
# api_router.include_router(users.router, prefix="/users", tags=["Users"])
# api_router.include_router(memberships.router, prefix="/memberships", tags=["Memberships"])
# ...
```

### 4.4 - Teste de Integração

**Arquivo:** `backend/app/tests/integration/test_health_endpoint.py`

```python
"""
Testes de integração para health endpoints
"""
import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


@pytest.mark.integration
def test_health_endpoint_returns_200():
    """Valida que /health retorna 200"""
    response = client.get("/api/v1/health")
    assert response.status_code == 200


@pytest.mark.integration
def test_health_endpoint_structure():
    """Valida estrutura do response de /health"""
    response = client.get("/api/v1/health")
    data = response.json()

    assert "status" in data
    assert "version" in data
    assert "environment" in data
    assert "database" in data

    # Validar database health
    assert data["database"]["status"] == "healthy"
    assert data["database"]["pgcrypto_enabled"] is True  # RDB1
    assert data["database"]["alembic_version"] is not None


@pytest.mark.integration
def test_liveness_endpoint():
    """Valida /health/liveness"""
    response = client.get("/api/v1/health/liveness")
    assert response.status_code == 200
    assert response.json()["status"] == "alive"


@pytest.mark.integration
def test_readiness_endpoint():
    """Valida /health/readiness"""
    response = client.get("/api/v1/health/readiness")
    assert response.status_code == 200
    assert response.json()["status"] == "ready"


def test_root_endpoint():
    """Valida endpoint raiz /"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert "docs" in response.json()
```

### 4.5 - Executar Aplicação

**Comando:**
```bash
# Development server
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000

# Ou com hot reload e log detalhado
uvicorn backend.app.main:app --reload --log-level debug
```

**Validar:**
```bash
# 1. Health check
curl http://localhost:8000/api/v1/health

# 2. OpenAPI docs
open http://localhost:8000/api/v1/docs

# 3. Liveness
curl http://localhost:8000/api/v1/health/liveness

# 4. Readiness
curl http://localhost:8000/api/v1/health/readiness
```

### ✅ CHECKLIST FASE 4

- [ ] `backend/app/main.py` implementado
- [ ] `/api/v1/health` retorna 200 e estrutura correta
- [ ] `/api/v1/health/liveness` retorna 200
- [ ] `/api/v1/health/readiness` valida database
- [ ] OpenAPI docs acessível em `/api/v1/docs`
- [ ] CORS configurado para desenvolvimento
- [ ] Testes de integração passando: `pytest backend/app/tests/integration/test_health_endpoint.py -v`
- [ ] Aplicação roda sem erros: `uvicorn backend.app.main:app --reload`

---

## 🏗️ FASE 5 - CRUDS POR RECURSO

**Status:** ⬜ Pendente
**Duração Estimada:** 10-15 horas (iterativo)
**Objetivo:** Implementar CRUDs para cada recurso com testes

### 5.1 - Template de Implementação

Para cada recurso (persons, users, memberships, etc.), seguir o padrão:

1. **Model** (SQLAlchemy) - `backend/app/models/<resource>.py`
2. **Schemas** (Pydantic) - `backend/app/schemas/<resource>.py`
3. **Service** (Lógica de negócio) - `backend/app/services/<resource>_service.py`
4. **Router** (FastAPI) - `backend/app/api/v1/routers/<resource>.py`
5. **Tests** (Pytest) - `backend/app/tests/integration/test_<resource>.py`

### 5.2 - Exemplo Completo: Persons (R1)

#### Model

**Arquivo:** `backend/app/models/person.py`

```python
"""
Model: Person (R1)

Referências RAG:
- R1: Pessoa é entidade raiz (pode ser atleta ou não)
- RDB2: PKs são UUID v4 server-generated
- RDB3: Timestamps em UTC
- RDB4: Soft delete obrigatório
"""
from sqlalchemy import Column, String, Date, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from backend.app.models.base import Base
import uuid


class Person(Base):
    __tablename__ = "persons"

    # PK (RDB2)
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, server_default=func.gen_random_uuid())

    # Dados básicos (R1)
    full_name = Column(String(200), nullable=False)
    birth_date = Column(Date, nullable=True)
    cpf = Column(String(11), nullable=True, unique=True)

    # Contato
    phone = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)

    # Endereço
    address_street = Column(String(200), nullable=True)
    address_number = Column(String(20), nullable=True)
    address_complement = Column(String(100), nullable=True)
    address_neighborhood = Column(String(100), nullable=True)
    address_city = Column(String(100), nullable=True)
    address_state = Column(String(2), nullable=True)
    address_zip_code = Column(String(8), nullable=True)

    # Observações
    notes = Column(Text, nullable=True)

    # Soft delete (RDB4)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    deleted_reason = Column(Text, nullable=True)

    # Timestamps (RDB3)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
```

#### Schemas

**Arquivo:** `backend/app/schemas/person.py`

```python
"""
Schemas: Person (R1)
"""
from pydantic import BaseModel, Field, field_validator
from uuid import UUID
from datetime import date, datetime
from typing import Optional
from backend.app.schemas.base import BaseResponseSchema, SoftDeleteMixin


class PersonBase(BaseModel):
    """Campos comuns de Person"""
    full_name: str = Field(..., min_length=3, max_length=200)
    birth_date: Optional[date] = None
    cpf: Optional[str] = Field(None, pattern=r"^\d{11}$", description="CPF sem pontuação")
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[str] = Field(None, max_length=100)

    @field_validator('cpf')
    @classmethod
    def validate_cpf(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        # Validação básica de CPF
        if len(v) != 11 or not v.isdigit():
            raise ValueError("CPF deve ter 11 dígitos numéricos")
        return v


class PersonCreate(PersonBase):
    """Schema para criação de Person"""
    pass


class PersonUpdate(BaseModel):
    """Schema para atualização parcial de Person"""
    full_name: Optional[str] = Field(None, min_length=3, max_length=200)
    birth_date: Optional[date] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    notes: Optional[str] = None


class PersonResponse(PersonBase, BaseResponseSchema, SoftDeleteMixin):
    """Schema de resposta com todos os campos"""
    notes: Optional[str] = None


class PersonSoftDelete(BaseModel):
    """Schema para soft delete"""
    deleted_reason: str = Field(..., min_length=10, max_length=500, description="Motivo da exclusão (RDB4)")
```

#### Service

**Arquivo:** `backend/app/services/person_service.py`

```python
"""
Service: Person (R1)

Camada de lógica de negócio
"""
from sqlalchemy.orm import Session
from sqlalchemy import select
from uuid import UUID
from typing import Optional
from backend.app.models.person import Person
from backend.app.schemas.person import PersonCreate, PersonUpdate, PersonSoftDelete
from backend.app.schemas.error import ErrorResponse, ErrorCode
from fastapi import HTTPException, status
from datetime import datetime


class PersonService:
    """Service para operações de Person"""

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> list[Person]:
        """
        Lista todas as pessoas (exceto deletadas)

        Args:
            db: Sessão do banco
            skip: Offset de paginação
            limit: Limite de resultados

        Returns:
            Lista de Person
        """
        stmt = select(Person).where(Person.deleted_at == None).offset(skip).limit(limit)
        return db.execute(stmt).scalars().all()

    @staticmethod
    def get_by_id(db: Session, person_id: UUID) -> Optional[Person]:
        """
        Busca pessoa por ID

        Args:
            db: Sessão do banco
            person_id: UUID da pessoa

        Returns:
            Person ou None

        Raises:
            HTTPException 404: Se pessoa não encontrada
        """
        person = db.query(Person).filter(
            Person.id == person_id,
            Person.deleted_at == None
        ).first()

        if not person:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=ErrorResponse(
                    error_code=ErrorCode.NOT_FOUND,
                    message=f"Person {person_id} não encontrada"
                ).model_dump()
            )

        return person

    @staticmethod
    def create(db: Session, person_data: PersonCreate) -> Person:
        """
        Cria nova pessoa

        Args:
            db: Sessão do banco
            person_data: Dados da pessoa

        Returns:
            Person criada

        Raises:
            HTTPException 409: Se CPF já existe
        """
        # Validar CPF único
        if person_data.cpf:
            existing = db.query(Person).filter(
                Person.cpf == person_data.cpf,
                Person.deleted_at == None
            ).first()

            if existing:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=ErrorResponse(
                        error_code="CPF_ALREADY_EXISTS",
                        message=f"CPF {person_data.cpf} já cadastrado",
                        details={"field": "cpf", "existing_person_id": str(existing.id)}
                    ).model_dump()
                )

        # Criar person
        person = Person(**person_data.model_dump())
        db.add(person)
        db.flush()  # Gerar ID antes de commit

        return person

    @staticmethod
    def update(db: Session, person_id: UUID, person_data: PersonUpdate) -> Person:
        """
        Atualiza pessoa

        Args:
            db: Sessão do banco
            person_id: UUID da pessoa
            person_data: Dados para atualizar

        Returns:
            Person atualizada
        """
        person = PersonService.get_by_id(db, person_id)

        # Atualizar apenas campos fornecidos
        update_data = person_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(person, field, value)

        db.flush()
        return person

    @staticmethod
    def soft_delete(db: Session, person_id: UUID, delete_data: PersonSoftDelete) -> Person:
        """
        Soft delete de pessoa

        Args:
            db: Sessão do banco
            person_id: UUID da pessoa
            delete_data: Motivo da exclusão

        Returns:
            Person deletada

        Referências RAG:
            - RDB4: deleted_reason obrigatório
        """
        person = PersonService.get_by_id(db, person_id)

        person.deleted_at = datetime.utcnow()
        person.deleted_reason = delete_data.deleted_reason

        db.flush()
        return person
```

#### Router

**Arquivo:** `backend/app/api/v1/routers/persons.py`

```python
"""
Router: Persons (R1)
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from uuid import UUID
from backend.app.core.database import get_db
from backend.app.core.context import ExecutionContext
from backend.app.api.v1.deps.auth import get_current_context, require_role
from backend.app.services.person_service import PersonService
from backend.app.schemas.person import PersonCreate, PersonUpdate, PersonResponse, PersonSoftDelete
from backend.app.schemas.base import PaginatedResponse

router = APIRouter()


@router.get("", response_model=PaginatedResponse)
async def list_persons(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    ctx: ExecutionContext = Depends(require_role(["coordenador", "dirigente"]))
):
    """
    Lista todas as pessoas

    Permissões: coordenador, dirigente (R26)
    """
    persons = PersonService.get_all(db, skip, limit)
    total = db.query(Person).filter(Person.deleted_at == None).count()

    return PaginatedResponse(
        items=[PersonResponse.model_validate(p) for p in persons],
        total=total,
        skip=skip,
        limit=limit
    )


@router.get("/{person_id}", response_model=PersonResponse)
async def get_person(
    person_id: UUID,
    db: Session = Depends(get_db),
    ctx: ExecutionContext = Depends(require_role(["coordenador", "dirigente"]))
):
    """
    Busca pessoa por ID

    Permissões: coordenador, dirigente (R26)
    """
    person = PersonService.get_by_id(db, person_id)
    return PersonResponse.model_validate(person)


@router.post("", response_model=PersonResponse, status_code=status.HTTP_201_CREATED)
async def create_person(
    person_data: PersonCreate,
    db: Session = Depends(get_db),
    ctx: ExecutionContext = Depends(require_role(["coordenador", "dirigente"]))
):
    """
    Cria nova pessoa

    Permissões: coordenador, dirigente (R26)
    Regras: R1
    """
    person = PersonService.create(db, person_data)
    return PersonResponse.model_validate(person)


@router.put("/{person_id}", response_model=PersonResponse)
async def update_person(
    person_id: UUID,
    person_data: PersonUpdate,
    db: Session = Depends(get_db),
    ctx: ExecutionContext = Depends(require_role(["coordenador", "dirigente"]))
):
    """
    Atualiza pessoa

    Permissões: coordenador, dirigente (R26)
    """
    person = PersonService.update(db, person_id, person_data)
    return PersonResponse.model_validate(person)


@router.delete("/{person_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_person(
    person_id: UUID,
    delete_data: PersonSoftDelete,
    db: Session = Depends(get_db),
    ctx: ExecutionContext = Depends(require_role(["coordenador", "dirigente"]))
):
    """
    Soft delete de pessoa

    Permissões: coordenador, dirigente (R26)
    Regras: RDB4 (deleted_reason obrigatório)
    """
    PersonService.soft_delete(db, person_id, delete_data)
    return None  # 204 No Content
```

#### Tests

**Arquivo:** `backend/app/tests/integration/test_persons.py`

```python
"""
Testes de integração: Persons (R1)
"""
import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.models.person import Person
from sqlalchemy.orm import Session

client = TestClient(app)


@pytest.mark.integration
def test_create_person_success(db: Session):
    """Testa criação de pessoa com sucesso"""
    response = client.post("/api/v1/persons", json={
        "full_name": "João Silva",
        "birth_date": "1990-01-15",
        "cpf": "12345678901"
    })

    assert response.status_code == 201
    data = response.json()
    assert data["full_name"] == "João Silva"
    assert "id" in data
    assert data["deleted_at"] is None


@pytest.mark.integration
def test_create_person_duplicate_cpf(db: Session):
    """Testa criação com CPF duplicado (deve retornar 409)"""
    # Primeira pessoa
    client.post("/api/v1/persons", json={
        "full_name": "Maria Santos",
        "cpf": "11111111111"
    })

    # Segunda pessoa com mesmo CPF
    response = client.post("/api/v1/persons", json={
        "full_name": "José Santos",
        "cpf": "11111111111"
    })

    assert response.status_code == 409
    assert response.json()["error_code"] == "CPF_ALREADY_EXISTS"


@pytest.mark.integration
def test_get_person_by_id(db: Session):
    """Testa busca por ID"""
    # Criar pessoa
    create_response = client.post("/api/v1/persons", json={
        "full_name": "Ana Costa"
    })
    person_id = create_response.json()["id"]

    # Buscar por ID
    response = client.get(f"/api/v1/persons/{person_id}")

    assert response.status_code == 200
    assert response.json()["full_name"] == "Ana Costa"


@pytest.mark.integration
def test_soft_delete_person(db: Session):
    """Testa soft delete com deleted_reason (RDB4)"""
    # Criar pessoa
    create_response = client.post("/api/v1/persons", json={
        "full_name": "Pedro Oliveira"
    })
    person_id = create_response.json()["id"]

    # Soft delete
    response = client.delete(f"/api/v1/persons/{person_id}", json={
        "deleted_reason": "Cadastro duplicado - pessoa já existe no sistema"
    })

    assert response.status_code == 204

    # Validar que não aparece mais em listagens
    list_response = client.get("/api/v1/persons")
    persons = list_response.json()["items"]
    assert not any(p["id"] == person_id for p in persons)
```

### 5.3 - Ordem de Implementação Recomendada

Implementar recursos na seguinte ordem (respeita dependências):

1. ✅ **Persons** (R1) - Entidade raiz
2. **Categories** (R15, RDB11) - Categorias globais
3. **Roles** (R4) - Papéis do sistema
4. **Organizations** (R34) - Clube único
5. **Seasons** (R8, RF5, RDB8) - Temporadas
6. **Users** (R2, R3) - Usuários
7. **Memberships** (R6, R7, RDB9) - Vínculos
8. **Teams** (RF6) - Equipes por temporada
9. **Athletes** (R12, R13, R14) - Atletas
10. **Team Registrations** (R17, RDB10) - Inscrições de atletas
11. **Training Sessions** (R18) - Treinos
12. **Matches** (R19, RDB13) - Jogos
13. **Match Events** (RD1-RD91) - Estatísticas

### ✅ CHECKLIST FASE 5 (por recurso)

- [ ] Model implementado com todas as colunas conforme RAG
- [ ] Schemas (Create, Update, Response) implementados
- [ ] Service com validações de negócio implementado
- [ ] Router com endpoints REST implementado
- [ ] Tests de integração (create, read, update, delete) passando
- [ ] Router adicionado ao `api_router` em `backend/app/api/v1/__init__.py`
- [ ] OpenAPI docs atualizado (`/api/v1/docs`)
- [ ] Regras RAG referenciadas em comentários

---

## 🔒 FASE 6 - ENDURECIMENTO E SEGURANÇA

**Status:** ⬜ Pendente
**Duração Estimada:** 4 horas
**Objetivo:** Implementar autenticação JWT, RBAC, exception handler global

### 6.1 - Implementar JWT (Substituir Mock)

**Arquivo:** `backend/app/core/security.py`

```python
"""
Segurança: JWT, password hashing

Referências RAG:
- R3: Super Admin
- R42: Vínculo ativo obrigatório
"""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from backend.app.core.config import settings
from uuid import UUID

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash de senha usando bcrypt"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica senha"""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Cria JWT access token

    Payload:
    - sub: user_id (UUID)
    - person_id: UUID
    - membership_id: UUID ou None
    - role_code: str
    - is_superadmin: bool
    - organization_id: UUID
    - exp: timestamp de expiração

    Args:
        data: Dict com claims
        expires_delta: Duração do token (padrão: settings.JWT_EXPIRES_MINUTES)

    Returns:
        Token JWT assinado
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRES_MINUTES)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM
    )

    return encoded_jwt


def decode_access_token(token: str) -> dict:
    """
    Decodifica JWT

    Args:
        token: JWT string

    Returns:
        Payload decodificado

    Raises:
        JWTError: Se token inválido
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except JWTError:
        raise
```

**Atualizar:** `backend/app/api/v1/deps/auth.py` (remover mock)

```python
"""
Autenticação JWT REAL (FASE 6)
"""
from fastapi import Depends, Header, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from backend.app.core.context import ExecutionContext
from backend.app.core.security import decode_access_token
from backend.app.core.database import get_db
from backend.app.models.user import User
from backend.app.models.membership import Membership
from backend.app.schemas.error import ErrorResponse, ErrorCode
from uuid import UUID
from datetime import datetime
from jose import JWTError

security = HTTPBearer()


async def get_current_context(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    x_request_id: str = Header(default=None),
    db: Session = Depends(get_db)
) -> ExecutionContext:
    """
    Obtém contexto de execução a partir do JWT

    Fluxo:
    1. Decodifica JWT
    2. Busca usuário no banco
    3. Valida vínculo ativo (R42, RF3) exceto superadmin
    4. Retorna ExecutionContext

    Raises:
        HTTPException 401: Token inválido
        HTTPException 403: Usuário sem vínculo ativo
    """
    token = credentials.credentials

    try:
        # Decodificar JWT
        payload = decode_access_token(token)
        user_id = UUID(payload.get("sub"))
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ErrorResponse(
                error_code=ErrorCode.UNAUTHORIZED,
                message="Token inválido ou expirado"
            ).model_dump(),
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Buscar usuário
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ErrorResponse(
                error_code=ErrorCode.UNAUTHORIZED,
                message="Usuário não encontrado"
            ).model_dump()
        )

    # Validar vínculo ativo (R42, RF3) exceto superadmin (R3)
    if not user.is_superadmin:
        active_membership = db.query(Membership).filter(
            Membership.person_id == user.person_id,
            Membership.status == "ativo",
            Membership.deleted_at == None
        ).first()

        if not active_membership:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=ErrorResponse(
                    error_code=ErrorCode.NO_ACTIVE_MEMBERSHIP,
                    message="Usuário sem vínculo ativo não pode operar",
                    details={"constraint": "R42"}
                ).model_dump()
            )

        membership_id = active_membership.id
        role_code = active_membership.role.code
        organization_id = active_membership.organization_id
    else:
        # Superadmin pode não ter vínculo (R3)
        membership_id = None
        role_code = "dirigente"  # Default para superadmin
        # Buscar organização (único clube - R34)
        org = db.query(Organization).first()
        organization_id = org.id if org else None

    # Criar contexto
    return ExecutionContext(
        user_id=user.id,
        person_id=user.person_id,
        membership_id=membership_id,
        organization_id=organization_id,
        role_code=role_code,
        is_superadmin=user.is_superadmin,
        request_id=x_request_id or str(uuid4()),
        timestamp=datetime.utcnow()
    )


async def require_role(allowed_roles: list[str]):
    """
    Dependency para validar papel (REAL - FASE 6)

    Referências RAG:
    - R25: Permissões por papel
    - R26: Hierarquia (coordenador > treinador > atleta)
    - R3: Superadmin bypassa

    Args:
        allowed_roles: Lista de papéis autorizados

    Raises:
        HTTPException 403: Se papel não autorizado
    """
    async def dependency(ctx: ExecutionContext = Depends(get_current_context)):
        if ctx.is_superadmin:
            return ctx  # Bypass (R3)

        if ctx.role_code not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=ErrorResponse(
                    error_code=ErrorCode.FORBIDDEN,
                    message=f"Papel '{ctx.role_code}' não autorizado para esta operação",
                    details={
                        "constraint": "R25",
                        "allowed_roles": allowed_roles,
                        "user_role": ctx.role_code
                    }
                ).model_dump()
            )

        return ctx

    return dependency
```

### 6.2 - Login Endpoint

**Arquivo:** `backend/app/api/v1/routers/auth.py`

```python
"""
Router: Autenticação
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from backend.app.core.database import get_db
from backend.app.core.security import verify_password, create_access_token
from backend.app.models.user import User
from backend.app.schemas.error import ErrorResponse, ErrorCode

router = APIRouter(tags=["Authentication"])


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    full_name: str
    role_code: str
    is_superadmin: bool


@router.post("/login", response_model=LoginResponse)
async def login(
    credentials: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Login com email e senha

    Retorna JWT access token

    Referências RAG:
    - R2: Usuário com email único
    - R42: Vínculo ativo obrigatório (exceto superadmin)
    """
    # Buscar usuário por email
    user = db.query(User).filter(User.email == credentials.email).first()

    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ErrorResponse(
                error_code=ErrorCode.UNAUTHORIZED,
                message="Email ou senha inválidos"
            ).model_dump()
        )

    # Validar vínculo ativo (exceto superadmin)
    if not user.is_superadmin:
        active_membership = db.query(Membership).filter(
            Membership.person_id == user.person_id,
            Membership.status == "ativo",
            Membership.deleted_at == None
        ).first()

        if not active_membership:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=ErrorResponse(
                    error_code=ErrorCode.NO_ACTIVE_MEMBERSHIP,
                    message="Usuário sem vínculo ativo não pode fazer login",
                    details={"constraint": "R42"}
                ).model_dump()
            )

        role_code = active_membership.role.code
    else:
        role_code = "dirigente"

    # Criar JWT
    access_token = create_access_token(
        data={
            "sub": str(user.id),
            "person_id": str(user.person_id),
            "role_code": role_code,
            "is_superadmin": user.is_superadmin
        }
    )

    return LoginResponse(
        access_token=access_token,
        user_id=str(user.id),
        full_name=user.full_name,
        role_code=role_code,
        is_superadmin=user.is_superadmin
    )
```

### 6.3 - Exception Handler Global

**Atualizar:** `backend/app/main.py`

```python
"""
Exception handlers globais
"""
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError
from backend.app.schemas.error import ErrorResponse, ErrorCode
import logging

logger = logging.getLogger(__name__)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handler para erros de validação Pydantic"""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=ErrorResponse(
            error_code=ErrorCode.VALIDATION_ERROR,
            message="Erro de validação",
            details={"errors": exc.errors()},
            request_id=request.headers.get("X-Request-ID")
        ).model_dump()
    )


@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    """Handler para erros de integridade do banco"""
    logger.error(f"IntegrityError: {exc}")

    # Detectar constraint específica
    error_msg = str(exc.orig)
    error_code = "DATABASE_CONSTRAINT_VIOLATION"

    if "uq_team_reg_active_athlete_team_season" in error_msg:
        error_code = ErrorCode.TEAM_REG_OVERLAP
        message = "Atleta já possui inscrição ativa nesta equipe/temporada"
    elif "membership" in error_msg and "overlap" in error_msg:
        error_code = ErrorCode.MEMBERSHIP_OVERLAP
        message = "Vínculo sobrepõe período existente"
    else:
        message = "Violação de constraint do banco de dados"

    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content=ErrorResponse(
            error_code=error_code,
            message=message,
            request_id=request.headers.get("X-Request-ID")
        ).model_dump()
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """Handler genérico para erros não tratados"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            error_code=ErrorCode.INTERNAL_ERROR,
            message="Erro interno do servidor",
            request_id=request.headers.get("X-Request-ID")
        ).model_dump()
    )
```

### ✅ CHECKLIST FASE 6

- [ ] `backend/app/core/security.py` implementado (JWT, password hashing)
- [ ] `backend/app/api/v1/deps/auth.py` substituído (remover mock, implementar JWT real)
- [ ] `/api/v1/auth/login` funcionando e retornando JWT
- [ ] `get_current_context()` valida JWT e busca usuário
- [ ] `require_role()` valida papéis conforme R25, R26
- [ ] Exception handlers globais funcionando
- [ ] IntegrityError mapeado para error codes específicos
- [ ] Testes de autenticação passando
- [ ] Superadmin pode operar sem vínculo (R3)
- [ ] Usuário normal sem vínculo recebe 403 (R42, RF3)

---

## 🚀 FASE 7 - PREPARAÇÃO PARA PRODUÇÃO

**Status:** ⬜ Pendente
**Duração Estimada:** 3 horas
**Objetivo:** Logging estruturado, CORS restritivo, healthchecks completos

### 7.1 - Logging Estruturado

**Arquivo:** `backend/app/core/logging.py`

```python
"""
Logging estruturado JSON

Para produção, usar logging em JSON para integração com:
- CloudWatch (AWS)
- Stackdriver (GCP)
- Application Insights (Azure)
"""
import logging
import json
from datetime import datetime
from typing import Any


class JSONFormatter(logging.Formatter):
    """Formatter para logs em JSON"""

    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }

        # Adicionar campos extras
        if hasattr(record, "request_id"):
            log_data["request_id"] = record.request_id

        if hasattr(record, "user_id"):
            log_data["user_id"] = record.user_id

        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_data)


def setup_logging(env: str, log_level: str):
    """
    Configura logging conforme ambiente

    Args:
        env: "local", "staging", "production"
        log_level: "DEBUG", "INFO", "WARNING", "ERROR"
    """
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level))

    # Remover handlers existentes
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Console handler
    console_handler = logging.StreamHandler()

    if env == "production":
        # JSON em produção
        console_handler.setFormatter(JSONFormatter())
    else:
        # Human-readable em dev
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        console_handler.setFormatter(formatter)

    root_logger.addHandler(console_handler)
```

**Atualizar:** `backend/app/main.py`

```python
from backend.app.core.logging import setup_logging

# Configurar logging no startup
@app.on_event("startup")
async def startup_event():
    setup_logging(settings.ENV, settings.LOG_LEVEL)
    logger.info(f"🚀 HB Tracking API {settings.API_VERSION_NUMBER} iniciada", extra={
        "environment": settings.ENV,
        "log_level": settings.LOG_LEVEL
    })
```

### 7.2 - CORS Restritivo em Produção

**Atualizar:** `backend/app/main.py`

```python
# CORS (restritivo em produção)
if settings.is_production:
    # Produção: apenas origens permitidas
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,  # Deve ser lista específica
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
        allow_headers=["Authorization", "Content-Type", "X-Request-ID"],
        max_age=600
    )
else:
    # Dev: permissivo
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
```

### 7.3 - Middleware de Request ID

**Arquivo:** `backend/app/core/middleware.py`

```python
"""
Middlewares customizados
"""
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import uuid
import logging

logger = logging.getLogger(__name__)


class RequestIDMiddleware(BaseHTTPMiddleware):
    """
    Middleware para adicionar Request ID único em cada requisição

    Usado para correlação de logs (R31, R32)
    """

    async def dispatch(self, request: Request, call_next):
        # Gerar ou pegar Request ID do header
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())

        # Adicionar ao request state
        request.state.request_id = request_id

        # Log de entrada
        logger.info(f"{request.method} {request.url.path}", extra={
            "request_id": request_id,
            "method": request.method,
            "path": request.url.path,
            "client_ip": request.client.host
        })

        # Processar request
        response = await call_next(request)

        # Adicionar Request ID ao response header
        response.headers["X-Request-ID"] = request_id

        return response
```

**Atualizar:** `backend/app/main.py`

```python
from backend.app.core.middleware import RequestIDMiddleware

# Adicionar middleware
app.add_middleware(RequestIDMiddleware)
```

### 7.4 - Healthcheck Avançado

**Atualizar:** `backend/app/api/v1/routers/health.py`

```python
@router.get("/health/full", status_code=status.HTTP_200_OK)
async def health_full():
    """
    Healthcheck completo (validações profundas)

    Verifica:
    - Database connection
    - Critical tables exist
    - Alembic migration version
    - Super admin exists (R3, RDB6)
    - Roles seeded (R4)
    - Categories seeded (R15)
    """
    db_health = healthcheck_db()

    if db_health["status"] != "healthy":
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "unhealthy", "database": db_health}
        )

    # Validações adicionais
    checks = {}

    try:
        with engine.connect() as conn:
            # Verificar super admin (R3, RDB6)
            result = conn.execute(text(
                "SELECT COUNT(*) FROM users WHERE is_superadmin = true"
            ))
            superadmin_count = result.scalar()
            checks["superadmin_exists"] = superadmin_count == 1

            # Verificar roles (R4)
            result = conn.execute(text("SELECT COUNT(*) FROM roles"))
            roles_count = result.scalar()
            checks["roles_seeded"] = roles_count >= 4

            # Verificar categorias (R15)
            result = conn.execute(text("SELECT COUNT(*) FROM categories"))
            categories_count = result.scalar()
            checks["categories_seeded"] = categories_count >= 6

            # Verificar VIEW v_seasons_with_status
            result = conn.execute(text(
                "SELECT COUNT(*) FROM pg_views WHERE viewname = 'v_seasons_with_status'"
            ))
            checks["view_seasons_exists"] = result.scalar() > 0

    except Exception as e:
        logger.error(f"Healthcheck failed: {e}")
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "unhealthy", "error": str(e)}
        )

    all_healthy = all(checks.values())

    return {
        "status": "healthy" if all_healthy else "degraded",
        "version": settings.API_VERSION_NUMBER,
        "environment": settings.ENV,
        "database": db_health,
        "checks": checks
    }
```

### ✅ CHECKLIST FASE 7

- [ ] Logging estruturado em JSON para produção
- [ ] CORS configurado com origens específicas em produção
- [ ] RequestIDMiddleware adicionado
- [ ] X-Request-ID propagado em responses
- [ ] `/api/v1/health/full` retorna validações profundas
- [ ] Logs incluem `request_id`, `user_id`, `timestamp`
- [ ] Exception logs estruturados com stack trace
- [ ] `.env` de produção validado (sem valores default)

---

## ✅ FASE 8 - VALIDAÇÃO PRODUCTION-READY

**Status:** ⬜ Pendente
**Duração Estimada:** 2 horas
**Objetivo:** Checklist final de conformidade e prontidão

### 8.1 - Checklist de Conformidade RAG

**Executar validações:**

```bash
# 1. Conectar ao banco de produção
psql $DATABASE_URL

-- 2. Validar migrations aplicadas
SELECT version_num FROM alembic_version;
-- Esperado: 4af09f9d46a0 (ou posterior)

-- 3. Validar RDB1 (PostgreSQL + pgcrypto)
SELECT version(), extname FROM pg_extension WHERE extname = 'pgcrypto';
-- Esperado: PostgreSQL 17, pgcrypto instalado

-- 4. Validar RDB3 (timezone UTC)
SHOW timezone;
-- Esperado: UTC

-- 5. Validar RDB6 (1 Super Admin)
SELECT COUNT(*) FROM users WHERE is_superadmin = true;
-- Esperado: 1

-- 6. Validar R4 (Roles seedados)
SELECT code FROM roles ORDER BY id;
-- Esperado: dirigente, coordenador, treinador, atleta

-- 7. Validar R15 (Categorias seedadas)
SELECT code, min_age, max_age FROM categories ORDER BY min_age;
-- Esperado: SUB12, SUB14, SUB16, SUB18, SUB20, ADULTO

-- 8. Validar RDB10 (team_registrations com start_at/end_at)
\d+ team_registrations
-- Esperado: start_at NOT NULL, end_at, EXCLUDE constraint

-- 9. Validar RDB5 (audit_logs imutável)
SELECT tgname FROM pg_trigger WHERE tgrelid = 'audit_logs'::regclass;
-- Esperado: trg_audit_logs_immutable

-- 10. Validar VIEW v_seasons_with_status
\d+ v_seasons_with_status
-- Esperado: VIEW com status_derivado + flags booleanos

-- 11. Validar triggers documentados
SELECT COUNT(*) FROM pg_proc p
JOIN pg_namespace n ON p.pronamespace = n.oid
WHERE n.nspname = 'public'
  AND pg_catalog.obj_description(p.oid, 'pg_proc') IS NOT NULL;
-- Esperado: >= 16

\q
```

### 8.2 - Checklist de Testes

```bash
# 1. Rodar todos os testes unitários
pytest backend/app/tests/unit/ -v --cov

# 2. Rodar testes de integração
pytest backend/app/tests/integration/ -v -m integration

# 3. Validar cobertura mínima (80%)
pytest --cov=backend/app --cov-report=term-missing --cov-fail-under=80

# 4. Rodar testes de conformidade RAG
pytest backend/app/tests/integration/ -v -m rdb
pytest backend/app/tests/integration/ -v -m r
pytest backend/app/tests/integration/ -v -m rd
```

### 8.3 - Checklist de Segurança

- [ ] JWT_SECRET é secreto e forte (>= 32 chars random)
- [ ] Passwords são hasheadas com bcrypt
- [ ] CORS restrito a origens conhecidas em produção
- [ ] SQL Injection prevenido (SQLAlchemy ORM)
- [ ] Soft delete implementado (RDB4)
- [ ] Auditoria imutável (RDB5, R35)
- [ ] Super Admin único e protegido (R3, RDB6)
- [ ] Validação de vínculo ativo (R42, RF3)
- [ ] RBAC implementado (R25, R26)

### 8.4 - Checklist de Performance

- [ ] Índices criados em colunas de busca frequente
- [ ] Paginação implementada em listagens
- [ ] Pool de conexões configurado (DB_POOL_SIZE)
- [ ] Queries otimizadas (usar EXPLAIN ANALYZE)
- [ ] VIEW v_seasons_with_status criada para status derivado
- [ ] Logs estruturados (não bloqueantes)

### 8.5 - Checklist de Observabilidade

- [ ] Logging estruturado em JSON (produção)
- [ ] Request ID propagado em logs e responses
- [ ] Exception logs com stack trace
- [ ] Healthcheck endpoints funcionando
- [ ] Métricas expostas (opcional: Prometheus)

### 8.6 - Checklist de Deploy

- [ ] `.env` de produção criado (sem secrets commitados)
- [ ] DATABASE_URL válido (Neon production)
- [ ] Migrations aplicadas (`alembic upgrade head`)
- [ ] Seeds aplicados (roles, superadmin, categories)
- [ ] Uvicorn configurado com workers (`--workers 4`)
- [ ] Reverse proxy configurado (nginx, caddy, ou cloud load balancer)
- [ ] HTTPS habilitado
- [ ] Logs centralizados (CloudWatch, Stackdriver, etc.)
- [ ] Backups automáticos do banco (Neon snapshots)

### ✅ CHECKLIST FINAL FASE 8

- [ ] Todas as validações RAG passando
- [ ] Cobertura de testes >= 80%
- [ ] Segurança validada
- [ ] Performance otimizada
- [ ] Observabilidade configurada
- [ ] Deploy checklist completo
- [ ] Documentação API_CONTRACT.md atualizada
- [ ] README.md atualizado com instruções de deploy

---

## 📚 APÊNDICES

### A. Troubleshooting Comum

#### Erro: "psycopg2: SSL connection error"
**Solução:**
```bash
# Adicionar `sslmode=require` no DATABASE_URL
DATABASE_URL=postgresql://user:pass@host/db?sslmode=require
```

#### Erro: "IntegrityError: duplicate key value violates unique constraint"
**Causa:** Violação de constraint (RDB9, RDB10, RDB6)
**Solução:** Validar dados antes de INSERT/UPDATE, usar error handlers

#### Erro: "No active membership"
**Causa:** Usuário sem vínculo ativo tentando operar (R42, RF3)
**Solução:** Criar vínculo ativo ou marcar como superadmin

#### Erro: "Alembic migration conflict"
**Causa:** Múltiplos developers criando migrations simultâneas
**Solução:**
```bash
# Resolver conflito manualmente
alembic merge <rev1> <rev2> -m "merge migrations"
alembic upgrade head
```

### B. Comandos Úteis

```bash
# Gerar dry-run SQL
cd backend/db_migrations
alembic upgrade head --sql > review.sql

# Reverter última migration
alembic downgrade -1

# Criar nova migration
alembic revision -m "description"

# Ver histórico de migrations
alembic history

# Executar testes específicos
pytest backend/app/tests/ -k "test_membership" -v

# Ver cobertura de testes
pytest --cov=backend/app --cov-report=html
open htmlcov/index.html

# Rodar servidor com hot reload
uvicorn backend.app.main:app --reload --log-level debug

# Gerar hash de senha
python -c "from backend.app.core.security import hash_password; print(hash_password('senha123'))"
```

### C. Estrutura de Auditoria

**Exemplo de log em audit_logs (R31, R32, RDB5):**

```json
{
  "id": "uuid",
  "entity": "match",
  "entity_id": "uuid",
  "action": "correction",
  "actor_user_id": "uuid",
  "actor_person_id": "uuid",
  "actor_role": "coordenador",
  "justification": "Correção de gol mal anotado",
  "context": {
    "old_value": {"goals": 15},
    "new_value": {"goals": 14},
    "admin_note": "Gol foi anotado em duplicidade"
  },
  "timestamp": "2025-12-24T10:30:00Z",
  "request_id": "uuid"
}
```

### D. Referências RAG Rápidas

| Regra | Descrição | Enforcement |
|-------|-----------|-------------|
| **RDB1** | PostgreSQL 17 + pgcrypto | 7.1 (DB only) |
| **RDB2** | PKs são UUID v4 server-generated | 7.1 (DB only) |
| **RDB3** | timestamptz em UTC | 7.1 (DB only) |
| **RDB4** | Soft delete obrigatório | 7.1 (DB trigger) |
| **RDB5** | audit_logs imutável | 7.1 (DB trigger) |
| **RDB6** | 1 Super Admin único | 7.1 (DB constraint) |
| **RDB9** | Vínculos sem sobreposição | 7.1 (DB EXCLUDE) |
| **RDB10** | team_registrations com períodos | 7.1 (DB EXCLUDE) |
| **R3** | Super Admin vitalício | 7.2 (DB + Backend) |
| **R13** | Estados de atleta (ativa, lesionada, dispensada) | 7.2 (DB + Backend) |
| **R42** | Sem vínculo = modo leitura | 7.2 (Backend) |
| **RF3** | Vínculo ativo obrigatório | 7.2 (Backend) |
| **RD2, RD3** | Validação etária de categoria | 7.2 (DB trigger + Backend) |

---

## 🎉 CONCLUSÃO

Este manual fornece um caminho **canônico** e **sem retrabalho** para desenvolvimento do backend do HB Tracking.

**Próximos passos:**

1. ✅ Seguir FASE 0-1 para setup inicial
2. ✅ Implementar FASE 2 (núcleo do backend)
3. ✅ Definir FASE 3 (contrato da API)
4. ✅ FASE 4 (FastAPI mínimo rodando)
5. ⏳ **FASE 5 (ITERATIVO)**: Implementar CRUDs seguindo template (persons, users, memberships, etc.)
6. ⏳ FASE 6 (substituir mocks por JWT real)
7. ⏳ FASE 7 (preparar para produção)
8. ⏳ FASE 8 (validação final)

**Conformidade RAG:**
- ✅ 97% de aderência (análise de [review_with_improvements.sql](../review_with_improvements.sql))
- ✅ VIEW para status de temporadas (performance)
- ✅ 16 triggers documentados (manutenibilidade)

**Contato de Suporte:**
- Repositório: [GitHub - HB Tracking]
- Documentação RAG: [regras-sistema-v1.1_Version2.md](regras-sistema-v1.1_Version2.md)

---

**Versão do Manual:** 1.0
**Última Atualização:** 2025-12-24
**Status:** ✅ Completo e pronto para uso
