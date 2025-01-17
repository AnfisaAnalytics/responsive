from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import plotly.io as pio
import pandas as pd
from datetime import datetime
import os

# PDF Configuration
PDF_STYLES = {
    # Размеры шрифтов - базовые размеры, которые будут масштабироваться
    'fonts': {
        'title': 16,
        'subtitle': 10,
        'heading': 14,
        'table_header': 12,
        'table_body': 10,
        'metrics': 12,
    },
    
    # Размеры визуализаций
    'charts': {
        'performance': {
            'width': 650,
            'height': 325
        },
        'distribution': {
            'width': 400,
            'height': 300
        }
    },
    
    # Размеры таблиц
'tables': {
        'base_scale': 1.2,  # Здесь меняете масштаб (было 1.0)
        'metrics': {
            'col_widths': [150,150],  # Здесь меняете ширину столбцов (было [250, 250])
            'min_height': 30,
            'padding': 12,
            'font_scale': 1.0
        },
        'stats': {
            'col_widths': [100, 100, 100, 100],  # Здесь можете изменить ширину столбцов статистики
            'min_height': 25,
            'padding': 12,
            'font_scale': 1.0
        }
    },
    
    'spacing': {
        'after_title': 30,
        'after_heading': 12,
        'between_sections': 20
    },
    
    'colors': {
        'table_header': colors.grey,
        'table_header_text': colors.whitesmoke,
        'table_text': colors.black,
        'grid': colors.black
    }
}

# Регистрируем шрифт DejaVuSans
pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf'))

def create_paragraph_cell(text, style):
    """Создает ячейку с автоматическим переносом текста"""
    return Paragraph(str(text), style)

def create_table_with_autosize(data, col_widths, table_style, min_height=30, base_scale=1.0):
    """Создает таблицу с автоматическим масштабированием"""
    # Создаем стиль для ячеек с переносом текста
    styles = getSampleStyleSheet()
    cell_style = ParagraphStyle(
        'CellStyle',
        parent=styles['Normal'],
        fontName='DejaVuSans',
        fontSize=PDF_STYLES['fonts']['table_body'] * base_scale,
        leading=PDF_STYLES['fonts']['table_body'] * base_scale * 1.2,
        wordWrap='CJK'  # Обеспечивает перенос слов
    )

    # Преобразуем все ячейки в Paragraph для автоматического переноса
    formatted_data = [
        [create_paragraph_cell(cell, cell_style) for cell in row]
        for row in data
    ]

    # Создаем таблицу с указанными размерами
    scaled_widths = [width * base_scale for width in col_widths]
    table = Table(
        formatted_data,
        colWidths=scaled_widths,
        rowHeights=None  # Автоматическая высота строк
    )
    
    # Применяем стили
    table.setStyle(table_style)
    
    return table

def generate_pdf_report(df, operator_stats, performance_fig, distribution_fig, start_date, end_date):
    if not os.path.exists('temp'):
        os.makedirs('temp')
    
    performance_fig.write_image(
        "temp/performance.png",
        width=PDF_STYLES['charts']['performance']['width'],
        height=PDF_STYLES['charts']['performance']['height']
    )
    distribution_fig.write_image(
        "temp/distribution.png",
        width=PDF_STYLES['charts']['distribution']['width'],
        height=PDF_STYLES['charts']['distribution']['height']
    )
    
    doc = SimpleDocTemplate(
        f"temp/service_support_report_{start_date}_{end_date}.pdf",
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=PDF_STYLES['fonts']['title'],
        fontName='DejaVuSans',
        spaceAfter=PDF_STYLES['spacing']['after_title']
    )
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=PDF_STYLES['fonts']['heading'],
        fontName='DejaVuSans',
        spaceAfter=PDF_STYLES['spacing']['after_heading']
    )
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontName='DejaVuSans',
        fontSize=PDF_STYLES['fonts']['subtitle']
    )
    
    content = []
    
    # Title
    content.append(Paragraph("Анализ эффективности работы сервиса поддержки", title_style))
    content.append(Paragraph(f"Период: {start_date} - {end_date}", normal_style))
    content.append(Spacer(1, PDF_STYLES['spacing']['between_sections']))
    
    # Key Metrics
    content.append(Paragraph("Ключевые показатели", heading_style))
    avg_response = df['avg_response_minutes'].mean()
    avg_sla = df['sla_percentage'].mean()
    total_responses = df['total_responses'].sum()
    
    metrics_data = [
        ["Среднее время ответа", f"{avg_response:.1f} мин"],
        ["SLA", f"{avg_sla:.1f}%"],
        ["Всего обращений", f"{total_responses:,}"]
    ]
    
    metrics_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, -1), PDF_STYLES['colors']['table_text']),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'DejaVuSans'),
        ('GRID', (0, 0), (-1, -1), 1, PDF_STYLES['colors']['grid']),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ])
    
    metrics_table = create_table_with_autosize(
        metrics_data,
        PDF_STYLES['tables']['metrics']['col_widths'],
        metrics_style,
        PDF_STYLES['tables']['metrics']['min_height'],
        PDF_STYLES['tables']['base_scale']
    )
    content.append(metrics_table)
    
    # Performance Chart
    content.append(Paragraph("Показатели эффективности операторов", heading_style))
    content.append(Image(
        "temp/performance.png",
        width=PDF_STYLES['charts']['performance']['width'],
        height=PDF_STYLES['charts']['performance']['height']
    ))
    content.append(PageBreak())
    
    # Distribution Chart
    content.append(Paragraph("Распределение времени ответа", heading_style))
    content.append(Image(
        "temp/distribution.png",
        width=PDF_STYLES['charts']['distribution']['width'],
        height=PDF_STYLES['charts']['distribution']['height']
    ))
    content.append(PageBreak())
    
    # Operator Statistics
    content.append(Paragraph("Статистика по операторам", heading_style))
    stats_data = [operator_stats.columns.tolist()] + operator_stats.values.tolist()
    
    stats_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PDF_STYLES['colors']['table_header']),
        ('TEXTCOLOR', (0, 0), (-1, 0), PDF_STYLES['colors']['table_header_text']),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'DejaVuSans'),
        ('GRID', (0, 0), (-1, -1), 1, PDF_STYLES['colors']['grid']),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ])
    
    stats_table = create_table_with_autosize(
        stats_data,
        PDF_STYLES['tables']['stats']['col_widths'],
        stats_style,
        PDF_STYLES['tables']['stats']['min_height'],
        PDF_STYLES['tables']['base_scale']
    )
    content.append(stats_table)
    
    # Build PDF
    doc.build(content)
    
    # Read the generated PDF
    with open(doc.filename, 'rb') as f:
        pdf_data = f.read()
    
    # Cleanup temp files
    os.remove("temp/performance.png")
    os.remove("temp/distribution.png")
    os.remove(doc.filename)

    
    return pdf_data
