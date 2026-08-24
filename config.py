"""Configuración compartida del dashboard: colores, paleta de especies y etiquetas.

Separado del resto para que dashboard.py no empiece con 30 líneas de constantes
antes de llegar a la lógica real.
"""

# Colores del tema oscuro (fondo, tarjetas, texto, grilla)
FONDO = "#0E1117"
TARJETA = "#161B22"
TEXTO = "#E6E6E6"
GRILLA = "#30363D"

# Colores semánticos para los badges de veredicto (verde = ok, amarillo = alerta, rojo = mal, azul = info)
COLOR_OK = "#3FB950"
COLOR_WARN = "#D29922"
COLOR_BAD = "#F85149"
COLOR_INFO = "#58A6FF"

# Un color fijo por especie, para que se mantenga consistente en todos los paneles
PALETA = {"Adelie": "#5B9BD5", "Chinstrap": "#F2A65A", "Gentoo": "#70C1A0"}

# Variables numéricas que se usan en los paneles de outliers, tendencia y separabilidad
NUMERICAS = ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"]

# Nombres legibles en español para mostrar en selectboxes, títulos y ejes
ETIQUETAS = {
    "bill_length_mm": "Largo del pico (mm)",
    "bill_depth_mm": "Profundidad del pico (mm)",
    "flipper_length_mm": "Largo de la aleta (mm)",
    "body_mass_g": "Masa corporal (g)",
    "sex": "Sexo",
}