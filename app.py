import streamlit as st
import difflib

st.set_page_config(page_title="Duplicate Remover", layout="centered")

st.title("🧹 Remove Duplicate Lines with Filters")

# 🎯 Built-in job title list
DEFAULT_JOB_TITLES = [
    "President", "Vice President", "CEO", "COO", "CFO", "CMO", "CTO", "Chief", "Director", "Executive", "Managing Director", "Owner", "Partner", 
    "Co-Founder", "Founder", "Principal", "Chairman", "Chairperson", "Manager", "Operations Manager", "Project Manager", "Product Manager", 
    "General Manager", "Finance Manager", "HR Manager", "Office Manager", "Maintenance Manager", "Account Manager", "Marketing Manager", 
    "Officer", "Controller", "Specialist", "Analyst", "Consultant", "Coordinator", "Assistant", "Advisor", "Representative", "Strategist", 
    "Auditor", "Buyer", "Planner", "Supervisor", "Team Lead", "Lead", "Sr", "Senior", "Jr", "Junior", "Intern", "Apprentice", "Trainee", 
    "Photographer", "Designer", "Editor", "Videographer", "Artist", "Content Creator", "Creative Director", "Developer", "Engineer", "Technician", 
    "IT Support", "Support Engineer", "Programmer", "Web Developer", "Systems Administrator", "Architect"
]

# --- 📝 User Inputs ---
input_text = st.text_area(
    "Paste your dataset below (one line per entry):",
    height=300,
    placeholder="Example:\nJohn Doe\nJane Doe\nDirector of Finance\nView Bio\n..."
)

job_filter_input = st.text_input(
    "🔍 Job titles to filter out (comma-separated, optional):",
    placeholder="Leave empty to use built-in job title list"
)

job_exclusion_input = st.text_input(
    "🛑 Job titles you want to keep (exclude from filtering):",
    placeholder="Example: Architect, Designer"
)

extra_keyword_input = st.text_input(
    "❌ Remove lines containing these keywords (comma-separated, optional):",
    placeholder="Example: View Bio, Learn More, Contact Info"
)

# --- 🚀 Start Processing ---
if st.button("Remove Duplicates"):
    # Step 1: Load job filter list
    if job_filter_input.strip():
        job_keywords = [kw.strip().lower() for kw in job_filter_input.split(",") if kw.strip()]
    else:
        job_keywords = [kw.lower() for kw in DEFAULT_JOB_TITLES]

    # Step 2: Remove exclusions
    if job_exclusion_input.strip():
        exclusions = [kw.strip().lower() for kw in job_exclusion_input.split(",") if kw.strip()]
        job_keywords = [kw for kw in job_keywords if kw not in exclusions]

    # Step 3: Extra keywords like "View Bio"
    extra_keywords = [kw.strip().lower() for kw in extra_keyword_input.split(",") if kw.strip()]

    # Step 4: Read lines
    lines = [line.strip() for line in input_text.splitlines() if line.strip()]
    seen = set()
    unique_lines = []

    for line in lines:
        line_lower = line.lower()
        words = line_lower.split()

        # Filter by job title (approx match)
        remove_due_to_job = any(
            difflib.get_close_matches(word, job_keywords, n=1, cutoff=0.85)
            for word in words
        )
        if remove_due_to_job:
            continue

        # Filter by custom keywords
        if any(extra_kw in line_lower for extra_kw in extra_keywords):
            continue

        # Remove duplicates
        if line not in seen:
            unique_lines.append(line)
            seen.add(line)

    cleaned_text = "\n".join(unique_lines)

    # ✅ Display result
    st.success(f"✅ {len(unique_lines)} unique lines (removed {len(lines) - len(unique_lines)} duplicates or filtered lines)")

    st.text_area("🎯 Cleaned Result (copy from here):", value=cleaned_text, height=300)

    st.download_button(
        label="📄 Download Result as TXT",
        data=cleaned_text,
        file_name="cleaned_output.txt",
        mime="text/plain"
    )
