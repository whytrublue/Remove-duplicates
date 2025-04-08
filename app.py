import streamlit as st
import difflib

st.set_page_config(page_title="Duplicate Remover", layout="centered")
st.title("🧹 Remove Duplicate Lines with Filters")

# ✅ Always-remove keywords (hardcoded)
DEFAULT_REMOVE_KEYWORDS = ["view bio", "learn more", "contact info", "photo of"]

# 🎯 Built-in job title list
DEFAULT_JOB_TITLES = [
    "President", "Vice President", "CEO", "COO", "CFO", "CMO", "CTO", "Chief", "Director", "Executive", "Managing Director", "Owner", "Partner", 
    "Co-Founder", "Founder", "Principal", "Chairman", "Chairperson", "Manager", "Operations Manager", "Project Manager", "Product Manager", 
    "General Manager", "Finance Manager", "HR Manager", "Office Manager", "Maintenance Manager", "Account Manager", "Marketing Manager", 
    "Officer", "Controller", "Specialist", "Analyst", "Consultant", "Coordinator", "Assistant", "Advisor", "Representative", "Strategist", 
    "Auditor", "Buyer", "Planner", "Supervisor", "Team Lead", "Lead", "Sr", "Senior", "Jr", "Junior", "Intern", "Apprentice", "Trainee", 
    "Photographer", "Designer", "Editor", "Videographer", "Artist", "Content Creator", "Creative Director", "Developer", "Engineer", "Technician", 
    "IT Support", "Support Engineer", "Programmer", "Web Developer", "Systems Administrator", "Architect", "Concierge", "Quality Assurance", "Accountant", "Property Manager"
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
    placeholder="Example: View Bio, Learn More, Contact Info, Photo of"
)

# --- 🚀 Start Processing ---
if st.button("Remove Duplicates"):
    # Step 1: Job title list
    if job_filter_input.strip():
        job_keywords = [kw.strip().lower() for kw in job_filter_input.split(",") if kw.strip()]
    else:
        job_keywords = [kw.lower() for kw in DEFAULT_JOB_TITLES]

    # Step 2: Exclude from filter
    if job_exclusion_input.strip():
        exclusions = [kw.strip().lower() for kw in job_exclusion_input.split(",") if kw.strip()]
        job_keywords = [kw for kw in job_keywords if kw not in exclusions]

    # Step 3: Merge default + extra removal keywords
    user_keywords = [kw.strip().lower() for kw in extra_keyword_input.split(",") if kw.strip()]
    all_removal_keywords = list(set(DEFAULT_REMOVE_KEYWORDS + user_keywords))

    # Step 4: Process text
    lines = [line.strip() for line in input_text.splitlines() if line.strip()]
    seen = set()
    unique_lines = []

    for line in lines:
        line_lower = line.lower()

        # ✅ Remove by job titles (phrase-aware)
        remove_due_to_job = any(job_kw in line_lower for job_kw in job_keywords)
        if remove_due_to_job:
            continue

        # ✅ Remove by default/custom keywords
        if any(keyword in line_lower for keyword in all_removal_keywords):
            continue

        if line not in seen:
            unique_lines.append(line)
            seen.add(line)

    # Display cleaned results
    cleaned_text = "\n".join(unique_lines)
    st.success(f"✅ {len(unique_lines)} unique lines (removed {len(lines) - len(unique_lines)} duplicates or filtered lines)")

    st.text_area("🎯 Cleaned Result (copy from here):", value=cleaned_text, height=300)

    st.download_button(
        label="📄 Download Result as TXT",
        data=cleaned_text,
        file_name="cleaned_output.txt",
        mime="text/plain"
    )
