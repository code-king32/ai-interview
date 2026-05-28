"""
简历解析服务 —— 支持 PDF、DOCX、DOC、TXT 格式。
"""

import os
from PyPDF2 import PdfReader
from docx import Document as DocxDocument


def parse_resume(file_path: str) -> str:
    """根据文件后缀解析简历，返回纯文本。"""
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".txt":
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    if ext == ".pdf":
        reader = PdfReader(file_path)
        return "\n".join(page.extract_text() or "" for page in reader.pages)

    if ext in (".docx", ".doc"):
        doc = DocxDocument(file_path)
        return "\n".join(p.text for p in doc.paragraphs)

    raise ValueError(f"不支持的简历文件格式: {ext}")
