import re
import pandas as pd

def normalize_column(col: str) -> str:
    col = col.strip().lower() # Elimina espacial y convierte a minúsculas
    col = re.sub(r"[^\w\s]", "", col) # Quita todo lo que no sea letras
    col = re.sub(r"\s+", "_", col) # Reemplazar espacios por guiones bajos
    return col
 
 
def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    original = df.columns.tolist()
    normalized = [normalize_column(c) for c in original]
    return df.rename(columns=dict(zip(original, normalized)))