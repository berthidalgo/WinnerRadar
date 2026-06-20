import pandas as pd
import json
import os
import sys
from datetime import datetime

def analizar_copies_con_ia(csv_path, keyword):
    """
    Analiza los copies de anuncios usando técnicas de IA/heurística
    
    Args:
        csv_path (str): Ruta al archivo CSV con los datos de anuncios
        keyword (str): Palabra clave asociada al análisis
    
    Returns:
        list: Lista de diccionarios con el análisis de cada copy
    """
    
    # Leer el archivo CSV
    df = pd.read_csv(csv_path)
    
    resultados = []
    
    for index, row in df.iterrows():
        copy_text = row.get('Copy_Full', '')
        
        if pd.isna(copy_text) or copy_text == '':
            continue
        
        # Análisis heurístico del copy (simulando lo que haría la IA)
        # En un entorno real, esto se haría con un modelo de lenguaje
        analysis = analisis_heuristico_copy(copy_text)
        
        # Calcular Winner Score basado en los pesos especificados
        winner_score = calcular_winner_score(analysis)
        
        resultado = {
            'ad_id': row.get('Ad_ID_Representativo', ''),
            'copy_original': copy_text,
            'hook_principal': analysis['hook_principal'],
            'pain_point': analysis['pain_point'],
            'objection_killed': analysis['objection_killed'],
            'sales_angle': analysis['sales_angle'],
            'tone': analysis['tone'],
            'target_audience': analysis['target_audience'],
            'cta_type': analysis['cta_type'],
            'winner_score': winner_score,
            'confidence': analysis['confidence']
        }
        
        resultados.append(resultado)
    
    return resultados


def analisis_heuristico_copy(copy_text):
    """
    Realiza un análisis heurístico básico del copy simulando lo que haría una IA
    """
    
    # Convertir a minúsculas para análisis
    lower_text = copy_text.lower()
    
    # Detectar posibles hooks (palabras que captan atención)
    hook_indicators = [
        '¡', '?', 'atención', 'importante', 'novedad', 'nuevo', 'exclusivo',
        'sorpresa', 'checa', 'mira', 'ojo', 'alerta', 'urgente'
    ]
    
    # Detectar posibles pain points (problemas emocionales/físicos/financieros)
    pain_points = [
        'problema', 'dolor', 'miedo', 'preocupación', 'ansiedad', 'insomnio',
        'estrés', 'presión', 'dificultad', 'fracaso', 'fracasar', 'engaño',
        'estafa', 'engaños', 'riesgo', 'riesgos', 'pérdida', 'pérdidas'
    ]
    
    # Detectar posibles objeciones resueltas
    objections = [
        'garantía', 'gratis', 'sin costo', 'prueba', 'devolución', 'devolver',
        'riesgo cero', 'seguro', 'confiable', 'certificado', 'verificado'
    ]
    
    # Detectar ángulos de venta
    angles = {
        'salud': ['salud', 'bienestar', 'nutrición', 'vitamina', 'orgánico', 'natural', 'medicina', 'cura', 'tratamiento'],
        'estética': ['belleza', 'piel', 'cuerpo', 'adelgazar', 'estético', 'juvenil', 'joven', 'gordura', 'flacura'],
        'ahorro': ['ahorro', 'barato', 'económico', 'oferta', 'descuento', 'promo', 'promoción', 'rebaja', 'precio'],
        'urgencia': ['ahora', 'corre', 'último', 'limitado', 'temporal', 'hoy', 'día', 'tiempo', 'prisa', 'rápido'],
        'autoridad': ['científico', 'médico', 'doctor', 'experto', 'estudio', 'investigación', 'prueba', 'evidencia'],
        'estatus': ['exclusivo', 'premium', 'elite', 'vip', 'único', 'especial', 'lujo', 'clase', 'alta'],
        'miedo': ['riesgo', 'peligro', 'cuidado', 'prevención', 'protección', 'daño', 'lesión', 'accidente'],
        'comodidad': ['cómodo', 'fácil', 'simple', 'rápido', 'instantáneo', 'directo', 'desde casa', 'online']
    ]
    
    # Detectar tonos
    tones = {
        'agresivo': ['¡', 'corre', 'urgente', 'ahora', 'inmediato', 'rápido', 'solo hoy', 'últimas unidades'],
        'educativo': ['información', 'datos', 'estudio', 'ciencia', 'investigación', 'como', 'por qué', 'cuándo'],
        'empático': ['entiendo', 'comprendo', 'igual', 'también', 'contigo', 'apoyo', 'ayuda', 'juntos'],
        'científico': ['estudio', 'investigación', 'ciencia', 'datos', 'prueba', 'evidencia', 'científico', 'médico'],
        'humorístico': ['risa', 'divertido', 'chiste', 'gracioso', 'comedia', 'reír', 'sonreír', 'entretenido'],
        'inspiracional': ['inspira', 'motiva', 'lograr', 'superar', 'triunfar', 'éxito', 'ganador', 'campeón']
    }
    
    # Detectar CTAs (Call to Action)
    ctas = [
        'comprar', 'agendar', 'descargar', 'contactar', 'registrarse', 'llamar', 
        'pedir', 'obtener', 'adquirir', 'solicitar', 'comienza', 'iniciar', 
        'click', 'haz clic', 'presiona', 'visita', 'envía', 'mensaje'
    ]
    
    # Extraer información heurística
    hook_principal = ""
    pain_point = ""
    objection_killed = ""
    sales_angle = "otros"
    tone = "neutro"
    target_audience = "general"
    cta_type = "otros"
    
    # Detectar hook
    for indicator in hook_indicators:
        if indicator in lower_text:
            # Obtener las primeras frases como posible hook
            sentences = copy_text.split('.')
            for sentence in sentences[:2]:  # Tomar las primeras dos frases
                if indicator in sentence.lower():
                    hook_principal = sentence.strip()
                    break
            if hook_principal:
                break
    
    # Si no se encontró hook con indicadores, tomar las primeras palabras
    if not hook_principal:
        words = copy_text.split()
        hook_principal = ' '.join(words[:5])  # Primeras 5 palabras como hook
    
    # Detectar pain point
    for pain in pain_points:
        if pain in lower_text:
            pain_point = pain
            break
    
    # Detectar objeción resuelta
    for obj in objections:
        if obj in lower_text:
            objection_killed = obj
            break
    
    # Detectar ángulo de venta
    detected_angles = []
    for angle, keywords in angles.items():
        for keyword in keywords:
            if keyword in lower_text:
                if angle not in detected_angles:
                    detected_angles.append(angle)
    
    if detected_angles:
        sales_angle = detected_angles[0]  # Tomar el primero detectado
    
    # Detectar tono
    detected_tones = []
    for tone_name, keywords in tones.items():
        for keyword in keywords:
            if keyword in lower_text:
                if tone_name not in detected_tones:
                    detected_tones.append(tone_name)
    
    if detected_tones:
        tone = detected_tones[0]  # Tomar el primero detectado
    
    # Detectar CTA
    for cta in ctas:
        if cta in lower_text:
            cta_type = cta
            break
    
    # Determinar audiencia objetivo (heurística básica)
    if any(word in lower_text for word in ['mujer', 'femenino', 'ella']):
        target_audience = "mujeres"
    elif any(word in lower_text for word in ['hombre', 'masculino', 'él']):
        target_audience = "hombres"
    elif any(word in lower_text for word in ['adulto', 'mayor', 'tercera edad']):
        target_audience = "adultos mayores"
    elif any(word in lower_text for word in ['joven', 'adolescente', 'niño', 'niña']):
        target_audience = "jóvenes"
    
    return {
        'hook_principal': hook_principal,
        'pain_point': pain_point,
        'objection_killed': objection_killed,
        'sales_angle': sales_angle,
        'tone': tone,
        'target_audience': target_audience,
        'cta_type': cta_type,
        'confidence': 0.7  # Confianza promedio para análisis heurístico
    }


