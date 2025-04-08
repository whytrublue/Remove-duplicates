import re
import streamlit as st

st.set_page_config(page_title="Duplicate Remover", layout="centered")
st.title("🧹 Remove Duplicate Lines + Extract Name/Title/Email/Phone")

DEFAULT_REMOVE_KEYWORDS = ["view bio", "learn more", "contact info", "photo of", "headshot", "portrait"]

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
    all_removal_keywords = list(set([kw.lower() for kw in DEFAULT_REMOVE_KEYWORDS] + user_keywords))

    lines = [line.strip() for line in input_text.splitlines() if line.strip()]
    seen = set()
    unique_lines = []

    for line in lines:
        line_lower = line.lower()
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

    # 🔍 Extract contacts from cleaned_text block-by-block
    st.subheader("📬 Extracted Contacts with Phones")
    contact_blocks = cleaned_text.split("\n\n")
    extracted_rows = []

    for block in contact_blocks:
        lines = block.strip().split("\n")
        full_block = " ".join(lines)

        name = ""
        email = ""
        title = ""
        cell = ""
        phone = ""

        # Email
        email_match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", full_block)
        if email_match:
            email = email_match.group()

        # Name (First Last or First Middle Last)
        name_match = re.search(r"\b([A-Z][a-z]+(?:\s[A-Z][a-z]+)+)\b", full_block)
        if name_match:
            name = name_match.group()

        # Title
        for job in DEFAULT_JOB_TITLES:
            if re.search(rf"\b{re.escape(job)}\b", full_block, re.IGNORECASE):
                title = job
                break

        # Cell
        cell_match = re.search(r"(?:Cell(?: Phone)?|Mobile(?: Number)?)\s*[:\-]?\s*([\d\-\+\(\)\s]{7,})", full_block, re.IGNORECASE)
        if cell_match:
            cell = re.sub(r"[^\d+]", "", cell_match.group(1))

        # Phone
        phone_match = re.search(r"(?:Phone(?: Number)?|Tel(?:ephone)?|Office|Work|Direct)\s*[:\-]?\s*([\d\-\+\(\)\s]{7,})", full_block, re.IGNORECASE)
        if phone_match:
            phone = re.sub(r"[^\d+]", "", phone_match.group(1))

        if name or email or title or cell or phone:
            extracted_rows.append([name, title, email, cell, phone])

    if extracted_rows:
        st.text_area(
            "Structured Contacts (Name | Title | Email | Cell | Phone):",
            value="\n".join([" | ".join(row) for row in extracted_rows]),
            height=300
        )

        st.download_button(
            label="📄 Download Contacts as CSV",
            data="Name,Title,Email,Cell,Phone\n" + "\n".join([",".join(row) for row in extracted_rows]),
            file_name="contacts_with_phone.csv",
            mime="text/csv"
        )
    else:
        st.info("🔍 No contacts found using pattern. Try with different formatting.")
