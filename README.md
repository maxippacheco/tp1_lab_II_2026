# TP1 — Análisis Exploratorio de Datos y Visualización

**Laboratorio de Datos II** — Ingeniería en Inteligencia Artificial — UNL / FICH

Resolución del Trabajo Práctico N°1 sobre el dataset [Palmer Penguins](https://github.com/allisonhorst/penguins),
que contiene mediciones morfológicas de tres especies de pingüinos (*Adelie*, *Chinstrap* y *Gentoo*)
recolectadas en islas del archipiélago Palmer (Antártida).

## Integrantes

- Maximo Pacheco.
- Maximo Zanetta.

## Estructura del repositorio

```
├── TP1_Laboratorio_de_datos_2.ipynb   # Notebook con la resolución de los Ejercicios 1 a 4
├── dashboard.py                    # Dashboard interactivo en Streamlit (Ejercicio 5)
├── pyproject.toml                  # Dependencias del proyecto (con uv)
└── uv.lock                         # Lockfile del entorno
```

## Contenido del trabajo

El notebook `TP1_Laboratorio_de_datos_2.ipynb` resuelve, en orden:

1. **Estadística descriptiva y análisis univariado** — estructura del dataset, valores faltantes,
   medidas de tendencia central y dispersión, asimetría/curtosis, histogramas, boxplots y
   distribución de variables categóricas.
2. **Análisis bivariado** — matriz de correlación, scatter plots con línea de tendencia,
   significancia estadística (Pearson/Spearman), tablas de contingencia con heatmap y test
   chi-cuadrado.
3. **Análisis multivariado y visualización avanzada** — pairplot, coordenadas paralelas, heatmaps
   de correlación segmentados por especie, dendrograma de variables y gráficos de radar.
4. **Muestreo y reducción dimensional** — muestreo aleatorio simple vs. estratificado, PCA con
   varianza explicada, y comparación PCA vs. t-SNE.

El **Ejercicio 5** (dashboard interactivo) se resuelve aparte en `dashboard.py`, ya que Streamlit no
corre dentro de un notebook. Presenta una grilla 2×2 con cuatro visualizaciones que evidencian
valores faltantes, outliers, tendencias bivariadas y separabilidad de especies.

## Cómo correrlo

El proyecto usa [`uv`](https://docs.astral.sh/uv/) para gestionar el entorno y las dependencias.

```bash
# Instalar dependencias (crea el entorno virtual .venv)
uv sync

# Abrir el notebook
uv run jupyter notebook TP1_Palmer_Penguins_EDA.ipynb

# Levantar el dashboard del Ejercicio 5
uv run streamlit run dashboard.py
```

> **Nota (WSL):** si `uv` falla al detectar el intérprete de Python por un `python.exe` de Windows
> en el `PATH`, anteponer `UV_PYTHON_PREFERENCE=only-managed` a los comandos anteriores.

## Flujo de trabajo y colaboración

- **Rama principal:** `main` — siempre debe quedar en estado funcional (notebook ejecutable sin
  errores, dashboard corriendo).
- **Ramas de trabajo:** una rama por ejercicio, con la convención `feature/exercise1`,
  `feature/exercise2`, `feature/exercise3`, `feature/exercise4`, `feature/exercise5`. Cambios
  adicionales (fixes, documentación) van en ramas `fix/...` o `docs/...`.
- **Pull Requests:** cada rama se integra a `main` mediante un Pull Request, nunca con push directo.
- **Revisión cruzada obligatoria:** todo PR debe ser revisado y aprobado por el otro integrante antes
  de mergear (Maximo P. revisa el trabajo de Maximo Z. y viceversa). No se realizan self-merges.
- **Mensajes de commit:** descriptivos y en tiempo presente (ej. `agrega analisis PCA`, `corrige
  heatmap de contingencia`).

## Fuente de datos

Dataset Palmer Penguins (Gorman, Williams & Fraser, 2014), distribuido a través del paquete
`seaborn` (`sns.load_dataset("penguins")`). Repositorio original:
https://github.com/allisonhorst/penguins

## Checklist de avance

- [x] Entorno del proyecto (`pyproject.toml` / `uv.lock`) definido y probado
- [x] README con estructura, instrucciones y flujo de trabajo
- [x] Notebook subido al repositorio (`feature/exercise1` → PR → `main`)
- [x] Ejercicio 1 — Estadística descriptiva y análisis univariado
- [ ] Ejercicio 2 — Análisis bivariado (correlaciones y asociaciones)
- [ ] Ejercicio 3 — Análisis multivariado y visualización avanzada
- [ ] Ejercicio 4 — Muestreo y reducción dimensional
- [ ] Ejercicio 5 — Dashboard Streamlit (`dashboard.py`)
- [ ] Revisión cruzada de cada PR (Maximo P. ↔ Maximo Z.)
- [ ] Notebook corre de punta a punta sin errores (`jupyter nbconvert --execute`)
- [ ] Dashboard probado localmente (`streamlit run dashboard.py`)
- [ ] Entrega final revisada por ambos integrantes en `main`
