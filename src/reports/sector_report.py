from __future__ import annotations

from pathlib import Path
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


class SectorReport:
    def __init__(self, output_dir=None):
        self.output_dir = Path(output_dir or "reports/sector")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def build(self, sector_name, companies_df, output_path=None):
        output_path = Path(output_path or self.output_dir / f"{sector_name}.pdf")
        doc = SimpleDocTemplate(str(output_path), pagesize=letter)
        story = []
        title_style = ParagraphStyle(name="Title", fontName="Helvetica-Bold", fontSize=16, textColor=colors.HexColor("#0f2b5b"))
        story.append(Paragraph(sector_name, title_style))
        story.append(Spacer(1, 0.15 * inch))
        if not companies_df.empty:
            table_data = [["Company", "Ticker", "Sector"]]
            for _, row in companies_df.iterrows():
                table_data.append([row.get("company_name", ""), row.get("company_id", ""), row.get("sector", "")])
            table = Table(table_data, repeatRows=1)
            table.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.5, colors.grey), ("WORDWRAP", (0, 0), (-1, -1), True)]))
            story.append(table)
        doc.build(story)
        return output_path
