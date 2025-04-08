import re
import streamlit as st

st.set_page_config(page_title="Duplicate Remover", layout="centered")
st.title("🧹 Remove Duplicate Lines + Extract Name/Title/Email/Phone")

DEFAULT_REMOVE_KEYWORDS = ["view bio", "learn more", "contact info", "photo of", "headshot", "Portrait"]

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

extra_keyword_input = st.text_input(
    "❌ Remove lines containing these keywords (comma-separated, optional):",
    placeholder="Example: View Bio, Learn More, Contact Info, Photo of"
)

if st.button("Remove Duplicates and Extract Contacts"):
    job_keywords = [kw.lower() for kw in DEFAULT_JOB_TITLES]

    user_keywords = [kw.strip().lower() for kw in extra_keyword_input.split(",") if kw.strip()]
    all_removal_keywords = list(set([k.lower() for k in DEFAULT_REMOVE_KEYWORDS] + user_keywords))

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

    # ✨ Extract contact info
    name_pattern = re.compile(r"^[A-Z][a-z]+(?:\s[A-Z][a-z]+)+$")
    email_pattern = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
    phone_patterns = {
        "mobile": re.compile(r"(?:mobile|cell|cellphone)[\s:\-]*([\+\d\(\)\s\-]{7,})", re.IGNORECASE),
        "direct": re.compile(r"(?:direct)[\s:\-]*([\+\d\(\)\s\-]{7,})", re.IGNORECASE),
        "office": re.compile(r"(?:tel|telephone|office|work|phone)[\s:\-]*([\+\d\(\)\s\-]{7,})", re.IGNORECASE),
    }

    entries = []
    current = {"Name": "", "Title": "", "Email": "", "Mobile": "", "Direct": "", "Office": ""}

    for line in unique_lines:
        line = line.strip()
        if name_pattern.match(line):
            if current["Name"]:
                entries.append(current.copy())
                current = {"Name": "", "Title": "", "Email": "", "Mobile": "", "Direct": "", "Office": ""}
            current["Name"] = line
        elif any(title.lower() in line.lower() for title in DEFAULT_JOB_TITLES):
            current["Title"] = line
        elif email_match := email_pattern.search(line):
            current["Email"] = email_match.group(0)
        else:
            for key, pattern in phone_patterns.items():
                match = pattern.search(line)
                if match:
                    num = re.sub(r"[^\d+]", "", match.group(1))
                    current[key.capitalize()] = num

    if current["Name"]:
        entries.append(current)

    if entries:
        st.subheader("📬 Extracted Structured Contacts")
        csv_header = "Name,Title,Email,Mobile,Direct,Office"
        csv_data = [csv_header]
        display_text = []

        for e in entries:
            csv_line = f"{e['Name']},{e['Title']},{e['Email']},{e['Mobile']},{e['Direct']},{e['Office']}"
            csv_data.append(csv_line)
            display_text.append(" | ".join([e['Name'], e['Title'], e['Email'], e['Mobile'], e['Direct'], e['Office']]))

        result = "\n".join(display_text)
        st.text_area("Structured Contacts:", value=result, height=300)

        st.download_button(
            label="📄 Download Contacts as CSV",
            data="\n".join(csv_data),
            file_name="contacts.csv",
            mime="text/csv"
        )
    else:
        st.info("🔍 No contacts found. Please try with a different format.")
