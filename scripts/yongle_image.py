#!/usr/bin/env python3
"""
永乐大典风格图片生成器
将 Markdown 词条转换为古籍风格的 PNG 图片
"""

from PIL import Image, ImageDraw, ImageFont
import sys
import os
import re

def get_font(size):
    """获取中文字体"""
    font_paths = [
        '/usr/share/fonts/google-noto-cjk/NotoSansCJK-Regular.ttc',
        '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',
        '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',
        '/System/Library/Fonts/PingFang.ttc',
        '/System/Library/Fonts/STHeiti Light.ttc',
        '/mnt/c/Windows/Fonts/simhei.ttf',
        '/mnt/c/Windows/Fonts/simsun.ttc',
    ]
    
    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                return ImageFont.truetype(font_path, size)
            except:
                continue
    
    # 回退到默认字体
    return ImageFont.load_default()

def parse_markdown(md_content):
    """解析 Markdown 内容"""
    lines = md_content.split('\n')
    sections = []
    current_section = {'title': '', 'content': []}
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
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
        elif line.startswith('**') and '**' in line[2:]:
            current_section['content'].append({'type': 'bold', 'text': line.replace('**', '')})
        elif line.startswith('- '):
            current_section['content'].append({'type': 'list', 'text': line[2:]})
        elif line.startswith('> '):
            current_section['content'].append({'type': 'quote', 'text': line[2:]})
        elif line == '---':
            current_section['content'].append({'type': 'hr'})
        else:
            current_section['content'].append({'type': 'p', 'text': line})
    
    if current_section['content'] or current_section['title']:
        sections.append(current_section)
    
    return sections

def wrap_text(text, font, max_width):
    """自动换行"""
    lines = []
    current_line = ""
    
    for char in text:
        test_line = current_line + char
        bbox = font.getbbox(test_line)
        if bbox and bbox[2] > max_width:
            lines.append(current_line)
            current_line = char
        else:
            current_line = test_line
    
    if current_line:
        lines.append(current_line)
    
    return lines

def create_yongle_image(input_file, output_file):
    """创建永乐大典风格的图片"""
    
    # 读取 Markdown
    with open(input_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    sections = parse_markdown(md_content)
    
    # 图片尺寸 (A4 比例，竖版古籍风格)
    width = 1200
    height = 1697  # A4 比例
    
    # 创建图片（米黄色古籍纸张背景）
    img = Image.new('RGB', (width, height), color='#F5F0E1')
    draw = ImageDraw.Draw(img)
    
    # 加载字体
    title_font = get_font(48)
    subtitle_font = get_font(28)
    section_font = get_font(24)
    body_font = get_font(18)
    small_font = get_font(14)
    
    # 边距
    margin = 80
    content_width = width - 2 * margin
    
    # 当前 Y 位置
    y = margin
    
    # 绘制装饰边框
    border_color = '#8B0000'  # 深红色
    border_width = 3
    
    # 外边框
    draw.rectangle(
        [(margin-20, margin-20), (width-margin+20, height-margin+20)],
        outline=border_color, width=border_width
    )
    
    # 内边框
    draw.rectangle(
        [(margin-10, margin-10), (width-margin+10, height-margin+10)],
        outline=border_color, width=1
    )
    
    # 处理内容
    for section in sections:
        if section['level'] == 1:
            # 主标题
            title = section['title']
            bbox = title_font.getbbox(title)
            title_width = bbox[2] - bbox[0] if bbox else 200
            x = (width - title_width) // 2
            draw.text((x, y), title, font=title_font, fill='#8B0000')
            y += 70
            
            # 分隔线
            draw.line([(margin, y), (width-margin, y)], fill=border_color, width=2)
            y += 30
            
        elif section['level'] == 2:
            # 章节标题
            if y > margin + 100:  # 不是第一个章节，添加间距
                y += 20
            
            title = f"【{section['title']}】"
            draw.text((margin, y), title, font=section_font, fill='#2F4F4F')
            y += 40
        
        # 处理内容
        for item in section['content']:
            if item['type'] == 'p':
                lines = wrap_text(item['text'], body_font, content_width)
                for line in lines:
                    draw.text((margin, y), line, font=body_font, fill='#000000')
                    y += 28
                y += 10
                
            elif item['type'] == 'h3':
                y += 10
                draw.text((margin, y), item['text'], font=section_font, fill='#2F4F4F')
                y += 35
                
            elif item['type'] == 'bold':
                y += 5
                draw.text((margin, y), f"【{item['text']}】", font=body_font, fill='#8B0000')
                y += 28
                
            elif item['type'] == 'list':
                lines = wrap_text(f"  • {item['text']}", body_font, content_width)
                for line in lines:
                    draw.text((margin, y), line, font=body_font, fill='#000000')
                    y += 26
                y += 5
                
            elif item['type'] == 'quote':
                y += 5
                lines = wrap_text(f"  「{item['text']}」", small_font, content_width - 40)
                for line in lines:
                    draw.text((margin + 20, y), line, font=small_font, fill='#666666')
                    y += 22
                y += 5
                
            elif item['type'] == 'hr':
                y += 10
                draw.line([(margin + 50, y), (width - margin - 50, y)], fill='#CCCCCC', width=1)
                y += 15
            
            # 检查是否超出页面
            if y > height - margin - 60:
                break
        
        if y > height - margin - 60:
            break
    
    # 页脚
    footer_y = height - margin - 40
    footer_text = "永乐小典 · 一东 · 互联网"
    bbox = small_font.getbbox(footer_text)
    footer_width = bbox[2] - bbox[0] if bbox else 200
    x = (width - footer_width) // 2
    draw.text((x, footer_y), footer_text, font=small_font, fill='#888888')
    
    footer2_text = "解缙奉敕编纂 · 公元二〇〇〇年后之新学"
    bbox = small_font.getbbox(footer2_text)
    footer2_width = bbox[2] - bbox[0] if bbox else 200
    x = (width - footer2_width) // 2
    draw.text((x, footer_y + 20), footer2_text, font=small_font, fill='#888888')
    
    # 保存图片
    img.save(output_file, 'PNG', quality=95)
    print(f"图片已生成: {output_file}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python yongle_image.py <input.md> [output.png]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    if len(sys.argv) >= 3:
        output_file = sys.argv[2]
    else:
        output_file = input_file.replace('.md', '.png')
    
    create_yongle_image(input_file, output_file)
