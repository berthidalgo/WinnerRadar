import pandas as pd
import numpy as np
from datetime import datetime
import os
import sys

def aplicar_filtro_ballenas(input_file, keyword):
    """
    Aplica el filtro de ballenas a un CSV de resultados del radar
    
    Args:
        input_file (str): Ruta al archivo CSV de entrada
        keyword (str): Palabra clave asociada al análisis
    
    Returns:
        pd.DataFrame: DataFrame con las ballenas filtradas
    """
    
    # Leer el archivo CSV
    df = pd.read_csv(input_file)
    
    print(f"Total de registros antes del filtro: {len(df)}")
    
    # Aplicar filtro de Ballenas:
    # - Days_Active >= 7 (Scaler confirmado)
    # - Creative_Variants >= 2 (creative testing validado)
    df_filtrado = df[
        (df['Days_Active'] >= 7) &
        (df['Creative_Variants'] >= 2)
    ].copy()
    
    print(f"Registros después del filtro (Days_Active >= 7 y Creative_Variants >= 2): {len(df_filtrado)}")
    
    # Agrupar por Fanpage_Name y calcular métricas
    df_agrupado = df_filtrado.groupby('Fanpage_Name').agg({
        'Total_Ads_Active': ['sum', 'count'],
        'Days_Active': 'mean',
        'Creative_Variants': 'max'
    }).round(2)
    
    # Renombrar columnas
    df_agrupado.columns = [
        'total_ads_por_fanpage',
        'cantidad_registros',
        'avg_days_active',
        'max_creative_variants'
    ]
    
    # Resetear índice para que Fanpage_Name sea una columna
    df_agrupado = df_agrupado.reset_index()
    
    # Calcular Ballena_Score = (total_ads * 0.4) + (avg_days * 0.3) + (max_variants * 0.3)
    df_agrupado['ballena_score'] = (
        df_agrupado['total_ads_por_fanpage'] * 0.4 +
        df_agrupado['avg_days_active'] * 0.3 +
        df_agrupado['max_creative_variants'] * 0.3
    ).round(2)
    
    # Ordenar descendente por Ballena_Score
    df_resultado = df_agrupado.sort_values(by='ballena_score', ascending=False)
    
    # Añadir columna con la posición de ranking
    df_resultado['ranking_position'] = range(1, len(df_resultado) + 1)
    
    # Seleccionar solo las columnas relevantes
    df_resultado = df_resultado[[
        'ranking_position',
        'Fanpage_Name',
        'total_ads_por_fanpage',
        'avg_days_active',
        'max_creative_variants',
        'ballena_score'
    ]]
    
    # Añadir la keyword buscada
    df_resultado.insert(0, 'keyword_buscada', keyword)
    
    return df_resultado


def main():
    """
    Función principal para ejecutar el filtro de ballenas
    """
    if len(sys.argv) != 3:
        print("Uso: python filtro_ballenas.py <ruta_al_archivo_csv> <keyword>")
        print("Ejemplo: python filtro_ballenas.py output/radar/bd_meta_ads_moringa.csv moringa")
        return
    
    input_file = sys.argv[1]
    keyword = sys.argv[2]
    
    # Verificar que el archivo existe
    if not os.path.exists(input_file):
        print(f"Archivo no encontrado: {input_file}")
        return
    
    # Aplicar filtro de ballenas
    df_resultado = aplicar_filtro_ballenas(input_file, keyword)
    
    if df_resultado.empty:
        print("No se encontraron ballenas con los criterios especificados.")
        return
    
    # Imprimir Top 5 con sus métricas
    print("\nTop 5 Ballenas:")
    print(df_resultado.head().to_string(index=False))
    
    # Guardar en CSV
    output_path = f"output/infiltracion/ballenas_{keyword}.csv"
    
    # Crear directorio si no existe
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    df_resultado.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"\nResultados guardados en: {output_path}")
    
    # Registrar timestamp de ejecución en el log de ejecuciones
    log_path = "output/ejecuciones_log.csv"
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_entry = pd.DataFrame([{
        'timestamp': timestamp,
        'keyword': keyword,
        'bloques_total': len(pd.read_csv(input_file)),
        'bloques_ok': len(df_resultado),
        'fallos': 0,
        'status': 'completed'
    }])
    
    # Si el archivo de log existe, agregar, si no crear con encabezado
    if os.path.exists(log_path):
        log_entry.to_csv(log_path, mode='a', header=False, index=False, encoding='utf-8-sig')
    else:
        log_entry.to_csv(log_path, mode='w', header=True, index=False, encoding='utf-8-sig')
    
    print(f"Registro de ejecución agregado a: {log_path}")


if __name__ == "__main__":
    main()