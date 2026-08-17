"""
Ejercicio 5: Diseño Visual y Narrativa de Datos
Dashboard interactivo (Streamlit) sobre el dataset Palmer Penguins.

Objetivo: comprobar visualmente que el dataset presenta valores faltantes,
outliers y alta separabilidad de clases para la tarea de clasificacion de
especies. Cuatro visualizaciones en grilla 2x2.

Ejecutar con:
    uv run streamlit run dashboard.py
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="Palmer Penguins — EDA", layout="wide")

sns.set_theme(style="whitegrid")
PALETA = {"Adelie": "#4C72B0", "Chinstrap": "#DD8452", "Gentoo": "#55A868"}


@st.cache_data
def cargar_datos():
    return sns.load_dataset("penguins")


datos = cargar_datos()
datos_completos = datos.dropna()

st.title("🐧 Palmer Penguins — Patrones, anomalías y separabilidad de especies")
st.markdown(
    """
El conjunto de datos **Palmer Penguins** presenta características típicas de un problema de EDA:
valores faltantes, presencia de outliers y alta separabilidad de clases para la tarea de
clasificación de especies. Este panel comprueba visualmente estas tres afirmaciones mediante
cuatro visualizaciones complementarias.
"""
)

with st.sidebar:
    st.header("Filtros")
    especies_sel = st.multiselect(
        "Especies a mostrar", options=sorted(datos["species"].dropna().unique()),
        default=sorted(datos["species"].dropna().unique()),
    )
    islas_sel = st.multiselect(
        "Islas a mostrar", options=sorted(datos["island"].dropna().unique()),
        default=sorted(datos["island"].dropna().unique()),
    )

datos_f = datos[datos["species"].isin(especies_sel) & datos["island"].isin(islas_sel)]
datos_f_completos = datos_f.dropna()

col_izq, col_der = st.columns(2)

# ---------------------------------------------------------------------------
# 1) Valores faltantes  (arriba - izquierda)
# ---------------------------------------------------------------------------
with col_izq:
    st.subheader("1. Valores faltantes por variable")
    faltantes = (
        datos_f.isnull().sum().rename("faltantes").reset_index().rename(columns={"index": "variable"})
    )
    faltantes = faltantes[faltantes["faltantes"] > 0].sort_values("faltantes", ascending=True)

    fig1, ax1 = plt.subplots(figsize=(5, 3.5))
    if len(faltantes) > 0:
        ax1.barh(faltantes["variable"], faltantes["faltantes"], color="#C44E52")
        ax1.set_xlabel("Cantidad de valores faltantes")
        ax1.set_title(f"Faltantes sobre {len(datos_f)} filas filtradas")
    else:
        ax1.text(0.5, 0.5, "Sin valores faltantes\nen la seleccion actual",
                  ha="center", va="center", fontsize=11)
        ax1.axis("off")
    st.pyplot(fig1, clear_figure=True)
    st.caption(
        "Evidencia una anomalía de calidad de datos: hay filas incompletas "
        "(principalmente en `sex` y en el bloque de medidas físicas), que deben tratarse "
        "antes de modelar."
    )

# ---------------------------------------------------------------------------
# 2) Outliers via boxplot  (arriba - derecha)
# ---------------------------------------------------------------------------
with col_der:
    st.subheader("2. Outliers en la masa corporal, por especie")
    fig2, ax2 = plt.subplots(figsize=(5, 3.5))
    if len(datos_f_completos) > 0:
        sns.boxplot(
            data=datos_f_completos, x="species", y="body_mass_g",
            hue="species", palette=PALETA, legend=False, ax=ax2,
            order=sorted(datos_f_completos["species"].unique()),
        )
        ax2.set_xlabel("Especie")
        ax2.set_ylabel("Masa corporal (g)")
    else:
        ax2.text(0.5, 0.5, "Sin datos para la seleccion actual", ha="center", va="center")
        ax2.axis("off")
    st.pyplot(fig2, clear_figure=True)
    st.caption(
        "El boxplot resume mediana, dispersión y valores atípicos por especie de un vistazo: "
        "permite comprobar si existen outliers y comparar la variabilidad de tamaño entre especies."
    )

col_izq2, col_der2 = st.columns(2)

# ---------------------------------------------------------------------------
# 3) Tendencia bivariada  (abajo - izquierda)
# ---------------------------------------------------------------------------
with col_izq2:
    st.subheader("3. Relación entre largo y profundidad del pico")
    fig3, ax3 = plt.subplots(figsize=(5, 3.5))
    if len(datos_f_completos) > 0:
        sns.scatterplot(
            data=datos_f_completos, x="bill_length_mm", y="bill_depth_mm",
            hue="species", palette=PALETA, alpha=0.75, ax=ax3,
        )
        for especie, sub in datos_f_completos.groupby("species", observed=True):
            if len(sub) > 1:
                m, b = np.polyfit(sub["bill_length_mm"], sub["bill_depth_mm"], 1)
                xs = np.linspace(sub["bill_length_mm"].min(), sub["bill_length_mm"].max(), 50)
                ax3.plot(xs, m * xs + b, color=PALETA.get(especie, "gray"), linewidth=1.5)
        ax3.set_xlabel("Largo del pico (mm)")
        ax3.set_ylabel("Profundidad del pico (mm)")
        ax3.legend(title="Especie", fontsize=8)
    else:
        ax3.text(0.5, 0.5, "Sin datos para la seleccion actual", ha="center", va="center")
        ax3.axis("off")
    st.pyplot(fig3, clear_figure=True)
    st.caption(
        "Sin segmentar por especie la correlación global parece negativa (paradoja de Simpson); "
        "al segmentar y trazar una tendencia por especie se revela una asociación positiva dentro "
        "de cada grupo, y patrones/agrupamientos claros por especie."
    )

# ---------------------------------------------------------------------------
# 4) Separabilidad de especies  (abajo - derecha)
# ---------------------------------------------------------------------------
with col_der2:
    st.subheader("4. Separabilidad de especies (aleta vs. masa corporal)")
    fig4, ax4 = plt.subplots(figsize=(5, 3.5))
    if len(datos_f_completos) > 0:
        sns.scatterplot(
            data=datos_f_completos, x="flipper_length_mm", y="body_mass_g",
            hue="species", style="species", palette=PALETA, s=55, alpha=0.8, ax=ax4,
        )
        ax4.set_xlabel("Largo de la aleta (mm)")
        ax4.set_ylabel("Masa corporal (g)")
        ax4.legend(title="Especie", fontsize=8)
    else:
        ax4.text(0.5, 0.5, "Sin datos para la seleccion actual", ha="center", va="center")
        ax4.axis("off")
    st.pyplot(fig4, clear_figure=True)
    st.caption(
        "Las tres especies forman agrupamientos casi no solapados en este par de variables, "
        "evidenciando la alta separabilidad de clases que hace de `species` una variable "
        "fácilmente predecible a partir de las medidas morfológicas."
    )

st.divider()
st.caption(
    "TP1 — Laboratorio de Datos II — UNL/FICH — Ejercicio 5. "
    "Fuente: Palmer Penguins (Gorman, Williams & Fraser, 2014) via seaborn."
)
