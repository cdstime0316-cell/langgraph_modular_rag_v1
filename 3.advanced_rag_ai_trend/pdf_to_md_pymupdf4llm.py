from pathlib import Path
import pymupdf4llm
from markdown_pre_processing import clean_markdown


# --------------------------------------------------
# 1. PDF를 Markdown으로 변환해서 저장
# --------------------------------------------------
def convert_pdf_to_markdown(pdf_path: Path, md_path: Path):
    md_text = pymupdf4llm.to_markdown(str(pdf_path))

    md_path.write_text(md_text, encoding="utf-8")

    print(f"Markdown 파일 저장 완료: {md_path}")
    print(f"Markdown 미리보기:\n{md_text[:500]}")


if __name__ == "__main__":
    PDF_PATH = Path("data/AI@Data_Report_토픽_분석을_통한_AI_주요_트렌드_및_2026_전망_251223(최종).pdf")
    MD_PATH = PDF_PATH.with_suffix(".md")

    convert_pdf_to_markdown(PDF_PATH, MD_PATH)
    RAW_MD_PATH = Path("data/AI@Data_Report_토픽_분석을_통한_AI_주요_트렌드_및_2026_전망_251223(최종).md")
    CLEAN_MD_PATH = Path("data/AI@Data_Report_CLEANED.md")
    clean_markdown(RAW_MD_PATH, CLEAN_MD_PATH)