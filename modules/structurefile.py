import os
from pathlib import Path

def create_thesis_structure():
    # Define the directory and file mapping based on the methodological design
    structure = {
        "configs": [
            "base_config.yaml",      # Shared: vocab_size=32k, max_length=128
            "experiment_baseline.yaml",
            "experiment_hybrid.yaml"
        ],
        "data/raw": [],              # IndicCorp v2 subset & SIB-200
        "data/processed": [],        # Normalized and Shielded text
        "data/reference": [],        # Linguistically annotated reference set
        "src/preprocessing": [
            "__init__.py",
            "normalizer.py",         # Unicode NFC & Artifact removal
            "shield_rules.py",       # Regex for Nominal/Verbal morphology
            "sandhi_engine.py"       # Reversible morphophonemic transformations
        ],
        "src/tokenizer": [
            "__init__.py",
            "trainer.py",            # BpeTrainer with boundary enforcement
            "hybrid_tokenizer.py"    # Custom wrapper for ▁ markers
        ],
        "src/models": [
            "__init__.py",
            "classifier.py"          # IndicBERT v2 with PEFT/Frozen layers
        ],
        "src/utils": [
            "__init__.py",
            "seed_manager.py",       # Managing n=6 controlled runs
            "metrics_logger.py"      # CSV logging for significance testing
        ],
        "scripts": [
            "01_prepare_data.py",
            "02_train_tokenizers.py",
            "03_run_experiments.py", # Main orchestrator for 6 runs
            "04_compute_statistics.py"
        ],
        "outputs/tokenizers": [],    # vocab.json and merges.txt
        "outputs/checkpoints": [],   # .pt files for 4GB VRAM compatibility
        "outputs/results": []        # Final evaluation logs
    }

    # Root files
    root_files = ["requirements.txt", "README.md", ".gitignore"]

    print(f"Creating Master Thesis Project Structure: 'Morphology-Aware Tokenization for Malayalam'...")

    # Create directories and files
    for folder, files in structure.items():
        folder_path = Path(folder)
        folder_path.mkdir(parents=True, exist_ok=True)
        for file in files:
            (folder_path / file).touch()
            print(f"  Created: {folder}/{file}")

    for file in root_files:
        Path(file).touch()
        print(f"  Created: {file}")

    print("\nProject structure initialized successfully.")

if __name__ == "__main__":
    create_thesis_structure()