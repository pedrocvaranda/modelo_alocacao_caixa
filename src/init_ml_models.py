"""
Script para inicializar modelos ML
Executa uma única vez para treinar e salvar os modelos
"""

import sys
sys.path.insert(0, '.')

from ml_optimizer import MLOptimizer
import os


def initialize_ml_models():
    """
    Inicializa os modelos de ML se não existirem
    """
    print("=" * 80)
    print("🤖 INICIALIZAÇÃO DE MODELOS ML")
    print("=" * 80)
    
    # Verificar se modelos já existem na pasta models/
    if os.path.exists("models/ml_optimizer_reserva.pkl"):
        print("\n✅ Modelos ML já existem!")
        print("   - models/ml_optimizer_reserva.pkl")
        print("   - models/ml_optimizer_crescimento.pkl")
        print("   - models/ml_optimizer_risco.pkl")
        print("   - models/ml_optimizer_scaler.pkl")
        
        # Tentar carregar para validar
        try:
            optimizer = MLOptimizer()
            optimizer.load_models(folder="models")
            print("\n✅ Modelos carregados com sucesso!")
            return optimizer
        except Exception as e:
            print(f"\n⚠️ Erro ao carregar modelos: {e}")
            print("   Treinando novos modelos...")
    else:
        print("\n📋 Modelos não encontrados. Iniciando treinamento...")
    
    # Treinar novos modelos
    print("\n" + "=" * 80)
    print("🔄 TREINAMENTO DE MODELOS")
    print("=" * 80)
    
    optimizer = MLOptimizer()
    
    # Gerar dados de treino
    print("\n1️⃣  Gerando dados de treino...")
    df = optimizer.generate_training_data(n_samples=10000)
    
    # Treinar
    print("\n2️⃣  Treinando modelos...")
    optimizer.train(df)
    
    # Salvar na pasta models/
    print("\n3️⃣  Salvando modelos na pasta models/...")
    optimizer.save_models(folder="models")
    
    print("\n" + "=" * 80)
    print("✅ INICIALIZAÇÃO CONCLUÍDA!")
    print("=" * 80)
    print("\nOs modelos estão prontos para uso na GUI do Streamlit")
    print("Arquivos salvos em:")
    print("  - models/ml_optimizer_*.pkl (modelos treinados)")
    print("  - data/training_data.csv (dados de treinamento)")
    print("\nVocê pode executar: streamlit run src/gui_streamlit.py")
    
    return optimizer


if __name__ == "__main__":
    optimizer = initialize_ml_models()
