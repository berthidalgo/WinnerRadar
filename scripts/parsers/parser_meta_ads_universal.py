import pandas as pd
import re
from datetime import datetime
import os
from dateutil.relativedelta import relativedelta
import sys
import json

def parse_meta_ads_file(file_path, keyword):
    """
    Parser Universal de Meta Ads Library
    Extrae información de anuncios desde un archivo .txt copiado manualmente
    
    Args:
        file_path (str): Ruta al archivo .txt con los datos de Meta Ads
        keyword (str): Palabra clave asociada al archivo
    
    Returns:
        pd.DataFrame: DataFrame con la información extraída
    """
    
    # Leer el archivo
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Dividir en bloques usando "Identificador de la biblioteca:" como ancla
    blocks = re.split(r'(?=Identificador de la biblioteca:)', content)
    
    # Eliminar el primer bloque si está vacío o solo tiene texto antes del primer identificador
    if blocks and not blocks[0].strip():
        blocks = blocks[1:]
    
    parsed_data = []
    failed_blocks = 0
    
    for i, block in enumerate(blocks):
        try:
            # Extraer Ad_ID
            ad_id_match = re.search(r'Identificador de la biblioteca:\s*(.+)', block)
            ad_id = ad_id_match.group(1).strip() if ad_id_match else None
            
            # Extraer Start_Date
            date_match = re.search(r'En circulación desde el\s+(\d{1,2}\s+\w+\s+\d{4})', block)
            start_date_str = date_match.group(1).strip() if date_match else None
            start_date = None
            if start_date_str:
                # Convertir la fecha a formato YYYY-MM-DD
                day, month, year = start_date_str.split(' ')
                
                # Diccionario para traducir meses en español a números
                months_map = {
                    'ene': '01', 'feb': '02', 'mar': '03', 'abr': '04',
                    'may': '05', 'jun': '06', 'jul': '07', 'ago': '08',
                    'sep': '09', 'oct': '10', 'nov': '11', 'dic': '12'
                }
                
                month_num = months_map.get(month.lower(), month)
                start_date = f"{year}-{month_num.zfill(2)}-{day.zfill(2)}"
            
            # Calcular Days_Active
            days_active = 0
            if start_date:
                start_dt = datetime.strptime(start_date, '%Y-%m-%d')
                days_active = (datetime.now() - start_dt).days
            
            # Extraer Creative_Variants
            variants_match = re.search(r'(\d+)\s+anuncios usan este contenido', block)
            creative_variants = int(variants_match.group(1)) if variants_match else 1
            
            # Extraer Impressions_Level
            if 'Número de impresiones bajo' in block:
                impressions_level = 'Bajo'
            elif 'Número de impresiones alto' in block:
                impressions_level = 'Alto'
            else:
                impressions_level = 'Normal'
            
            # Extraer Fanpage (última línea válida antes de "Publicidad")
            lines_before_publicidad = block.split('Publicidad')[0].split('\n')
            # Buscar el nombre de la fanpage (generalmente aparece varias veces)
            fanpage_candidates = []
            for line in reversed(lines_before_publicidad):
                line = line.strip()
                if line and 'Identificador de la biblioteca:' not in line and \
                   'En circulación desde el' not in line and \
                   'Plataformas' not in line and \
                   'Número de impresiones' not in line and \
                   'Activo' not in line:
                    fanpage_candidates.append(line)
                    if len(fanpage_candidates) == 2:  # Tomamos el penúltimo si hay varios
                        break
            
            fanpage_name = fanpage_candidates[0] if fanpage_candidates else None
            
            # Extraer Copy_Completo (todo entre "Publicidad" y la duración/número de impresiones)
            publicidad_parts = block.split('Publicidad')
            if len(publicidad_parts) > 1:
                copy_part = publicidad_parts[1]
                # Terminar en duración (MM:SS) o en número de impresiones
                end_patterns = [
                    r'\d+:\d+',  # Duración MM:SS
                    r'anuncios usan este contenido',  # Fin por número de anuncios
                    r'Número de impresiones'  # Fin por impresiones
                ]
                
                copy_end_pos = len(copy_part)
                for pattern in end_patterns:
                    match = re.search(pattern, copy_part)
                    if match:
                        pos = match.start()
                        if pos < copy_end_pos:
                            copy_end_pos = pos
                
                copy_full = copy_part[:copy_end_pos].strip()
            else:
                copy_full = ""
            
            # Detectar formato y duración
            duration_match = re.search(r'(\d+:\d+)(?:\s*/\s*\d+:\d+)?', block)
            duration = duration_match.group(1) if duration_match else None
            format_type = 'Video' if duration else 'Imagen'
            
            # Detectar embudo
            if 'wa.me/' in copy_full or 'WhatsApp' in copy_full:
                funnel_type = 'WhatsApp'
            elif 'http://' in copy_full or 'https://' in copy_full:
                funnel_type = 'Web'
            elif 'formulario' in copy_full.lower() or 'form' in copy_full.lower():
                funnel_type = 'Formulario'
            else:
                funnel_type = 'Otro'
            
            # Detectar ofertas
            oferta_matches = re.findall(r'(2x1|\d+% OFF|[S$]\d+|USD \d+|Gratis)', copy_full)
            oferta = ', '.join(oferta_matches) if oferta_matches else None
            
            # Agregar datos al resultado
            parsed_data.append({
                'Keyword_Buscada': keyword,
                'Fanpage_Name': fanpage_name,
                'Fanpage_ID': None,  # No se extrae directamente del texto
                'Total_Ads_Active': 1,  # Cada bloque representa un anuncio
                'Ad_ID_Representativo': ad_id,
                'Start_Date': start_date,
                'Days_Active': days_active,
                'Creative_Variants': creative_variants,
                'Impressions_Level': impressions_level,
                'Format': format_type,
                'Duration': duration,
                'Funnel_Type': funnel_type,
                'Offer_Extracted': oferta,
                'Copy_Full': copy_full
            })
        
        except Exception as e:
            print(f"Bloque {i} fallido: {str(e)}")
            failed_blocks += 1
            continue
    
    print(f"Bloques detectados: {len(blocks)} | Bloques parseados: {len(parsed_data)} | Fallos: {failed_blocks}")
    
    return pd.DataFrame(parsed_data)


def main():
    """
    Función principal para ejecutar el parser
    """
    if len(sys.argv) != 3:
        print("Uso: python parser_meta_ads_universal.py <ruta_al_archivo_txt> <keyword>")
        print("Ejemplo: python parser_meta_ads_universal.py data/meta_ads_raw/moringa_raw.txt moringa")
        return
    
    file_path = sys.argv[1]
    keyword = sys.argv[2]
    
    # Verificar que el archivo existe
    if not os.path.exists(file_path):
        print(f"Archivo no encontrado: {file_path}")
        return
    
    # Parsear el archivo
    df = parse_meta_ads_file(file_path, keyword)
    
    if df.empty:
        print("No se pudieron extraer datos del archivo.")
        return
    
    # Mostrar las primeras 5 filas
    print("\nPrimeras 5 filas:")
    print(df.head())
    
    # Guardar en CSV
    output_path = f"output/radar/bd_meta_ads_{keyword}.csv"
    
    # Crear directorio si no existe
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"\nDatos guardados en: {output_path}")


if __name__ == "__main__":
    main()