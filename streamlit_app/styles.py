"""Shared styling for the Streamlit application."""

import streamlit as st


def apply_styles():
    """Apply the application's visual theme."""

    st.markdown(
        """
        <style>
        /* Main application background */
        .stApp {
            background-color: #F8FAFC;
        }

        /* Main content container */
        .block-container {
            max-width: 1100px;
            padding-top: 2.5rem;
            padding-bottom: 3rem;
        }

        /* Typography */
        h1, h2, h3 {
            color: #1F2937;
            font-weight: 650;
        }

        p {
            line-height: 1.65;
        }

        /* Application introduction */
        .app-subtitle {
            color: #64748B;
            font-size: 1.05rem;
            margin-top: -0.5rem;
            margin-bottom: 1.75rem;
        }

        /* Tab navigation */
        .stTabs [data-baseweb="tab-list"] {
            gap: 12px;
            border-bottom: 1px solid #E2E8F0;
        }

        .stTabs [data-baseweb="tab"] {
            padding: 12px 18px;
            font-weight: 550;
            border-radius: 8px 8px 0 0;
        }

        /* Form containers */
        [data-testid="stForm"] {
            border: 1px solid #E2E8F0;
            border-radius: 14px;
            background-color: #FFFFFF;
            padding: 1.25rem;
        }

        /* Input fields */
        .stTextArea textarea,
        .stTextInput input {
            border-radius: 8px;
        }

        /* Primary buttons */
        .stButton button[kind="primary"],
        .stFormSubmitButton button[kind="primary"] {
            border-radius: 8px;
            font-weight: 600;
            min-height: 44px;
        }

        /* Metrics */
        [data-testid="stMetric"] {
            background-color: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 12px;
            padding: 1rem;
        }

        /* Footer */
        .app-footer {
            color: #64748B;
            font-size: 0.85rem;
            margin-top: 3rem;
            padding-top: 1rem;
            border-top: 1px solid #E5E7EB;
        }

        /* Mobile adjustments */
        @media (max-width: 640px) {
            .block-container {
                padding-top: 1.25rem;
                padding-left: 1rem;
                padding-right: 1rem;
            }

            .stTabs [data-baseweb="tab-list"] {
                gap: 2px;
            }

            .stTabs [data-baseweb="tab"] {
                padding: 8px 10px;
                font-size: 0.85rem;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )