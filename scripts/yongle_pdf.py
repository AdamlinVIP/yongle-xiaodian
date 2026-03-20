#!/usr/bin/env python3
"""
永乐大典风格 PDF 生成器
将 Markdown 词条转换为古籍风格的 PDF 图片
"""

import markdown
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
import re
import sys
import os

def register_fonts():
    """注册中文字体"""
    # 尝试注册常见中文字体
    font_paths = [
        # Google Noto CJK (CentOS/RHEL 9)
        '/usr/share/fonts/google-noto-cjk/NotoSansCJK-Regular.ttc',
        # Linux 系统字体
        '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',
        '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',
        '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
        '/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc',
        # macOS 字体
        '/System/Library/Fonts/PingFang.ttc',
        '/System/Library/Fonts/STHeiti Light.ttc',
        # Windows 字体 (WSL)
        '/mnt/c/Windows/Fonts/simhei.ttf',
        '/mnt/c/Windows/Fonts/simsun.ttc',
    ]
    
    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                pdfmetrics.registerFont(TTFont('ChineseFont', font_path))
                print(f"已注册字体: {font_path}")
                return 'ChineseFont'
            except Exception as e:
                print(f"字体注册失败 {font_path}: {e}")
                continue
    
    raise RuntimeError("未找到可用的中文字体，请安装 wqy-zenhei 或 Noto Sans CJK")

def parse_markdown(md_content):
    """解析 Markdown 内容"""
    lines = md_content.split('\n')
    sections = []
    current_section = {'title': '', 'content': []}
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # 标题
        if line.startswith('# '):
            if current_section['content']:
                sections.append(current_section)
            current_section = {'title': line[2:], 'content': [], 'level': 1}
        elif line.startswith('## '):
            if current_section['content']:
                sections.append(current_section)
            current_section = {'title': line[3:], 'content': [], 'level': 2}
        elif line.startswith('### '):
            current_section['content'].append({'type': 'h3', 'text': line[4:]})
        elif line.startswith('**') and line.endswith('**'):
            # 粗体作为小标题
            current_section['content'].append({'type': 'bold', 'text': line[2:-2]})
        elif line.startswith('- '):
            # 列表项
            current_section['content'].append({'type': 'list', 'text': line[2:]})
        elif line.startswith('> '):
            # 引用
            current_section['content'].append({'type': 'quote', 'text': line[2:]})
        elif line == '---':
            # 分隔线
            current_section['content'].append({'type': 'hr'})
        else:
            # 普通段落
            current_section['content'].append({'type': 'p', 'text': line})
    
    if current_section['content'] or current_section['title']:
        sections.append(current_section)
    
    return sections

