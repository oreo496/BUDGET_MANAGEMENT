from src.config import AppConfig
from src.pipeline import FinanceAIEngine

if __name__ == "__main__":
    cfg = AppConfig()
    engine = FinanceAIEngine(cfg)
    try:
        engine.load_data(cfg.train_dataset_path or 'final_train_dataset.csv')
        alerts = engine.run_monthly_alerts()
        print(f"Monthly alerts triggered: {alerts}")
        print(f"Audit entries: {len(engine.audit.df)}")
    except Exception as e:
        print("Pipeline failed:", e)
