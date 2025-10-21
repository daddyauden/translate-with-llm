import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def draw_wrapped_text(canvas, text, x, y, max_width, line_height, font_name, font_size):
    canvas.setFont(font_name, font_size)

    for paragraph in text.split("\n"):
        line = ""
        for char in paragraph:
            test_line = line + char
            if canvas.stringWidth(test_line, font_name, font_size) <= max_width:
                line = test_line
            else:
                canvas.drawString(x, y, line)
                y -= line_height
                if y < 50:
                    canvas.showPage()
                    canvas.setFont(font_name, font_size)
                    y = A4[1] - 50
                line = char

        if line.strip():
            canvas.drawString(x, y, line)
            y -= line_height
            if y < 50:
                canvas.showPage()
                canvas.setFont(font_name, font_size)
                y = A4[1] - 50

        y -= line_height

    return y


def save(
    pages,
    pdf_path="output.pdf",
    txt_path="output.txt",
    font_path=None,
):
    _, height = A4
    c = canvas.Canvas(pdf_path, pagesize=A4)

    if font_path and os.path.exists(font_path):
        pdfmetrics.registerFont(TTFont("CustomFont", font_path))
        font_name = "CustomFont"
    else:
        font_name = "Helvetica"

    c.setFont(font_name, 12)

    with open(txt_path, "w", encoding="utf-8") as txt_file:
        for title, content in pages:
            c.setFont(font_name, 12)
            c.drawString(50, height - 50, title)

            y = height - 80

            y = draw_wrapped_text(
                canvas=c,
                text=content,
                x=50,
                y=y,
                max_width=A4[0] - 100,
                line_height=18,
                font_name=font_name,
                font_size=12,
            )

            c.showPage()

            txt_file.write(f"{title}\n")
            txt_file.write(content.strip() + "\n")
            txt_file.write("-" * 40 + "\n\n")

    c.save()
    print(f"[✅] PDF saved to: {pdf_path}")
    print(f"[✅] TXT saved to: {txt_path}")
