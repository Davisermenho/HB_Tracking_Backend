# Test Log — Integração API (FastAPI)

Data: 2025-12-14

Objetivo:
- Documentar os testes de integração que exercitam os endpoints CRUD para `Usuario`, `Equipe` e `Atleta`.

Ambiente:
- Servidor local: http://127.0.0.1:8000 (uvicorn app.main:app --reload)
- Venv: `.venv` (Python usado: `.venv\Scripts\python.exe`)
- Script de teste: `app/tests/api_test.py`

Nota importante:
- Todos os testes automatizados devem residir em `/app/tests` (mover ou manter scripts de teste nessa pasta). A refatoração já alinhou os scripts para este diretório.
- Ao executar localmente, exportar `PYTHONPATH` para a raiz do projeto (Windows CMD: `set PYTHONPATH=.`) para que imports absolutos funcionem.

Resumo dos testes executados:

- Usuario CRUD
  - POST /usuarios/ — cria usuário
    - Payload exemplo: {"nome":"Teste","email":"teste@example.com","senha":"senha","papel":"atleta"}
    - Validação: resposta 200 com objeto contendo `id`, `nome`, `email`, `papel`, `data_cadastro`.
    - Exemplo de saída verificada: `{'id': 1, 'nome': 'Teste', 'email': 'teste@example.com', 'papel': 'atleta', 'data_cadastro': '2025-12-14T05:10:21.551637'}`

  - GET /usuarios/ — lista
    - Validação: lista contém o usuário criado.

  - GET /usuarios/{id} — detalha
    - Validação: retorna o objeto com `id` correto.

  - PUT /usuarios/{id} — atualiza
    - Payload de atualização exemplo: {"nome":"Teste2","email":"teste2@example.com","senha":"nova","papel":"atleta"}
    - Validação: resposta 200 com campos atualizados (ex.: `nome` e `email`).

  - DELETE /usuarios/{id}
    - Validação: resposta com `{"ok": True}` e recurso removido.

  Autenticação / Token
    - Antes de acessar endpoints protegidos, realizar login em `POST /login` com payload: {"email": "...", "senha": "..."}
    - Resposta: `{ "access_token": "...", "token_type": "bearer" }`.
    - Incluir header nas chamadas protegidas: `Authorization: Bearer <access_token>`.

- Equipe & Atleta CRUD (fluxo integrado)
  - Criar treinador (usuário com `papel`="treinador").
  - POST /equipes/ — cria equipe vinculada ao treinador.
    - Exemplo: `{'id': 1, 'nome': 'Equipe A', 'categoria': 'juvenil', 'treinador_id': 2}`
  - POST /atletas/ — cria atleta vinculado à equipe.
    - Exemplo: `{'id': 1, 'nome': 'Atleta1', 'email': 'atleta1@example.com', 'nascimento': '2005-01-01', 'posicao': 'ala', 'equipe_id': 1}`
  - GET/PUT/DELETE aplicados para equipe e atleta; validações: status 200 e objetos coerentes.

Resultados (resumo):
- Todos os endpoints CRUD testados retornaram status 200 e payloads conforme esperado.
- Import-check executado: `app.main`, `app.models`, `app.schemas`, `config.config` — todos OK (executado com `PYTHONPATH` set).
- Check de esquema no banco confirmou as tabelas esperadas (ver `app/tests/check_db.py`).

Comandos para reproduzir os testes (Windows CMD):

```bat
set PYTHONPATH=.
.venv\Scripts\activate
uvicorn app.main:app --reload
python app\tests\api_test.py
python app\tests\check_db.py
```

Observações:
- Os testes usam JSON simples e validam apenas contratos básicos (status e presença de campos). Para testes mais robustos, integrar `pytest` + fixtures e asserts detalhados.
- Manter `app/tests` como único diretório de testes para evitar confusão e assegurar CI/runner consistência.

## 2025-12-14 23:27 (pytest smoke usuarios)
- Comandos:
  - `.\\.venv\\Scripts\\python.exe -m pytest -q app/tests/test_usuarios_smoke.py`
- Resumo: total=17, passed=0, failed=0, skipped=17
- PASSOU: nenhum
- FALHOU: nenhum
- SKIP:
  - test_01_login_dirigente_ok — DATABASE_URL nao definido
  - test_02_create_user_forces_must_change_password_true — DATABASE_URL nao definido
  - test_03_new_user_login_returns_must_change_password_true — DATABASE_URL nao definido
  - test_04_block_access_until_change_password — DATABASE_URL nao definido
  - test_05_change_password_unlocks_user — DATABASE_URL nao definido
  - test_06_lock_after_5_wrong_attempts — DATABASE_URL nao definido
  - test_07_temp_password_expired_blocks_login — DATABASE_URL nao definido
  - test_08_temp_password_null_with_must_change_should_block — DATABASE_URL nao definido
  - test_09_successful_login_resets_failed_count_and_lock — DATABASE_URL nao definido
  - test_10_login_blocked_while_locked_even_with_correct_password — DATABASE_URL nao definido
  - test_11_create_user_duplicate_email_fails — DATABASE_URL nao definido
  - test_12_create_user_invalid_role_fails — DATABASE_URL nao definido
  - test_13_create_user_requires_auth — DATABASE_URL nao definido
  - test_14_inactive_user_cannot_login — DATABASE_URL nao definido
  - test_15_cross_org_user_not_visible — DATABASE_URL nao definido
  - test_16_soft_delete_blocks_login_and_get — DATABASE_URL nao definido
  - test_17_update_forbids_user_email_field — DATABASE_URL nao definido

