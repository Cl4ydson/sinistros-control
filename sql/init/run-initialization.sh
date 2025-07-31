#!/bin/bash

# Wait for SQL Server to be ready
echo "Waiting for SQL Server to start..."
sleep 30s

# Run initialization scripts
echo "Running database initialization scripts..."

# Run each SQL script in order
for sql_file in /docker-entrypoint-initdb.d/*.sql; do
    if [ -f "$sql_file" ]; then
        echo "Executing $sql_file..."
        /opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P $MSSQL_SA_PASSWORD -d master -i "$sql_file"
        
        if [ $? -eq 0 ]; then
            echo "Successfully executed $sql_file"
        else
            echo "Error executing $sql_file"
        fi
    fi
done

echo "Database initialization completed."