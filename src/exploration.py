try:
    from IPython.display import display
except ImportError:
    display = print


def info_df(dataframe, sample_n=5):
    """
    Genera un informe técnico del DataFrame: separa estadísticas por tipo de dato (str vs num),
    muestra dimensiones y describe el contenido.

    Parámetros:
    -----------
    dataframe : pandas.DataFrame
        El conjunto de datos a analizar.
    sample_n : int, opcional (default=5)
        Número de filas a mostrar en la previsualizaciones y muestras aleatorias.

    """

    print("\n" + "="*80)
    print("INFORME TÉCNICO DEL DATAFRAME")
    print("="*80)


     # Validación inicial
    if dataframe is None:
        print("❌ Error: El DataFrame es None.")
        return
    
    if not hasattr(dataframe, "shape"):
        print("❌ Error: El objeto proporcionado no es un DataFrame válido.")
        return

    if dataframe.empty:
        print("⚠️ El DataFrame está vacío. No hay datos que analizar.")
        return
    
  # Dimensiones
    print("\n🔹 Dimensiones:")
    print(f"- Filas: {dataframe.shape[0]}")
    print(f"- Columnas: {dataframe.shape[1]}")

    # Info general
    print("\n🔹 Info general:")
    try:
        dataframe.info()
    except Exception as e:
        print(f"❌ Error al mostrar dataframe.info(): {e}")

    # Nulos
    print("\n🔹 Nulos:")
    try:
        print(f"{dataframe.isna().sum()/dataframe.shape[0]*100}")
    except Exception as e:
        print(f"❌ Error al calcular nulos: {e}")

    # Duplicados
    print("\n🔹 Duplicados:")
    try:
        print(f"Total duplicados: {dataframe.duplicated().sum()}")
    except Exception as e:
        print(f"❌ Error al calcular duplicados: {e}")

    # Descriptivo cualitativo
    print("\n🔹 Descriptivo variables cualitativas:")
    try:
        qual_cols = dataframe.select_dtypes(include=['object', 'category'])
        if qual_cols.shape[1] > 0:
            display(qual_cols.describe().T)
        else:
            print("No hay variables cualitativas.")
    except Exception as e:
        print(f"❌ Error en descriptivo cualitativo: {e}")

    # Descriptivo cuantitativo
    print("\n🔹 Descriptivo variables cuantitativas:")
    try:
        num_cols = dataframe.select_dtypes(include='number')
        if num_cols.shape[1] > 0:
            display(num_cols.describe().T.round(2))
        else:
            print("No hay variables numéricas.")
    except Exception as e:
        print(f"❌ Error en descriptivo cuantitativo: {e}")

    print("\n🔹 Muestra del dataframe:")
    display(dataframe.sample(min(sample_n, len(dataframe))))