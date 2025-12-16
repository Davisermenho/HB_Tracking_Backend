# Hand Lab - Backend

Este é o backend do projeto **Hand Lab**, implementado com [FastAPI](https://fastapi.tiangolo.com/) e persistência em PostgreSQL (Neon.tech).

## Funcionalidades

- API REST para cadastro e autenticação de atletas e treinadores
- Gerenciamento de equipes
- Registro de presença em treinos/jogos
- Upload de vídeos (armazenamento em cloud)
- Autenticação com JWT e permissões básicas por perfil

## Como rodar localmente

1. **Crie e ative o ambiente virtual:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # ou .venv\Scripts\activate no Windows
   ```

2. **Instale as dependências:**
   ```bash
   pip install fastapi uvicorn python-dotenv psycopg2-binary sqlalchemy passlib[bcrypt] python-jose[cryptography]
   ```

3. **Configure o banco (Neon/Postgres) e o arquivo `.env` com as variáveis de conexão.**

4. **Rode o servidor:**
   ```bash
   uvicorn main:app --reload
   ```

5. **Acesse a documentação interativa:**  
   http://localhost:8000/docs

---

*Mais detalhes de endpoints e modelos serão adicionados com a evolução do projeto.*




Regras do Sistema



1. Cadastro de Usuário

O dirigente não pode ser criado via API; deve ser criado manualmente no banco de dados com um hash de senha já pronto.

Usuário pode ser criado por um dirigente ou coordenador, mas o role_id e organization_id são definidos pelo usuário logado.

Usuário precisa fornecer nome (user_nome), email (user_email), senha (password), papel (role_id), e outros detalhes de status como is_active, must_change_password.

O campo organization_id será automaticamente preenchido com a organization_id do usuário logado, não podendo ser fornecido pelo payload.

2. Senha Temporária (Primeiro Acesso)

A senha de primeiro acesso é sempre temporária.

Quando o usuário é criado, must_change_password é marcado como True, obrigando a troca de senha no primeiro login.

O sistema define o campo temp_password_expires_at, indicando quando a senha provisória expira.

Caso o usuário tente acessar a aplicação antes de trocar a senha ou a senha temporária tenha expirado, ele não poderá fazer login e receberá uma mensagem de erro (ex: “Senha temporária expirada”).

3. Login

Quando o usuário faz login com a senha temporária, ele deve ser redirecionado para a troca de senha via o endpoint /usuarios/change-password.

O sistema não permite login enquanto o campo must_change_password for True.

O campo must_change_password será alterado para False quando o usuário trocar sua senha, permitindo o login completo.

Login falho (senha errada) aumenta o contador failed_login_count, bloqueando o acesso por 1 hora após 5 tentativas erradas.

4. Bloqueio de Conta

Se o usuário ultrapassar 5 tentativas de login falhadas, sua conta será bloqueada por 1 hora (campo locked_until).

Durante o bloqueio, o sistema retornará um erro 403, informando o tempo restante do bloqueio.

5. Expiração de Senha Temporária

A senha temporária expira após 7 dias, e o usuário precisa mudar a senha antes de expirar (campo temp_password_expires_at).

Caso a senha tenha expirado, o usuário não pode fazer login e receberá um erro do tipo “Temporary password expired”.

6. Permissões por Role

Dirigente pode acessar todos os dados do sistema, inclusive de outras organizações.

Coordenador pode acessar somente dados da sua organização, como gerenciar equipes e usuários.

Treinador pode gerenciar somente as equipes para as quais é designado.

Atleta pode acessar somente os dados que lhe dizem respeito, como seu próprio perfil e suas presenças nas equipes.

7. Validações de Campos

O email do usuário deve ser único e case insensitive (CITEXT no banco).

O campo email deve seguir um formato válido (validado via expressão regular).

O nome de usuário (user_nome) deve ter entre 2 e 80 caracteres, e o email deve ter entre 5 e 100 caracteres.

As senhas devem ter um comprimento mínimo de 8 caracteres e máximo de 128 caracteres e devem incluir letras e números.

O CPF e o RG (caso usados) devem ser únicos no sistema e seguir formatos específicos.

8. Soft Delete

Se um usuário for inativo ou deletado, ele não pode ser listado ou acessar o sistema. O campo deleted_at é usado para marcar quando o usuário foi deletado.

9. Controle de Acesso com Tokens

O sistema utiliza tokens JWT para controle de acesso, e o token inclui informações como o ID do usuário, role, e organização.

O token contém a flag must_change_password, que será usada para forçar a troca de senha no primeiro login.

O sistema gera e envia o token de acesso ao usuário após login bem-sucedido.

10. Gestão de Permissões em Equipes e Membros

Membros de equipes são gerenciados dentro das permissões de seu papel (atleta, treinador, coordenador).

Apenas o treinador principal pode adicionar ou remover membros de sua equipe, e cada membro só pode estar em uma equipe em um determinado momento.

Coordenadores podem gerenciar múltiplos treinadores, mas não podem alterar o papel de outros coordenadores.

11. Regras de Organizações

Usuários com o papel de coordenador podem criar e gerenciar equipes, atletas, treinadores dentro da sua própria organização (definida pelo campo organization_id).

A organização do usuário logado é utilizada automaticamente na criação de equipes, atletas, e outros registros relacionados.

12. Relações de Foreign Key

O sistema usa chaves estrangeiras para relacionar role_id com roles, organization_id com organizations, entre outras tabelas.

As chaves estrangeiras garantem a integridade referencial no banco de dados.



13. Expiração da senha temporária

Usuário que acessa o sistema a primeira vez deve


14. Email imutável

No backend, o schema UsuarioUpdate nao pode permitir user_email. 


15. Lock de conta

errar senha 5 vezes (seu LOCK_THRESHOLD) → bloqueia (locked_until setado) e zera contador

tentar login durante lock → 403 com mensagem de lock

login após lock expirar + senha correta → libera e zera lock/contador

16. Regras de permissão e escopo

usuário com must_change_password=True tentando chamar endpoint que usa get_active_user → 403 Password change required

usuário de outra organization tentando GET/PUT/DELETE /usuarios/{id} → 404 (ou 403, mas do jeito que você fez hoje tende a 404)

list_usuarios só retorna usuários da mesma organization_id

17. Integridade / constraints

criar usuário com user_email já existente → 400

criar usuário com role_id inválido → 400

criar usuário sem auth (sem token) → 401

criar usuário com is_active=False e tentar login → 403 User is inactive

18.  Soft delete 
   
deletar usuário deveria marcar deleted_at (e não remover) e o GET/login não deve mais aceitar esse usuário




