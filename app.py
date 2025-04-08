import streamlit as st
import difflib

st.set_page_config(page_title="Duplicate Remover", layout="centered")

st.title("🧹 Remove Duplicate Lines with Filters")

# Default job titles
DEFAULT_JOB_TITLES = [
    "President", "Vice President", "CEO", "COO", "CFO", "CMO", "CTO", "Chief", "Director", "Executive", "Managing Director", "Owner", "Partner", 
    "Co-Founder", "Founder", "Principal", "Chairman", "Chairperson", "Manager", "Operations Manager", "Project Manager", "Product Manager", 
    "General Manager", "Finance Manager", "HR Manager", "Office Manager", "Maintenance Manager", "Account Manager", "Marketing Manager", 
    "Officer", "Controller", "Specialist", "Analyst", "Consultant", "Coordinator", "Assistant", "Advisor", "Representative", "Strategist", 
    "Auditor", "Buyer", "Planner", "Supervisor", "Team Lead", "Lead", "Sr", "Senior", "Jr", "Junior", "Intern", "Apprentice", "Trainee", 
    "Photographer", "Designer", "Editor", "Videographer", "Artist", "Content Creator", "Creative Director", "Developer", "Engineer", "Technician", 
    "IT Support", "Support Engineer", "Programmer", "Web Developer", "Systems Administrator", "Architect"
]

# User input area
input_text = st.text_area(
    "Paste your dataset below (one line per entry):",
    height=300,
    placeholder="Example:\nJohn Doe\nJane Doe\nDirector of Finance\nView Bio\n..."
)

# Optional job title filter
job_filter_input = st.text_input(
    "🔍 Filter out lines containing these job titles (comma-separated, optional):",
    placeholder="Leave empty to use built-in job title list"
)

# Custom keywords to filter (like 'View Bio', etc.)
extra_keyword_input = st.text_input(
    "❌ Remove lines containing these keywords (comma-separated, optional):",
    placeholder="Example: View Bio, Learn More, Contact Info, Photo of"
)

# Button click
if st.button("Remove Duplicates"):
    # Load job keywords
    if job_filter_input.strip():
        job_keywords = [kw.strip().lower() for kw in job_filter_input.split(",") if kw.strip()]
    else:
        job_keywords = [kw.lower() for kw in DEFAULT_JOB_TITLES]

    # Load additional keywords (e.g. View Bio)
    extra_keywords = [kw.strip().lower() for kw in extra_keyword_input.split(",") if kw.strip()]

    lines = [line.strip() for line in input_text.splitlines() if line.strip()]
    seen = set()
    unique_lines = []

    for line in lines:
        line_lower = line.lower()
        words = line_lower.split()

        # Remove lines similar to job titles
        remove_due_to_job = any(
            difflib.get_close_matches(word, job_keywords, n=1, cutoff=0.85)
            for word in words
        )
        if remove_due_to_job:
            continue

        # Remove lines containing extra keywords
        if any(extra_kw in line_lower for extra_kw in extra_keywords):
            continue

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
