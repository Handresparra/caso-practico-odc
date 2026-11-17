# Caso práctico · Del dato a la toma de decisiones

[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Handresparra/caso-practico-odc/blob/main/notebooks/caso_practico.ipynb)
[![Licencia: CC BY 4.0](https://img.shields.io/badge/Licencia-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/deed.es)

Caso práctico del Objeto Digital de Conocimiento (ODC) **«Del dato a la toma de decisiones: guía interactiva de diseño estadístico para datos estructurados y no estructurados»**, Especialización en Analítica y Ciencia de Datos, Universidad de Cundinamarca.

## La situación

Un servicio técnico de celulares debe decidir qué repuestos mantener en inventario. Los clientes se quejan de demoras, pero el dinero inmovilizado en repuestos también preocupa a la gerencia. El cuaderno guía el análisis en los cinco pasos del ODC:

1. **Formular la pregunta** · decisión, preguntas de análisis y tipos de variables.
2. **Diseñar la muestra** · tamaño de muestra (384) y muestreo estratificado por marca.
3. **Asegurar la calidad** · perfilado, limpieza y bitácora de cambios.
4. **Transformar el texto** · polaridad, «menciona demora» y tópicos de las reseñas.
5. **Modelar, graficar y decidir** · Pareto, correlación de Pearson, ANOVA, regresión logística y recomendación.

## Cómo usarlo

- **En línea, sin instalar nada:** haz clic en el botón **Abrir en Colab** y ejecuta las celdas en orden (`Shift + Enter`).
- **En tu computador:** descarga el repositorio (botón verde **Code → Download ZIP**), instala las librerías con `pip install -r requirements.txt` y abre `notebooks/caso_practico.ipynb` en Jupyter.
- **Solo los datos:** descarga los archivos de la carpeta [`data/`](data/).

## Estructura

```
caso-practico-odc/
├── README.md
├── LICENSE
├── requirements.txt
├── data/
│   ├── ordenes.csv           # 1.212 filas (1.200 órdenes + 12 duplicados a propósito)
│   ├── inventario.csv        # 31 repuestos (kardex)
│   ├── resenas.csv           # 350 reseñas de clientes
│   └── notas_tecnicos.csv    # 1.200 notas de los técnicos
├── notebooks/
│   └── caso_practico.ipynb   # el caso práctico, paso a paso
└── scripts/
    ├── generar_datos.py      # crea los CSV (semilla fija)
    └── construir_notebook.py # crea el cuaderno
```

## Diccionario de datos

**`ordenes.csv`** (datos estructurados, enero a junio de 2026)

| Columna | Tipo | Descripción |
|---|---|---|
| `orden_id` | Identificador | Número de la orden; **clave para unir todas las fuentes** |
| `fecha_ingreso` | Fecha | Día en que el equipo ingresó al taller |
| `fecha_entrega_estimada` | Fecha | Día prometido al cliente |
| `fecha_entrega` | Fecha | Día real de entrega (con algunos vacíos) |
| `sede` | Categórica nominal | Norte, Centro o Sur |
| `marca` | Categórica nominal | Samsung, Xiaomi u Otras marcas (escrita de varias formas a propósito) |
| `modelo` | Categórica nominal | Modelo del celular (con cerca del 18 % de vacíos) |
| `tipo_falla` | Categórica nominal | Pantalla, Batería, Puerto de carga, Cámara, Altavoz u Otros |
| `repuesto_ref` | Identificador | Referencia del repuesto usado; une con `inventario.csv` |
| `costo_total` | Numérica continua | Costo cobrado en pesos colombianos (con algunos errores de un cero de más) |
| `dias_reparacion` | Numérica discreta | Días entre el ingreso y la entrega |
| `calificacion` | Categórica ordinal | Satisfacción del cliente de 1 a 5 |
| `cliente_id` | Identificador | Código del cliente |

**`inventario.csv`**: `repuesto_ref`, `tipo_repuesto`, `marca_compatible`, `descripcion`, `stock_promedio` (unidades en bodega) y `costo_unitario` (pesos).

**`resenas.csv`** (datos no estructurados): `resena_id`, `orden_id`, `fecha_resena`, `texto` (reseña libre), `calificacion` y `polaridad_etiquetada` (polaridad asignada por una persona en 120 reseñas, para validar el análisis automático).

**`notas_tecnicos.csv`** (datos no estructurados): `orden_id` y `nota_tecnico` (diagnóstico libre; puede indicar «sin stock en bodega»).

## Sobre los datos

Los datos son **sintéticos**: se generaron con `scripts/generar_datos.py` (semilla 2026), de modo que cualquiera puede reproducirlos. Imitan el comportamiento de un taller real y traen errores de calidad intencionales para practicar la depuración. No describen a ninguna empresa ni persona.

## Cómo citar

Parra Enciso, H. A. (2026). *Caso práctico · Del dato a la toma de decisiones* [Cuaderno de Jupyter y conjunto de datos]. GitHub. https://github.com/Handresparra/caso-practico-odc

## Licencia

Contenido y datos bajo licencia [Creative Commons Atribución 4.0 Internacional (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/deed.es). Autor: Hansel Andres Parra Enciso · Universidad de Cundinamarca.

Los datos y el cuaderno se prepararon con apoyo de una herramienta de IA generativa (Claude, Anthropic), a partir del diseño y las indicaciones del autor, quien los revisó.
