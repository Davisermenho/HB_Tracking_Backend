CREATE TABLE memberships (
    id SERIAL PRIMARY KEY,
    equipe_id INTEGER NOT NULL REFERENCES equipes(id),
    atleta_id INTEGER NOT NULL REFERENCES atletas(id),
    CONSTRAINT uq_membership_equipe_atleta UNIQUE (equipe_id, atleta_id)
);
