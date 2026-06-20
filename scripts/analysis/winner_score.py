import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
import xgboost as xgb
import json
import os
import sys
from datetime import datetime

class WinnerScoreCalculator:
    """
    Clase para calcular el Winner Score de anuncios basado en múltiples factores
    """
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.feature_columns = [
            'copy_length', 'word_count', 'sentence_count', 'emoji_count',
            'exclamation_count', 'question_count', 'uppercase_ratio',
            'price_mentions', 'urgency_words', 'social_proof_words',
            'fear_words', 'benefit_words', 'hook_score', 'pain_score',
            'objection_score', 'angle_score', 'cta_score', 'days_active',
            'creative_variants'
        ]
    
    def extract_features(self, df):
        """
        Extrae características del DataFrame para el cálculo del Winner Score
        """
        features_df = df.copy()
        
        # Características de texto
        if 'Copy_Full' in df.columns:
            features_df['copy_length'] = df['Copy_Full'].apply(lambda x: len(str(x)) if pd.notna(x) else 0)
            features_df['word_count'] = df['Copy_Full'].apply(lambda x: len(str(x).split()) if pd.notna(x) else 0)
            features_df['sentence_count'] = df['Copy_Full'].apply(lambda x: str(x).count('.') + str(x).count('!') + str(x).count('?') if pd.notna(x) else 0)
            
            # Contar emojis (caracteres fuera del rango ASCII estándar)
            features_df['emoji_count'] = df['Copy_Full'].apply(lambda x: sum(1 for c in str(x) if ord(c) > 127 and ord(c) < 0x1F600 or ord(c) >= 0x1F600 and ord(c) <= 0x1F64F or ord(c) >= 0x1F300 and ord(c) <= 0x1F5FF or ord(c) >= 0x1F680 and ord(c) <= 0x1F6FF or ord(c) >= 0x1F1E0 and ord(c) <= 0x1F1FF) if pd.notna(x) else 0)
            
            # Contar signos de exclamación y pregunta
            features_df['exclamation_count'] = df['Copy_Full'].apply(lambda x: str(x).count('!') if pd.notna(x) else 0)
            features_df['question_count'] = df['Copy_Full'].apply(lambda x: str(x).count('?') if pd.notna(x) else 0)
            
            # Proporción de mayúsculas
            features_df['uppercase_ratio'] = df['Copy_Full'].apply(lambda x: sum(1 for c in str(x) if c.isupper()) / len(str(x)) if pd.notna(x) and len(str(x)) > 0 else 0)
        
        # Contar menciones de precios
        if 'Copy_Full' in df.columns:
            features_df['price_mentions'] = df['Copy_Full'].apply(lambda x: len(re.findall(r'[S$€¥]\d+|[S$€¥]\d+,\d+|[S$€¥]\d+\.\d+', str(x))) if pd.notna(x) else 0)
        
        # Contar palabras de urgencia
        urgency_words = ['ahora', 'corre', 'último', 'limitado', 'temporal', 'hoy', 'día', 'tiempo', 'prisa', 'rápido', 'urgente']
        if 'Copy_Full' in df.columns:
            features_df['urgency_words'] = df['Copy_Full'].apply(lambda x: sum(str(x).lower().count(word) for word in urgency_words) if pd.notna(x) else 0)
        
        # Contar palabras de prueba social
        social_proof_words = ['testimonios', 'miles', 'clientes', 'usuarios', 'opiniones', 'recomendado', 'popular', 'éxito']
        if 'Copy_Full' in df.columns:
            features_df['social_proof_words'] = df['Copy_Full'].apply(lambda x: sum(str(x).lower().count(word) for word in social_proof_words) if pd.notna(x) else 0)
        
        # Contar palabras de miedo
        fear_words = ['riesgo', 'peligro', 'cuidado', 'prevención', 'protección', 'daño', 'lesión', 'accidente', 'problema', 'dolor']
        if 'Copy_Full' in df.columns:
            features_df['fear_words'] = df['Copy_Full'].apply(lambda x: sum(str(x).lower().count(word) for word in fear_words) if pd.notna(x) else 0)
        
        # Contar palabras de beneficio
        benefit_words = ['gratis', 'gana', 'mejora', 'resultados', 'solución', 'ventaja', 'ganancia', 'beneficio', 'plus']
        if 'Copy_Full' in df.columns:
            features_df['benefit_words'] = df['Copy_Full'].apply(lambda x: sum(str(x).lower().count(word) for word in benefit_words) if pd.notna(x) else 0)
        
        # Características adicionales si están disponibles
        if 'Hook_Score' in df.columns:
            features_df['hook_score'] = df['Hook_Score']
        else:
            features_df['hook_score'] = 50  # Valor por defecto
            
        if 'Pain_Score' in df.columns:
            features_df['pain_score'] = df['Pain_Score']
        else:
            features_df['pain_score'] = 50  # Valor por defecto
            
        if 'Objection_Score' in df.columns:
            features_df['objection_score'] = df['Objection_Score']
        else:
            features_df['objection_score'] = 50  # Valor por defecto
            
        if 'Angle_Score' in df.columns:
            features_df['angle_score'] = df['Angle_Score']
        else:
            features_df['angle_score'] = 50  # Valor por defecto
            
        if 'CTA_Score' in df.columns:
            features_df['cta_score'] = df['CTA_Score']
        else:
            features_df['cta_score'] = 50  # Valor por defecto
        
        # Asegurar que las columnas de días activos y variantes creativas existen
        if 'Days_Active' in df.columns:
            features_df['days_active'] = df['Days_Active']
        else:
            features_df['days_active'] = 0
            
        if 'Creative_Variants' in df.columns:
            features_df['creative_variants'] = df['Creative_Variants']
        else:
            features_df['creative_variants'] = 1
        
        # Rellenar valores nulos con 0
        for col in self.feature_columns:
            if col in features_df.columns:
                features_df[col] = features_df[col].fillna(0)
            else:
                features_df[col] = 0
        
        return features_df[self.feature_columns]
    
    def calculate_basic_score(self, df):
        """
        Calcula un Winner Score básico basado en los pesos especificados:
        Hook 30% · Pain_Point 25% · Objection_Killed 20% · Sales_Angle 15% · CTA 10%
        """
        # Verificar si las columnas necesarias existen
        weights = {
            'Hook_Score': 0.30,
            'Pain_Score': 0.25,
            'Objection_Score': 0.20,
            'Angle_Score': 0.15,
            'CTA_Score': 0.10
        }
        
        total_weight = sum(weights.values())
        scores = []
        
        for idx, row in df.iterrows():
            score = 0
            actual_weights_sum = 0
            
            for col, weight in weights.items():
                if col in df.columns:
                    # Asegurarse de que el valor esté entre 0 y 100
                    value = min(max(row[col], 0), 100) if pd.notna(row[col]) else 50
                    score += value * weight
                    actual_weights_sum += weight
            
            # Si no todas las columnas estaban disponibles, ajustar los pesos
            if actual_weights_sum > 0:
                score = (score / actual_weights_sum) * total_weight
            
            scores.append(score)
        
        return scores
    
    def calculate_advanced_score(self, df):
        """
        Calcula un Winner Score más avanzado usando machine learning
        (Esto sería para fases posteriores cuando tengamos datos históricos)
        """
        # Por ahora, simplemente usar el score básico
        # En fases futuras, aquí se entrenaría un modelo con datos históricos
        return self.calculate_basic_score(df)
    
    def calculate_score(self, df, method='basic'):
        """
        Método principal para calcular el Winner Score
        """
        if method == 'basic':
            scores = self.calculate_basic_score(df)
        else:
            scores = self.calculate_advanced_score(df)
        
        # Asegurar que todos los scores estén entre 0 y 100
        scores = [min(max(score, 0), 100) for score in scores]
        
        return scores


