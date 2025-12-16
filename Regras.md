# Relatório de Regras — Implementadas vs Faltando

## Fontes analisadas
- Código: `app/routes/*.py` (usuario, auth, equipe, atleta, membership, team_staff, presenca, video), `app/deps.py`, `app/schemas.py`, `app/models.py`
- SQL: `app/sql/*.sql`
- Testes: `app/tests/test_usuarios_smoke.py`

## A) Autenticação (login/token)
- IMPLEMENTADA — Login em `/usuarios/login` gera JWT com `sub=user_id`, `role_id`, `organization_id`, `must_change_password`. **Onde:** `app/routes/usuario.py` (login). **Prova:** select por `user_email` + `create_access_token({... "must_change_password": must_change})`. **Teste:** `test_01_login_dirigente_ok`, `test_03_new_user_login_returns_must_change_password_true`.
- IMPLEMENTADA — Endpoint `/login` (auth) similar, mas não filtra `deleted_at`. **Onde:** `app/routes/auth.py` (login). **Prova:** select por `user_email`, sem `deleted_at` check. **Teste:** sem teste.
- FALTANDO — Refresh/logout; rotação de secret. **Teste:** sem teste.

## B) Segurança (lock, tentativas, expiração de senha temporária)
- IMPLEMENTADA — Lock após 5 falhas por 60 minutos; reseta em sucesso. **Onde:** `app/routes/usuario.py` (LOCK_THRESHOLD=5, LOCK_MINUTES=60) e `app/routes/auth.py`. **Prova:** incrementa `failed_login_count`, seta `locked_until = now + 60min`. **Teste:** `test_06_lock_after_5_wrong_attempts`, `test_09_successful_login_resets_failed_count_and_lock`, `test_10_login_blocked_while_locked_even_with_correct_password`.
- PARCIAL — Bloqueio por `must_change_password` + `temp_password_expires_at` no passado. **Onde:** `app/routes/usuario.py` login. **Prova:** `if user.must_change_password and ... now > temp_password_expires_at: raise 403`. **Teste:** `test_07_temp_password_expired_blocks_login`.
- FALTANDO — Caso `must_change_password=True` com `temp_password_expires_at=NULL` deveria bloquear; hoje permite (teste falha). **Teste:** `test_08_temp_password_null_with_must_change_should_block`.

## C) Primeiro acesso / troca de senha
- IMPLEMENTADA — Criação de usuário força `must_change_password=True` e `temp_password_expires_at` (+7d). **Onde:** `app/routes/usuario.py` create_usuario. **Prova:** define `must_change_password=True`, `temp_password_expires_at=expires`. **Teste:** `test_02_create_user_forces_must_change_password_true`.
- IMPLEMENTADA — POST `/usuarios/change-password` atualiza `password_hash`, zera `must_change_password`, seta `password_changed_at`. **Onde:** `app/routes/usuario.py` change_password. **Teste:** `test_05_change_password_unlocks_user`.
- PARCIAL — Guard global `get_active_user` bloqueia `must_change_password` em rotas, mas `/auth.py` não usa. **Onde:** `app/deps.py` get_active_user. **Teste:** `test_04_block_access_until_change_password`.

## D) Organização
- IMPLEMENTADA — Todos os recursos principais têm `organization_id` obrigatório e comparam com `current_user.organization_id`. **Onde:** `app/routes/equipe.py`, `atleta.py`, `membership.py`, `team_staff.py`, `presenca.py`, `video.py`, `usuario.py` (list/get). **Prova:** checks `if payload.org_id != current_user.org_id` ou filtros `where organization_id == current_user.organization_id`. **Teste:** `test_15_cross_org_user_not_visible` (usuários).
- FALTANDO — Endpoints para criar/gerir organizations não existem; schema não prevê org nula. **Teste:** sem teste.

## E) RBAC (dirigente/coordenador/treinador/atleta)
- PARCIAL — `require_role` suporta ids/nomes; usado pontualmente (team_staff exige dirigente/coordenador; equipe bloqueia atleta; memberships bloqueia atleta). **Onde:** `app/deps.py`, `app/routes/team_staff.py`, `equipe.py`, `membership.py`. **Prova:** uso de `get_role_name` e `user_is_staff_of_team`. **Teste:** indireto (smoke cobre fluxos de treinador/dirigente).
- FALTANDO — Papel “coordenador” pouco aplicado; RBAC não padronizado em todos os endpoints; `/auth.py` sem checagem de role. **Teste:** sem teste.

## F) Escopo de leitura/gravação por role
- IMPLEMENTADA — Atleta: só lê equipes onde tem membership; só vê próprio registro; vídeos e presenças filtrados pelas equipes/membership. **Onde:** `app/routes/equipe.py` (list/get com membership), `atleta.py` (list/get), `video.py` e `presenca.py` (filters). **Teste:** sem teste direto.
- IMPLEMENTADA — Treinador: restrito a equipes onde é staff para equipes/atletas/presenças/vídeos/memberships. **Onde:** `app/routes/*` mencionados com `user_is_staff_of_team` e filtros TeamStaff. **Teste:** sem teste direto.
- IMPLEMENTADA — Dirigente/coordenador: acesso amplo à organização (default). **Onde:** mesmas rotas (não bloqueiam). **Teste:** indireto via criação/listagens.
- FALTANDO — Escopo para usuários por role (todos veem todos da org); leitura de roles inexistente; coordinador não diferenciado. **Teste:** sem teste.

