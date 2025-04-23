import pandas as pd

def read_table_file(file_path, has_headers=True, delimiters=None):
    """
    Reads a table file (CSV/TXT) with flexible delimiter detection.
    Returns a pandas DataFrame.
    """
    if delimiters is None:
        delimiters = [',', ';', '\t', '|', ' || ', ' | ']

    # Try pandas' automatic detection first
    try:
        df = pd.read_csv(file_path, engine='python', sep=None, header=0 if has_headers else None)
        if len(df.columns) > 1:
            if not has_headers:
                df.columns = [f"col{i+1}" for i in range(df.shape[1])]
            return df
    except Exception:
        pass

    # Try each delimiter
    for delimiter in delimiters:
        try:
            df = pd.read_csv(file_path, sep=delimiter, engine='python', header=0 if has_headers else None)
            if len(df.columns) > 1:
                if not has_headers:
                    df.columns = [f"col{i+1}" for i in range(df.shape[1])]
                return df
        except Exception:
            continue

    raise ValueError("Could not detect delimiter or parse file.")

# You can add more functions for NetCDF, Excel, etc.