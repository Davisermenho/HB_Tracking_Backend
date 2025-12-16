-- Tabela de equipes (com organização e treinador opcional)
CREATE TABLE equipes (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    categoria VARCHAR(50),
    organization_id UUID NOT NULL,
    treinador_id UUID REFERENCES usuarios(user_id)
);
