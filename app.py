import streamlit as st
import re

st.set_page_config(page_title="Contact Extractor", layout="centered")
st.title("📇 Contact Cleaner & Extractor")

DEFAULT_REMOVE_KEYWORDS = ["view bio", "learn more", "contact info", "photo of"]

DEFAULT_JOB_TITLES = [
    "President", "Vice President", "CEO", "COO", "CFO", "CMO", "CTO", "Chief", "Director", "Executive", "Managing Director", "Owner", "Partner", 
    "Co-Founder", "Founder", "Principal", "Chairman", "Chairperson", "Manager", "Operations Manager", "Project Manager", "Product Manager", 
    "General Manager", "Finance Manager", "HR Manager", "Office Manager", "Maintenance Manager", "Account Manager", "Marketing Manager", 
    "Officer", "Controller", "Specialist", "Analyst", "Consultant", "Coordinator", "Assistant", "Advisor", "Representative", "Strategist", 
    "Auditor", "Buyer", "Planner", "Supervisor", "Team Lead", "Lead", "Sr", "Senior", "Jr", "Junior", "Intern", "Apprentice", "Trainee", 
    "Photographer", "Designer", "Editor", "Videographer", "Artist", "Content Creator", "Creative Director", "Developer", "Engineer", "Technician", 
    "IT Support", "Support Engineer", "Programmer", "Web Developer", "Systems Administrator", "Architect", "Concierge", "Quality Assurance", "Accountant", "Property Manager"
]

# 📝 Inputs
input_text = st.text_area("Paste your dataset:", height=300, placeholder="John Doe - CEO - john@example.com - Mobile: (123) 456-7890")
job_filter_input = st.text_input("🎯 Include Job Titles (optional):", placeholder="CEO, Director")
job_exclusion_input = st.text_input("🚫 Exclude Job Titles (optional):", placeholder="Intern, Assistant")
extra_keyword_input = st.text_input("❌ Remove lines containing these keywords (optional):", placeholder="Learn More, View Bio")

if st.button("Extract & Download"):
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
    extracted_contacts = []

    for line in lines:
        line_lower = line.lower()
        if any(job_kw in line_lower for job_kw in job_keywords):
            continue
        if any(keyword in line_lower for keyword in all_removal_keywords):
            continue
        if line_lower in seen:
            continue
        seen.add(line_lower)

        # Extract name, title, email
        name, title, email = "", "", ""
        mobile, direct, office = "", "", ""

        # Split on dash or bullet or pipe or comma
        parts = re.split(r"\s*[-–—•|,]\s*", line)

        for part in parts:
            p = part.strip()
            if not name and not any(char.isdigit() for char in p) and "@" not in p and not any(x in p.lower() for x in ["cell", "mobile", "phone", "direct", "tel", "office"]):
                name = p
            elif not title and not any(char.isdigit() for char in p) and "@" not in p and not any(x in p.lower() for x in ["cell", "mobile", "phone", "direct", "tel", "office"]):
                title = p
            elif "@" in p:
                email = p
            elif any(x in p.lower() for x in ["cell", "mobile"]):
                mobile_match = re.search(r"(\+?\d[\d\s().-]{7,}\d)", p)
                if mobile_match:
                    mobile = mobile_match.group(1)
            elif any(x in p.lower() for x in ["direct"]):
                direct_match = re.search(r"(\+?\d[\d\s().-]{7,}\d)", p)
                if direct_match:
                    direct = direct_match.group(1)
            elif any(x in p.lower() for x in ["phone", "office", "tel", "telephone"]):
                office_match = re.search(r"(\+?\d[\d\s().-]{7,}\d)", p)
                if office_match:
                    office = office_match.group(1)

        extracted_contacts.append({
            "Name": name,
            "Title": title,
            "Email": email,
            "Mobile": mobile,
            "Direct": direct,
            "Office": office
        })

    if extracted_contacts:
        csv_output = "Name,Title,Email,Mobile,Direct,Office\n"
        for c in extracted_contacts:
            csv_output += f"{c['Name']},{c['Title']},{c['Email']},{c['Mobile']},{c['Direct']},{c['Office']}\n"

        st.success(f"✅ Extracted {len(extracted_contacts)} contact entries.")
        st.text_area("📋 Copy this and paste into Excel:", value=csv_output, height=300)

        st.download_button(
            label="📄 Download as CSV",
            data=csv_output,
            file_name="contacts.csv",
            mime="text/csv"
        )
