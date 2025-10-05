


# 🎧 Whisper Evaluation Dashboard

This project is an advanced, interactive dashboard built with **Streamlit** to analyze and evaluate the results of an Automatic Speech Recognition (ASR) model like **Whisper**. The dashboard allows users to visually inspect the model's performance, listen to audio samples, and compare predicted text against reference transcripts.

---

## ✨ Key Features

- **Modern UI (Cyberpunk Theme):** A sleek and engaging dark-themed interface with custom CSS for a unique user experience.
- **Overall Statistics & Error Distribution:** Displays key metrics like the average **Word Error Rate (WER)** and a histogram of its distribution in the sidebar.
- **Interactive Smart Filters:** Filter results by a specific WER range and sort the data by various columns.
- **Integrated Audio Player:** Input the `original_index` of one or more samples to listen to the corresponding audio file.
- **Detailed Comparison View:** Simultaneously view the model's predicted text and the original reference text for any audio sample.
- **Quick Sample Selection:** Instantly view samples with the **lowest** and **highest** error rates to analyze the model's best and worst-performing cases.
- **Performance-Optimized with Caching:** Uses Streamlit's `@st.cache_resource` and `@st.cache_data` decorators for faster data loading and a responsive app.

---

## 🛠️ Tech Stack

- **Programming Language:** Python 3.8+
- **Core Framework:** [Streamlit](https://streamlit.io/)
- **Key Libraries:**
  - `pandas`: For managing and processing tabular data (from the CSV file).
  - `datasets` (from Hugging Face): For loading and handling the audio dataset.
  - `plotly`: For creating beautiful and interactive charts.

---

## 🚀 Setup and Installation

Follow these steps to run the project locally.

### 1. Prerequisites

- Python 3.8 or higher must be installed.
- The `pip` package manager must be available.

### 2. Install Libraries

First, clone the project repository (or download the files). Then, navigate into the project directory and install the required libraries. It is highly recommended to do this within a virtual environment.

```bash
# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required libraries
pip install streamlit pandas datasets plotly plotly-express
````

### 3. Prepare the Data

This application requires two main data components:

1. **Audio Dataset (Hugging Face Dataset):**

   * The main dataset containing the audio files. In the code, this dataset is expected to be located at `CV-17-01/validated`.
   * You must download this dataset and place it in the specified path beforehand.

2. **Results File (CSV):**

   * A CSV file containing the model's evaluation results. This file should include columns such as `original_index`, `wer_normalized`, `prediction_normalized`, and `reference_normalized`.
   * In the code, this file is named `results_no_audio_preprocessing.csv` and is expected to be in the project's root directory.

Your folder structure should look like this:

```
.
├── streamlit_app.py
├── results_no_audio_preprocessing.csv
└── CV-17-01/
    └── validated/
        ├── dataset_info.json
        ├── state.json
        └── ... (Other dataset files)
```

### 4. Run the Application

After installing the dependencies and preparing the data, run the app with the following command:

```bash
streamlit run streamlit_app.py
```

The application will automatically open in your web browser.

---

## ⚙️ Code Structure Explained

The `streamlit_app.py` script is organized into the following logical sections:

### 1. Imports and Constants

The script begins by importing the necessary libraries and defining constants for the dataset path (`DATASET_PATH`) and the results file path (`CSV_PATH`).

```python
import streamlit as st
import pandas as pd
from datasets import load_from_disk, Audio
import plotly.express as px

DATASET_PATH = "CV-17-01/validated"
CSV_PATH = "results_no_audio_preprocessing.csv"
TARGET_SR = 16000
```

### 2. Custom CSS Styling

A large block of CSS code is injected into the app using `st.markdown(..., unsafe_allow_html=True)`. This code overrides the default Streamlit styles to create the custom dark/cyberpunk theme. The CSS classes defined here are used later in HTML blocks to style the header, cards, buttons, and other elements.

### 3. Data Loading Functions (with Caching)

To prevent reloading data on every user interaction, Streamlit's caching mechanism is used:

* `@st.cache_resource`: Used for loading heavy, unchanging resources like large datasets. It's used here to load the `full_dataset`.
* `@st.cache_data`: Used for loading data that might be processed but whose final result is static, like reading a CSV file.

```python
@st.cache_resource
def load_dataset():
    # ...

@st.cache_data
def load_csv():
    # ...

with st.spinner('Loading dataset...'):
    full_dataset = load_dataset()
    df = load_csv()
```

### 4. Sidebar

The sidebar displays global information and controls:

* **Overall statistics:** total samples and average WER are shown using `st.metric`.
* **WER distribution:** A histogram of the WER distribution is generated with `plotly.express` and displayed using `st.plotly_chart`.

### 5. Main Page

#### Section 1: Filters and DataFrame Display

* Streamlit widgets like `st.slider` and `st.selectbox` allow the user to filter the data by WER range and select a sort order.
* Statistics for the filtered data are displayed in a styled card.
* The filtered and sorted DataFrame is displayed using `st.dataframe`.

#### Section 2: Audio Player by Index

* An `st.text_input` widget prompts the user to enter one or more comma-separated indices (`original_index`).
* When the button is clicked, the code processes the indices in a loop:

  1. It retrieves the corresponding sample from `full_dataset` using the index (`full_dataset[idx]`).
  2. It extracts the textual information (prediction and WER) from the `df`.
  3. It displays the information in custom-styled cards (`sample-card`) and text blocks (`text-prediction`, `text-reference`).
  4. The audio is played using `st.audio`.
* This section includes error handling for invalid inputs.

#### Section 3: Quick Selection by WER

* This section allows users to quickly find samples with the lowest or highest WER.
* Using `st.selectbox` and `st.number_input`, the user chooses the sort order (best/worst) and the number of samples to display.
* Upon button click, the DataFrame is sorted by WER, and the top `n` samples are selected.
* These samples are then displayed with their audio and text, similar to the previous section.

---

## 🎨 Customization

* **Change Data Paths:** To use a different dataset or results file, simply update the `DATASET_PATH` and `CSV_PATH` constants at the top of the script.
* **Modify Styles:** All CSS is located within the initial `st.markdown` block. You can easily change colors, fonts, and other styles there.
* **Add New Charts:** You can extend the dashboard by adding more plots and visual analyses using Plotly and `st.plotly_chart`.

