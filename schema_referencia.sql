-- Script SQL - As migrações do Django gerarão estruturas correspondentes a este diagrama.
-- PostgreSQL (Supabase) - 15 Tabelas do Domínio Trilha

CREATE TABLE CURSO (
    id_curso SERIAL PRIMARY KEY,
    codigo VARCHAR(50) UNIQUE NOT NULL,
    nome VARCHAR(255) NOT NULL
);

CREATE TABLE USUARIO (
    id_usuario SERIAL PRIMARY KEY,
    id_curso INT NOT NULL REFERENCES CURSO(id_curso) ON DELETE PROTECT,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    senha_hash VARCHAR(255) NOT NULL,
    ativo BOOLEAN DEFAULT TRUE,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE MATRIZ (
    id_matriz SERIAL PRIMARY KEY,
    id_curso INT NOT NULL REFERENCES CURSO(id_curso) ON DELETE PROTECT,
    titulo VARCHAR(255) NOT NULL,
    ano INT NOT NULL CHECK (ano > 0),
    qtd_optativas_necessarias INT DEFAULT 0 CHECK (qtd_optativas_necessarias >= 0),
    versao INT NOT NULL CHECK (versao > 0),
    status VARCHAR(20) DEFAULT 'RASCUNHO' CHECK (status IN ('RASCUNHO', 'VIGENTE', 'ARQUIVADA')),
    UNIQUE(id_curso, titulo, ano, versao)
);

CREATE TABLE ALUNO (
    id_usuario INT PRIMARY KEY REFERENCES USUARIO(id_usuario) ON DELETE CASCADE,
    id_matriz_ativa INT REFERENCES MATRIZ(id_matriz) ON DELETE SET NULL
);

CREATE TABLE COORDENADOR (
    id_usuario INT PRIMARY KEY REFERENCES USUARIO(id_usuario) ON DELETE CASCADE
);

CREATE TABLE DISCIPLINA (
    id_disciplina SERIAL PRIMARY KEY,
    id_curso INT NOT NULL REFERENCES CURSO(id_curso) ON DELETE PROTECT,
    codigo VARCHAR(50) NOT NULL,
    nome VARCHAR(255) NOT NULL,
    ementa TEXT,
    UNIQUE(id_curso, codigo)
);

CREATE TABLE MATRIZ_DISCIPLINA (
    id_item_matriz SERIAL PRIMARY KEY,
    id_matriz INT NOT NULL REFERENCES MATRIZ(id_matriz) ON DELETE PROTECT,
    id_disciplina INT NOT NULL REFERENCES DISCIPLINA(id_disciplina) ON DELETE PROTECT,
    semestre INT NOT NULL CHECK (semestre > 0),
    creditos INT NOT NULL CHECK (creditos >= 0),
    tipo VARCHAR(50) NOT NULL,
    horas INT NOT NULL CHECK (horas >= 0),
    min_creditos INT DEFAULT 0 CHECK (min_creditos >= 0),
    UNIQUE(id_matriz, id_disciplina)
);

CREATE TABLE PRE_REQUISITO (
    id_item_dependente INT NOT NULL REFERENCES MATRIZ_DISCIPLINA(id_item_matriz) ON DELETE CASCADE,
    id_item_requisito INT NOT NULL REFERENCES MATRIZ_DISCIPLINA(id_item_matriz) ON DELETE CASCADE,
    PRIMARY KEY (id_item_dependente, id_item_requisito),
    CHECK (id_item_dependente <> id_item_requisito)
);

CREATE TABLE OFERTA (
    id_oferta SERIAL PRIMARY KEY,
    id_curso INT NOT NULL REFERENCES CURSO(id_curso) ON DELETE PROTECT,
    id_criador INT NOT NULL REFERENCES COORDENADOR(id_usuario) ON DELETE PROTECT,
    semestre_letivo VARCHAR(50) NOT NULL,
    data_publicacao TIMESTAMP,
    data_encerramento TIMESTAMP,
    status VARCHAR(20) DEFAULT 'RASCUNHO' CHECK (status IN ('RASCUNHO', 'PUBLICADA', 'ENCERRADA', 'CANCELADA')),
    criada_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
-- Índice único parcial que impede duas ofertas publicadas no mesmo curso simultaneamente
CREATE UNIQUE INDEX uq_oferta_publicada_curso ON OFERTA (id_curso) WHERE status = 'PUBLICADA';

CREATE TABLE ITEM_OFERTA (
    id_item_oferta SERIAL PRIMARY KEY,
    id_oferta INT NOT NULL REFERENCES OFERTA(id_oferta) ON DELETE CASCADE,
    id_disciplina INT NOT NULL REFERENCES DISCIPLINA(id_disciplina) ON DELETE PROTECT,
    UNIQUE(id_oferta, id_disciplina)
);

CREATE TABLE ENCONTRO (
    id_encontro SERIAL PRIMARY KEY,
    id_item_oferta INT NOT NULL REFERENCES ITEM_OFERTA(id_item_oferta) ON DELETE CASCADE,
    dia_semana INT NOT NULL CHECK (dia_semana BETWEEN 1 AND 7),
    horario_inicio TIME NOT NULL,
    horario_fim TIME NOT NULL,
    CHECK (horario_fim > horario_inicio)
);

CREATE TABLE PROGRESSO (
    id_progresso SERIAL PRIMARY KEY,
    id_aluno INT NOT NULL REFERENCES ALUNO(id_usuario) ON DELETE CASCADE,
    id_item_matriz INT NOT NULL REFERENCES MATRIZ_DISCIPLINA(id_item_matriz) ON DELETE PROTECT,
    situacao VARCHAR(50) NOT NULL,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(id_aluno, id_item_matriz)
);

CREATE TABLE PLANEJAMENTO (
    id_planejamento SERIAL PRIMARY KEY,
    id_aluno INT NOT NULL REFERENCES ALUNO(id_usuario) ON DELETE CASCADE,
    id_matriz INT NOT NULL REFERENCES MATRIZ(id_matriz) ON DELETE CASCADE,
    nome VARCHAR(255) NOT NULL,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE SEMESTRE_PLANEJAMENTO (
    id_semestre_planejamento SERIAL PRIMARY KEY,
    id_planejamento INT NOT NULL REFERENCES PLANEJAMENTO(id_planejamento) ON DELETE CASCADE,
    nome VARCHAR(255) NOT NULL,
    ordem INT NOT NULL CHECK (ordem > 0),
    UNIQUE(id_planejamento, ordem)
);

CREATE TABLE ITEM_PLANEJAMENTO (
    id_item_planejamento SERIAL PRIMARY KEY,
    id_semestre_planejamento INT NOT NULL REFERENCES SEMESTRE_PLANEJAMENTO(id_semestre_planejamento) ON DELETE CASCADE,
    id_item_matriz INT NOT NULL REFERENCES MATRIZ_DISCIPLINA(id_item_matriz) ON DELETE CASCADE,
    UNIQUE(id_semestre_planejamento, id_item_matriz)
);
