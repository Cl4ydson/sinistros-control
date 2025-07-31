-- Insert sample data for testing the application
-- This script creates initial test data

USE AUTOMACAO_BRSAMOR;
GO

-- Insert sample user if it doesn't exist
IF NOT EXISTS (SELECT 1 FROM users WHERE username = 'admin')
BEGIN
    INSERT INTO users (username, email, hashed_password, is_active)
    VALUES ('admin', 'admin@example.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 1);
    -- Password is "secret123" hashed with bcrypt
    
    PRINT 'Sample admin user created successfully.';
END
ELSE
BEGIN
    PRINT 'Admin user already exists.';
END
GO

-- Insert sample user if it doesn't exist
IF NOT EXISTS (SELECT 1 FROM users WHERE username = 'user')
BEGIN
    INSERT INTO users (username, email, hashed_password, is_active)
    VALUES ('user', 'user@example.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 1);
    -- Password is "secret123" hashed with bcrypt
    
    PRINT 'Sample regular user created successfully.';
END
ELSE
BEGIN
    PRINT 'Regular user already exists.';
END
GO

-- Insert sample sinistros data
DECLARE @admin_id INT = (SELECT id FROM users WHERE username = 'admin');

IF NOT EXISTS (SELECT 1 FROM sinistros WHERE numero_sinistro = 'SIN-2025-001')
BEGIN
    INSERT INTO sinistros (numero_sinistro, data_ocorrencia, descricao, status, valor_estimado, segurado, tipo_sinistro, created_by)
    VALUES 
    ('SIN-2025-001', '2025-01-15 10:30:00', 'Colisão traseira em cruzamento', 'PENDENTE', 15000.00, 'João Silva', 'AUTOMOTIVO', @admin_id),
    ('SIN-2025-002', '2025-01-16 14:45:00', 'Incêndio em residência', 'EM_ANALISE', 75000.00, 'Maria Santos', 'RESIDENCIAL', @admin_id),
    ('SIN-2025-003', '2025-01-17 09:15:00', 'Roubo de veículo', 'APROVADO', 45000.00, 'Carlos Oliveira', 'AUTOMOTIVO', @admin_id),
    ('SIN-2025-004', '2025-01-18 16:20:00', 'Danos por granizo', 'REJEITADO', 8000.00, 'Ana Costa', 'AUTOMOTIVO', @admin_id),
    ('SIN-2025-005', '2025-01-19 11:00:00', 'Vazamento de água', 'FINALIZADO', 12000.00, 'Pedro Almeida', 'RESIDENCIAL', @admin_id);
    
    PRINT 'Sample sinistros data inserted successfully.';
END
ELSE
BEGIN
    PRINT 'Sample sinistros data already exists.';
END
GO

-- Switch to dtbTransporte database and insert sample data
USE dtbTransporte;
GO

IF NOT EXISTS (SELECT 1 FROM transportes WHERE codigo = 'TRANSP-001')
BEGIN
    INSERT INTO transportes (codigo, descricao, status)
    VALUES 
    ('TRANSP-001', 'Transporte Rodoviário - São Paulo', 'ATIVO'),
    ('TRANSP-002', 'Transporte Marítimo - Santos', 'ATIVO'),
    ('TRANSP-003', 'Transporte Aéreo - Guarulhos', 'ATIVO'),
    ('TRANSP-004', 'Transporte Ferroviário - MRS', 'INATIVO');
    
    PRINT 'Sample transport data inserted successfully.';
END
ELSE
BEGIN
    PRINT 'Sample transport data already exists.';
END
GO

PRINT 'Sample data insertion completed successfully.';