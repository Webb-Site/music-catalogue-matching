"""Streamlit view of match results.  Run: uv run streamlit run app.py"""

from pathlib import Path

import streamlit as st

from catalogue_matching.pipeline import run
from catalogue_matching.royalties import match_rate, royalties_at_risk

st.set_page_config(page_title="Catalogue Matching", layout="wide")
st.title("Music catalogue matching")
st.caption("Synthetic sample data. Royalty figures use an illustrative rate, not a real one.")

results = run(Path("data/sample"))
unmatched = [r for r in results if not r.matched]

col1, col2, col3 = st.columns(3)
col1.metric("Recordings", len(results))
col2.metric("Matched", f"{match_rate(results):.0%}")
col3.metric("Royalties at risk", f"£{royalties_at_risk(results):,.2f}")

st.subheader("Unmatched recordings")
st.dataframe(
    [
        {
            "Recording": r.recording.title,
            "Artist": r.recording.artist,
            "ISRC": r.recording.isrc or "missing",
            "Streams": r.recording.streams,
            "Reason": r.reason,
        }
        for r in sorted(unmatched, key=lambda r: r.recording.streams, reverse=True)
    ],
    use_container_width=True,
)

st.subheader("Matched recordings")
st.dataframe(
    [
        {"Recording": r.recording.title, "Artist": r.recording.artist,
         "Work": r.work_id, "Method": r.method}
        for r in results if r.matched
    ],
    use_container_width=True,
)
