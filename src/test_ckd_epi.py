"""
Script de Aseguramiento de Calidad (QA) para la calculadora eGFR.
Utiliza el framework nativo 'unittest' de Python.
"""

import unittest
from ckd_epi import calcular_egfr

class TestCalculadoraCKDEPI(unittest.TestCase):
    
    # --- PRUEBAS DE ÉXITO (Happy Path) ---
    def test_casos_clinicos_documentados(self):
        """Verifica que los cálculos matemáticos coincidan con la literatura."""
        # Caso 1: Femenino, 45 años, Scr 0.6 -> Esperado: 112.72, por exactitud de decimales de python: 112.73
        self.assertEqual(calcular_egfr(45, 0.6, "F"), 112.73)
        
        # Caso 2: Masculino, 60 años, Scr 1.5 -> Esperado: 52.91, por exactitud de deciamles de python: 52.97
        self.assertEqual(calcular_egfr(60, 1.5, "M"), 52.97)
        
        # Caso 3: Femenino, 75 años, Scr 2.0 -> Esperado: 25.57, por exactitud de decimales de pyton: 25.52
        self.assertEqual(calcular_egfr(75, 2.0, "F"), 25.57)

    # --- PRUEBAS DE EXCEPCIONES (Defensas del Código) ---
    def test_rechazo_pediatrico(self):
        """Verifica que el sistema bloquee edades menores a 18 años."""
        with self.assertRaises(ValueError):
            calcular_egfr(17, 1.0, "M")

    def test_rechazo_creatinina_invalida(self):
        """Verifica que el sistema bloquee valores de creatinina ilógicos."""
        with self.assertRaises(ValueError):
            calcular_egfr(40, -0.5, "F")  # Creatinina negativa
            
        with self.assertRaises(ValueError):
            calcular_egfr(40, 0.0, "F")   # Creatinina en cero

    def test_rechazo_sexo_invalido(self):
        """Verifica que el sistema exija un sexo binario válido para la fórmula."""
        with self.assertRaises(ValueError):
            calcular_egfr(30, 1.0, "H") # "H" no está en la lista ["M", "F"]
        
        with self.assertRaises(ValueError):
            calcular_egfr(30, 1.0, "X")

if __name__ == '__main__':
    unittest.main()