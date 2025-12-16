-- Tabela de usuários (novo esquema)
CREATE TABLE usuarios (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_nome VARCHAR(100) NOT NULL,
    user_email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role_id INTEGER NOT NULL REFERENCES roles(role_id),
    organization_id UUID NOT NULL,
    failed_login_count INTEGER NOT NULL DEFAULT 0,
    locked_until TIMESTAMP NULL,
    last_login_at TIMESTAMP NULL,
    password_changed_at TIMESTAMP NULL,
    temp_password_expires_at TIMESTAMP NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    must_change_password BOOLEAN NOT NULL DEFAULT FALSE,
    data_cadastro TIMESTAMP DEFAULT NOW()
);
