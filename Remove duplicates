import streamlit as st

st.set_page_config(page_title="Duplicate Remover", layout="centered")

st.title("🧹 Remove Duplicate Lines")

input_text = st.text_area(
    "Paste your dataset below (one line per entry):",
    height=300,
    placeholder="Example:\nJohn Doe\nJane Doe\nJohn Doe\n..."
)

if st.button("Remove Duplicates"):
    lines = [line.strip() for line in input_text.splitlines() if line.strip()]

    seen = set()
    unique_lines = []
    for line in lines:
        if line not in seen:
            unique_lines.append(line)
            seen.add(line)

    cleaned_text = "\n".join(unique_lines)

    st.success(f"✅ {len(unique_lines)} unique lines (removed {len(lines) - len(unique_lines)} duplicates)")

    st.text_area("🎯 Cleaned Result (copy from here):", value=cleaned_text, height=300)

    st.download_button(
        label="📄 Download Result as TXT",
        data=cleaned_text,
        file_name="cleaned_output.txt",
        mime="text/plain"
    )