def create_pdf(input_file, output_file):
    """创建永乐大典风格的 PDF"""
    
    # 注册字体
    chinese_font = register_fonts()
    
    # 读取 Markdown 文件
    with open(input_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # 解析内容
    sections = parse_markdown(md_content)
    
    # 创建 PDF
    doc = SimpleDocTemplate(
        output_file,
        pagesize=A4,
        rightMargin=2.5*cm,
        leftMargin=2.5*cm,
        topMargin=2.5*cm,
        bottomMargin=2.5*cm
    )
    
    # 定义样式
    styles = getSampleStyleSheet()
    
    # 永乐大典风格样式
    title_style = ParagraphStyle(
        'YongleTitle',
        parent=styles['Heading1'],
        fontName=chinese_font,
        fontSize=28,
        leading=36,
        alignment=TA_CENTER,
        spaceAfter=30,
        textColor=colors.HexColor('#8B0000'),  # 深红色
    )
    
    subtitle_style = ParagraphStyle(
        'YongleSubtitle',
        parent=styles['Heading2'],
        fontName=chinese_font,
        fontSize=16,
        leading=24,
        alignment=TA_CENTER,
        spaceAfter=20,
        textColor=colors.HexColor('#4A4A4A'),
    )
    
    section_title_style = ParagraphStyle(
        'YongleSection',
        parent=styles['Heading2'],
        fontName=chinese_font,
        fontSize=18,
        leading=26,
        alignment=TA_LEFT,
        spaceAfter=12,
        spaceBefore=20,
        textColor=colors.HexColor('#2F4F4F'),
        borderWidth=0,
        borderColor=colors.HexColor('#8B0000'),
        borderPadding=5,
    )
    
    body_style = ParagraphStyle(
        'YongleBody',
        parent=styles['Normal'],
        fontName=chinese_font,
        fontSize=12,
        leading=22,
        alignment=TA_JUSTIFY,
        spaceAfter=10,
        firstLineIndent=24,  # 首行缩进
    )
    
    bold_style = ParagraphStyle(
        'YongleBold',
        parent=styles['Normal'],
        fontName=chinese_font,
        fontSize=12,
        leading=22,
        alignment=TA_LEFT,
        spaceAfter=6,
        textColor=colors.HexColor('#8B0000'),
    )
    
    list_style = ParagraphStyle(
        'YongleList',
        parent=styles['Normal'],
        fontName=chinese_font,
        fontSize=11,
        leading=20,
        alignment=TA_LEFT,
        spaceAfter=6,
        leftIndent=20,
    )
    
    quote_style = ParagraphStyle(
        'YongleQuote',
        parent=styles['Normal'],
        fontName=chinese_font,
        fontSize=11,
        leading=20,
        alignment=TA_LEFT,
        spaceAfter=10,
        leftIndent=30,
        textColor=colors.HexColor('#666666'),
        fontStyle='italic',
    )
    
    footer_style = ParagraphStyle(
        'YongleFooter',
        parent=styles['Normal'],
        fontName=chinese_font,
        fontSize=10,
        leading=16,
        alignment=TA_CENTER,
        spaceBefore=30,
        textColor=colors.HexColor('#888888'),
    )
    
    # 构建文档内容
    story = []
    
    # 添加边框装饰
    def add_decorative_border():
        """添加装饰性边框"""
        border_data = [['']]
        border_table = Table(border_data, colWidths=[16*cm], rowHeights=[0.5*cm])
        border_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LINEBELOW', (0, 0), (-1, -1), 2, colors.HexColor('#8B0000')),
        ]))
        return border_table
    
    # 顶部装饰线
    story.append(add_decorative_border())
    story.append(Spacer(1, 0.5*cm))
    
    # 处理各个部分
    for i, section in enumerate(sections):
        if section['level'] == 1:
            # 主标题
            story.append(Paragraph(section['title'], title_style))
        elif section['level'] == 2:
            # 章节标题
            story.append(Paragraph(section['title'], section_title_style))
        
        # 处理内容
        for item in section['content']:
            if item['type'] == 'p':
                story.append(Paragraph(item['text'], body_style))
            elif item['type'] == 'h3':
                story.append(Paragraph(item['text'], section_title_style))
            elif item['type'] == 'bold':
                story.append(Paragraph(f"【{item['text']}】", bold_style))
            elif item['type'] == 'list':
                story.append(Paragraph(f"• {item['text']}", list_style))
            elif item['type'] == 'quote':
                story.append(Paragraph(item['text'], quote_style))
            elif item['type'] == 'hr':
                story.append(Spacer(1, 0.3*cm))
    
    # 底部装饰线
    story.append(Spacer(1, 1*cm))
    story.add(add_decorative_border())
    
    # 页脚
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph("永乐小典 · 一东 · 互联网", footer_style))
    story.append(Paragraph("解缙奉敕编纂 · 公元二〇〇〇年后之新学", footer_style))
    
    # 生成 PDF
    doc.build(story)
    print(f"PDF 已生成: {output_file}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python yongle_pdf.py <input.md> [output.pdf]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    if len(sys.argv) >= 3:
        output_file = sys.argv[2]
    else:
        output_file = input_file.replace('.md', '.pdf')
    
    create_pdf(input_file, output_file)