## G) Soft delete (deleted_at)
- IMPLEMENTADA — `usuarios` possui `deleted_at`; list/get filtram; delete faz soft delete. **Onde:** `app/routes/usuario.py` (list_usuarios, get_usuario, delete_usuario). **Prova:** filtros `deleted_at is None`; delete seta `deleted_at` e `is_active=False`. **Teste:** `test_16_soft_delete_blocks_login_and_get`.
- PARCIAL — `/auth.py` login não filtra `deleted_at`; associações não checam usuários deletados. **Teste:** sem teste.

## H) Regras de integridade do banco
- IMPLEMENTADA — Unicidade: `user_email`, `role_name`, membership (equipe_id, atleta_id), team_staff (equipe_id, user_id, staff_role). **Onde:** `app/models.py` UniqueConstraint; `app/sql/*`. **Teste:** `test_11_create_user_duplicate_email_fails`.
- IMPLEMENTADA — Role FK e checagem de existência em create/update. **Onde:** `app/routes/usuario.py` role validation. **Teste:** `test_12_create_user_invalid_role_fails`.
- PARCIAL — Check constraint `chk_temp_password_required` no banco (bloqueia must_change_password TRUE com temp_password_expires_at NULL), mas lógica não trata mensagem amigável. **Prova:** erro em `test_08_temp_password_null_with_must_change_should_block`. **Teste:** `test_08_temp_password_null_with_must_change_should_block` (falha).

## Checklist do que falta
- Alta: Bloquear must_change_password com temp_password_expires_at NULL (ajustar login/fluxo e/ou relaxar constraint vs teste).
- Alta: Garantir API estável/health antes de testes (timeouts nos testes 01-03).
- Média: Aplicar RBAC consistente (coordenador/dirigente) em todas as rotas e em `/auth.py` (deleted_at, is_active, must_change_password).
- Média: Endpoints de organizations (criação/lista) ou documentar ausência.
- Baixa: Tratamento de deleted_at em auth geral e associações; refresh/logout tokens.

## Endpoints por recurso (método/caminho/quem pode)
- Usuários: POST `/usuarios/` (auth; bloqueio para atleta), POST `/usuarios/login` (público), POST `/login` (público), GET/PUT/DELETE `/usuarios/{id}` (auth; mesma org; atleta bloqueado na prática), POST `/usuarios/change-password` (auth).
- Equipes: CRUD em `/equipes` (auth; atleta bloqueado; treinador apenas equipes dele; dirigente/coordenador livre na org).
- Atletas: CRUD em `/atletas` (auth; atleta bloqueado; treinador limitado a suas equipes; dirigente/coordenador livre).
- Memberships: `/memberships` CRUD (auth; atleta bloqueado; treinador apenas equipes dele).
- Team staff: `/team-staff` CRUD (auth; dirigente/coordenador).
- Presenças: `/presencas` CRUD (auth; atleta leitura limitada; treinador equipes dele; dirigente/coordenador livre).
- Vídeos: `/videos` CRUD (auth; atleta leitura limitada; treinador equipes dele; dirigente/coordenador livre).
- Organizations: não há endpoints.

## Gap list
- Ausência de endpoints/gestão de organizations.
- RBAC formal para coordenador/dirigente em todas as rotas.
- Login (/auth.py) sem filtro de deleted_at e sem guard must_change_password.
- Falta de refresh/logout.
- Tratamento explícito para temp_password_expires_at NULL (de acordo com teste esperado).

## Tabela (Regra | Status | Onde | Teste)
- Login JWT inclui role/org/must_change | Implementada | app/routes/usuario.py login | test_01, test_03
- Lock 5 tentativas / 60min | Implementada | app/routes/usuario.py, auth.py | test_06, test_10
- Reset contador no sucesso | Implementada | app/routes/usuario.py login | test_09
- Bloqueio senha provisória expirada | Implementada | app/routes/usuario.py login | test_07
- Bloqueio temp_password NULL | Faltando | app/routes/usuario.py login (não bloqueia) | test_08 (falha)
- must_change_password True em criação | Implementada | app/routes/usuario.py create_usuario | test_02
- Troca senha libera usuário | Implementada | app/routes/usuario.py change_password | test_05
- Soft delete usuarios (list/get/delete) | Implementada | app/routes/usuario.py | test_16
- Login ignora deleted_at em /auth.py | Faltando | app/routes/auth.py | sem teste
- Escopo org em equipes/atletas/etc | Implementada | app/routes/equipe.py, atleta.py, membership.py, presenca.py, video.py | test_15 (usuários)
- Atleta só lê onde é membro | Implementada | app/routes/equipe.py, atleta.py, presenca.py, video.py | sem teste
- Treinador limitado a equipes staff | Implementada | app/routes/equipe.py, atleta.py, membership.py, presenca.py, video.py | sem teste
- Dirigente/coordenador amplo | Parcial | require_role + rotas (team_staff) | sem teste
- Unicidade email usuário | Implementada | models.py + validação | test_11
- Role válido | Implementada | app/routes/usuario.py | test_12

## Conclusão — próximas 5 ações
1) Ajustar login/must_change_password para bloquear caso temp_password_expires_at esteja NULL (alinhar com test_08).  
2) Garantir disponibilidade da API/health antes de login (timeouts nos testes 01–03) — revisar servidor/ping.  
3) Filtrar deleted_at e must_change_password também em `/login` (auth.py) e padronizar guards.  
4) Formalizar RBAC: coordenador/dirigente claros em todas as rotas e documentação; considerar leitura de usuários por role.  
5) Considerar endpoint/fluxo de organizations e cobrir escopos por role/organização com testes adicionais.
