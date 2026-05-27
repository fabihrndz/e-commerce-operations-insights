import os
import pandas as pd
from sqlalchemy import create_engine, text

# --- CONFIGURACIÓN DE CONEXIÓN (Variables del sistema) ---
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", "3306")


def get_connection_string(db_name=None, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT):
    """
    Centraliza la creación de la URL. Por defecto usa el .env, 
    pero permite cambiar cualquier parámetro si se le pasa explícitamente.
    """
    if db_name:
        return f"mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}"
    return f"mysql+pymysql://{user}:{password}@{host}:{port}"


## 1️⃣ Crear Base de Datos
def create_database_if_not_exists(db_name):
    """Crea la base de datos si no existe usando la conexión por defecto."""
    connection_url = get_connection_string()  # Sin base de datos para la creación
    engine_server = create_engine(connection_url)
    
    try:
        with engine_server.begin() as con:
            con.execute(text(f"CREATE DATABASE IF NOT EXISTS {db_name}"))
            print(f"✅ Base de datos '{db_name}' verificada/creada con éxito.")
    finally:
        engine_server.dispose()


## 2️⃣ Cargar el DataFrame
def load_dataframe_to_mysql(df, table_name, db_name, if_exists="replace"):
    """Carga un DataFrame pidiéndote solo los datos esenciales."""
    connection_url = get_connection_string(db_name=db_name)
    engine = create_engine(connection_url)
    
    try:
        df.to_sql(table_name, con=engine, if_exists=if_exists, index=False)
        print(f"✅ Datos cargados exitosamente en la tabla '{table_name}'.")
    finally:
        engine.dispose()


## 3️⃣ Definir la Clave Primaria
def set_primary_key(table_name, pk_column, db_name):
    """Asigna la PK en la tabla indicada."""
    connection_url = get_connection_string(db_name=db_name)
    engine = create_engine(connection_url)
    
    try:
        with engine.begin() as con:
            con.execute(text(f"ALTER TABLE {table_name} MODIFY {pk_column} INT NOT NULL"))
            con.execute(text(f"ALTER TABLE {table_name} ADD PRIMARY KEY ({pk_column})"))
            print(f"✅ Clave primaria '{pk_column}' asignada en '{table_name}'.")
    finally:
        engine.dispose()

## 4️⃣ Función para definir una Clave Foránea (Foreign Key)
def set_foreign_key(fact_table, dimension_table, fk_column, db_name, pk_column=None):
    """
    Crea una relación de clave foránea entre una tabla de hechos y una de dimensión.
    Si pk_column no se define, se asume que se llama exactamente igual que fk_column.
    """
    if pk_column is None:
        pk_column = fk_column
        
    connection_url = get_connection_string(db_name=db_name)
    engine = create_engine(connection_url)
    
    # Nombre único para evitar conflictos de restricciones en MySQL
    constraint_name = f"fk_{fact_table}_{dimension_table}_{fk_column}"
    
    try:
        with engine.begin() as con:
            # 1. Asegurar que la columna en la tabla de hechos sea NOT NULL y del tipo correcto (INT)
            con.execute(text(f"ALTER TABLE {fact_table} MODIFY {fk_column} INT NOT NULL"))
            
            # 2. Añadir la Foreign Key con reglas de actualización/borrado en cascada
            query = f"""
                ALTER TABLE {fact_table}
                ADD CONSTRAINT {constraint_name}
                FOREIGN KEY ({fk_column}) 
                REFERENCES {dimension_table}({pk_column})
                ON DELETE CASCADE
                ON UPDATE CASCADE
            """
            con.execute(text(query))
            print(f"🔗 Relación creada: {fact_table}.{fk_column} ➡️ {dimension_table}.{pk_column}")
            
    except Exception as e:
        print(f"❌ Error al asignar la clave foránea en {fact_table}: {e}")
        raise
    finally:
        engine.dispose()