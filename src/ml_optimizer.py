"""
Módulo de Otimização com Machine Learning
Para usar: pip install scikit-learn joblib
"""

import sys
sys.path.insert(0, '.')

from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas as pd
import joblib
from cash_allocation_model import InputParameters, AllocationStrategy, CashAllocationModel


class MLOptimizer:
    """
    Otimizador baseado em Machine Learning
    Aprende padrões de alocações bem-sucedidas para sugerir estratégias ótimas
    """
    
    def __init__(self):
        self.model_reserva = None
        self.model_crescimento = None
        self.model_risco = None
        self.scaler = StandardScaler()
        self.is_trained = False
    
    def generate_training_data(self, n_samples=10000):
        """
        Gera dados de treino simulando múltiplos cenários
        """
        print(f"🔄 Gerando {n_samples} amostras de treino...")
        
        data = []
        
        for i in range(n_samples):
            # Gerar parâmetros aleatórios
            params = InputParameters(
                dinheiro_em_maos=np.random.uniform(10000, 500000),
                caixa_mensal_esperado=np.random.uniform(5000, 100000),
                despesas_fixas=np.random.uniform(2000, 50000),
                despesas_variaveis=np.random.uniform(1000, 30000),
                volatilidade_caixa=np.random.uniform(0.05, 0.40),
                tolerancia_risco=np.random.uniform(0.1, 0.9),
                meses_protegidos=np.random.randint(3, 12)
            )
            
            # Criar modelo e sugerir alocação
            modelo = CashAllocationModel(params)
            alocacao = modelo.suggest_allocation()
            
            # Avaliar (sem Monte Carlo para rapidez)
            resultado = modelo.evaluate_allocation(alocacao, use_monte_carlo=False)
            
            # Armazenar features e targets
            features = [
                params.dinheiro_em_maos,
                params.caixa_mensal_esperado,
                params.despesas_fixas,
                params.despesas_variaveis,
                params.volatilidade_caixa,
                params.tolerancia_risco,
                params.meses_protegidos,
                params.caixa_mensal_esperado / (params.despesas_fixas + params.despesas_variaveis),  # Índice de folga
                params.dinheiro_em_maos / (params.despesas_fixas + params.despesas_variaveis)  # Meses de reserva
            ]
            
            targets = [
                alocacao.reserva_seguranca_pct,
                alocacao.crescimento_pct,
                alocacao.risco_pct,
                float(resultado.alocacao_valida),
                resultado.probabilidade_sobrevivencia_ruim
            ]
            
            data.append(features + targets)
            
            if (i + 1) % 1000 == 0:
                print(f"   Processadas {i + 1}/{n_samples} amostras...")
        
        # Criar DataFrame
        columns = [
            'dinheiro', 'caixa_mensal', 'despesas_fixas', 'despesas_variaveis',
            'volatilidade', 'tolerancia', 'meses_protegidos', 'indice_folga', 'meses_reserva',
            'reserva_pct', 'crescimento_pct', 'risco_pct', 'valida', 'prob_sobrev'
        ]
        
        df = pd.DataFrame(data, columns=columns)
        
        # Salvar na pasta data/
        import os
        os.makedirs('data', exist_ok=True)
        df.to_csv('data/training_data.csv', index=False)
        print("✅ Dados de treino salvos em 'data/training_data.csv'")
        
        return df
    
    def train(self, df=None):
        """
        Treina modelos de ML para prever alocações ótimas
        """
        if df is None:
            try:
                df = pd.read_csv('data/training_data.csv')
            except FileNotFoundError:
                print("⚠️  Dados de treino não encontrados. Gerando...")
                df = self.generate_training_data()
        
        print("\n🤖 Treinando modelos de Machine Learning...")
        
        # Features e targets
        feature_cols = [
            'dinheiro', 'caixa_mensal', 'despesas_fixas', 'despesas_variaveis',
            'volatilidade', 'tolerancia', 'meses_protegidos', 'indice_folga', 'meses_reserva'
        ]
        
        X = df[feature_cols].values
        y_reserva = df['reserva_pct'].values
        y_crescimento = df['crescimento_pct'].values
        y_risco = df['risco_pct'].values
        
        # Normalizar features
        X_scaled = self.scaler.fit_transform(X)
        
        # Treinar modelos
        print("   Treinando modelo para Reserva de Segurança...")
        self.model_reserva = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
        self.model_reserva.fit(X_scaled, y_reserva)
        
        print("   Treinando modelo para Crescimento...")
        self.model_crescimento = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
        self.model_crescimento.fit(X_scaled, y_crescimento)
        
        print("   Treinando modelo para Risco...")
        self.model_risco = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
        self.model_risco.fit(X_scaled, y_risco)
        
        self.is_trained = True
        
        # Avaliar
        print("\n📊 Avaliação dos modelos:")
        print(f"   Reserva - R²: {self.model_reserva.score(X_scaled, y_reserva):.3f}")
        print(f"   Crescimento - R²: {self.model_crescimento.score(X_scaled, y_crescimento):.3f}")
        print(f"   Risco - R²: {self.model_risco.score(X_scaled, y_risco):.3f}")
        
        print("\n✅ Modelos treinados com sucesso!")
    
    def predict_allocation(self, params: InputParameters) -> AllocationStrategy:
        """
        Prevê a melhor alocação usando ML
        """
        if not self.is_trained:
            raise ValueError("Modelos não treinados. Execute train() primeiro.")
        
        # Preparar features
        folga = params.caixa_mensal_esperado / (params.despesas_fixas + params.despesas_variaveis)
        meses_res = params.dinheiro_em_maos / (params.despesas_fixas + params.despesas_variaveis)
        
        features = np.array([[
            params.dinheiro_em_maos,
            params.caixa_mensal_esperado,
            params.despesas_fixas,
            params.despesas_variaveis,
            params.volatilidade_caixa,
            params.tolerancia_risco,
            params.meses_protegidos,
            folga,
            meses_res
        ]])
        
        # Normalizar
        features_scaled = self.scaler.transform(features)
        
        # Prever (RandomForest pode gerar valores negativos/inesperados)
        reserva_raw = self.model_reserva.predict(features_scaled)[0]
        crescimento_raw = self.model_crescimento.predict(features_scaled)[0]
        risco_raw = self.model_risco.predict(features_scaled)[0]
        
        # Garantir valores não-negativos com mínimos
        reserva_pct = max(0.1, reserva_raw)
        crescimento_pct = max(0.1, crescimento_raw)
        risco_pct = max(0.0, risco_raw)
        
        # Normalizar para somar 100% com safety check
        total = reserva_pct + crescimento_pct + risco_pct
        if total <= 0:
            # Fallback: alocação padrão conservadora
            return AllocationStrategy(
                reserva_seguranca_pct=50.0,
                crescimento_pct=30.0,
                risco_pct=20.0
            )
        
        # Normalizar percentuais
        reserva_pct = (reserva_pct / total) * 100
        crescimento_pct = (crescimento_pct / total) * 100
        risco_pct = (risco_pct / total) * 100
        
        # Garantir que somam exatamente 100% (ajustar risco por rounding)
        risco_pct = 100.0 - reserva_pct - crescimento_pct
        
        return AllocationStrategy(
            reserva_seguranca_pct=round(max(0.0, reserva_pct), 2),
            crescimento_pct=round(max(0.0, crescimento_pct), 2),
            risco_pct=round(max(0.0, risco_pct), 2)
        )
    
    def evaluate_allocation_with_ml(
        self, 
        params: InputParameters,
        use_monte_carlo: bool = True,
        n_monte_carlo: int = 500
    ):
        """
        Combina previsão ML com validação Monte Carlo para eficiência
        Retorna o resultado da avaliação usando a alocação do ML
        """
        if not self.is_trained:
            raise ValueError("Modelos não treinados. Execute train() primeiro.")
        
        # Usar previsão do ML (muito rápido)
        alocacao = self.predict_allocation(params)
        
        # Validar com Monte Carlo do modelo tradicional (mais confiável)
        modelo = CashAllocationModel(params)
        resultado = modelo.evaluate_allocation(alocacao, use_monte_carlo=use_monte_carlo)
        
        return resultado, alocacao
    
    def save_models(self, prefix="ml_optimizer", folder="models"):
        """Salva modelos treinados na pasta models/"""
        import os
        os.makedirs(folder, exist_ok=True)
        joblib.dump(self.model_reserva, f"{folder}/{prefix}_reserva.pkl")
        joblib.dump(self.model_crescimento, f"{folder}/{prefix}_crescimento.pkl")
        joblib.dump(self.model_risco, f"{folder}/{prefix}_risco.pkl")
        joblib.dump(self.scaler, f"{folder}/{prefix}_scaler.pkl")
        print(f"✅ Modelos salvos em '{folder}/' com prefixo '{prefix}'")
    
    def load_models(self, prefix="ml_optimizer", folder="models"):
        """Carrega modelos treinados da pasta models/"""
        self.model_reserva = joblib.load(f"{folder}/{prefix}_reserva.pkl")
        self.model_crescimento = joblib.load(f"{folder}/{prefix}_crescimento.pkl")
        self.model_risco = joblib.load(f"{folder}/{prefix}_risco.pkl")
        self.scaler = joblib.load(f"{folder}/{prefix}_scaler.pkl")
        self.is_trained = True
        print(f"✅ Modelos carregados de '{folder}/'")


