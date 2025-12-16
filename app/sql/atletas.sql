-- Tabela de atletas (sem FK direta para equipe, usa memberships)
CREATE TABLE atletas (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    nascimento DATE,
    posicao VARCHAR(50),
    organization_id UUID NOT NULL
);
