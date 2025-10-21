import os
import argparse
from langchain_community.document_loaders import PyMuPDFLoader
from translator import translator
from writer import save


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model", type=str, required=False, help="LLM, eg: gpt-oss", default="gpt-oss"
    )
    parser.add_argument("--language", type=str, required=True, help="target language")
    parser.add_argument("--file", type=str, required=True, help="file name")

    args = parser.parse_args()

    target_language = args.language

    pdf_path = args.file

    loader = PyMuPDFLoader(pdf_path)
    pages = loader.load_and_split()

    translate = translator(model=args.model, target_language=target_language)

    translations = []

    for i, page in enumerate(pages):
        print(f"[🔄] Translating Page {i+1}...")
        translated_text = translate(page.page_content.strip())
        translations.append((f"Page {i+1}", translated_text.strip()))

    font_path = None

    common_fonts = [
        "/usr/share/fonts/truetype/noto/STSong.ttf",
        "C:/Windows/Fonts/simfang.ttf",
    ]

    for path in common_fonts:
        if os.path.exists(path):
            font_path = path
            break

    save(
        translations,
        pdf_path="output.pdf",
        txt_path="output.txt",
        font_path=font_path,
    )


if __name__ == "__main__":
    main()