def main():
    """
    Función principal para ejecutar el cálculo del Winner Score
    """
    if len(sys.argv) != 3:
        print("Uso: python winner_score.py <ruta_al_archivo_csv> <keyword>")
        print("Ejemplo: python winner_score.py output/radar/bd_meta_ads_moringa.csv moringa")
        return
    
    csv_path = sys.argv[1]
    keyword = sys.argv[2]
    
    # Verificar que el archivo existe
    if not os.path.exists(csv_path):
        print(f"Archivo no encontrado: {csv_path}")
        return
    
    # Leer el archivo CSV
    df = pd.read_csv(csv_path)
    
    # Inicializar calculadora
    calculator = WinnerScoreCalculator()
    
    # Calcular Winner Scores
    scores = calculator.calculate_score(df, method='basic')
    
    # Agregar los scores al dataframe
    df['Winner_Score'] = scores
    
    # Ordenar por Winner Score descendente
    df_sorted = df.sort_values(by='Winner_Score', ascending=False)
    
    # Guardar el ranking
    output_path = f"output/reportes_ia/ranking_ganadores.csv"
    
    # Crear directorio si no existe
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Si el archivo ya existe, agregar los nuevos resultados manteniendo los anteriores
    if os.path.exists(output_path):
        existing_df = pd.read_csv(output_path)
        combined_df = pd.concat([existing_df, df_sorted], ignore_index=True)
        combined_df = combined_df.sort_values(by='Winner_Score', ascending=False)
        combined_df.to_csv(output_path, index=False, encoding='utf-8-sig')
    else:
        df_sorted.to_csv(output_path, index=False, encoding='utf-8-sig')
    
    print(f"Ranking de ganadores actualizado y guardado en: {output_path}")
    
    # Imprimir Top 10
    print(f"\nTop 10 anuncios ganadores para la keyword '{keyword}':")
    top_10 = df_sorted.head(10)[['Fanpage_Name', 'Winner_Score']].reset_index(drop=True)
    top_10.index = range(1, len(top_10) + 1)
    print(top_10.to_string())
    
    # Guardar también un archivo específico para esta keyword
    keyword_output_path = f"output/reportes_ia/ranking_ganadores_{keyword}.csv"
    df_sorted.to_csv(keyword_output_path, index=False, encoding='utf-8-sig')
    print(f"\nRanking específico guardado en: {keyword_output_path}")


if __name__ == "__main__":
    import re  # Importar re para el procesamiento de texto
    
    main()