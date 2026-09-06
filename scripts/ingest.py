from pypdf import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import json

def parse_pdf_text(pdf_path):
    parser = PdfReader(pdf_path)

    full_text = []

    for page_n, page in enumerate(parser.pages):
        text = page.extract_text()
        if text:
            full_text.append(f"--- Page {page_n} + 1 ---\n{text}")

    return "/n".join(full_text)


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

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunkOverlap=50,
    separators=["\n\n", "\n", ". ", " "]
)

with open("data/processed/201", "r", encoding="utf-8") as file:
    text_201 = file.read()
chunk_201 = splitter.split_text(text_201)

with open("data/processed/201", "r", encoding="utf-8") as file:
    text_201 = file.read()
chunk_201 = splitter.split_text(text_201)

with open("data/processed/201", "r", encoding="utf-8") as file:
    text_201 = file.read()
chunk_201 = splitter.split_text(text_201)

with open("data/processed/201", "r", encoding="utf-8") as file:
    text_201 = file.read()
chunk_201 = splitter.split_text(text_201)




