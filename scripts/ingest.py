from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import json

def parse_pdf_text(pdf_path):
    parser = PdfReader(pdf_path)

    full_text = []

    for page_n, page in enumerate(parser.pages):
        text = page.extract_text()
        if text:
            full_text.append(f"--- Page {page_n + 1} ---\n{text}")

    return "\n".join(full_text)


#csci270 = parse_pdf_text("/Users/charlotte/Documents/GitHub/course-assistant/pdfs/270-syllabus.pdf")
#with open("/Users/charlotte/Documents/GitHub/course-assistant/text-files/270", "w", encoding="utf-8") as file:
#    file.write(csci270)
#csci201 = parse_pdf_text("/Users/charlotte/Documents/GitHub/course-assistant/pdfs/CSCI201_syllabus_Fall_2026_v6.pdf")
#with open("/Users/charlotte/Documents/GitHub/course-assistant/text-files/201", "w", encoding="utf-8") as file:
#    file.write(csci201)
#buad304 = parse_pdf_text("/Users/charlotte/Documents/GitHub/course-assistant/pdfs/BUAD 304 Fa 2026 Course Syllabus.pdf")
#with open("/Users/charlotte/Documents/GitHub/course-assistant/text-files/304", "w", encoding="utf-8") as file:
#    file.write(buad304)
#econ352 = parse_pdf_text("/Users/charlotte/Documents/GitHub/course-assistant/pdfs/Syllabus_ECON_352X_26055_Fall_2026.pdf")
#with open("/Users/charlotte/Documents/GitHub/course-assistant/text-files/352", "w", encoding="utf-8") as file:
#    file.write(econ352)

# Section headers as they actually appear in each syllabus's extracted text.
# Content is split at these lines instead of at a fixed character count, so a
# policy/rubric section is never cut in the middle.
#
# Each entry is (header_text, exact). "exact" headers must match the whole
# stripped line -- this is the default and the safe choice, since it's what
# stops a short header like "Labs" or "Exams" from false-matching a table row
# ("Labs 10") or a preamble line ("Labs: Monday 12:00-1:50pm...") that merely
# starts with the same word. Only headers marked exact=False (contact/resource
# lines that always have a phone number, URL, or the next sentence glued onto
# the same physical line by PDF extraction) use prefix matching; the text
# after the header on that line is kept as the start of the new section's
# body, not discarded.
SECTION_HEADERS = {
    "201": [
        ("Catalog Description", True), ("Course Description", True),
        ("Learning Objectives", True), ("Course Notes", True),
        ("In-person and Online Lectures", True),
        ("Technological Proficiency and Hardware/Software Required", True),
        ("Readings and Supplementary Materials", True),
        ("Assessment and Assignments", True), ("Participation", True),
        ("Grading Breakdown", True), ("Grading Scale", True),
        ("Assignments Weights", True), ("Course Policies", True),
        ("Assignment Submission", True), ("Grading Timeline", True),
        ("Regrading", True), ("Late Submission", True), ("Exams", True),
        ("Attendance", True), ("Final Project", True), ("Labs", True),
        ("Weekly Quizzes", True), ("Academic Integrity", True),
        ("Permitted Use of Artificial Intelligence (AI) Tools", True),
        ("Course Content Distribution and Synchronous Session", True),
        ("Learning Experience Evaluations", True), ("Course Schedule", True),
        ("Assessments Schedule", True),
        ("Statement on Academic Conduct and Support Systems", True),
        ("Students and Disability Accommodations", True),
        ("Student Financial Aid and Satisfactory Academic Progress", True),
        ("Support Systems", True), ("Counseling and Mental Health", False),
        ("988 Suicide and Crisis Lifeline", False), ("CARE-SC", False),
        ("Office of Civil Rights Compliance", False),
        ("USC Campus Support and Intervention", False),
        ("USC Emergency Information", True), ("USC Department of Public Safety", True),
        ("Office of the Ombuds", False), ("Occupational Therapy Faculty Practice", False),
    ],
    "270": [
        ("Catalogue Description", True), ("Course Description", True),
        ("Learning Objectives", True), ("Recommended Preparation:", True),
        ("Course Notes:", True), ("Grading Breakdown:", True),
        ("Textbook:", True), ("Participation", True), ("Grading Scale", True),
        ("Assignment Submission Policy:", True), ("Grading Timeline:", True),
        ("Use of Generative AI in this Course:", False), ("Course Schedule", True),
        ("Academic Integrity", True),
        ("Course Content Distribution and Synchronous Session Recordings Policies", True),
        ("Statement on University Academic and Support Systems", True),
        ("Students and Disability Accommodations:", True),
        ("Student Financial Aid and Satisfactory Academic Progress:", True),
        ("Support Systems:", True), ("Counseling and Mental Health", False),
        ("988 Suicide and Crisis Lifeline", False), ("CARE-SC", False),
        ("Office of Civil Rights Compliance", False), ("USC Report & Response", False),
        ("USC Campus Support and Intervention", False),
        ("USC Emergency Information", True), ("USC Department of Public Safety", True),
        ("Office of the Ombuds", False), ("Occupational Therapy Faculty Practice", False),
    ],
    "304": [
        ("Course Description", True), ("Learning Objectives", True),
        ("Open Expression and Respect for All", True), ("Required Materials", True),
        ("Additional Readings, Resources and Assessments", True),
        ("Brightspace", True), ("Grading", True),
        ("Statement on Use of AI Tools:", False),
        ("Course Requirements: Exams", True),
        ("Course Requirements: Team Project", True),
        ("Course Requirements: Individual Assignments", True),
        ("Course Requirements: Participation", True),
        ("Weekly Schedule (listed in Brightspace)", True),
        ("ADDITIONAL INFORMATION", True), ("USC Marshall Critical Thinking Initiative", True),
        ("Add/Drop Process", True), ("Retention of Graded Coursework", True),
        ("Statement on Technology Use", True), ("Religious/Cultural Observance", True),
        ("Use of Recordings", True), ("Emergency Preparedness/Course Continuity", True),
        ("Incomplete Grades", True),
        ("Statement on Academic Conduct and Support Systems", True),
        ("Students and Disability Accommodations:", False),
        ("Student Financial Aid and Satisfactory Academic Progress:", False),
        ("Support Systems:", False), ("Appendix A", True),
    ],
    "352": [
        ("COURSE DESCRIPTION", True), ("COURSE OBJECTIVES", True),
        ("Alignment with Marshall School of Business Program Learning Goals", True),
        ("Course Focus on Past, Current, and Future Macro-Finance Issues", True),
        ("COURSE MATERIALS", True), ("GRADING", True), ("EXAMS", True),
        ("TEAM PROJECT", True), ("GETTING HELP", True),
        ("THE IMPORTANCE OF COURSE EVALUATIONS", True), ("CLASS ETIQUETTE", True),
        ("COMMUNICATION PROTOCOLS", True), ("OTHER PROCEDURES", True),
        ("STATEMENT OF ACADEMIC CONDUCT AND SUPPORT SYSTEMS", True),
        ("Students with Disabilities:", True), ("Support Systems:", True),
        ("Sexual Assault Resource Center", True),
        ("Office of Equity and Diversity (OED)", False),
        ("Bias Assessment Response and Support", True),
        ("Student Support & Advocacy", False), ("Diversity at USC", False),
        ("Emergency Preparations", True),
        ("OPEN EXPRESSION AND RESPECT FOR ALL", True), ("Technology Policy", True),
        ("COURSE OUTLINE: COURSE CALENDAR / READINGS / CLASS SESSIONS", True),
        ("Evaluation Form for Group Project", True),
    ],
}

