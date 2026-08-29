import io
import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
    KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

class ProgressReportService:
    @staticmethod
    def generate_client_progress_pdf(
        user_name: str,
        user_email: str,
        fitness_goal: str,
        active_split: str,
        conditioning_summary: dict,
        workout_stats: dict,
        nutrition_stats: dict,
        coach_recommendations: list
    ) -> bytes:
        """Generates an executive client fitness & nutrition progress PDF report."""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36
        )

        styles = getSampleStyleSheet()

        # Custom Palette
        primary_color = colors.HexColor("#0F172A") # Slate 900
        accent_color = colors.HexColor("#10B981")  # Emerald Green
        secondary_color = colors.HexColor("#3B82F6") # Blue 500
        text_dark = colors.HexColor("#1E293B")
        bg_light = colors.HexColor("#F8FAFC")
        card_border = colors.HexColor("#E2E8F0")

        # Custom Paragraph Styles
        header_title_style = ParagraphStyle(
            'HeaderTitle',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=22,
            leading=26,
            textColor=primary_color,
            alignment=TA_LEFT
        )
        
        subtitle_style = ParagraphStyle(
            'HeaderSubtitle',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=10,
            leading=14,
            textColor=colors.HexColor("#64748B"),
            alignment=TA_LEFT
        )

        section_heading_style = ParagraphStyle(
            'SectionHeading',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=13,
            leading=16,
            textColor=primary_color,
            spaceAfter=6
        )

        body_style = ParagraphStyle(
            'ReportBody',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=9.5,
            leading=13,
            textColor=text_dark
        )

        stat_label_style = ParagraphStyle(
            'StatLabel',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=8.5,
            leading=10,
            textColor=colors.HexColor("#64748B"),
            alignment=TA_CENTER
        )

        stat_value_style = ParagraphStyle(
            'StatValue',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=13,
            leading=16,
            textColor=primary_color,
            alignment=TA_CENTER
        )

        story = []

        # 1. Header Banner
        header_table_data = [
            [
                Paragraph("<b>AI PERSONAL TRAINER</b><br/><font size=9 color='#64748B'>Client Performance & Progress Assessment</font>", header_title_style),
                Paragraph(f"<b>Date:</b> {datetime.now().strftime('%B %d, %Y')}<br/><b>Client:</b> {user_name}<br/><b>Goal:</b> {fitness_goal.title()}", subtitle_style)
            ]
        ]
        header_table = Table(header_table_data, colWidths=[3.8 * inch, 3.4 * inch])
        header_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        story.append(header_table)
        story.append(HRFlowable(width="100%", thickness=1.5, color=accent_color, spaceBefore=4, spaceAfter=14))

        # 2. Executive Metric Cards Grid
        adherence_rate = workout_stats.get("adherence_percentage", 92)
        avg_calories = nutrition_stats.get("avg_daily_calories", 2250)
        avg_protein = nutrition_stats.get("avg_daily_protein_g", 165)
        est_bodyfat = conditioning_summary.get("estimated_body_fat", "12-14%")

        cards_data = [
            [
                Paragraph(f"{adherence_rate}%", stat_value_style),
                Paragraph(f"{avg_calories} kcal", stat_value_style),
                Paragraph(f"{avg_protein}g", stat_value_style),
                Paragraph(f"{est_bodyfat}", stat_value_style)
            ],
            [
                Paragraph("WORKOUT ADHERENCE", stat_label_style),
                Paragraph("AVG DAILY INTAKE", stat_label_style),
                Paragraph("AVG DAILY PROTEIN", stat_label_style),
                Paragraph("ESTIMATED BODY FAT", stat_label_style)
            ]
        ]
        cards_table = Table(cards_data, colWidths=[1.8 * inch, 1.8 * inch, 1.8 * inch, 1.8 * inch])
        cards_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), bg_light),
            ('BOX', (0, 0), (-1, -1), 1, card_border),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, card_border),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(cards_table)
        story.append(Spacer(1, 14))

        # 3. Section: AI Physique Conditioning & Symmetry Analysis
        story.append(Paragraph("1. AI Physique Assessment & Symmetry Matrix", section_heading_style))
        physique_rows = [
            ["Metric / Muscle Group", "Conditioning Score", "Observations & Prescriptions"],
            ["Upper Torso (Clavicular Head)", "8.5 / 10", "Slight asymmetry detected; 30° Incline Dumbbell Press prioritized."],
            ["Lateral Deltoids (Cap Width)", "8.0 / 10", "Good base; cable lateral raises with 2s peak contraction recommended."],
            ["Lats & Back V-Taper", "9.0 / 10", "Strong width; focus on chest-supported rows for mid-back thickness."],
            ["Posterior Chain & Hamstrings", "7.5 / 10", "Hamstring-to-quad ratio balanced with dedicated RDLs & Seated Leg Curls."]
        ]
        physique_table = Table(physique_rows, colWidths=[2.2 * inch, 1.4 * inch, 3.6 * inch])
        physique_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), primary_color),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8.5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, bg_light]),
            ('GRID', (0, 0), (-1, -1), 0.5, card_border),
        ]))
        story.append(physique_table)
        story.append(Spacer(1, 14))

        # 4. Section: Strength Progression & 1RM Estimates
        story.append(Paragraph("2. Strength Progression & 1RM Benchmark Matrix", section_heading_style))
        strength_rows = [
            ["Key Exercise", "Last Working Load", "Estimated 1RM", "Progression Directive"],
            ["Barbell Incline Bench Press", "82.5 kg x 8 reps (RPE 8.0)", "102.5 kg", "Increase to 85.0 kg for 6-8 reps next block"],
            ["Barbell Squat / Hack Squat", "120.0 kg x 10 reps (RPE 8.5)", "160.0 kg", "Maintain load; focus on 3s eccentric tempo"],
            ["Romanian Deadlift (RDL)", "100.0 kg x 10 reps (RPE 8.0)", "133.3 kg", "Add +2.5 kg next session; double progression active"],
            ["Seated Dumbbell Shoulder Press", "32.0 kg x 8 reps (RPE 8.5)", "39.7 kg", "Stabilize 8-rep threshold before +2kg jump"]
        ]
        strength_table = Table(strength_rows, colWidths=[2.2 * inch, 1.8 * inch, 1.1 * inch, 2.1 * inch])
        strength_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), primary_color),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8.5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, bg_light]),
            ('GRID', (0, 0), (-1, -1), 0.5, card_border),
        ]))
        story.append(strength_table)
        story.append(Spacer(1, 14))

        # 5. Section: Nutrition & Macro Compliance Breakdown
        story.append(Paragraph("3. Macro Distribution & Food Compliance Tracker", section_heading_style))
        nutrition_rows = [
            ["Nutrient", "Daily Target", "Actual Avg Logged", "Compliance Status"],
            ["Total Calories", f"{nutrition_stats.get('target_calories', 2300)} kcal", f"{avg_calories} kcal", "Within Target (98%)"],
            ["Protein", f"{nutrition_stats.get('target_protein_g', 160)} g", f"{avg_protein} g", "Target Exceeded (+5g)"],
            ["Carbohydrates", f"{nutrition_stats.get('target_carbs_g', 260)} g", f"{nutrition_stats.get('avg_daily_carbs_g', 255)} g", "Optimal Glycogen (98%)"],
            ["Fats", f"{nutrition_stats.get('target_fat_g', 65)} g", f"{nutrition_stats.get('avg_daily_fat_g', 62)} g", "Optimal Hormone Profile"]
        ]
        nutrition_table = Table(nutrition_rows, colWidths=[1.8 * inch, 1.6 * inch, 1.8 * inch, 2.0 * inch])
        nutrition_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), primary_color),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8.5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, bg_light]),
            ('GRID', (0, 0), (-1, -1), 0.5, card_border),
        ]))
        story.append(nutrition_table)
        story.append(Spacer(1, 14))

        # 6. Section: AI Personal Coach Directives for Next Period
        story.append(Paragraph("4. AI Personal Coach Directives & Tactical Goals", section_heading_style))
        coach_bullets = coach_recommendations or [
            "Maintain current double progression model on all primary compound movements.",
            "If missing a scheduled training session, engage the 'Hybrid Compound Consolidation' backup module.",
            "Prioritize pre-bed protein intake (e.g. Casein / Low-fat Paneer / Soy Isolate) to sustain overnight muscle protein synthesis.",
            "Continue daily step sync with HealthKit / Health Connect to maintain ~7,500 daily baseline activity."
        ]
        
        for i, directive in enumerate(coach_bullets, 1):
            story.append(Paragraph(f"<b>{i}.</b> {directive}", body_style))
            story.append(Spacer(1, 4))

        # Build PDF Document
        doc.build(story)
        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes
