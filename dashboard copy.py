"""Ejercicio 5: Diseño Visual y Narrativa de Datos.

Dashboard interactivo (Streamlit) que comprueba visualmente, en una grilla 2x2, las
afirmaciones típicas del EDA de Palmer Penguins: valores faltantes, outliers, tendencias
bivariadas y alta separabilidad entre especies. Cada panel abre con un título de acción y un
KPI/veredicto de color, y arriba de todo se arma una "Gran Idea" que resume el hallazgo
combinado, siguiendo los principios de narrativa de datos de Knaflic (2015).

Ejecutar con: uv run streamlit run dashboard.py
"""

import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

st.set_page_config(page_title="Palmer Penguins — EDA", page_icon="🐧", layout="wide")

FONDO = "#0E1117"
TARJETA = "#161B22"
TEXTO = "#E6E6E6"
GRILLA = "#30363D"
COLOR_OK = "#3FB950"
COLOR_WARN = "#D29922"
COLOR_BAD = "#F85149"
COLOR_INFO = "#58A6FF"
PALETA = {"Adelie": "#5B9BD5", "Chinstrap": "#F2A65A", "Gentoo": "#70C1A0"}
NUMERICAS = ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"]
ETIQUETAS = {
    "bill_length_mm": "Largo del pico (mm)",
    "bill_depth_mm": "Profundidad del pico (mm)",
    "flipper_length_mm": "Largo de la aleta (mm)",
    "body_mass_g": "Masa corporal (g)",
    "sex": "Sexo",
}

sns.set_theme(
    style="darkgrid",
    rc={
        "figure.facecolor": TARJETA,
        "axes.facecolor": TARJETA,
        "savefig.facecolor": TARJETA,
        "axes.edgecolor": GRILLA,
        "axes.labelcolor": TEXTO,
        "axes.titlecolor": TEXTO,
        "text.color": TEXTO,
        "xtick.color": TEXTO,
        "ytick.color": TEXTO,
        "grid.color": GRILLA,
        "legend.facecolor": TARJETA,
        "legend.edgecolor": GRILLA,
        "legend.labelcolor": TEXTO,
    },
)

