from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

assets = Path(__file__).parent / "assets"
assets.mkdir(exist_ok=True)


def load_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for path in (
        r"C:\Windows\Fonts\georgia.ttf",
        r"C:\Windows\Fonts\Georgia.ttf",
        r"C:\Windows\Fonts\segoeui.ttf",
        r"C:\Windows\Fonts\arial.ttf",
    ):
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def center_text(draw: ImageDraw.ImageDraw, box, text, font, fill) -> None:
    x0, y0, x1, y1 = box
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = x0 + (x1 - x0 - tw) / 2 - bbox[0]
    y = y0 + (y1 - y0 - th) / 2 - bbox[1]
    draw.text((x, y), text, font=font, fill=fill)


def make_profile() -> None:
    size = 1000
    img = Image.new("RGB", (size, size), "#0f2c3c")
    draw = ImageDraw.Draw(img)
    draw.ellipse((70, 70, 930, 930), fill="#16384b", outline="#b8954f", width=18)
    draw.ellipse((250, 210, 750, 710), fill="#2a6f7f")
    center_text(draw, (0, 280, size, 620), "YN", load_font(220), "#f7f4ef")
    center_text(draw, (80, 720, 920, 820), "Replace this photo", load_font(42), "#d9c48a")
    img.save(assets / "profile.png", optimize=True)


def make_favicon() -> None:
    fav = Image.new("RGB", (256, 256), "#0f2c3c")
    draw = ImageDraw.Draw(fav)
    draw.ellipse((18, 18, 238, 238), outline="#b8954f", width=10)
    center_text(draw, (0, 0, 256, 256), "YN", load_font(92), "#f7f4ef")
    fav.save(assets / "favicon.png", optimize=True)


def make_project_image() -> None:
    proj = Image.new("RGB", (1200, 720), "#123544")
    draw = ImageDraw.Draw(proj)
    draw.rectangle((0, 620, 1200, 720), fill="#0f2c3c")
    draw.polygon(
        [(0, 420), (420, 220), (780, 460), (1200, 180), (1200, 720), (0, 720)],
        fill="#2a6f7f",
    )
    draw.polygon(
        [(0, 560), (360, 360), (700, 520), (1200, 300), (1200, 720), (0, 720)],
        fill="#b8954f",
    )
    center_text(draw, (0, 80, 1200, 280), "Project image placeholder", load_font(56), "#f7f4ef")
    proj.save(assets / "project-placeholder.png", optimize=True)


def pdf_escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def make_cv_pdf() -> None:
    lines = [
        (72, 720, 22, "YOUR NAME"),
        (72, 688, 13, "Curriculum Vitae  |  Placeholder"),
        (72, 650, 11, "Email: YOUR.EMAIL@case.edu"),
        (72, 632, 11, "LinkedIn: linkedin.com/in/YOUR-LINKEDIN"),
        (72, 614, 11, "GitHub: github.com/YOUR-GITHUB"),
        (72, 576, 14, "Education"),
        (72, 554, 11, "DEGREE, DEPARTMENT, Case Western Reserve University, YEARS"),
        (72, 536, 11, "PREVIOUS DEGREE, UNIVERSITY, YEARS"),
        (72, 498, 14, "Experience"),
        (72, 476, 11, "ROLE, ORGANIZATION, DATES"),
        (72, 458, 11, "ROLE, ORGANIZATION, DATES"),
        (72, 420, 14, "Projects"),
        (72, 398, 11, "PROJECT TITLE - one-line result"),
        (72, 380, 11, "PROJECT TITLE - one-line result"),
        (72, 342, 14, "Skills"),
        (72, 320, 11, "Methods: regression, causal inference, machine learning, ..."),
        (72, 302, 11, "Computing: R, Python, SQL, Git, Quarto, ..."),
        (72, 250, 11, "Replace this file with your real CV before you submit the site."),
    ]

    content_lines = ["BT"]
    for x, y, size, text in lines:
        content_lines.append(f"/F1 {size} Tf")
        content_lines.append(f"1 0 0 1 {x} {y} Tm")
        content_lines.append(f"({pdf_escape(text)}) Tj")
    content_lines.append("ET")
    stream = "\n".join(content_lines).encode("latin-1")

    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        (
            b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
            b"/Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>"
        ),
        b"<< /Length %d >>\nstream\n" % len(stream) + stream + b"\nendstream",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    ]

    out = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for i, obj in enumerate(objects, start=1):
        offsets.append(len(out))
        out += f"{i} 0 obj\n".encode("ascii")
        out += obj
        out += b"\nendobj\n"

    xref = len(out)
    out += f"xref\n0 {len(objects) + 1}\n".encode("ascii")
    out += b"0000000000 65535 f \n"
    for off in offsets[1:]:
        out += f"{off:010d} 00000 n \n".encode("ascii")
    out += (
        f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\n"
        f"startxref\n{xref}\n%%EOF\n"
    ).encode("ascii")
    (assets / "YourName_CV.pdf").write_bytes(out)


if __name__ == "__main__":
    make_profile()
    make_favicon()
    make_project_image()
    make_cv_pdf()
    print("Wrote", [path.name for path in assets.iterdir()])
