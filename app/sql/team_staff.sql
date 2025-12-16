CREATE TABLE team_staff (
    id SERIAL PRIMARY KEY,
    equipe_id INTEGER NOT NULL REFERENCES equipes(id),
    user_id UUID NOT NULL REFERENCES usuarios(user_id),
    staff_role VARCHAR(50) NOT NULL,
    CONSTRAINT uq_team_staff_unique UNIQUE (equipe_id, user_id, staff_role)
);
