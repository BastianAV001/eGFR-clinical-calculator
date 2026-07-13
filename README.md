# eGFR-clinical-calculator

Sistema de Soporte a la Decisión Clínica (CDSS) para el cálculo de la Tasa de Filtración Glomerular estimada (eGFR) y evaluación de riesgo de inyección de contraste. Desarrollado en Python.

## Investigación y Selección de la Ecuación

La elección del motor matemático responde a un análisis exhaustivo de la literatura nefrológica actual. Se implementó la **ecuación CKD-EPI 2021** por sobre alternativas históricas por los siguientes motivos de rigor clínico:
* **Superioridad frente a MDRD:** La ecuación MDRD tiende a subestimar sistemáticamente la función renal en pacientes con eGFR > 60 mL/min, lo cual generaba falsos positivos en el tamizaje. CKD-EPI corrige esta desviación.
* **Eliminación de Sesgos (Equidad en Salud):** Se actualizó desde la versión CKD-EPI 2009 para adherir a las directrices conjuntas de la National Kidney Foundation (NKF) y la American Society of Nephrology (ASN). Esta versión elimina el coeficiente de raza (afrodescendiente vs. no afrodescendiente), estandarizando la herramienta para creatinina IDMS y asegurando decisiones clínicas libres de sesgos demográficos.

## Arquitectura del Código

El proyecto sigue una arquitectura modular para separar la lógica médica de la interfaz visual, facilitando futuras integraciones o auditorías:
* `ckd_epi.py`: "Backend", contiene la ecuación matemática, las compuertas de validación de datos y los diccionarios de clasificación según directrices KDIGO y ACR/ESUR.
* `app.py`: "Frontend", construido con Streamlit, gestiona la captura de datos y el despliegue visual de alertas.
* `test_ckd_epi.py`: Módulo de Test. Pruebas unitarias que garantizan la exactitud de los cálculos frente a los valores esperados de la literatura médica.

## Lógica Algorítmica de la Fórmula

**Ecuación base:**
`eGFR = 142 * min(Scr / k, 1)^a * max(Scr / k, 1)^(-1.200) * 0.9938^Edad * Factor Sexo`

Desde el punto de vista del código, la ecuación opera de forma dinámica como una **función por trozos**. El algoritmo utiliza las funciones matemáticas `min()` y `max()`. Esto actúa como un "interruptor" que suaviza o castiga la curva de filtración glomerular automáticamente dependiendo de si la proporción de creatinina del paciente supera el umbral normal para su sexo.

## Validaciones y Dominio de Datos

El motor lógico bloquea entradas biológicamente imposibles o fuera del marco de validación del modelo para prevenir errores médicos:
* **Edad:** Rango aceptado de 18 a 120 años (el modelo matemático no está validado en pediatría).
* **Creatinina (Scr):** Límite estricto de > 0 a <= 15.0 mg/dL.
* **Sexo Biológico:** Entrada binaria estricta ("M" o "F") requerida por las constantes de la ecuación.

### Limitación Clínica Transparente

Actualmente, no existen ecuaciones eGFR basadas en creatinina validadas clínicamente para pacientes intersexuales o personas transgénero en terapia hormonal afirmativa (TRH), debido a las alteraciones en la composición de masa muscular. Obligar a estos pacientes a encajar en un cálculo binario representa un riesgo para la dosificación de fármacos o uso de contraste yodado. La recomendación clínica actual, es sugerir la medición de Cistatina C (biomarcador independiente de masa muscular) y el uso de la ecuación CKD-EPI Cistatina C. Únicamente en entornos clínicos donde este examen no se encuentre disponible, la literatura sugiere como medida de mitigación pragmática calcular y reportar ambos valores (femenino y masculino) para establecer un rango estimado de la función renal, el cual debe ser interpretado con extrema cautela clínica.

## Decisiones de Arquitectura UX/UI

La interfaz fue diseñada con principios de interacción humano-computadora para reducir la fricción en entornos de urgencia (ej. consolas de tomografía):
* **Identidad Visual Clínica:** Se diseñó una paleta de alto contraste y profesionalismo con alertas nativas (verde/naranja/rojo) para la lectura rápida del riesgo asociado a los medios de contraste.
* **Prevención de Fatiga por Error:** Se agrupó la captura de datos en un componente de formulario (`st.form`). Esto adapta el flujo a la *Ley de Jakob*, permitiendo al usuario navegar con la tecla "Enter" entre los campos, y solo ejecutar el cálculo matematico al confirmar el último dato, evitando alertas visuales innecesarias por información incompleta.
* **Trazabilidad:** El redondeo al número entero de eGFR se procesa únicamente en la capa visual, manteniendo intacta la precisión decimal en el backend para auditorías.