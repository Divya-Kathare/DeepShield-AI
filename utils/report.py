from io import BytesIO
from datetime import datetime
import random

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    Table,
    TableStyle,
    PageBreak,
)

def add_watermark(canvas, doc):

    canvas.saveState()

    page_width, page_height = doc.pagesize

    # Draw watermark at the center
    canvas.drawImage(
        "assets/watermark.png",
        x=80,
        y=180,
        width=430,
        height=430,
        preserveAspectRatio=True,
        mask="auto",
    )

    canvas.restoreState()

def generate_report(
    result,
    reasoning,
    image_path=None,
    heatmap_path=None,
    overlay_path=None,
):

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        rightMargin=35,
        leftMargin=35,
        topMargin=0,
        bottomMargin=35,
    )

    styles = getSampleStyleSheet()

    title_style = styles["Title"]
    title_style.spaceBefore = 0
    title_style.spaceAfter = 0
    title_style.alignment = TA_CENTER
    title_style.textColor = colors.HexColor("#0F4C81")

    heading_style = styles["Heading2"]
    heading_style.textColor = colors.HexColor("#0F4C81")

    body_style = styles["BodyText"]

    elements = []

    # =====================================================
    # HEADER
    # =====================================================


    logo = Image(
        "assets/logo_horizontal.png",
        width=3.8 * inch,
        height=1.4 * inch,
    )
    logo.hAlign = "CENTER"
    elements.append(logo)

    elements.append(Spacer(1, 0.05 * inch))

    elements.append(
        Paragraph(
            "<b>Explainable Deepfake Detection Report</b>",
            heading_style,
        )
    )

    elements.append(Spacer(1, 0.08 * inch))

    # =====================================================
    # REPORT ID
    # =====================================================
    report_id = f"DS-{datetime.now().strftime('%Y%m%d')}-{random.randint(1000,9999)}"
    elements.append(
        Paragraph(
            f"<b>Report ID:</b> {report_id}",
            body_style,
        )
    )
    elements.append(Spacer(1,0.15*inch))

    # =====================================================
    # PREDICTION CARD
    # =====================================================

    label = result["label"]

    if label == "REAL":
        bg = colors.HexColor("#D1FAE5")
        text = colors.HexColor("#065F46")
        risk = "LOW"
    else:
        bg = colors.HexColor("#FEE2E2")
        text = colors.HexColor("#991B1B")
        risk = "HIGH"

    prediction_table = Table(
        [
            ["Prediction", label],
            ["Confidence", f"{result['confidence']:.2f}%"],
            ["Inference Time", f"{result['time']:.3f} sec"],
            ["Risk Level", risk],
        ],
        colWidths=[2.3 * inch, 3 * inch],
    )

    prediction_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), bg),
                ("TEXTCOLOR", (0, 0), (-1, -1), text),
                ("GRID", (0, 0), (-1, -1), 1, colors.white),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ]
        )
    )

    elements.append(prediction_table)
    confidence = float(result["confidence"])
    bar = Table(
        [[""]],
        colWidths=[confidence * 4.8],
        rowHeights=[0.18 * inch],
    )
    bar.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#22C55E")),
            ]
        )
    )
    elements.append(Spacer(1,0.12*inch))
    elements.append(bar)
    elements.append(Spacer(1,0.25*inch))

    # =====================================================
    # ORIGINAL IMAGE
    # =====================================================

    if image_path:

        elements.append(
            Paragraph(
                "<b>Original Uploaded Image</b>",
                heading_style,
            )
        )

        elements.append(Spacer(1, 0.15 * inch))

        img = Image(
            image_path,
            width=3 * inch,
            height=3 * inch,
        )

        img.hAlign = "CENTER"

        elements.append(img)

        elements.append(Spacer(1, 0.30 * inch))

    # =====================================================
    # AI REASONING
    # =====================================================

    elements.append(
        Paragraph(
            "<b>AI Reasoning</b>",
            heading_style,
        )
    )

    elements.append(Spacer(1, 0.10 * inch))

    for item in reasoning:
        elements.append(
            Paragraph(
                "• " + item,
                body_style,
            )
        )

    elements.append(Spacer(1, 0.40 * inch))

    # =====================================================
    # MODEL INFORMATION
    # =====================================================

    elements.append(
        Paragraph(
            "<b>Model Information</b>",
            heading_style,
        )
    )

    elements.append(Spacer(1, 0.30 * inch))

    model_table = Table(
        [
            ["Model", "DeepShield CNN"],
            ["Framework", "TensorFlow / Keras"],
            ["Input Size", "224 × 224"],
            ["Explainability", "Grad-CAM"],
        ],
        colWidths=[2.3 * inch, 3 * inch],
    )

    model_table.setStyle(
        TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#E5F2FF")),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )

    elements.append(model_table)
    elements.append(Spacer(1, 0.25 * inch))

    # =====================================================
    # SECOND PAGE
    # =====================================================

    elements.append(
        Paragraph(
            "<b>Explainability (Grad-CAM)</b>",
            heading_style,
        )
    )

    elements.append(Spacer(1, 0.25 * inch))

    # =====================================================
    # ORIGINAL / HEATMAP / OVERLAY
    # =====================================================

    image_row = []
    caption_row = []

    if image_path:
        img = Image(image_path, width=2 * inch, height=2 * inch)
        img.hAlign = "CENTER"
        image_row.append(img)
        caption_row.append("Original")

    if heatmap_path:
        img = Image(heatmap_path, width=2 * inch, height=2 * inch)
        img.hAlign = "CENTER"
        image_row.append(img)
        caption_row.append("Heatmap")

    if overlay_path:
        img = Image(overlay_path, width=2 * inch, height=2 * inch)
        img.hAlign = "CENTER"
        image_row.append(img)
        caption_row.append("Overlay")

    image_table = Table(
        [
            image_row,
            caption_row,
        ],
        colWidths=[2.1 * inch] * len(image_row),
    )

    image_table.setStyle(
        TableStyle(
            [
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )

    elements.append(image_table)

    elements.append(Spacer(1, 0.35 * inch))

    # =====================================================
    # INTERPRETATION
    # =====================================================

    elements.append(
        Paragraph(
            "<b>Grad-CAM Interpretation</b>",
            heading_style,
        )
    )

    explanation = """
    Grad-CAM highlights the image regions that contributed most to the CNN's prediction.
    Warmer colors (yellow/red) indicate regions that strongly influenced the decision,
    while cooler colors (blue/purple) contributed less. This visualization improves
    transparency by showing where the model focused before classifying the image.
    """

    elements.append(
        Paragraph(
            explanation,
            body_style,
        )
    )

    elements.append(Spacer(1, 0.40 * inch))

    # =====================================================
    # FOOTER
    # =====================================================

    elements.append(
        Paragraph(
            f"<b>Generated on:</b> {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}",
            body_style,
        )
    )

    elements.append(
        Paragraph(
            "© 2026 DeepShield AI",
            body_style,
        )
    )

    # =====================================================

    doc.build(
        elements,
        onFirstPage=add_watermark,
        onLaterPages=add_watermark,
    )

    buffer.seek(0)

    return buffer