def exemplo_uso_ml():
    """Exemplo de uso do otimizador ML"""
    print("=" * 80)
    print("🤖 EXEMPLO: OTIMIZAÇÃO COM MACHINE LEARNING")
    print("=" * 80)
    
    # Criar otimizador
    optimizer = MLOptimizer()
    
    # Treinar modelos
    optimizer.train()
    
    # Salvar modelos
    optimizer.save_models()
    
    # Testar predição
    params = InputParameters(
        dinheiro_em_maos=100000.0,
        caixa_mensal_esperado=15000.0,
        despesas_fixas=8000.0,
        despesas_variaveis=3000.0,
        volatilidade_caixa=0.15,
        tolerancia_risco=0.3,
        meses_protegidos=6
    )
    
    # Predição com ML
    alocacao_ml = optimizer.predict_allocation(params)
    print("\n📊 ALOCAÇÃO SUGERIDA PELO ML:")
    print(f"   Reserva: {alocacao_ml.reserva_seguranca_pct:.2f}%")
    print(f"   Crescimento: {alocacao_ml.crescimento_pct:.2f}%")
    print(f"   Risco: {alocacao_ml.risco_pct:.2f}%")
    
    # Comparar com modelo tradicional
    modelo = CashAllocationModel(params)
    alocacao_tradicional = modelo.suggest_allocation()
    print("\n📊 ALOCAÇÃO SUGERIDA PELO MODELO TRADICIONAL:")
    print(f"   Reserva: {alocacao_tradicional.reserva_seguranca_pct:.2f}%")
    print(f"   Crescimento: {alocacao_tradicional.crescimento_pct:.2f}%")
    print(f"   Risco: {alocacao_tradicional.risco_pct:.2f}%")


if __name__ == "__main__":
    exemplo_uso_ml()
