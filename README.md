# eGFR-clinical-calculator

Calculadora clínica de Tasa de Filtración Glomerular (eGFR) utilizando la ecuación CKD-EPI 2021 libre de raza. Desarrollada en Python puro con estándares de informática médica.

La implementación utiliza la ecuación CKD-EPI 2021, la cual fue actualizada en conjunto por la National Kidney Foundation (NKF) y la American Society of Nephrology (ASN). Esta versión elimina el coeficiente multiplicador de raza (afrodescendiente vs. no afrodescendiente). Su adopción es un estándar de calidad y equidad en salud, convirtiendo a esta calculadora en una herramienta clínicamente moderna, libre de sesgos raciales y estandarizada para creatinina IDMS.

## Fórmula Matemática

El cálculo del eGFR (Tasa de Filtración Glomerular estimada) entregará el resultado en mL/min/1.73 m^2.

**Ecuación base:**
`eGFR = 142 * min(Scr / k, 1)^a * max(Scr / k, 1)^(-1.200) * 0.9938^Edad * Factor Sexo`

**Donde:**
* **Scr**: Creatinina sérica en mg/dL (asumiendo calibración IDMS).
* **k (kappa)**: Constante basada en el sexo.
* **a (alfa)**: Exponente basado en el sexo.
* **Edad**: Años cumplidos.
* **Factor Sexo**: Multiplicador aplicado solo si el paciente es mujer.

## Lógica de los factores min / max

La fórmula se adapta al nivel de creatinina del paciente usando las funciones matemáticas min y max. Aquí está el desglose algorítmico:

**1. Cálculo de la proporción:** Dividimos la creatinina del paciente (Scr) por la constante de su sexo (k).

**2. Paciente con Creatinina Baja/Normal (Scr / k <= 1):**
* La función `min(Scr / k, 1)` toma el valor de la proporción.
* La función `max(Scr / k, 1)` toma el valor de 1. (Al elevar 1 al exponente -1.200, el factor se vuelve 1 y se anula).

**3. Paciente con Creatinina Elevada (Scr / k > 1):**
* La función `min(Scr / k, 1)` toma el valor de 1. (Al elevar 1 al exponente "a", el factor se vuelve 1 y se anula).
* La función `max(Scr / k, 1)` toma el valor de la proporción y se penaliza fuertemente con el exponente negativo -1.200.

## Dominio de Valores Válidos y Excepciones

Antes de calcular, el código validará las entradas. Si no cumplen estas reglas, lanzaremos una excepción (error) en lugar de un resultado falso:

* **Edad:** Debe ser un entero >= 18 (no validado para pediatría) y <= 120 (límite biológico razonable para la interfaz).
* **Creatinina (Scr):** Debe ser un número decimal > 0 (no puede ser cero ni negativa fisiológicamente). Límite superior razonable <= 15.0 mg/dL.
* **Sexo:** Carácter exacto ("M" o "F"). Si un paciente es intersexual o está en transición, las guías actuales recomiendan usar el sexo biológico asignado al nacer para la masa muscular, o reportar ambos valores. Para la ejecución del núcleo matemático, el sistema requiere una entrada binaria estricta de acuerdo con las variables de la ecuación original.

### ⚠️ Limitaciones Clínicas y Equidad en Salud (Llamado a la Acción)

Las ecuaciones basadas en creatinina (como CKD-EPI) utilizan el sexo binario como un estimador indirecto de la masa muscular. Actualmente, **no existen ecuaciones eGFR basadas en creatinina validadas clínicamente para pacientes intersexuales o personas transgénero en terapia hormonal afirmativa (TRH)**, ya que la TRH altera significativamente la composición corporal y la generación endógena de creatinina.

Obligar a estos pacientes a encajar en un cálculo binario representa un riesgo clínico, especialmente al tomar decisiones críticas como la dosificación de fármacos de excreción renal o la evaluación de riesgo de nefrotoxicidad por medios de contraste yodados. 

Ante este vacío científico, las recomendaciones clínicas actuales sugieren:
1. **Acotar el rango:** Calcular y reportar ambos valores (usando las constantes M y F) para establecer un rango de función renal que apoye el juicio médico.
2. **Uso de biomarcadores independientes:** Recomendar la medición de **Cistatina C** y utilizar la ecuación CKD-EPI Cistatina C, la cual no depende de la masa muscular ni requiere la variable de sexo.

Desde la Informática Médica, este proyecto expone esta limitación algorítmica de forma transparente. Sirva esto como un llamado a la comunidad científica para fomentar modelos predictivos inclusivos y para impulsar la transición hacia biomarcadores independientes de la raza y el sexo en el desarrollo de software clínico.

## Criterio de Redondeo

Clínicamente, el eGFR se reporta como un número entero. Sin embargo, para evitar enmascarar errores de coma flotante durante las pruebas unitarias, la función base retornará el valor con 2 decimales. El redondeo al entero se hará únicamente en la interfaz de usuario final.
