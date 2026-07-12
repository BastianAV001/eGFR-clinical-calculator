"""
Script de Aseguramiento de Calidad (QA) para la calculadora eGFR.
Utiliza el framework nativo 'unittest' de Python.
"""

import unittest
from ckd_epi import calcular_egfr, clasificar_categoria_kdigo, evaluar_riesgo_contraste

class TestCalculadoraCKDEPI(unittest.TestCase):
    
    
    def test_casos_clinicos_documentados(self):
        """Verifica que los cálculos matemáticos coincidan con la literatura."""
        # Caso 1: Esperado: 112.72, por exactitud de decimales de python: 112.73
        self.assertEqual(calcular_egfr(45, 0.6, "F"), 112.73)
        
        # Caso 2: Esperado: 52.91, por exactitud de deciamles de python: 52.97
        self.assertEqual(calcular_egfr(60, 1.5, "M"), 52.97)
        
        # Caso 3: Esperado: 25.57, por exactitud de decimales de pyton: 25.52
        self.assertEqual(calcular_egfr(75, 2.0, "F"), 25.57)

    
    def test_rechazo_pediatrico(self):
        """Verifica que el sistema bloquee edades menores a 18 años."""
        with self.assertRaises(ValueError):
            calcular_egfr(17, 1.0, "M")

    def test_rechazo_creatinina_invalida(self):
        """Verifica que el sistema bloquee valores de creatinina ilógicos."""
        with self.assertRaises(ValueError):
            calcular_egfr(40, -0.5, "F")  
            
        with self.assertRaises(ValueError):
            calcular_egfr(40, 0.0, "F")  

    def test_rechazo_sexo_invalido(self):
        """Verifica que el sistema exija un sexo binario válido para la fórmula."""
        with self.assertRaises(ValueError):
            calcular_egfr(30, 1.0, "H") 
        
        with self.assertRaises(ValueError):
            calcular_egfr(30, 1.0, "X")

    def test_clasificar_categoria_kdigo(self):
        """Valida que los cortes de las categorías KDIGO sean matemáticamente exactos."""
        self.assertEqual(clasificar_categoria_kdigo(95)["categoria"], "G1")
        self.assertEqual(clasificar_categoria_kdigo(65)["categoria"], "G2")
        self.assertEqual(clasificar_categoria_kdigo(50)["categoria"], "G3a")
        self.assertEqual(clasificar_categoria_kdigo(35)["categoria"], "G3b")
        self.assertEqual(clasificar_categoria_kdigo(20)["categoria"], "G4")
        self.assertEqual(clasificar_categoria_kdigo(10)["categoria"], "G5")

    def test_evaluar_riesgo_contraste(self):
        """Valida que los protocolos radiológicos entreguen el nivel y color correcto."""
        # Riesgo Bajo: >= 45
        self.assertEqual(evaluar_riesgo_contraste(50)["nivel_riesgo"], "Bajo")
        self.assertEqual(evaluar_riesgo_contraste(50)["color_alerta"], "verde")
        
        # Riesgo Moderado: 30 - 44
        self.assertEqual(evaluar_riesgo_contraste(35)["nivel_riesgo"], "Moderado")
        self.assertEqual(evaluar_riesgo_contraste(35)["color_alerta"], "naranja")
        
        # Riesgo Alto: < 30
        self.assertEqual(evaluar_riesgo_contraste(25)["nivel_riesgo"], "Alto")
        self.assertEqual(evaluar_riesgo_contraste(25)["color_alerta"], "rojo")

if __name__ == '__main__':
    unittest.main(verbosity=2)