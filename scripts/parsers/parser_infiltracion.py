import pandas as pd
import re
from datetime import datetime
import os
import sys

def parse_infiltracion_file(file_path, fanpage_name):
    """
    Parser de Infiltración para perfiles completos de anunciantes
    
    Args:
        file_path (str): Ruta al archivo .txt con los datos del perfil completo
        fanpage_name (str): Nombre de la fanpage infiltrada
    
    Returns:
        pd.DataFrame: DataFrame con la información extraída
    """
    
    # Leer el archivo
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    parsed_data = []
    
    # Detectar productos/servicios (patrones comunes en el texto)
    # Esto puede incluir nombres de productos, categorías, etc.
    product_patterns = [
        r'([A-Z][a-z]+\w+)',  # Palabras que comienzan con mayúscula
        r'(\w+\s+\w+)',  # Combinaciones de dos palabras
    ]
    
    # Detectar tipos de embudo
    whatsapp_count = len(re.findall(r'(wa\.me|whatsapp|mensaje|contacto)', content, re.IGNORECASE))
    web_count = len(re.findall(r'(http|www|landing|pagina|sitio|web)', content, re.IGNORECASE))
    form_count = len(re.findall(r'(formulario|registro|form|formulario)', content, re.IGNORECASE))
    dm_count = len(re.findall(r'(dm|mensaje directo|inbox)', content, re.IGNORECASE))
    
    total_funnel_types = max(1, whatsapp_count + web_count + form_count + dm_count)
    
    whatsapp_pct = round((whatsapp_count / total_funnel_types) * 100, 2)
    web_pct = round((web_count / total_funnel_types) * 100, 2)
    form_pct = round((form_count / total_funnel_types) * 100, 2)
    dm_pct = round((dm_count / total_funnel_types) * 100, 2)
    
    # Detectar rangos de precios
    price_patterns = re.findall(r'([S$€]\d+|[S$€]\d+,\d+|[S$€]\d+\.\d+)', content)
    if price_patterns:
        price_ranges = {'min': min(price_patterns), 'max': max(price_patterns)}
    else:
        price_ranges = {}
    
    # Detectar patrones de oferta
    offer_patterns = []
    offer_matches = re.findall(r'(2x1|\d+% OFF|gratis|oferta|promoción|descuento)', content, re.IGNORECASE)
    for match in set(offer_matches):  # Usar set para evitar duplicados
        offer_patterns.append(match.lower())
    
    # Detectar ángulos de venta
    angle_keywords = {
        'salud': ['salud', 'bienestar', 'nutrición', 'vitamina', 'orgánico', 'natural'],
        'estética': ['belleza', 'piel', 'cuerpo', 'adelgazar', 'estético'],
        'ahorro': ['ahorro', 'barato', 'económico', 'oferta', 'descuento'],
        'urgencia': ['ahora', 'corre', 'último', 'limitado', 'rápido'],
        'autoridad': ['científico', 'médico', 'doctor', 'experto', 'estudio'],
        'estatus': ['exclusivo', 'premium', 'elite', 'vip', 'único'],
        'miedo': ['riesgo', 'peligro', 'cuidado', 'prevención'],
        'comodidad': ['cómodo', 'fácil', 'simple', 'rápido', 'instantáneo']
    }
    
    detected_angles = []
    content_lower = content.lower()
    for angle, keywords in angle_keywords.items():
        for keyword in keywords:
            if keyword in content_lower:
                if angle not in detected_angles:
                    detected_angles.append(angle)
    
    # Detectar CTAs frecuentes
    cta_patterns = []
    cta_matches = re.findall(r'(comprar|agendar|descargar|contactar|registrarse|llamar|pedir|obtener|adquirir|solicitar|comienza|iniciar)', content, re.IGNORECASE)
    for match in set(cta_matches):
        cta_patterns.append(match.lower())
    
    # Contar ads activos vs inactivos (esto es una aproximación basada en patrones)
    # Asumiendo que ciertos términos indican actividad
    active_patterns = len(re.findall(r'(activo|vigente|disponible|en stock|disponible ahora)', content, re.IGNORECASE))
    inactive_patterns = len(re.findall(r'(inactivo|finalizado|terminado|fuera de stock)', content, re.IGNORECASE))
    
    activity_ratio = 0
    if (active_patterns + inactive_patterns) > 0:
        activity_ratio = round((active_patterns / (active_patterns + inactive_patterns)) * 100, 2)
    
    # Crear una entrada con toda la información recolectada
    parsed_data.append({
        'fanpage_name': fanpage_name,
        'fanpage_id': None,  # No se extrae directamente del texto
        'productos_detectados': str([]),  # Placeholder, se podría mejorar con NLP
        'frontend_products': str([]),  # Placeholder
        'backend_products': str([]),  # Placeholder
        'funnel_whatsapp_pct': whatsapp_pct,
        'funnel_web_pct': web_pct,
        'funnel_form_pct': form_pct,
        'funnel_dm_pct': dm_pct,
        'price_ranges': str(price_ranges),
        'offer_patterns': str(offer_patterns),
        'dominant_angles': str(detected_angles),
        'frequent_ctas': str(cta_patterns),
        'active_ads_count': active_patterns,
        'inactive_ads_count': inactive_patterns,
        'activity_ratio': activity_ratio
    })
    
    return pd.DataFrame(parsed_data)


def main():
    """
    Función principal para ejecutar el parser de infiltración
    """
    if len(sys.argv) != 3:
        print("Uso: python parser_infiltracion.py <ruta_al_archivo_txt> <fanpage_name>")
        print("Ejemplo: python parser_infiltracion.py data/infiltracion/naturavida_completo.txt naturavida")
        return
    
    file_path = sys.argv[1]
    fanpage_name = sys.argv[2]
    
    # Verificar que el archivo existe
    if not os.path.exists(file_path):
        print(f"Archivo no encontrado: {file_path}")
        return
    
    # Parsear el archivo de infiltración
    df = parse_infiltracion_file(file_path, fanpage_name)
    
    if df.empty:
        print("No se pudieron extraer datos del archivo de infiltración.")
        return
    
    # Mostrar el resultado
    print("\nDatos extraídos:")
    print(df)
    
    # Guardar en CSV
    output_path = f"output/infiltracion/reporte_{fanpage_name}.csv"
    
    # Crear directorio si no existe
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"\nReporte guardado en: {output_path}")
    
    # Registrar timestamp de ejecución en el log de ejecuciones
    log_path = "output/ejecuciones_log.csv"
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_entry = pd.DataFrame([{
        'timestamp': timestamp,
        'keyword': fanpage_name,
        'bloques_total': len(df),
        'bloques_ok': len(df),
        'fallos': 0,
        'status': 'infiltration_completed'
    }])
    
    # Si el archivo de log existe, agregar, si no crear con encabezado
    if os.path.exists(log_path):
        log_entry.to_csv(log_path, mode='a', header=False, index=False, encoding='utf-8-sig')
    else:
        log_entry.to_csv(log_path, mode='w', header=True, index=False, encoding='utf-8-sig')
    
    print(f"Registro de ejecución agregado a: {log_path}")


if __name__ == "__main__":
    main()