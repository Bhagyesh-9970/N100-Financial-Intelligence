from __future__ import annotations

from pathlib import Path
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.enums import TA_CENTER


class TearsheetReport:
    def __init__(self, output_dir=None):
        self.output_dir = Path(output_dir or "reports/tearsheets")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def build(self, company_row, company_metrics, output_path=None):
        output_path = Path(output_path or self.output_dir / f"{company_row['company_id']}.pdf")
        doc = SimpleDocTemplate(str(output_path), pagesize=letter)
        story = []
        title_style = ParagraphStyle(name="Title", fontName="Helvetica-Bold", fontSize=18, textColor=colors.HexColor("#0f2b5b"), alignment=TA_CENTER)
        story.append(Paragraph(company_row.get("company_name", company_row.get("company_id", "Company")), title_style))
        story.append(Spacer(1, 0.1 * inch))
        table_data = [["Revenue", "Net Profit"], [company_metrics.get("sales", ""), company_metrics.get("net_profit", "")]]
        table = Table(table_data, repeatRows=1)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f2b5b")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("WORDWRAP", (0, 0), (-1, -1), True),
        ]))
        story.append(table)
        story.append(Spacer(1, 0.15 * inch))
        story.append(Paragraph("Pros", ParagraphStyle(name="Heading", fontName="Helvetica-Bold", fontSize=12, textColor=colors.green)))
        story.append(Paragraph("- Stable cash generation", ParagraphStyle(name="Body", fontSize=10)))
        story.append(Paragraph("Cons", ParagraphStyle(name="Heading", fontName="Helvetica-Bold", fontSize=12, textColor=colors.red)))
        story.append(Paragraph("- Monitor leverage", ParagraphStyle(name="Body", fontSize=10)))
        story.append(PageBreak())
        story.append(Paragraph("Balance Sheet", ParagraphStyle(name="Heading", fontName="Helvetica-Bold", fontSize=12)))
        story.append(Paragraph("Capital Allocation: Reinvestor", ParagraphStyle(name="Body", fontSize=10)))
        doc.build(story)
        return output_path

    def build_batch(self, companies_df, metrics_df, output_dir=None):
        output_dir = Path(output_dir or self.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        outputs = []
        for _, row in companies_df.iterrows():
            company_id = row.get("company_id")
            company_metrics = metrics_df[metrics_df["company_id"] == company_id]
            metrics_row = company_metrics.iloc[0] if not company_metrics.empty else None
            metrics_payload = metrics_row.to_dict() if metrics_row is not None else {}
            output_path = self.build(row.to_dict(), metrics_payload, output_dir / f"{company_id}.pdf")
            outputs.append(output_path)
        return outputs
