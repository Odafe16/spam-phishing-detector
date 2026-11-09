# Spam & Phishing Detector
[🚀 Launch Live Application](https://spamphishingdetector.streamlit.app/)

A machine-learning application for detecting spam messages, phishing emails, and potentially malicious URLs using text classification and URL feature engineering.

The project combines three independently trained classifiers into a Streamlit application, with particular attention to dataset quality, evaluation reliability, and model generalization.

## Features

- **SMS Spam Detection:** Classifies text messages as legitimate or spam.
- **Email Phishing Detection:** Analyzes email text for phishing patterns.
- **URL Phishing Detection:** Evaluates URL structure using 21 engineered numerical features.
- **Interactive Application:** Provides a Streamlit interface for all three detectors.
- **Input Validation:** Handles empty, malformed, and unsupported inputs.

URL analysis does not visit websites or inspect their contents.

## Machine Learning Approach

| Detector | Model | Features |
|---|---|---|
| SMS Spam | Linear SVM | TF-IDF |
| Email Phishing | Linear SVM | TF-IDF |
| URL Phishing | Histogram Gradient Boosting | 21 numerical URL features |

The text classifiers use serialized scikit-learn pipelines, while the URL classifier uses a separate feature extraction module.

### Model Evaluation

| Detector | Evaluation | Precision | Recall | F1-score |
|---|---|---:|---:|---:|
| SMS Spam | Held-out test | 98.72% | 85.56% | 91.67% |
| Email Phishing | Held-out test | 98.61% | 98.78% | 98.69% |
| URL Phishing | Exploratory evaluation | 87.04% | 89.54% | 88.27% |

Metrics are reported for the positive class: spam or phishing.

The URL results are exploratory and should not be interpreted as performance on a fully independent, previously unseen dataset.

## URL Dataset Investigation

During development, I investigated multiple phishing URL datasets and identified structural patterns that could allow models to achieve misleadingly high classification scores.

These included differences in HTTPS usage, URL paths, query parameters, and hostname distributions.

I subsequently constructed a revised dataset using hostname-disjoint development splits and a separate challenge set containing frequently occurring hostnames.

The URL model achieved an exploratory evaluation F1-score of **88.27%**, but performance deteriorated substantially on the large-hostname challenge set.

**Challenge-set phishing recall: 51.28%.**

The model particularly struggled with phishing-labeled URLs hosted on otherwise legitimate third-party platforms, including Google Docs and Google Sites.

These findings demonstrate an important limitation of URL-only classification: structural features cannot reliably establish whether the content behind a URL is malicious.

For this reason, the URL classifier is retained as a **research baseline**, not a production-ready security system.

Detailed experimental results are available in the project notebooks and `outputs/` directory.

## Project Structure

```text
spam-phishing-detector/
├── streamlit_app/
│   ├── app.py
│   └── styles.py
├── src/
│   ├── inference.py
│   └── url_features.py
├── models/
│   ├── sms_svm_pipeline.joblib
│   ├── phishing_svm_pipeline.joblib
│   ├── url_v3_hgb_model.joblib
│   └── url_v3_model_config.json
├── notebooks/
├── outputs/
├── requirements.txt
├── runtime.txt
└── README.md
```

The seven notebooks document data exploration, model development, URL dataset investigations, evaluation, and inference integration.

Raw and processed datasets are excluded from the repository.

## Installation

**1. Clone the repository**

```bash
git clone https://github.com/Odafe16/spam-phishing-detector.git
cd spam-phishing-detector
```

**2. Create a virtual environment**

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

**3. Install dependencies**

```bash
python -m pip install -r requirements.txt
```

**4. Run the application**

```bash
python -m streamlit run streamlit_app/app.py
```

The application will normally be available at `http://localhost:8501`.

Python 3.12 is recommended.

## Limitations

- Model predictions do not guarantee that messages, emails, or websites are safe.
- SMS and email classifiers were evaluated using historical datasets and may not generalize equally well to new attack patterns.
- The email classifier does not inspect attachments or verify sender identities.
- The URL classifier examines URL structure only and does not inspect webpage contents, redirects, or destination behavior.
- URL classification showed substantial generalization weaknesses during challenge evaluation.
- URL model scores should not be interpreted as calibrated real-world phishing probabilities.

## Live Application

**Try the application:** https://spamphishingdetector.streamlit.app/

## Technologies

Python · scikit-learn · NumPy · pandas · SciPy · TF-IDF · Linear SVM · Histogram Gradient Boosting · Streamlit

## Author

**Jonathan Ojo**

Machine Learning

[GitHub](https://github.com/Odafe16) · [Portfolio](https://ojojonathanportfolio.netlify.app/)
