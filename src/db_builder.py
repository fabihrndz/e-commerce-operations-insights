import os
import re
import pandas as pd
from urllib.parse import quote_plus
from sqlalchemy import create_engine, text

def _validate_identifier(identifier, identifier_name="identifier"):
    """
    Validates that an identifier (table/column/db name) contains only safe characters.
    Raises ValueError if validation fails.
    """
    if not re.match(r'^[A-Za-z0-9_]+$', identifier):
        raise ValueError(
            f"Invalid {identifier_name}: '{identifier}'. "
            f"Only alphanumeric characters and underscores allowed."
        )

def get_connection_string(db_name=None, user=None, password=None, host=None, port=None):
    """
    Centraliza la creación de la URL de forma dinámica.
    Resuelve problemas de importación y añade la barra de seguridad para SQLAlchemy.
    Credentials are URL-encoded to handle special characters.
    """
    # Evaluación dinámica: si es None, va a buscarlo al entorno en este instante
    user = user or os.getenv("DB_USER")
    password = password or os.getenv("DB_PASSWORD") or os.getenv("DB_PASS")
    host = host or os.getenv("DB_HOST")
    port = port or os.getenv("DB_PORT", "3306")
    
    # URL-encode credentials to handle special characters
    user_quoted = quote_plus(user) if user else ""
    password_quoted = quote_plus(password) if password else ""
    
    if db_name:
        return f"mysql+pymysql://{user_quoted}:{password_quoted}@{host}:{port}/{db_name}"
    return f"mysql+pymysql://{user_quoted}:{password_quoted}@{host}:{port}/"


## 1️⃣ Crear Base de Datos
def create_database_if_not_exists(db_name):
    """Crea la base de datos si no existe usando la conexión por defecto."""
    _validate_identifier(db_name, "database_name")
    
    connection_url = get_connection_string()
    engine_server = create_engine(connection_url)
    
    try:
        with engine_server.begin() as con:
            con.execute(text(f"CREATE DATABASE IF NOT EXISTS `{db_name}`"))
            print(f"Database '{db_name}' verified/created successfully.")
    except Exception as e:
        raise RuntimeError(f"Database creation failed: {e}") from e
    finally:
        engine_server.dispose()


## 2️⃣ Cargar el DataFrame
def load_dataframe_to_mysql(df, table_name, db_name, if_exists="replace"):
    """Carga un DataFrame pidiéndote solo los datos esenciales."""
    connection_url = get_connection_string(db_name=db_name)
    engine = create_engine(connection_url)
    
    try:
        df.to_sql(table_name, con=engine, if_exists=if_exists, index=False)
        print(f"Data loaded successfully into table '{table_name}'.")
    finally:
        engine.dispose()


## 3️⃣ Definir la Clave Primaria
def set_primary_key(table_name, pk_column, db_name, data_type="INT"):
    """
    Asigna la PK en la tabla indicada. 
    Permite cambiar el tipo de dato (por defecto INT) por si tu clave es VARCHAR.
    Validates that the column exists before modifying and checks for existing constraints.
    """
    _validate_identifier(table_name, "table_name")
    _validate_identifier(pk_column, "pk_column")
    
    connection_url = get_connection_string(db_name=db_name)
    engine = create_engine(connection_url)
    
    try:
        with engine.begin() as con:
            # Check if column exists
            result = con.execute(
                text(
                    "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS "
                    "WHERE TABLE_NAME = :table_name AND TABLE_SCHEMA = :db_name "
                    "AND COLUMN_NAME = :column_name"
                ),
                {"table_name": table_name, "db_name": db_name, "column_name": pk_column}
            )
            if not result.fetchone():
                raise ValueError(f"Column '{pk_column}' does not exist in table '{table_name}'")
            
            # Check if primary key already exists
            pk_result = con.execute(
                text(
                    "SELECT CONSTRAINT_NAME FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS "
                    "WHERE TABLE_NAME = :table_name AND TABLE_SCHEMA = :db_name "
                    "AND CONSTRAINT_TYPE = 'PRIMARY KEY'"
                ),
                {"table_name": table_name, "db_name": db_name}
            )
            if pk_result.fetchone():
                raise RuntimeError(f"Primary key already exists on table '{table_name}'")
            
            # Primero modificamos la columna para asegurarnos que no acepte nulos
            con.execute(text(f"ALTER TABLE `{table_name}` MODIFY `{pk_column}` {data_type} NOT NULL"))
            con.execute(text(f"ALTER TABLE `{table_name}` ADD PRIMARY KEY (`{pk_column}`)"))
            print(f"Primary key '{pk_column}' ({data_type}) assigned to '{table_name}'.")
    finally:
        engine.dispose()