## 2025-12-15 01:55 (pytest smoke usuarios)
- Flags: DATABASE_URL_SET=true; BASE_URL_SET=false; DATABASE_URL_HAS_SSLMODE_REQUIRE=true; PING_STATUS=200
- Comandos:
  - `.venv\Scripts\python.exe --version` / `pip --version` / `python -m pytest --version`
  - `python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('DATABASE_URL_SET=' + str(bool(os.getenv('DATABASE_URL'))).lower()); print('BASE_URL_SET=' + str(bool(os.getenv('BASE_URL'))).lower()); du=os.getenv('DATABASE_URL',''); print('DATABASE_URL_HAS_SSLMODE_REQUIRE=' + str('sslmode=require' in du).lower());"`
  - `PowerShell: $env:BASE_URL='http://127.0.0.1:8000'` (BASE_URL não estava set)
  - `PowerShell: $env:DATABASE_URL='postgresql://neondb_owner:npg_fUn7GJZ3uBCi@ep-round-glitter-ahofbroz-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'`
  - `python -c "import os,requests; url=os.getenv('BASE_URL','http://127.0.0.1:8000')+'/ping-banco'; r=requests.get(url,timeout=10); print('PING_STATUS='+str(r.status_code)); print('PING_BODY='+r.text[:120])"`
  - `.venv\Scripts\python.exe -m pytest -q app/tests/test_usuarios_smoke.py`
- Resumo: total=17, passed=0, failed=0, skipped=17
- PASSOU: nenhum
- FALHOU: nenhum
- SKIP:
  - test_01_login_dirigente_ok — DATABASE_URL nao definido
  - test_02_create_user_forces_must_change_password_true — DATABASE_URL nao definido
  - test_03_new_user_login_returns_must_change_password_true — DATABASE_URL nao definido
  - test_04_block_access_until_change_password — DATABASE_URL nao definido
  - test_05_change_password_unlocks_user — DATABASE_URL nao definido
  - test_06_lock_after_5_wrong_attempts — DATABASE_URL nao definido
  - test_07_temp_password_expired_blocks_login — DATABASE_URL nao definido
  - test_08_temp_password_null_with_must_change_should_block — DATABASE_URL nao definido
  - test_09_successful_login_resets_failed_count_and_lock — DATABASE_URL nao definido
  - test_10_login_blocked_while_locked_even_with_correct_password — DATABASE_URL nao definido
  - test_11_create_user_duplicate_email_fails — DATABASE_URL nao definido
  - test_12_create_user_invalid_role_fails — DATABASE_URL nao definido
  - test_13_create_user_requires_auth — DATABASE_URL nao definido
  - test_14_inactive_user_cannot_login — DATABASE_URL nao definido
  - test_15_cross_org_user_not_visible — DATABASE_URL nao definido
  - test_16_soft_delete_blocks_login_and_get — DATABASE_URL nao definido
  - test_17_update_forbids_user_email_field — DATABASE_URL nao definido
## 2025-12-15 00:16 (pytest smoke usuarios, API indisponível)
- Flags: DATABASE_URL_SET=true; BASE_URL_SET=true; DATABASE_URL_HAS_SSLMODE_REQUIRE=true; PING_STATUS=timeout
- Comandos:
  - `$env:DATABASE_URL='...'; $env:BASE_URL='http://127.0.0.1:8000'; python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('DATABASE_URL_SET=' + str(bool(os.getenv('DATABASE_URL'))).lower()); print('BASE_URL_SET=' + str(bool(os.getenv('BASE_URL'))).lower()); du=os.getenv('DATABASE_URL',''); print('DATABASE_URL_HAS_SSLMODE_REQUIRE=' + str('sslmode=require' in du).lower());'"`
  - `$env:DATABASE_URL='...'; $env:BASE_URL='http://127.0.0.1:8000'; .\\.venv\\Scripts\\python.exe -c "import os,requests; url=os.getenv('BASE_URL','http://127.0.0.1:8000')+'/ping-banco'; print('PING_URL='+url); r=requests.get(url,timeout=10); print('PING_STATUS='+str(r.status_code)); print('PING_BODY='+r.text[:120])"` (timeout)
  - `$env:DATABASE_URL='...'; $env:BASE_URL='http://127.0.0.1:8000'; .\\.venv\\Scripts\\python.exe -m pytest -q app/tests/test_usuarios_smoke.py -vv`
- Resumo: total=17, passed=13, failed=4, skipped=0
- PASSOU: test_04_block_access_until_change_password; test_05_change_password_unlocks_user; test_06_lock_after_5_wrong_attempts; test_07_temp_password_expired_blocks_login; test_09_successful_login_resets_failed_count_and_lock; test_10_login_blocked_while_locked_even_with_correct_password; test_11_create_user_duplicate_email_fails; test_12_create_user_invalid_role_fails; test_13_create_user_requires_auth; test_14_inactive_user_cannot_login; test_15_cross_org_user_not_visible; test_16_soft_delete_blocks_login_and_get; test_17_update_forbids_user_email_field
- FALHOU:
  - test_01_login_dirigente_ok — requests.exceptions.ReadTimeout: HTTPConnectionPool(host='127.0.0.1', port=8000): Read timed out. (read timeout=20)
  - test_02_create_user_forces_must_change_password_true — requests.exceptions.ReadTimeout: HTTPConnectionPool(host='127.0.0.1', port=8000): Read timed out. (read timeout=20)
  - test_03_new_user_login_returns_must_change_password_true — requests.exceptions.ReadTimeout: HTTPConnectionPool(host='127.0.0.1', port=8000): Read timed out. (read timeout=20)
  - test_08_temp_password_null_with_must_change_should_block — sqlalchemy.exc.IntegrityError: (psycopg2.errors.CheckViolation) new row for relation "usuarios" violates check constraint "chk_temp_password_required"
- SKIP: nenhum
