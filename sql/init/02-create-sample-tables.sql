-- Create sample tables for the sinistros application
-- This script creates basic table structure

USE AUTOMACAO_BRSAMOR;
GO

-- Create Users table if it doesn't exist
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[users]') AND type in (N'U'))
BEGIN
    CREATE TABLE users (
        id INT IDENTITY(1,1) PRIMARY KEY,
        username NVARCHAR(50) NOT NULL UNIQUE,
        email NVARCHAR(100) NOT NULL UNIQUE,
        hashed_password NVARCHAR(255) NOT NULL,
        is_active BIT DEFAULT 1,
        created_at DATETIME2 DEFAULT GETDATE(),
        updated_at DATETIME2 DEFAULT GETDATE()
    );
    
    PRINT 'Table users created successfully.';
END
ELSE
BEGIN
    PRINT 'Table users already exists.';
END
GO

-- Create Sinistros table if it doesn't exist
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[sinistros]') AND type in (N'U'))
BEGIN
    CREATE TABLE sinistros (
        id INT IDENTITY(1,1) PRIMARY KEY,
        numero_sinistro NVARCHAR(50) NOT NULL UNIQUE,
        data_ocorrencia DATETIME2 NOT NULL,
        descricao NVARCHAR(MAX),
        status NVARCHAR(50) DEFAULT 'PENDENTE',
        valor_estimado DECIMAL(18,2),
        segurado NVARCHAR(100),
        tipo_sinistro NVARCHAR(50),
        created_at DATETIME2 DEFAULT GETDATE(),
        updated_at DATETIME2 DEFAULT GETDATE(),
        created_by INT,
        FOREIGN KEY (created_by) REFERENCES users(id)
    );
    
    PRINT 'Table sinistros created successfully.';
END
ELSE
BEGIN
    PRINT 'Table sinistros already exists.';
END
GO

-- Create an index on numero_sinistro for better performance
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_sinistros_numero_sinistro')
BEGIN
    CREATE INDEX IX_sinistros_numero_sinistro ON sinistros(numero_sinistro);
    PRINT 'Index IX_sinistros_numero_sinistro created successfully.';
END
GO

-- Create an index on status for better performance
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_sinistros_status')
BEGIN
    CREATE INDEX IX_sinistros_status ON sinistros(status);
    PRINT 'Index IX_sinistros_status created successfully.';
END
GO

-- Switch to dtbTransporte database
USE dtbTransporte;
GO

-- Create a basic transport table
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[transportes]') AND type in (N'U'))
BEGIN
    CREATE TABLE transportes (
        id INT IDENTITY(1,1) PRIMARY KEY,
        codigo NVARCHAR(50) NOT NULL UNIQUE,
        descricao NVARCHAR(255),
        status NVARCHAR(50) DEFAULT 'ATIVO',
        created_at DATETIME2 DEFAULT GETDATE(),
        updated_at DATETIME2 DEFAULT GETDATE()
    );
    
    PRINT 'Table transportes created successfully.';
END
ELSE
BEGIN
    PRINT 'Table transportes already exists.';
END
GO

PRINT 'Sample tables creation completed successfully.';