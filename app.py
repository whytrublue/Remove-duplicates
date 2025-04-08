import streamlit as st
import re

st.set_page_config(page_title="Duplicate Remover", layout="centered")
st.title("🧹 Remove Duplicate Lines with Filters + Extract Contacts")

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
    placeholder="Example:\nJohn Doe - CEO - john@example.com - (123) 456-7890\n..."
)

job_filter_input = st.text_input("🎯 Include Job Titles (comma-separated, optional):", placeholder="Example: CEO, Director, Manager")
job_exclusion_input = st.text_input("🚫 Exclude Job Titles (comma-separated, optional):", placeholder="Example: Intern, Assistant")

extra_keyword_input = st.text_input(
    "❌ Remove lines containing these keywords (comma-separated, optional):",
    placeholder="Example: View Bio, Learn More, Contact Info, Photo of"
)

# --- 🚀 Start Processing ---
if st.button("Remove Duplicates and Extract Contacts"):
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
    clean_lines = []
    extracted_contacts = []

    for line in lines:
        line_lower = line.lower()

        # ✅ Remove by job titles (phrase-aware)
        if any(job_kw in line_lower for job_kw in job_keywords):
            continue

        # ✅ Remove by default/custom keywords
        if any(keyword in line_lower for keyword in all_removal_keywords):
            continue

        if line_lower not in seen:
            clean_lines.append(line)
            seen.add(line_lower)

        # Extract contact info using regex (Name - Title - Email - Phone)
        match = re.match(
            r"^(.*?)\s*[-–—]\s*(.*?)\s*[-–—]?\s*([^\s@]+@[^\s@]+\.\w+)?\s*[-–—]?\s*(\+?\d[\d\s().-]{7,}\d)?$",
            line
        )
        if match:
            name = match.group(1).strip()
            title = match.group(2).strip()
            email = match.group(3).strip() if match.group(3) else ""
            phone = match.group(4).strip() if match.group(4) else ""
            extracted_contacts.append({
                "name": name,
                "title": title,
                "email": email,
                "phone": phone
            })

    # Show cleaned list
    cleaned_text = "\n".join(clean_lines)
    st.success(f"✅ {len(clean_lines)} unique lines (removed {len(lines) - len(clean_lines)} duplicates or filtered lines)")
    st.text_area("🎯 Cleaned Result (copy from here):", value=cleaned_text, height=300)

    st.download_button(
        label="📄 Download Cleaned Text as .TXT",
        data=cleaned_text,
        file_name="cleaned_output.txt",
        mime="text/plain"
    )

    # Optional: Show extracted contacts as CSV
    if extracted_contacts:
        csv_output = "Name,Title,Email,Phone\n"
        for c in extracted_contacts:
            csv_output += f"{c['name']},{c['title']},{c['email']},{c['phone']}\n"

        st.download_button(
            label="📄 Download Extracted Contacts as .CSV",
            data=csv_output,
            file_name="contacts.csv",
            mime="text/csv"
        )
