import re
import fitz


def extract_text(pdf_path):
    doc = fitz.open(pdf_path)

    text = ""

    for page in doc:
        text += page.get_text()

    doc.close()

    return text


def extract_email(text):
    emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)

    if emails:
        return emails[0]

    return "Not Found"


def extract_phone(text):

    phones = re.findall(r"\+?\d[\d\s\-]{9,14}", text)

    if phones:
        return phones[0]

    return "Not Found"
SKILLS = [
    "Python",
    "Java",
    "C",
    "C++",
    "Flask",
    "Django",
    "SQL",
    "HTML",
    "CSS",
    "JavaScript",
    "React",
    "Machine Learning",
    "Pandas",
    "NumPy",
    "Git",
    "AWS",
]


def extract_skills(text):

    found = []

    for skill in SKILLS:

        if skill.lower() in text.lower():
            found.append(skill)

    return found
