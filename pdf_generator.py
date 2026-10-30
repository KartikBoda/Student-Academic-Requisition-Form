"""Builds the Student Academic Requisition Form PDF following the institute's form layout."""
import io
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit

APPLICATION_TYPES = ["Bonafide", "Student Certificate", "Scholarship", "NOC",
                     "Academic Permission", "Examination", "Internship",
                     "Placement", "Other request"]

DECLARATION = ("I certify that the information provided above is correct and that the request "
               "is being submitted for academic purposes. I understand that the request will be "
               "processed as per applicable Institute/University rules and within the stipulated "
               "processing time.")

PROCESSING = ("Processing Time: The request will normally be processed within 4 working days after "
              "receiving the completed form and all required supporting documents. Students are "
              "advised to apply in advance, as incomplete applications may require additional "
              "processing time.")

L, R = 1.75 * cm, A4[0] - 1.75 * cm
W, H = A4


def _line(c, x1, x2, y):
    c.setLineWidth(0.6)
    c.line(x1, y - 2, x2, y - 2)


def _label_value(c, x, y, label, value, x_end, bold_label=False):
    """Draw 'label' followed by an underlined value up to x_end."""
    c.setFont("Helvetica-Bold" if bold_label else "Helvetica", 10)
    c.drawString(x, y, label)
    vx = x + c.stringWidth(label, "Helvetica-Bold" if bold_label else "Helvetica", 10) + 4
    _line(c, vx, x_end, y)
    c.setFont("Helvetica", 10)
    c.drawString(vx + 2, y, str(value)[:int((x_end - vx) / 5)])
    return vx


def _checkbox(c, x, y, checked=False, size=9):
    c.setLineWidth(0.8)
    c.rect(x, y - 1.5, size, size)
    if checked:
        c.setLineWidth(1.4)   # draw a tick with lines (no font change)
        c.line(x + 1.8, y + 3.5, x + 3.8, y + 1.2)
        c.line(x + 3.8, y + 1.2, x + 7.5, y + 7)
    c.setFont("Helvetica", 10)


def _wrapped(c, text, x, y, width, font="Helvetica", size=10, leading=14):
    c.setFont(font, size)
    for ln in simpleSplit(text, font, size, width):
        c.drawString(x, y, ln)
        y -= leading
    return y