# Fallback splitter: only used to break up a single section that is still too
# long on its own (e.g. a multi-week schedule table). Never crosses a section
# boundary, so it can't cut a policy/rubric in half.
fallback_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=80,
    separators=["\n\n", "\n", ". ", " "]
)
MAX_SECTION_CHARS = 1000


def split_by_sections(text, headers):
    lines = text.split("\n")
    sections = []
    current_header = "Course Info"
    current_lines = []

    for line in lines:
        stripped = line.strip()
        matched = None
        remainder = ""
        if stripped:
            for header_text, exact in headers:
                if stripped == header_text:
                    matched = header_text
                    break
                if not exact and stripped.startswith(header_text):
                    matched = header_text
                    remainder = stripped[len(header_text):].strip(" :-–")
                    break
        if matched:
            content = "\n".join(current_lines).strip()
            if content:
                sections.append((current_header, content))
            current_header = matched
            current_lines = [remainder] if remainder else []
        else:
            current_lines.append(line)

    content = "\n".join(current_lines).strip()
    if content:
        sections.append((current_header, content))
    return sections


def chunk_syllabus(text, headers):
    chunks = []
    for header, content in split_by_sections(text, headers):
        if len(content) <= MAX_SECTION_CHARS:
            chunks.append(f"{header}\n{content}")
        else:
            for piece in fallback_splitter.split_text(content):
                chunks.append(f"{header}\n{piece}")
    return chunks


for course in ["201", "270", "304", "352"]:
    with open(f"data/processed/text/{course}", "r", encoding="utf-8") as file:
        text = file.read()
    chunks = chunk_syllabus(text, SECTION_HEADERS[course])
    with open(f"data/processed/chunks/{course}_chunked", "w", encoding="utf-8") as file:
        json.dump(chunks, file, ensure_ascii=False, indent=4) 