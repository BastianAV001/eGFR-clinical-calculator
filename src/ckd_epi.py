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
        
    if not isinstance(edad, int) or edad < 18 or edad > 120: 
        raise ValueError("Error Clínico: La edad debe ser un número entero entre 18 y 120 años. (Fórmula no validada para pediatría).")
    
    if not isinstance(scr, (int, float)) or scr <= 0 or scr > 15.0:
        raise ValueError("Error Clínico: La creatinina sérica (Scr) debe ser mayor a 0 y menor a 15.0 mg/dL.")
    
    sexo = sexo.upper()
    if sexo not in ["M", "F"]:
        raise ValueError("Error de Parámetro: El sexo para este modelo matemático debe ser 'M' o 'F'.")
    
    if sexo == "F":
        kappa = 0.7
        alpha = -0.241
        factor_sexo = 1.012
    else:  
        kappa = 0.9
        alpha = -0.302
        factor_sexo = 1.000

    
    proporcion_scr = scr / kappa
    valor_min = min(proporcion_scr, 1.0)
    valor_max = max(proporcion_scr, 1.0)

    egfr = 142 * (valor_min ** alpha) * (valor_max ** -1.200) * (0.9938 ** edad) * factor_sexo

    return round(egfr, 2)

def clasificar_categoria_kdigo(egfr: float) -> dict:
    """
    Clasifica la categoría de eGFR (G1-G5) según KDIGO 2012 y proporciona
    soporte a la decisión clínica (CDSS).

    Args:
        egfr (float): El valor de la Tasa de Filtración Glomerular estimada.

    Returns:
        dict: Un diccionario con la categoría, descripción, estatus de ERC y recomendación clínica.
    """
    if egfr >= 90:
        return {
            "categoria": "G1",
            "descripcion": "eGFR Normal o Alto",
            "estatus_erc": "Ausencia de ERC por eGFR aislado. El diagnóstico requiere evidencia de daño renal (ej. albuminuria ≥ 30 mg/g, anomalías estructurales o sedimento urinario anormal) por > 3 meses.",
            "accion_clinica": "Control preventivo rutinario. Monitoreo anual solo si existen factores de riesgo (diabetes, hipertensión, antecedentes familiares)."
        }
    elif egfr >= 60:
        return {
            "categoria": "G2",
            "descripcion": "Disminución Leve del eGFR",
            "estatus_erc": "Ausencia de ERC por eGFR aislado. El diagnóstico requiere marcadores de daño renal persistentes por > 3 meses.",
            "accion_clinica": "Evaluar comorbilidades y riesgo cardiovascular. Sin derivación a nefrología a menos que exista proteinuria significativa."
        }
    elif egfr >= 45:
        return {
            "categoria": "G3a",
            "descripcion": "Disminución Leve a Moderada",
            "estatus_erc": "Confirma diagnóstico de Enfermedad Renal Crónica (independiente de otros marcadores).",
            "accion_clinica": "Monitoreo clínico cada 6 meses. Estricto control de presión arterial y ajuste de dosis de fármacos nefrotóxicos."
        }
    elif egfr >= 30:
        return {
            "categoria": "G3b",
            "descripcion": "Disminución Moderada a Severa",
            "estatus_erc": "Confirma diagnóstico de Enfermedad Renal Crónica. Alto riesgo de progresión.",
            "accion_clinica": "Derivación a nefrología recomendada. Evaluar activamente complicaciones asociadas (anemia, metabolismo óseo-mineral)."
        }
    elif egfr >= 15:
        return {
            "categoria": "G4",
            "descripcion": "Disminución Severa",
            "estatus_erc": "Confirma diagnóstico de Enfermedad Renal Crónica (Etapa Pre-diálisis).",
            "accion_clinica": "Derivación urgente a nefrología. Requiere preparación multidisciplinaria para futura Terapia de Reemplazo Renal (TRR)."
        }
    else:
        return {
            "categoria": "G5",
            "descripcion": "Falla Renal",
            "estatus_erc": "Enfermedad Renal Crónica Terminal.",
            "accion_clinica": "Manejo nefrológico activo para Terapia de Reemplazo Renal (diálisis/trasplante) o cuidados paliativos conservadores."
        }


def evaluar_riesgo_contraste(egfr: float) -> dict:
    """
    Evalúa el riesgo de administrar medios de contraste yodados (TC) y 
    basados en gadolinio (RM) según la TFG estimada (Consenso ACR/ESUR).
    
    Args:
        egfr (float): El valor de la TFG estimada.
        
    Returns:
        dict: Nivel de riesgo, código de color para la interfaz y protocolos para TC y RM.
    """
    if egfr >= 45:
        return {
            "nivel_riesgo": "Bajo",
            "color_alerta": "verde", 
            "yodo_tc": "Seguro. Riesgo mínimo de Nefropatía Inducida por Contraste (NIC). Proceder con protocolo estándar.",
            "gadolinio_rm": "Seguro. Riesgo extremadamente bajo de Fibrosis Sistémica Nefrogénica (FSN)."
        }
    elif egfr >= 30:
        return {
            "nivel_riesgo": "Moderado",
            "color_alerta": "naranja",  
            "yodo_tc": "Precaución. Riesgo moderado de NIC. Se recomienda protocolo de profilaxis (ej. hidratación con suero fisiológico) y suspender fármacos nefrotóxicos temporales.",
            "gadolinio_rm": "Precaución. Utilizar exclusivamente agentes de gadolinio de Grupo II (macrocíclicos). Evaluar relación riesgo/beneficio."
        }
    else:
        return {
            "nivel_riesgo": "Alto",
            "color_alerta": "rojo",  
            "yodo_tc": "Alerta Clínica: Alto riesgo de NIC. Buscar alternativas de imagen sin contraste. Si el examen es de urgencia vital, requiere hidratación estricta y monitoreo nefrológico.",
            "gadolinio_rm": "Contraindicación: Riesgo severo de FSN. Los agentes de Grupo I están absolutamente contraindicados. Buscar alternativas diagnósticas."
        }