def generate_pdf(d: dict, logo_path="logo.png") -> bytes:
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    y = H - 1.6 * cm

    # ---- Header box: logo | title ----
    box_h = 2.0 * cm
    split = L + 4.6 * cm
    c.setLineWidth(1)
    c.rect(L, y - box_h, R - L, box_h)
    c.line(split, y - box_h, split, y)
    try:
        c.drawImage(logo_path, L + 0.2 * cm, y - box_h + 0.15 * cm, width=4.2 * cm,
                    height=box_h - 0.3 * cm, preserveAspectRatio=True, mask="auto")
    except Exception:
        pass
    c.setFont("Helvetica-Bold", 15)
    c.drawCentredString((split + R) / 2, y - 0.85 * cm, "STUDENT ACADEMIC REQUISITION")
    c.drawCentredString((split + R) / 2, y - 1.5 * cm, "FORM")
    y -= box_h + 0.9 * cm

    # ---- Department / Outward No / Date ----
    _label_value(c, L, y, "Name of the Department.:", d["department"], L + 9.2 * cm, True)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(L + 9.6 * cm, y, "Department Outward No.:")
    _line(c, L + 9.6 * cm + 125, R, y)          # left blank - office use
    y -= 0.7 * cm
    _label_value(c, L, y, "Date:", d["date"], L + 5 * cm, True)
    y -= 0.8 * cm

    # ---- Processing time ----
    y = _wrapped(c, PROCESSING, L, y, R - L, "Helvetica-Bold", 9.5, 12.5)
    c.setLineWidth(0.4); c.line(L, y + 6, R, y + 6)
    y -= 0.5 * cm

    # ---- 1. Student details ----
    c.setFont("Helvetica-Bold", 10.5); c.drawString(L, y, "1. STUDENT DETAILS")
    y -= 0.8 * cm
    _label_value(c, L, y, "Name of Student:", d["name"], R - 1.5 * cm)
    y -= 0.8 * cm
    _label_value(c, L, y, "Roll No.:", d["roll"], L + 6 * cm)
    _label_value(c, L + 6.5 * cm, y, "Semester:", d["semester"], L + 10.8 * cm)
    _label_value(c, L + 11.3 * cm, y, "Division:", d["division"], R)
    y -= 0.8 * cm
    _label_value(c, L, y, "Email / Mobile:", f'{d["email"]} / {d["mobile"]}', R - 1.5 * cm)
    y -= 0.8 * cm

    # Application type: options as in the form, selected one ticked
    c.setFont("Helvetica", 10)
    c.drawString(L, y, "Application for \u2013")
    y -= 0.55 * cm
    x = L
    for opt in APPLICATION_TYPES:
        w = c.stringWidth(opt, "Helvetica", 9.5) + 22
        if x + w > R:
            x = L; y -= 0.65 * cm
        _checkbox(c, x, y, opt == d["app_type"])
        c.setFont("Helvetica-Bold" if opt == d["app_type"] else "Helvetica", 9.5)
        c.drawString(x + 13, y, opt)
        x += w + 8
    y -= 0.5 * cm
    if d["app_type"] == "Other request" and d.get("other_type"):
        _label_value(c, L, y - 0.15 * cm, "Other (specify):", d["other_type"], R - 1.5 * cm)
        y -= 0.6 * cm
    y -= 0.5 * cm

    # ---- 2. Purpose ----
    c.setFont("Helvetica-Bold", 10.5); c.drawString(L, y, "2. PURPOSE / BRIEF DETAILS OF REQUEST")
    y -= 0.7 * cm
    lines = []
    for para in d["purpose"].splitlines() or [""]:
        lines += simpleSplit(para, "Helvetica", 10, R - L - 4) or [""]
    n_lines = max(3, min(len(lines), 6))
    for i in range(n_lines):
        _line(c, L, R, y)
        if i < len(lines):
            c.setFont("Helvetica", 10); c.drawString(L + 2, y, lines[i])
        y -= 0.7 * cm
    y -= 0.2 * cm

    # ---- 3. Supporting documents ----
    c.setFont("Helvetica-Bold", 10.5); c.drawString(L, y, "3. SUPPORTING DOCUMENTS")
    y -= 0.75 * cm
    c.setFont("Helvetica", 10); c.drawString(L, y, "Documents attached:")
    _checkbox(c, L + 4 * cm, y, d["docs_attached"] == "Yes"); c.drawString(L + 4 * cm + 14, y, "Yes")
    _checkbox(c, L + 6.5 * cm, y, d["docs_attached"] == "No"); c.drawString(L + 6.5 * cm + 14, y, "No")
    y -= 0.75 * cm
    _label_value(c, L, y, "Document name(s), if applicable:", d["doc_names"], R)
    y -= 0.9 * cm

    # ---- 4. Declaration ----
    c.setFont("Helvetica-Bold", 10.5); c.drawString(L, y, "4. STUDENT DECLARATION")
    y -= 0.6 * cm
    y = _wrapped(c, DECLARATION, L, y, R - L, "Helvetica", 9.5, 12.5)
    y -= 0.7 * cm
    _label_value(c, L, y, "Student Signature:", "", L + 8 * cm)    # to be signed by hand
    _label_value(c, L + 9 * cm, y, "Date:", d["date"], R)
    y -= 1.0 * cm

    # ---- 5. HoD (blank) ----
    _label_value(c, L, y, "5. HoD Signature:", "", L + 8 * cm, True)
    _label_value(c, L + 8.8 * cm, y, "Remarks:", "", R, True)
    y -= 0.7 * cm
    y = _wrapped(c, "Forwarded to (VICE PRINCIPAL/ CHIEF ACADEMIC OFFICER/ ACCOUNTS/ SPORTS/ "
                    "PLACEMENT CELL/ SCHOLARSHIP CELL/ EXAM CELL) (if required)",
                 L, y, R - L, "Helvetica", 10, 13)
    _line(c, L, R, y - 6)
    y -= 1.1 * cm
    _label_value(c, L, y, "Signature:", "", L + 8 * cm, True)
    _label_value(c, L + 8.8 * cm, y, "Remarks:", "", R, True)
    y -= 1.0 * cm

    # ---- 6. Principal office (blank) ----
    c.setFont("Helvetica-Bold", 10.5); c.drawString(L, y, "6. PRINCIPAL OFFICE USE ONLY")
    y -= 0.75 * cm
    c.setFont("Helvetica", 10); c.drawString(L, y, "Decision by Principal.:")
    x = L + 4.2 * cm
    for t in ("Approved", "Not Approved", "Clarification Required"):
        _checkbox(c, x, y); c.drawString(x + 14, y, t)
        x += c.stringWidth(t, "Helvetica", 10) + 34
    y -= 0.75 * cm
    _label_value(c, L, y, "Remarks (if any):", "", R)
    y -= 1.0 * cm
    _label_value(c, L, y, "Principal Signature:", "", L + 9 * cm)

    c.showPage(); c.save()
    return buf.getvalue()
