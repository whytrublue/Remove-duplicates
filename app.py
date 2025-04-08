import re
import streamlit as st

st.set_page_config(page_title="Duplicate Remover", layout="centered")
st.title("🧹 Remove Duplicate Lines + Extract Name/Title/Email/Phone")

DEFAULT_REMOVE_KEYWORDS = ["view bio", "learn more", "contact info", "photo of", "headshot", "portrait"]

input_text = st.text_area(
    "Paste your dataset below (one line per entry):",
    height=300,
    placeholder="Example:\nJoe Allinder\nBroker with Joe Allinder\n(972) 930-0323\n..."
)

extra_keyword_input = st.text_input(
    "❌ Remove lines containing these keywords (comma-separated, optional):",
    placeholder="Example: View Bio, Learn More, Contact Info, Photo of"
)

if st.button("Remove Duplicates and Extract Contacts"):
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

    # Prepare to extract contact info
    entries = []
    current = {"Name": "", "Title": "", "Email": "", "Mobile": "", "Direct": "", "Office": ""}

    # Regex patterns
    name_pattern = re.compile(r"^[A-Z][a-zA-Z\s]+$")
    email_pattern = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
    phone_patterns = {
        "mobile": re.compile(r"(?:mobile|cell|cellphone)[\s:\-]*([\+\d\(\)\s\-]{7,})", re.IGNORECASE),
        "direct": re.compile(r"(?:direct)[\s:\-]*([\+\d\(\)\s\-]{7,})", re.IGNORECASE),
        "office": re.compile(r"(?:tel|telephone|office|work|phone)[\s:\-]*([\+\d\(\)\s\-]{7,})", re.IGNORECASE),
    }

    for line in unique_lines:
        line = line.strip()
        
        # Match name
        if name_pattern.match(line):
            if current["Name"]:
                entries.append(current.copy())
                current = {"Name": "", "Title": "", "Email": "", "Mobile": "", "Direct": "", "Office": ""}
            current["Name"] = line.strip()
        
        # Match title (assuming titles are present in a subsequent line)
        if "broker" in line.lower():
            current["Title"] = line
        
        # Match email
        email_match = email_pattern.search(line)
        if email_match:
            current["Email"] = email_match.group(0)
        
        # Match phone numbers
        for key, pattern in phone_patterns.items():
            match = pattern.search(line)
            if match:
                num = re.sub(r"[^\d+]", "", match.group(1))
                current[key.capitalize()] = num

    # Add the last entry if not empty
    if current["Name"]:
        entries.append(current)

    # Display extracted data
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
