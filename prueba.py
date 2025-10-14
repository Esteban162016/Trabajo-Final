import pandas as pd

sg = pd.read_csv('sorgo.csv')
print(f"Datos cargados correctamente. Fila {len(sg)}, Columnas: {len(sg.columns)}.")
