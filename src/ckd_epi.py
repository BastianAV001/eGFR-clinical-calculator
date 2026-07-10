"""
Módulo de cálculo de Tasa de Filtración Glomerular (eGFR).
Implementa la ecuación CKD-EPI 2021 libre de raza.
"""

def calcular_egfr(edad: int, scr: float, sexo: str) -> float:
    """
    Calcula la eGFR utilizando la ecuación CKD-EPI 2021.

    Args:
        edad (int): Edad del paciente en años (debe ser >= 18).
        scr (float): Creatinina sérica en mg/dL (debe ser > 0).
        sexo (str): Sexo biológico para el cálculo ('M' o 'F').

    Returns:
        float: Valor de eGFR calculado en mL/min/1.73 m², redondeado a 2 decimales.

    Raises:
        ValueError: Si los parámetros de entrada están fuera de los rangos clínicos válidos.
    """
    
    # Validación de entradas (Guard Clauses)
    if not isinstance(edad, int) or edad < 18 or edad > 120: 
        raise ValueError("Error Clínico: La edad debe ser un número entero entre 18 y 120 años. (Fórmula no validada para pediatría).")
    
    if not isinstance(scr, (int, float)) or scr <= 0 or scr > 15.0:
        raise ValueError("Error Clínico: La creatinina sérica (Scr) debe ser mayor a 0 y menor a 15.0 mg/dL.")
    
    sexo = sexo.upper()
    if sexo not in ["M", "F"]:
        raise ValueError("Error de Parámetro: El sexo para este modelo matemático debe ser 'M' o 'F'.")

    # Asignación de constantes según el sexo
    if sexo == "F":
        kappa = 0.7
        alpha = -0.241
        factor_sexo = 1.012
    else:  # sexo == "M"
        kappa = 0.9
        alpha = -0.302
        factor_sexo = 1.000

    # Lógica matemática de proporciones (min / max)
    proporcion_scr = scr / kappa
    valor_min = min(proporcion_scr, 1.0)
    valor_max = max(proporcion_scr, 1.0)

    # Ecuación principal CKD-EPI 2021
    egfr = 142 * (valor_min ** alpha) * (valor_max ** -1.200) * (0.9938 ** edad) * factor_sexo

    # Retorno con precisión para QA
    return round(egfr, 2)