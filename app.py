import streamlit as st

st.set_page_config(page_title="Duplicate Remover", layout="centered")

st.title("🧹 Remove Duplicate Lines with Filters")

# --- User Inputs ---
input_text = st.text_area(
    "Paste your dataset below (one line per entry):",
    height=300,
    placeholder="Example:\nJohn Doe\nJane Doe\nDirector of Finance\nView Bio\n..."
)

# Optional job title filter (comma-separated)
job_filter_input = st.text_input(
    "🔍 Filter out lines containing these job titles (comma-separated, optional):",
    placeholder="Example: Manager, Director, Officer"
)

# Checkbox to remove "View Bio" lines
remove_view_bio = st.checkbox("Remove lines containing 'View Bio'")

# --- Processing ---
if st.button("Remove Duplicates"):
    # Prepare job title filters
    job_keywords = [kw.strip().lower() for kw in job_filter_input.split(",") if kw.strip()]

    lines = [line.strip() for line in input_text.splitlines() if line.strip()]
    seen = set()
    unique_lines = []

    for line in lines:
        line_lower = line.lower()

        # Apply job title filter
        if any(job_kw in line_lower for job_kw in job_keywords):
            continue

        # Skip if "View Bio" removal is enabled
        if remove_view_bio and "view bio" in line_lower:
            continue

        # Add if not duplicate
        if line not in seen:
            unique_lines.append(line)
            seen.add(line)

    cleaned_text = "\n".join(unique_lines)

    st.success(f"✅ {len(unique_lines)} unique lines (removed {len(lines) - len(unique_lines)} duplicates or filtered lines)")

    st.text_area("🎯 Cleaned Result (copy from here):", value=cleaned_text, height=300)

    st.download_button(
        label="📄 Download Result as TXT",
        data=cleaned_text,
        file_name="cleaned_output.txt",
        mime="text/plain"
    )