## 4️⃣ Función para definir una Clave Foránea (Foreign Key)
def set_foreign_key(fact_table, dimension_table, fk_column, db_name, pk_column=None, data_type="INT"):
    """
    Crea una relación de clave foránea entre una tabla de hechos y una de dimensión.
    
    The data_type parameter specifies the type for the FK column. 
    IMPORTANT: This function modifies only the FK column; it does NOT modify the dimension table's PK column.
    You must ensure that the PK column in dimension_table already has the SAME type as data_type,
    or the foreign key constraint will fail.
    
    Args:
        fact_table: Table containing the foreign key
        dimension_table: Referenced dimension table
        fk_column: Column name in fact_table that will be the FK
        db_name: Database name
        pk_column: Column name in dimension_table (defaults to fk_column if not specified)
        data_type: SQL data type for the FK column (must match the PK column type)
    """
    _validate_identifier(fact_table, "fact_table")
    _validate_identifier(dimension_table, "dimension_table")
    _validate_identifier(fk_column, "fk_column")
    
    if pk_column is None:
        pk_column = fk_column
    else:
        _validate_identifier(pk_column, "pk_column")
        
    connection_url = get_connection_string(db_name=db_name)
    engine = create_engine(connection_url)
    
    constraint_name = f"fk_{fact_table}_{dimension_table}_{fk_column}"
    if len(constraint_name) > 64:  # MySQL constraint name limit
        constraint_name = f"fk_{hash((fact_table, dimension_table, fk_column)) & 0xFFFFFF:06x}"
    
    try:
        with engine.begin() as con:
            # Verify FK column exists in fact_table
            fk_col_result = con.execute(
                text(
                    "SELECT DATA_TYPE, IS_NULLABLE FROM INFORMATION_SCHEMA.COLUMNS "
                    "WHERE TABLE_NAME = :fact_table AND TABLE_SCHEMA = :db_name "
                    "AND COLUMN_NAME = :fk_column"
                ),
                {"fact_table": fact_table, "db_name": db_name, "fk_column": fk_column}
            )
            fk_col_info = fk_col_result.fetchone()
            if not fk_col_info:
                raise ValueError(f"Foreign key column '{fk_column}' does not exist in '{fact_table}'")
            
            # Verify PK column exists in dimension_table
            pk_col_result = con.execute(
                text(
                    "SELECT DATA_TYPE, IS_NULLABLE FROM INFORMATION_SCHEMA.COLUMNS "
                    "WHERE TABLE_NAME = :dimension_table AND TABLE_SCHEMA = :db_name "
                    "AND COLUMN_NAME = :pk_column"
                ),
                {"dimension_table": dimension_table, "db_name": db_name, "pk_column": pk_column}
            )
            pk_col_info = pk_col_result.fetchone()
            if not pk_col_info:
                raise ValueError(f"Primary key column '{pk_column}' does not exist in '{dimension_table}'")
            
            # Check for existing foreign key constraint
            constraint_result = con.execute(
                text(
                    "SELECT CONSTRAINT_NAME FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS "
                    "WHERE TABLE_NAME = :fact_table AND TABLE_SCHEMA = :db_name "
                    "AND CONSTRAINT_TYPE = 'FOREIGN KEY' AND CONSTRAINT_NAME = :constraint_name"
                ),
                {"fact_table": fact_table, "db_name": db_name, "constraint_name": constraint_name}
            )
            if constraint_result.fetchone():
                raise RuntimeError(f"Foreign key constraint '{constraint_name}' already exists")
            
            # Modify FK column type and nullability
            con.execute(text(f"ALTER TABLE `{fact_table}` MODIFY `{fk_column}` {data_type} NOT NULL"))
            
            # Create the foreign key constraint
            query = f"""
                ALTER TABLE `{fact_table}`
                ADD CONSTRAINT {constraint_name}
                FOREIGN KEY (`{fk_column}`)
                REFERENCES `{dimension_table}`(`{pk_column}`)
                ON DELETE CASCADE
                ON UPDATE CASCADE
            """
            con.execute(text(query))
            print(f"Foreign key created: {fact_table}.{fk_column} -> {dimension_table}.{pk_column}")
            
    except Exception as e:
        raise RuntimeError(f"Error creating foreign key on {fact_table}: {e}") from e
    finally:
        engine.dispose()