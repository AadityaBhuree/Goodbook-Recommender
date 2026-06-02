"""Shared application initialization utilities.

Keeps initialization logic (e.g. on-demand collaborative fitting) in one place
so both app.py and page modules can import it without circular import issues.
"""

import logging

import streamlit as st

logger = logging.getLogger(__name__)


def ensure_collab_fitted() -> None:
    """Fit collaborative model on demand if not already fitted.

    Collaborative filtering is expensive (~30s for 10k books, 6M ratings),
    so it is skipped during initial data load and fitted lazily when the
    user first visits the Recommendations tab.
    """
    if st.session_state.get("collab_ready", False):
        return
    if st.session_state.get("collaborative") is None:
        return
    with st.spinner(
        "👥 Training collaborative filtering model (this may take ~30 seconds on first use)..."
    ):
        st.session_state.collaborative.fit()
        st.session_state.collab_ready = True
        logger.info("Collaborative model fitted on demand.")
