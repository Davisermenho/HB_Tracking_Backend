# Execution Log — Ações realizadas no backend

Data: 2025-12-14

Objetivo:
- Registrar as mudanças feitas no repositório para preparar a Fase 3 (ORM, schemas, rotas, refatoração de pacotes e execução de testes).

Ações (arquivos criados/alterados) e motivo:

- `sql/schema.sql` — criado
  - Contém os comandos SQL para criar as tabelas `usuarios`, `equipes`, `atletas`, `presencas`, `videos`.
  - Motivo: versionar o esquema SQL do MVP conforme as instruções.

- `config/config.py` — criado (refatoração de `config.py`)
  - Agora exporta `engine`, `SessionLocal` e `Base` (SQLAlchemy engine, session factory e declarative base).
  - Motivo: organizar configurações em pacote `config` e permitir importações absolutas (`from config.config import ...`).

- `app/models.py` — criado (moved from root)
  - Implementa os modelos SQLAlchemy: `Usuario`, `Equipe`, `Atleta`, `Presenca`, `Video`.
  - Motivo: mapear o esquema SQL para ORM e possibilitar operações via SQLAlchemy.

- `app/schemas.py` — criado (moved from root)
  - Contém classes Pydantic (Create/Out) para as entidades; atualizado para Pydantic v2 (`model_config = {"from_attributes": True}`).
  - Motivo: validação de entrada/saída nas rotas FastAPI e compatibilidade com `from_attributes`.

- `app/routes/` — criado (arquivos)
  - `app/routes/usuario.py`, `app/routes/equipe.py`, `app/routes/atleta.py`, `app/routes/presenca.py`, `app/routes/video.py`
  - Cada arquivo implementa CRUD (POST/GET/PUT/DELETE) usando dependência `get_db()` que provê `SessionLocal` importado de `config.config`.
  - Motivo: implementar endpoints iniciais do MVP dentro do pacote `app`.

- `app/main.py` — criado (moved from root)
  - Registra os routers e mantém rota `/ping-banco` para checagem de conexão.
  - Motivo: ponto de entrada do FastAPI agora como `app.main:app`.

- `app/tests/check_db.py` e `.vscode/testedb/check_db.py` — criados
  - Scripts para inspecionar o banco e garantir que as tabelas esperadas existem.
  - Motivo: verificação rápida de integridade do esquema no Neon/Postgres.

- `app/tests/api_test.py` — criado (moved from tests)
  - Script de teste que realiza chamadas HTTP contra o servidor local para verificar fluxo CRUD de `Usuario`, `Equipe` e `Atleta`.
  - Motivo: validação automática das rotas durante desenvolvimento; agora os scripts de teste ficam em `/app/tests`.

- `app/tests/import_check.py` — criado
  - Script para verificar importações após refatoração (`app.main`, `app.models`, `app.schemas`, `config.config`).

Resultados e verificações realizadas:

- Import-check (executado com `PYTHONPATH` apontando para a raiz do projeto):
  - `import app.main` — OK
  - `import app.models` — OK
  - `import app.schemas` — OK
  - `import config.config` — OK
  - Observação: ao executar sem `PYTHONPATH` os imports falharam; solução usada foi executar a partir da raiz com `PYTHONPATH=.\\` ou usar `uvicorn app.main:app`.

- Testes de integração (script `app/tests/api_test.py`):
  - Fluxos CRUD para `Usuario`, `Equipe`, `Atleta` executados contra `uvicorn app.main:app`.
  - Resultado: todas as chamadas retornaram status 200 e payloads conforme o contrato esperado.

- Check de esquema no banco (`app/tests/check_db.py`):
  - Resultado: Found tables: [`usuarios`, `equipes`, `atletas`, `presencas`, `videos`]. Todas as tabelas esperadas presentes.

Comandos executados durante verificação (exemplos; Windows CMD):

```bat
set PYTHONPATH=.
.venv\\Scripts\\activate
uvicorn app.main:app --reload
python app\\tests\\api_test.py
python app\\tests\\check_db.py
python app\\tests\\import_check.py
```

Observações e próximos passos recomendados:
- Adicionar `.env.example` ao repositório (sem credenciais reais).
- Converter `app/tests/api_test.py` para `pytest` com fixtures e asserts formais (melhor integração CI).
- Considerar Alembic para versão de migrações do schema.

Notas de implementação e decisões relevantes:
- Uso de imports absolutos (`from app...` e `from config.config...`) para evitar ambiguidade ao rodar o servidor ou testes.
- Atualização de Pydantic para v2: substituído `orm_mode = True` por `model_config = {"from_attributes": True}` nas classes de saída.
- Para executar `uvicorn` após refatoração usar `uvicorn app.main:app` ou garantir `PYTHONPATH` apontando para a raiz do projeto.
