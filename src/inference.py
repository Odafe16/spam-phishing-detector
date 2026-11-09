"""
Reusable inference functions for the Spam & Phishing Detector.

The module loads trained classifiers and produces predictions from
SMS messages, email content, and URL strings.

URL classification is a research baseline, not a safety guarantee.
"""

import json
from functools import lru_cache
from pathlib import Path

import joblib
import numpy as np

from src.url_features import extract_features_dataframe


PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODELS_DIR = PROJECT_ROOT / "models"

SMS_MODEL_PATH = MODELS_DIR / "sms_svm_pipeline.joblib"
EMAIL_MODEL_PATH = MODELS_DIR / "phishing_svm_pipeline.joblib"
URL_MODEL_PATH = MODELS_DIR / "url_v3_hgb_model.joblib"
URL_CONFIG_PATH = MODELS_DIR / "url_v3_model_config.json"

MAX_TEXT_LENGTH = 100_000
MAX_URL_LENGTH = 4_096


@lru_cache(maxsize=1)
def load_models():
    """Load and cache all trained classifiers and URL configuration."""

    required_paths = [
        SMS_MODEL_PATH,
        EMAIL_MODEL_PATH,
        URL_MODEL_PATH,
        URL_CONFIG_PATH,
    ]

    for path in required_paths:
        if not path.is_file():
            raise FileNotFoundError(
                f"Required model artifact not found: {path}"
            )

    models = {
        "sms": joblib.load(SMS_MODEL_PATH),
        "email": joblib.load(EMAIL_MODEL_PATH),
        "url": joblib.load(URL_MODEL_PATH),
    }

    with open(URL_CONFIG_PATH, "r", encoding="utf-8") as file:
        models["url_config"] = json.load(file)

    return models


def validate_text(text, field_name="Text"):
    """Validate an SMS or email input before classification."""

    if not isinstance(text, str):
        raise TypeError(f"{field_name} must be a string.")

    text = text.strip()

    if not text:
        raise ValueError(f"{field_name} cannot be empty.")

    if len(text) > MAX_TEXT_LENGTH:
        raise ValueError(
            f"{field_name} exceeds the maximum supported length."
        )

    return text


def validate_url(url):
    """Validate basic URL format without making network requests."""

    from urllib.parse import urlsplit

    if not isinstance(url, str):
        raise TypeError("URL must be a string.")

    url = url.strip()

    if not url:
        raise ValueError("URL cannot be empty.")

    if len(url) > MAX_URL_LENGTH:
        raise ValueError("URL exceeds the maximum supported length.")

    try:
        parsed = urlsplit(url)
        hostname = parsed.hostname
    except ValueError as exc:
        raise ValueError("URL format is invalid.") from exc

    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError("URL must begin with http:// or https://.")

    if not hostname:
        raise ValueError("URL must contain a hostname.")

    if any(character.isspace() for character in hostname):
        raise ValueError("URL hostname cannot contain whitespace.")

    return url


def predict_sms(text):
    """Classify an SMS message as legitimate or spam."""

    text = validate_text(text, "SMS message")

    model = load_models()["sms"]

    prediction = int(model.predict([text])[0])

    return {
        "detector": "sms",
        "label": "spam" if prediction == 1 else "legitimate",
        "prediction": prediction,
        "message": (
            "This message was flagged as potential spam."
            if prediction == 1
            else "No spam was detected by the model."
        ),
    }


def predict_email(text):
    """Classify email content as legitimate or phishing."""

    text = validate_text(text, "Email content")

    model = load_models()["email"]

    prediction = int(model.predict([text])[0])

    return {
        "detector": "email",
        "label": "phishing" if prediction == 1 else "legitimate",
        "prediction": prediction,
        "message": (
            "This email was flagged as potential phishing."
            if prediction == 1
            else "No phishing was detected by the model."
        ),
    }


def predict_url(url):
    """Classify URL structure using the Version 3 research baseline."""

    url = validate_url(url)

    models = load_models()

    model = models["url"]
    config = models["url_config"]

    feature_frame = extract_features_dataframe([url])

    expected_features = config["feature_names"]

    if set(feature_frame.columns) != set(expected_features):
        raise RuntimeError(
            "URL feature extractor does not match the trained model."
        )

    feature_frame = feature_frame[expected_features]

    probability = float(
        model.predict_proba(feature_frame)[0, 1]
    )

    threshold = float(config["decision_threshold"])

    prediction = int(probability >= threshold)

    return {
        "detector": "url",
        "label": "phishing" if prediction == 1 else "not_flagged",
        "prediction": prediction,
        "phishing_probability": probability,
        "threshold": threshold,
        "model_role": config["model_role"],
        "message": (
            "This URL was flagged as potentially phishing."
            if prediction == 1
            else (
                "This URL was not flagged, but its safety "
                "has not been established."
            )
        ),
        "warning": (
            "This classifier analyzes URL structure only. "
            "It does not inspect website content, redirects, "
            "or verify that the destination is safe."
        ),
    }