def calcular_winner_score(analysis):
    """
    Calcula el Winner Score basado en los pesos especificados:
    Hook 30% · Pain_Point 25% · Objection_Killed 20% · Sales_Angle 15% · CTA 10%
    """
    # Asignar puntajes simples (0-100) basados en la presencia de elementos
    hook_score = 80 if analysis['hook_principal'] else 0
    pain_score = 80 if analysis['pain_point'] else 0
    objection_score = 80 if analysis['objection_killed'] else 0
    angle_score = 80 if analysis['sales_angle'] != 'otros' else 0
    cta_score = 80 if analysis['cta_type'] != 'otros' else 0
    
    # Calcular el score ponderado
    winner_score = (
        hook_score * 0.30 +
        pain_score * 0.25 +
        objection_score * 0.20 +
        angle_score * 0.15 +
        cta_score * 0.10
    )
    
    return round(winner_score, 2)


def main():
    """
    Función principal para ejecutar el análisis de IA de copies
    """
    if len(sys.argv) != 3:
        print("Uso: python ia_analisis_copies.py <ruta_al_archivo_csv> <keyword>")
        print("Ejemplo: python ia_analisis_copies.py output/radar/bd_meta_ads_moringa.csv moringa")
        return
    
    csv_path = sys.argv[1]
    keyword = sys.argv[2]
    
    # Verificar que el archivo existe
    if not os.path.exists(csv_path):
        print(f"Archivo no encontrado: {csv_path}")
        return
    
    # Analizar los copies
    resultados = analizar_copies_con_ia(csv_path, keyword)
    
    if not resultados:
        print("No se encontraron copies para analizar.")
        return
    
    # Guardar resultados en JSON
    output_path = f"output/reportes_ia/analisis_copies_{keyword}.json"
    
    # Crear directorio si no existe
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(resultados, f, ensure_ascii=False, indent=2)
    
    print(f"Análisis de IA completado. Resultados guardados en: {output_path}")
    
    # También guardar una versión CSV con los resultados principales
    csv_output_path = f"output/reportes_ia/analisis_copies_{keyword}.csv"
    
    df_resultados = pd.DataFrame(resultados)
    df_resultados.to_csv(csv_output_path, index=False, encoding='utf-8-sig')
    
    print(f"Resultados también guardados en formato CSV: {csv_output_path}")
    
    # Imprimir los primeros resultados como muestra
    print("\nPrimeros resultados del análisis:")
    for i, resultado in enumerate(resultados[:3]):
        print(f"\n{i+1}. Hook: {resultado['hook_principal'][:50]}...")
        print(f"   Ángulo: {resultado['sales_angle']}")
        print(f"   Winner Score: {resultado['winner_score']}")


if __name__ == "__main__":
    main()