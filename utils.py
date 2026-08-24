"""Funciones de cálculo puro (sin nada de Streamlit ni matplotlib).

Separadas del dashboard para poder probarlas de forma aislada, por ejemplo
en un notebook, sin tener que levantar toda la app.
"""

from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler


def contar_outliers_iqr(df, columnas):
    """Cuenta cuántas observaciones caen fuera del rango 1.5×IQR, sumando todas las columnas dadas.

    Para cada columna se calcula el rango intercuartílico (Q3 - Q1) y se marca como
    outlier todo valor por debajo de Q1 - 1.5*IQR o por encima de Q3 + 1.5*IQR
    (la regla clásica usada también por los boxplots).
    """
    q1 = df[columnas].quantile(0.25)
    q3 = df[columnas].quantile(0.75)
    iqr = q3 - q1
    lo, hi = q1 - 1.5 * iqr, q3 + 1.5 * iqr

    es_outlier = (df[columnas] < lo) | (df[columnas] > hi)
    return int(es_outlier.sum().sum())


def calcular_silhouette(df, var_x, var_y):
    """Silhouette score de las especies, usando solo dos variables ya estandarizadas.

    Devuelve None si no hay dos variables distintas para comparar, o si quedó
    seleccionada una sola especie (el silhouette score no tiene sentido con 1 sola clase).
    """
    if var_x == var_y or df["species"].nunique() < 2:
        return None
    X = StandardScaler().fit_transform(df[[var_x, var_y]])
    return silhouette_score(X, df["species"])