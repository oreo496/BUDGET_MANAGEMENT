# FinanceAI Refactored Architecture

This codebase introduces a modular, production-ready structure organized into seven layers:

1. Configuration and Global Control (`src/config.py`)
2. Data Integrity and Validation (`src/validation.py`)
3. Preprocessing Pipeline – Translator (`src/preprocessing.py`)
4. Unified Modeling Engine (`src/modeling.py`)
5. Intelligence & Action Layer – Brain (`src/intelligence.py`)
6. Audit and Logging Framework (`src/audit.py` + feedback in `src/feedback.py`)
7. Defensive Reliability Layer (`src/reliability.py`)

The orchestrator is `src/pipeline.py` with class `FinanceAIEngine`.

## Quick Start

```bash
python -c "from src.config import AppConfig; from src.pipeline import FinanceAIEngine; e=FinanceAIEngine(AppConfig()); e.load_data('final_train_dataset.csv'); print('alerts:', e.run_monthly_alerts())"
```

## Notebook Integration

Add a cell to import and run the engine:

```python
from src.config import AppConfig
from src.pipeline import FinanceAIEngine
engine = FinanceAIEngine(AppConfig())
engine.load_data('final_train_dataset.csv')
alerts = engine.run_monthly_alerts()
print('Monthly alerts:', alerts)
```
