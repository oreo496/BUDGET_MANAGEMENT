import os
import json
import argparse
from pathlib import Path

import nbformat
from nbclient import NotebookClient


def ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)


def build_save_cell(output_dir: str):
    """Return a code cell (as source string) that saves known artifacts if present.

    This cell does not rely on modifying the original notebook file; it's appended
    in-memory for execution only.
    """
    return "\n".join([
        "# Auto-appended export cell (runtime-only)",
        "import os, json", 
        "from pathlib import Path",
        "import joblib",
        "output_dir = Path(r'{}')".format(output_dir.replace("\\", "/")),
        "output_dir.mkdir(parents=True, exist_ok=True)",
        "manifest = {}",
        "def _safe_dump(obj, name):",
        "    try:",
        "        file = output_dir / f'{name}.joblib'",
        "        joblib.dump(obj, file)",
        "        manifest[name] = str(file)",
        "        print(f'[EXPORT] Saved {name} -> {file}')",
        "        return True",
        "    except Exception as e:",
        "        print(f'[EXPORT] Failed to save {name}: {e}')",
        "        return False",
        "",
        "# Common artifacts from the notebook",
        "if 'scaler' in globals(): _safe_dump(scaler, 'scaler')",
        "if 'label_encoder' in globals(): _safe_dump(label_encoder, 'label_encoder')",
        "if 'cat_encoder' in globals(): _safe_dump(cat_encoder, 'cat_encoder')",
        "if 'iso_forest' in globals(): _safe_dump(iso_forest, 'isolation_forest')",
        "",
        "# OOP engine models: try saving via known methods or pickling",
        "def _try_save_keras(model_obj, name):",
        "    try:",
        "        mdl = getattr(model_obj, 'model', None)",
        "        if mdl is not None and hasattr(mdl, 'save'):",
        "            file = output_dir / f'{name}.keras'",
        "            mdl.save(str(file))",
        "            manifest[name] = str(file)",
        "            print(f'[EXPORT] Saved Keras model {name} -> {file}')",
        "            return True",
        "        return False",
        "    except Exception as e:",
        "        print(f'[EXPORT] Failed to save keras {name}: {e}')",
        "        return False",
        "",
        "if 'engine' in globals():",
        "    try:",
        "        if hasattr(engine, 'categorizer'):",
        "            _try_save_keras(engine.categorizer, 'categorizer')",
        "        if hasattr(engine, 'fraud_detector'):",
        "            _try_save_keras(engine.fraud_detector, 'fraud_detector')",
        "        if hasattr(engine, 'goal_tracker'):",
        "            # goal_tracker might be rule/statistics based; export config if available",
        "            cfg = getattr(engine.goal_tracker, 'config', None)",
        "            if cfg is not None:",
        "                file = output_dir / 'goal_tracker_config.json'",
        "                try:",
        "                    with open(file, 'w', encoding='utf-8') as fh:",
        "                        json.dump(getattr(cfg, '__dict__', {}), fh)",
        "                    manifest['goal_tracker_config'] = str(file)",
        "                    print(f'[EXPORT] Saved goal tracker config -> {file}')",
        "                except Exception as e:",
        "                    print(f'[EXPORT] Failed to export goal tracker config: {e}')",
        "    except Exception as e:",
        "        print(f'[EXPORT] Engine export skipped: {e}')",
        "",
        "# Write manifest",
        "manifest_file = output_dir / 'artifact_manifest.json'",
        "with open(manifest_file, 'w', encoding='utf-8') as fh:",
        "    json.dump(manifest, fh, indent=2)",
        "print(f'[EXPORT] Manifest written -> {manifest_file}')",
    ])


def execute_notebook_with_append(nb_path: Path, extra_cell_source: str):
    nb = nbformat.read(nb_path.open('r', encoding='utf-8'), as_version=4)
    nb.cells.append(nbformat.v4.new_code_cell(source=extra_cell_source))
    client = NotebookClient(nb, timeout=600, kernel_name='python3')
    client.execute()


def main():
    parser = argparse.ArgumentParser(description='Export AI artifacts from notebook (without editing it).')
    parser.add_argument('--notebook', default=str(Path('Funder_AiModel') / 'AI_DL_MODEL.ipynb'), help='Path to the source notebook')
    parser.add_argument('--output', default=str(Path('backend') / 'model_store'), help='Destination directory in backend for artifacts')
    args = parser.parse_args()

    nb_path = Path(args.notebook).resolve()
    output_dir = Path(args.output).resolve()
    ensure_dir(output_dir)

    print(f'[INFO] Notebook: {nb_path}')
    print(f'[INFO] Output dir: {output_dir}')

    save_cell_src = build_save_cell(str(output_dir))
    execute_notebook_with_append(nb_path, save_cell_src)
    print('[OK] Export completed.')


if __name__ == '__main__':
    main()