st.markdown(
    f"""
    <style>
    div[data-testid="stMetric"] {{
        background-color: {TARJETA};
        border: 1px solid {GRILLA};
        border-radius: 0.6rem;
        padding: 0.8rem 1rem;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


def badge(texto, color):
    st.markdown(
        f'<div style="display:inline-block;background-color:{color}22;color:{color};'
        f'border:1px solid {color}66;padding:3px 12px;border-radius:999px;'
        f'font-size:0.82rem;font-weight:600;margin:0.4rem 0 0.3rem 0;">{texto}</div>',
        unsafe_allow_html=True,
    )


@st.cache_data
def cargar_datos():
    return sns.load_dataset("penguins")


def contar_outliers_iqr(df, columnas):
    total = 0
    for col in columnas:
        q1, q3 = df[col].quantile([0.25, 0.75])
        iqr = q3 - q1
        lo, hi = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        total += int(((df[col] < lo) | (df[col] > hi)).sum())
    return total


def calcular_silhouette(df, var_x, var_y):
    if var_x == var_y or df["species"].nunique() < 2:
        return None
    X = StandardScaler().fit_transform(df[[var_x, var_y]])
    return silhouette_score(X, df["species"])


pinguinos = cargar_datos()

st.title("🐧 Palmer Penguins: patrones, anomalías y separabilidad de especies")

st.sidebar.header("Filtros")
especies_sel = st.sidebar.multiselect(
    "Especies a incluir (paneles 2 a 4)",
    options=sorted(pinguinos["species"].unique()),
    default=sorted(pinguinos["species"].unique()),
)

if not especies_sel:
    st.warning("Seleccioná al menos una especie en la barra lateral para ver los paneles.")
    st.stop()

separar_outliers_por_especie = st.sidebar.checkbox(
    "Panel 2 — comparar outliers por especie", value=True
)
mostrar_tendencia = st.sidebar.checkbox("Panel 3 — mostrar línea de tendencia", value=True)
mostrar_contornos = st.sidebar.checkbox("Panel 4 — mostrar contornos de densidad", value=True)

st.sidebar.divider()
st.sidebar.header("Comparar variables")
st.sidebar.caption("Panel 3 — tendencia bivariada")
var_x_tendencia = st.sidebar.selectbox(
    "Eje X", NUMERICAS, index=NUMERICAS.index("flipper_length_mm"), key="tend_x",
    format_func=lambda c: ETIQUETAS[c],
)
var_y_tendencia = st.sidebar.selectbox(
    "Eje Y", NUMERICAS, index=NUMERICAS.index("body_mass_g"), key="tend_y",
    format_func=lambda c: ETIQUETAS[c],
)
st.sidebar.caption("Panel 4 — separabilidad de especies")
var_x_separa = st.sidebar.selectbox(
    "Eje X ", NUMERICAS, index=NUMERICAS.index("bill_length_mm"), key="sep_x",
    format_func=lambda c: ETIQUETAS[c],
)
var_y_separa = st.sidebar.selectbox(
    "Eje Y ", NUMERICAS, index=NUMERICAS.index("bill_depth_mm"), key="sep_y",
    format_func=lambda c: ETIQUETAS[c],
)

datos_filtrados = pinguinos[pinguinos["species"].isin(especies_sel)]
datos_completos = datos_filtrados.dropna(subset=NUMERICAS)

# --- Estadísticos compartidos entre la "Gran Idea", los KPI y los badges de cada panel ---
pct_incompletas = pinguinos.isna().any(axis=1).mean() * 100
outliers_kpi = contar_outliers_iqr(datos_completos, NUMERICAS)

hay_par_tendencia = var_x_tendencia != var_y_tendencia
r_tendencia = datos_completos[var_x_tendencia].corr(datos_completos[var_y_tendencia])
fuerza_tendencia = "fuerte" if abs(r_tendencia) >= 0.7 else "moderada" if abs(r_tendencia) >= 0.4 else "débil"

sil = calcular_silhouette(datos_completos, var_x_separa, var_y_separa)
nivel_separa = None if sil is None else ("alta" if sil >= 0.5 else "moderada" if sil >= 0.25 else "baja")

frase_tendencia = (
    f"una tendencia {fuerza_tendencia} (r = {r_tendencia:.2f}) entre "
    f"{ETIQUETAS[var_x_tendencia].lower()} y {ETIQUETAS[var_y_tendencia].lower()}"
    if hay_par_tendencia else "una tendencia bivariada (elegí dos variables distintas en el panel 3)"
)
frase_separa = (
    f"una separabilidad {nivel_separa} entre especies (silhouette = {sil:.2f}) usando "
    f"{ETIQUETAS[var_x_separa].lower()} y {ETIQUETAS[var_y_separa].lower()}"
    if sil is not None else "una separabilidad que no se puede medir con la selección actual"
)

st.markdown(
    f"**Idea principal:** el dataset está prácticamente limpio — solo **{pct_incompletas:.1f}%** de "
    f"las filas tiene datos faltantes (concentrados en `sex`) y casi no hay outliers — y ya se "
    f"observa {frase_tendencia}, además de {frase_separa}: un buen punto de partida para "
    f"clasificar especies con pocas variables."
)
st.caption("Usá los controles de la barra lateral para filtrar especies y comparar otros pares de variables.")

r_txt = f"{r_tendencia:.2f}" if hay_par_tendencia else "n/d"
sil_txt = f"{sil:.2f}" if sil is not None else "n/d"

m1, m2, m3, m4 = st.columns(4)
m1.metric("1. Filas con faltantes", f"{pct_incompletas:.1f}%", help="Sobre las 344 filas totales; no depende del filtro de especies.")
m2.metric("2. Outliers (1.5×IQR)", outliers_kpi, help="Sobre la selección de especies actual.")
m3.metric("3. Correlación (r)", r_txt, help=f"{ETIQUETAS[var_x_tendencia]} vs. {ETIQUETAS[var_y_tendencia]}")
m4.metric("4. Separabilidad (silhouette)", sil_txt, help=f"{ETIQUETAS[var_x_separa]} vs. {ETIQUETAS[var_y_separa]}")

st.write("")
fila1_col1, fila1_col2 = st.columns(2)
fila2_col1, fila2_col2 = st.columns(2)

with fila1_col1:
    with st.container(border=True):
        st.subheader("1. Valores faltantes")
        faltantes = pinguinos.isna().sum()
        faltantes = faltantes[faltantes > 0].sort_values(ascending=True)
        etiquetas_y = [ETIQUETAS.get(c, c) for c in faltantes.index]

        fig, ax = plt.subplots(figsize=(5.2, 3.6))
        barras = ax.barh(etiquetas_y, faltantes.values, color=COLOR_BAD, height=0.55)
        for barra, valor in zip(barras, faltantes.values):
            pct = valor / len(pinguinos) * 100
            ax.text(
                barra.get_width() + faltantes.max() * 0.03, barra.get_y() + barra.get_height() / 2,
                f"{valor} ({pct:.1f}%)", va="center", fontsize=9, color=TEXTO,
            )
        ax.set_xlim(0, faltantes.max() * 1.35)
        ax.set_xlabel("Observaciones con valor faltante")
        ax.set_title("Cantidad de valores faltantes por variable", fontsize=10)
        ax.grid(axis="y", visible=False)
        sns.despine(fig=fig, left=True)
        fig.tight_layout()
        st.pyplot(fig)

        badge(f"🟢 Baja proporción de faltantes ({pct_incompletas:.1f}%)", COLOR_OK)
        st.caption(
            "Concentrados en `sex`; además, 2 filas pierden también las 4 variables morfológicas "
            "a la vez — no es ruido aleatorio uniforme."
        )

with fila1_col2:
    with st.container(border=True):
        st.subheader("2. Outliers en variables morfológicas")
        fig, axes = plt.subplots(2, 2, figsize=(5.4, 3.6))
        for ax, col in zip(axes.ravel(), NUMERICAS):
            if separar_outliers_por_especie:
                sns.boxplot(
                    data=datos_filtrados, x="species", y=col, hue="species",
                    palette=PALETA, width=0.6, fliersize=3, legend=False, ax=ax,
                )
                ax.set_xlabel("")
                ax.tick_params(axis="x", labelsize=7, rotation=15)
            else:
                sns.boxplot(y=datos_filtrados[col], color="#8C8C8C", width=0.45, fliersize=4, ax=ax)
                ax.set_xlabel("")
            ax.set_title(ETIQUETAS[col], fontsize=8.5)
            ax.set_ylabel("")
        sns.despine(fig=fig)
        fig.tight_layout()
        st.pyplot(fig)

        if outliers_kpi == 0:
            badge("🟢 Sin outliers según la regla 1.5×IQR", COLOR_OK)
        else:
            badge(f"🟡 {outliers_kpi} outliers detectados (1.5×IQR)", COLOR_WARN)
        st.caption("Los bigotes cubren casi todo el rango observado en las 4 variables y en las 3 especies.")

with fila2_col1:
    with st.container(border=True):
        st.subheader("3. Explorá una tendencia bivariada")
        fig, ax = plt.subplots(figsize=(5.4, 3.7))
        sns.scatterplot(
            data=datos_completos, x=var_x_tendencia, y=var_y_tendencia,
            hue="species", palette=PALETA, alpha=0.85,
            edgecolor=FONDO, linewidth=0.4, s=45, ax=ax,
        )
        if mostrar_tendencia and hay_par_tendencia and len(datos_completos) > 2:
            sns.regplot(
                data=datos_completos, x=var_x_tendencia, y=var_y_tendencia,
                scatter=False, color=TEXTO, line_kws={"linestyle": "--", "linewidth": 1.5}, ax=ax,
            )
        ax.set_xlabel(ETIQUETAS[var_x_tendencia])
        ax.set_ylabel(ETIQUETAS[var_y_tendencia])
        ax.set_title(f"{ETIQUETAS[var_x_tendencia]} vs. {ETIQUETAS[var_y_tendencia]}", fontsize=10)
        ax.legend(title="Especie", fontsize=8, title_fontsize=9, loc="best")
        sns.despine(fig=fig)
        fig.tight_layout()
        st.pyplot(fig)

        if not hay_par_tendencia:
            badge("⚪ Elegí dos variables distintas", COLOR_INFO)
        else:
            icono = "🟢" if abs(r_tendencia) >= 0.7 else "🟡" if abs(r_tendencia) >= 0.4 else "🔴"
            color = COLOR_OK if abs(r_tendencia) >= 0.7 else COLOR_WARN if abs(r_tendencia) >= 0.4 else COLOR_BAD
            badge(f"{icono} Correlación {fuerza_tendencia} (r = {r_tendencia:.2f})", color)
        st.caption("Cambiá los ejes en la barra lateral para comparar otras relaciones.")

with fila2_col2:
    with st.container(border=True):
        st.subheader("4. Separabilidad de especies")
        fig, ax = plt.subplots(figsize=(5.4, 3.7))
        sns.scatterplot(
            data=datos_completos, x=var_x_separa, y=var_y_separa,
            hue="species", style="species", palette=PALETA, s=50,
            edgecolor=FONDO, linewidth=0.4, ax=ax,
        )
        if mostrar_contornos:
            for especie, color in PALETA.items():
                if especie not in especies_sel:
                    continue
                subset = datos_completos[datos_completos["species"] == especie]
                if len(subset) > 5 and var_x_separa != var_y_separa:
                    sns.kdeplot(
                        data=subset, x=var_x_separa, y=var_y_separa,
                        color=color, levels=2, linewidths=1, ax=ax,
                    )
        ax.set_xlabel(ETIQUETAS[var_x_separa])
        ax.set_ylabel(ETIQUETAS[var_y_separa])
        ax.set_title(f"{ETIQUETAS[var_x_separa]} vs. {ETIQUETAS[var_y_separa]}", fontsize=10)
        ax.legend(title="Especie", fontsize=8, title_fontsize=9)
        sns.despine(fig=fig)
        fig.tight_layout()
        st.pyplot(fig)

        if sil is None:
            badge("⚪ Seleccioná 2+ especies y variables distintas", COLOR_INFO)
        else:
            icono = "🟢" if sil >= 0.5 else "🟡" if sil >= 0.25 else "🔴"
            color = COLOR_OK if sil >= 0.5 else COLOR_WARN if sil >= 0.25 else COLOR_BAD
            badge(f"{icono} Separabilidad {nivel_separa} (silhouette = {sil:.2f})", color)
        st.caption("Probá distintos pares de variables en la barra lateral para ver cuáles separan mejor.")
