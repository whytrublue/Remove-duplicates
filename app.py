import re
import streamlit as st

st.set_page_config(page_title="Duplicate Remover", layout="centered")
st.title("🧹 Remove Duplicate Lines + Extract Name/Title/Email")

DEFAULT_REMOVE_KEYWORDS = ["view bio", "learn more", "contact info", "photo of", "Headshot"]

DEFAULT_JOB_TITLES = [
    "President", "Vice President", "CEO", "COO", "CFO", "CMO", "CTO", "Chief", "Director", "Executive",
    "Managing Director", "Owner", "Partner", "Co-Founder", "Founder", "Principal", "Chairman", "Chairperson",
    "Manager", "Operations Manager", "Project Manager", "Product Manager", "General Manager", "Finance Manager",
    "HR Manager", "Office Manager", "Maintenance Manager", "Account Manager", "Marketing Manager", "Officer",
    "Controller", "Specialist", "Analyst", "Consultant", "Coordinator", "Assistant", "Advisor", "Representative",
    "Strategist", "Auditor", "Buyer", "Planner", "Supervisor", "Team Lead", "Lead", "Sr", "Senior", "Jr", "Junior",
    "Intern", "Apprentice", "Trainee", "Photographer", "Designer", "Editor", "Videographer", "Artist",
    "Content Creator", "Creative Director", "Developer", "Engineer", "Technician", "IT Support",
    "Support Engineer", "Programmer", "Web Developer", "Systems Administrator", "Architect", "Concierge",
    "Quality Assurance", "Accountant", "Property Manager", "Realtor"
]

input_text = st.text_area(
    "Paste your dataset below (one line per entry):",
    height=300,
    placeholder="Example:\nJohn Doe\nJane Doe\nDirector of Finance\nView Bio\n..."
)

job_filter_input = st.text_input("🎯 Include Job Titles (comma-separated, optional):", placeholder="Example: CEO, Director, Manager")
job_exclusion_input = st.text_input("🚫 Exclude Job Titles (comma-separated, optional):", placeholder="Example: Intern, Assistant")

extra_keyword_input = st.text_input(
    "❌ Remove lines containing these keywords (comma-separated, optional):",
    placeholder="Example: View Bio, Learn More, Contact Info, Photo of"
)

if st.button("Remove Duplicates and Extract Contacts"):
    if job_filter_input.strip():
        job_keywords = [kw.strip().lower() for kw in job_filter_input.split(",") if kw.strip()]
    else:
        job_keywords = [kw.lower() for kw in DEFAULT_JOB_TITLES]

    if job_exclusion_input.strip():
        exclusions = [kw.strip().lower() for kw in job_exclusion_input.split(",") if kw.strip()]
        job_keywords = [kw for kw in job_keywords if kw not in exclusions]

    user_keywords = [kw.strip().lower() for kw in extra_keyword_input.split(",") if kw.strip()]
    all_removal_keywords = list(set(DEFAULT_REMOVE_KEYWORDS + user_keywords))

    lines = [line.strip() for line in input_text.splitlines() if line.strip()]
    seen = set()
    unique_lines = []

    for line in lines:
        line_lower = line.lower()
        if any(job_kw in line_lower for job_kw in job_keywords):
            continue
        if any(keyword in line_lower for keyword in all_removal_keywords):
            continue
        if line_lower not in seen:
            unique_lines.append(line)
            seen.add(line_lower)

    cleaned_text = "\n".join(unique_lines)
    st.success(f"✅ {len(unique_lines)} unique lines (removed {len(lines) - len(unique_lines)} duplicates or filtered lines)")
    st.text_area("🎯 Cleaned Result (copy from here):", value=cleaned_text, height=300)

    st.download_button(
        label="📄 Download Result as TXT",
        data=cleaned_text,
        file_name="cleaned_output.txt",
        mime="text/plain"
    )

    # ✨ Extract contacts from full original input
    contact_pattern = re.compile(
        r"(?P<name>[A-Z][a-z]+(?:\s[A-Z][a-z]+)+)\s+"
        r"(?P<title>[\w\s&/–-]+?)\s+"
        r"(?P<email>\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b)",
        re.MULTILINE
    )

    contacts = contact_pattern.findall(input_text)

    if contacts:
        st.subheader("📬 Extracted Contacts")
        contact_result = "\n".join([f"{name} | {title.strip()} | {email}" for name, title, email in contacts])
        st.text_area("Structured Contacts:", value=contact_result, height=300)

        st.download_button(
            label="📄 Download Contacts as CSV",
            data="Name,Title,Email\n" + "\n".join([f"{name},{title.strip()},{email}" for name, title, email in contacts]),
            file_name="contacts.csv",
            mime="text/csv"
        )
    else:
        st.info("🔍 No contacts found using pattern. Try with different formatting.")
