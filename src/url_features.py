from __future__ import annotations

import ipaddress
import re
from urllib.parse import urlsplit

import pandas as pd


SUSPICIOUS_KEYWORDS = (
    "login",
    "verify",
    "account",
    "secure",
    "update",
    "signin",
    "password",
    "confirm",
    "bank",
    "wallet",
)


def extract_url_features(url: str) -> dict:
    """Extract lexical and structural features without visiting the URL."""

    url = str(url).strip()

    # I add a temporary scheme to support URLs without one.
    parseable_url = (
        url if "://" in url else f"http://{url}"
    )

    try:
        parsed = urlsplit(parseable_url)
        hostname = (parsed.hostname or "").lower().rstrip(".")
    except ValueError:
        parsed = urlsplit("")
        hostname = ""

    path = parsed.path
    query = parsed.query

    # I check whether the hostname is an IP address.
    try:
        ipaddress.ip_address(hostname)
        is_ip = 1
    except ValueError:
        is_ip = 0

    # I identify suspicious lexical patterns.
    lower_url = url.lower()

    suspicious_keyword_count = sum(
        keyword in lower_url
        for keyword in SUSPICIOUS_KEYWORDS
    )

    # I calculate numeric and special-character patterns.
    digit_count = sum(char.isdigit() for char in url)

    special_char_count = sum(
        not char.isalnum()
        for char in url
    )

    # I approximate subdomain depth from hostname components.
    hostname_parts = [
        part for part in hostname.split(".") if part
    ]

    # I exclude IP addresses from subdomain counting.
    subdomain_count = (
        0 if is_ip
        else max(len(hostname_parts) - 2, 0)
    )

    features = {
        "url_length": len(url),
        "hostname_length": len(hostname),
        "path_length": len(path),
        "query_length": len(query),
        "digit_count": digit_count,
        "digit_ratio": digit_count / max(len(url), 1),
        "special_char_count": special_char_count,
        "dot_count": url.count("."),
        "hyphen_count": url.count("-"),
        "slash_count": url.count("/"),
        "at_symbol_count": url.count("@"),
        "question_mark_count": url.count("?"),
        "equal_sign_count": url.count("="),
        "percent_encoding_count": len(
            re.findall(r"%[0-9a-fA-F]{2}", url)
        ),
        "subdomain_count": subdomain_count,
        "path_depth": len([
            segment for segment in path.split("/")
            if segment
        ]),
        "is_ip_host": is_ip,
        "is_https": int(parsed.scheme.lower() == "https"),
        "has_query": int(bool(query)),
        "has_fragment": int(bool(parsed.fragment)),
        "suspicious_keyword_count": suspicious_keyword_count,
    }

    return features


def extract_features_dataframe(urls) -> pd.DataFrame:
    """Extract features for an iterable of URL strings."""

    return pd.DataFrame(
        [extract_url_features(url) for url in urls]
    )