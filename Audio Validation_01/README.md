# 🚀 End-to-End Whisper Model Evaluation & Analysis Suite

Welcome to the complete suite for evaluating, managing, and analyzing fine-tuned Persian Whisper ASR models. This project provides a set of powerful, interconnected scripts that cover the entire lifecycle of model analysis: from quantitative performance evaluation to interactive, qualitative exploration of results.

This suite is composed of three main components:
1.  **📊 The Evaluation Script**: Benchmarks your model's performance by calculating the Word Error Rate (WER) and generates a detailed results CSV.
2.  **🚀 The LoRA Merger Script**: Merges PEFT LoRA adapters into the base model to create a standalone, deployment-ready model.
3.  **🎧 The Interactive Dashboard**: A visually rich Streamlit application to explore the evaluation results, listen to audio, and perform in-depth error analysis.

---

## ✨ Core Features

-   **End-to-End Workflow**: A seamless process from model evaluation to deep-dive analysis.
-   **Quantitative & Qualitative Analysis**: Get hard numbers (WER) and the tools to understand *why* the errors occur.
-   **Advanced UI/UX**: A stunning, custom-themed "cyberpunk" Streamlit dashboard for an immersive analysis experience.
-   **Modular & Configurable**: Each script is self-contained and can be easily configured through simple path and parameter changes.
-   **Efficient & Optimized**: Scripts leverage CUDA, float16 precision, and smart caching for high performance.
-   **Deployment Ready**: Includes tools to productionize your fine-tuned models by merging LoRA adapters.

---

## 📦 Prerequisites & Installation

Before you begin, ensure you have Python 3.8+ installed. All required libraries can be installed with a single command:

```bash
pip install torch transformers datasets pandas tqdm evaluate scikit-learn peft accelerate streamlit plotly
```
*For GPU acceleration, ensure your PyTorch installation is compatible with your CUDA version.*

---

## 📂 Project Workflow & Structure

The components are designed to work together. The typical workflow is:

1.  Use the **Evaluation Script** to test your model against a dataset. This produces the crucial `results.csv` file.
2.  (Optional) If you used LoRA for training, use the **LoRA Merger Script** to create a standalone model for deployment.
3.  Use the **Interactive Dashboard** with the `results.csv` and the original dataset to visually analyze the model's performance.

Your recommended project directory should look like this:

```
your-project-folder/
│
├── 1_evaluate_model.py                 # The evaluation script
├── 2_merge_lora_adapter.py             # The LoRA merging script
├── 3_streamlit_dashboard.py            # The interactive dashboard script
│
├── results_model_v1.csv                # Example output CSV from evaluation
│
└── data/
    └── your_hf_dataset/                # The Hugging Face dataset saved to disk
        ├── dataset.arrow
        ├── dataset_info.json
        └── state.json
```

---

##  komponent 1: 📊 Model Evaluation Script

This script automates the process of benchmarking a Whisper model. It transcribes a set of audio samples, compares the predictions to ground truth references, and calculates the Word Error Rate (WER).

### Configuration
Modify the `Config` class inside the script (`1_evaluate_model.py`):
```python
class Config:
    MODEL_PATH = "/path/to/your/whisper_model/"
    DATASET_NAME = "/path/to/your/hf_dataset_folder"
    CSV_OUTPUT_PATH = "results_model_v1.csv"
    NUM_SAMPLES = 3000
```

### Usage
Execute the script from your terminal:
```bash
python 1_evaluate_model.py
```

### Output
-   **Console Report**: A final summary with the mean WER is printed.
-   **CSV File**: A detailed `.csv` file (e.g., `results_model_v1.csv`) is generated, containing predictions, references, individual WER scores, and other metadata for each sample. This file is the primary input for the interactive dashboard.

---

## Component 2: 🚀 LoRA Adapter Merging Script

If you fine-tuned your model using LoRA, this script merges the lightweight adapter into the base model to create a single, portable, and deployment-ready model.

### Configuration
Set the following path variables at the top of the script (`2_merge_lora_adapter.py`):
```python
# Path to the base model
merged_model_path = "/path/to/your/base_whisper_model/"

# Path to the LoRA adapter checkpoint
checkpoint_path = "/path/to/your/lora_adapter_checkpoint/"

# Path to save the new, fully merged model
final_output_dir = "/path/to/save/new_merged_model/"
```

### Usage
Run the script from your terminal:
```bash
python 2_merge_lora_adapter.py
```

### Output
-   A new directory at `final_output_dir` containing the complete, merged model, including all necessary configuration and tokenizer files. The model is now ready for inference without the `peft` library.

---

## Component 3: 🎧 Interactive Analysis Dashboard

This Streamlit application is the centerpiece for qualitative analysis. It provides a powerful and beautiful interface to explore the data generated by the Evaluation Script.

### File Requirements
The dashboard requires two inputs to be present in your project directory:
1.  **The Results CSV**: The `.csv` file generated by the evaluation script.
2.  **The Dataset Directory**: The Hugging Face `datasets` directory that was used for the evaluation.

Update the paths at the top of the script (`3_streamlit_dashboard.py`) to point to these files:
```python
DATASET_PATH = "data/your_hf_dataset"
CSV_PATH = "results_model_v1.csv"
```

### Usage
Launch the dashboard with the following command:
```bash
streamlit run 3_streamlit_dashboard.py
```

### Dashboard Guide
-   **Main View**: See overall statistics in the sidebar and a filterable table of all evaluation samples in the main area.
-   **Smart Filtering**: Use the WER slider and sorting options to quickly navigate the results.
-   **Audio Analysis**: Enter one or more sample `original_index` values from the table to listen to the audio, see the model's prediction, and compare it directly with the reference text.
-   **Quick Selection**: Automatically view the best-performing (lowest WER) or worst-performing (highest WER) samples to quickly identify model strengths and weaknesses.