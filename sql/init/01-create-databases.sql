-- Create databases for the sinistros application
-- This script will be executed when SQL Server container starts

USE master;
GO

-- Create AUTOMACAO_BRSAMOR database if it doesn't exist
IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = 'AUTOMACAO_BRSAMOR')
BEGIN
    CREATE DATABASE AUTOMACAO_BRSAMOR;
    PRINT 'Database AUTOMACAO_BRSAMOR created successfully.';
END
ELSE
BEGIN
    PRINT 'Database AUTOMACAO_BRSAMOR already exists.';
END
GO

-- Create dtbTransporte database if it doesn't exist
IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = 'dtbTransporte')
BEGIN
    CREATE DATABASE dtbTransporte;
    PRINT 'Database dtbTransporte created successfully.';
END
ELSE
BEGIN
    PRINT 'Database dtbTransporte already exists.';
END
GO

-- Set recovery model to SIMPLE for both databases (good for development/testing)
ALTER DATABASE AUTOMACAO_BRSAMOR SET RECOVERY SIMPLE;
ALTER DATABASE dtbTransporte SET RECOVERY SIMPLE;
GO

PRINT 'Database initialization completed successfully.';