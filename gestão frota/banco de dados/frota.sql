-- Criação do Banco de Dados
CREATE DATABASE IF NOT EXISTS gestao_frota;
USE gestao_frota;

-- 1. Tabela Motorista
CREATE TABLE Motorista (
    id_motorista INT AUTO_INCREMENT,
    nome VARCHAR(100) NOT NULL,
    cnh VARCHAR(20) NOT NULL UNIQUE,
    categoria_cnh VARCHAR(5) NOT NULL,
    telefone VARCHAR(20),
    CONSTRAINT PK_Motorista PRIMARY KEY (id_motorista)
);

-- 2. Tabela Veiculo
CREATE TABLE Veiculo (
    id_veiculo INT AUTO_INCREMENT,
    placa VARCHAR(10) NOT NULL UNIQUE,
    modelo VARCHAR(50) NOT NULL,
    ano INT NOT NULL,
    quilometragem INT NOT NULL,
    id_motorista INT,
    CONSTRAINT PK_Veiculo PRIMARY KEY (id_veiculo),
    CONSTRAINT FK_Veiculo_Motorista FOREIGN KEY (id_motorista) 
        REFERENCES Motorista(id_motorista) ON DELETE SET NULL
);

-- 3. Tabela Mecanico
CREATE TABLE Mecanico (
    id_mecanico INT AUTO_INCREMENT,
    nome VARCHAR(100) NOT NULL,
    especialidade VARCHAR(50) NOT NULL,
    turno VARCHAR(20) NOT NULL,
    CONSTRAINT PK_Mecanico PRIMARY KEY (id_mecanico)
);

-- 4. Tabela Peca
CREATE TABLE Peca (
    id_peca INT AUTO_INCREMENT,
    nome VARCHAR(100) NOT NULL,
    fabricante VARCHAR(100),
    valor DECIMAL(10,2) NOT NULL,
    qtd_estoque INT NOT NULL DEFAULT 0,
    estoque_minimo INT NOT NULL DEFAULT 5,
    CONSTRAINT PK_Peca PRIMARY KEY (id_peca)
);

-- 5. Tabela Manutencao
CREATE TABLE Manutencao (
    id_manutencao INT AUTO_INCREMENT,
    data_manutencao DATE NOT NULL,
    tipo VARCHAR(20) NOT NULL,
    descricao TEXT,
    custo_total DECIMAL(10,2) DEFAULT 0.00,
    id_veiculo INT NOT NULL,
    id_mecanico INT NOT NULL,
    CONSTRAINT PK_Manutencao PRIMARY KEY (id_manutencao),
    CONSTRAINT FK_Manutencao_Veiculo FOREIGN KEY (id_veiculo) 
        REFERENCES Veiculo(id_veiculo) ON DELETE CASCADE,
    CONSTRAINT FK_Manutencao_Mecanico FOREIGN KEY (id_mecanico) 
        REFERENCES Mecanico(id_mecanico) ON DELETE RESTRICT
);

-- 6. Tabela Associativa: Item_Manutencao (N:M Manutencao - Peca)
CREATE TABLE Item_Manutencao (
    id_item INT AUTO_INCREMENT,
    id_manutencao INT NOT NULL,
    id_peca INT NOT NULL,
    quantidade INT NOT NULL,
    valor_unitario DECIMAL(10,2) NOT NULL,
    CONSTRAINT PK_ItemManutencao PRIMARY KEY (id_item),
    CONSTRAINT FK_Item_Manutencao FOREIGN KEY (id_manutencao) 
        REFERENCES Manutencao(id_manutencao) ON DELETE CASCADE,
    CONSTRAINT FK_Item_Peca FOREIGN KEY (id_peca) 
        REFERENCES Peca(id_peca) ON DELETE RESTRICT
);