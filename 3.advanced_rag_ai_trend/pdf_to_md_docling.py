# 레이어, 레이아웃, 표, 이미지, OCR 등을 함께 활용할 수 있다. Docling 공식 설명에서도 PDF, DOCX, PPTX 등 다양한 문서를 파싱하며, PDF의 레이아웃, 읽기 순서, 테이블 구조, OCR 등을 처리한다고 설명
from pathlib import Path
import shutil
from docling.document_converter import DocumentConverter
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions, TableStructureOptions
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling_core.types.doc import ImageRefMode

def convert_pdf_to_markdown(pdf_path: Path, md_path: Path | None = None) -> Path:
    """
    PDF 파일을 Docling을 사용하여 Markdown 파일로 변환한다.

    Args:
        pdf_path: 변환할 PDF 파일 경로
        md_path: 저장할 Markdown 파일 경로. None이면 PDF와 같은 이름의 .md 파일로 저장한다.

    Returns:
        저장된 Markdown 파일 경로
    """

    # 경로 객체 변환
    pdf_path = Path(pdf_path)

    # 입력 PDF 존재 여부 확인
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF 파일을 찾을 수 없습니다: {pdf_path}")

    # 출력 경로 설정
    if md_path is None:
        md_path = pdf_path.with_suffix(".md")
    else:
        md_path = Path(md_path)

    # 출력 폴더가 없으면 생성
    md_path.parent.mkdir(parents=True, exist_ok=True)

    # Docling 변환기 생성
    converter = DocumentConverter()

    # PDF → Docling Document 변환
    result = converter.convert(str(pdf_path))
    doc = result.document

    # Docling Document → Markdown 변환
    markdown_text = doc.export_to_markdown()

    # Markdown 저장
    md_path.write_text(markdown_text, encoding="utf-8")

    print(f"Markdown 변환 완료: {md_path}")
    print(markdown_text[:1000])

    return md_path

def convert_pdf_to_markdown_with_images(pdf_path: Path):
    """
    OCR을 사용하지 않고 PDF를 Markdown으로 변환한다.

    목적:
    1. 텍스트 레이어 기반 본문 추출
    2. 표 구조 보존
    3. PDF 내부 이미지를 별도 파일로 저장
    4. Markdown에서 이미지 링크로 참조
    """

    pdf_path = Path(pdf_path)

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF 파일을 찾을 수 없습니다: {pdf_path}")

    # 출력 폴더
    output_dir = pdf_path.parent / "docling_output"
    output_dir.mkdir(parents=True, exist_ok=True)

    # 한글/특수문자 경로 문제를 피하기 위해 임시 파일명 단순화
    temp_pdf_path = output_dir / "input.pdf"
    shutil.copy2(pdf_path, temp_pdf_path)

    # PDF 파이프라인 옵션
    pipeline_options = PdfPipelineOptions()

    # 핵심: OCR 끄기
    pipeline_options.do_ocr = False

    # 표 구조 인식
    pipeline_options.do_table_structure = True
    pipeline_options.table_structure_options = TableStructureOptions(
        do_cell_matching=True
    )

    # 이미지 추출
    pipeline_options.images_scale = 2.0
    pipeline_options.generate_picture_images = True

    # 페이지 전체 이미지까지 필요하면 True
    # 보통 RAG용 Markdown에서는 False가 더 깔끔함
    pipeline_options.generate_page_images = False

    # 변환기 생성
    converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(
                pipeline_options=pipeline_options
            )
        }
    )

    # 변환 실행
    result = converter.convert(str(temp_pdf_path))

    # Markdown 저장
    md_path = output_dir / f"{pdf_path.stem}.md"

    result.document.save_as_markdown(
        md_path,
        image_mode=ImageRefMode.REFERENCED
    )

    print(f"Markdown 저장 완료: {md_path}")
    print(f"출력 폴더: {output_dir}")

    return md_path

if __name__ == "__main__":
    PDF_PATH = Path("data") / "AI@Data_Report_토픽_분석을_통한_AI_주요_트렌드_및_2026_전망_251223(최종).pdf"
    print(f"PDF 파일 경로: {PDF_PATH}")
    MD_PATH = PDF_PATH.with_suffix(".md")
    # 기본 변환 (이미지 포함하지 않음)
    convert_pdf_to_markdown(PDF_PATH, MD_PATH)
    # 이미지 포함 변환
    convert_pdf_to_markdown_with_images(PDF_PATH)