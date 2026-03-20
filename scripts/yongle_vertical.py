#!/usr/bin/env python3
"""
永乐大典风格竖版图片生成器
将 Markdown 词条转换为竖版古籍风格的 PNG 图片
从右至左，从上至下阅读
"""

from PIL import Image, ImageDraw, ImageFont
import sys
import os

def get_font(size, style='serif'):
    """获取中文字体 - 使用宋体(Serif)模拟古籍风格"""
    if style == 'title':
        # 标题用粗体宋体
        font_paths = [
            '/usr/share/fonts/google-noto-cjk/NotoSerifCJK-Bold.ttc',
            '/usr/share/fonts/google-noto-cjk/NotoSerifCJK-Regular.ttc',
        ]
    elif style == 'body':
        # 正文用常规宋体
        font_paths = [
            '/usr/share/fonts/google-noto-cjk/NotoSerifCJK-Regular.ttc',
            '/usr/share/fonts/google-noto-cjk/NotoSerifCJK-Light.ttc',
        ]
    else:
        font_paths = [
            '/usr/share/fonts/google-noto-cjk/NotoSerifCJK-Regular.ttc',
            '/usr/share/fonts/google-noto-cjk/NotoSansCJK-Regular.ttc',
            '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',
        ]
    
    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                return ImageFont.truetype(font_path, size)
            except:
                continue
    
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

def draw_vertical_text(draw, text, x, y, font, fill, line_height=30):
    """绘制竖排文字（从上至下）"""
    for char in text:
        draw.text((x, y), char, font=font, fill=fill)
        bbox = font.getbbox(char)
        char_height = (bbox[3] - bbox[1]) if bbox else line_height
        y += char_height + 4
    return y

def get_text_height(text, font):
    """计算文字高度"""
    total_height = 0
    for char in text:
        bbox = font.getbbox(char)
        char_height = (bbox[3] - bbox[1]) if bbox else 20
        total_height += char_height + 4
    return total_height

def create_yongle_vertical_image(input_file, output_file):
    """创建永乐大典竖版风格的图片"""
    
    # 读取 Markdown
    with open(input_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    sections = parse_markdown(md_content)
    
    # 图片尺寸 - 竖版古籍（宽>高，横向排列多列）
    width = 2400
    height = 1600
    
    # 创建图片（米黄色古籍纸张背景）
    img = Image.new('RGB', (width, height), color='#F5F0E1')
    draw = ImageDraw.Draw(img)
    
    # 加载字体 - 使用宋体模拟古籍
    title_font = get_font(48, 'title')      # 标题大字
    subtitle_font = get_font(28, 'body')
    section_font = get_font(26, 'title')    # 章节标题稍粗
    body_font = get_font(22, 'body')        # 正文宋体
    small_font = get_font(16, 'body')
    
    # 边距
    margin_x = 100
    margin_y = 80
    
    # 列宽（每列竖排文字的宽度）
    col_width = 36
    col_gap = 50
    
    # 从右至左排列，从最右边开始
    current_x = width - margin_x - col_width
    current_y = margin_y + 50
    
    # 绘制装饰边框
    border_color = '#8B0000'
    
    # 外边框
    draw.rectangle(
        [(margin_x-30, margin_y-30), (width-margin_x+30, height-margin_y+30)],
        outline=border_color, width=4
    )
    
    # 内边框
    draw.rectangle(
        [(margin_x-15, margin_y-15), (width-margin_x+15, height-margin_y+15)],
        outline=border_color, width=2
    )
    
    # 顶部装饰线
    draw.line([(margin_x, margin_y+10), (width-margin_x, margin_y+10)], 
              fill=border_color, width=3)
    
    # 底部装饰线
    draw.line([(margin_x, height-margin_y-10), (width-margin_x, height-margin_y-10)], 
              fill=border_color, width=3)
    
    # 书根标签（右下角）
    label_text = "一東"
    label_x = width - margin_x - 60
    label_y = height - margin_y + 5
    draw.text((label_x, label_y), label_text, font=section_font, fill=border_color)
    
    # 处理内容 - 从最右边开始，向左排列
    for section in sections:
        if section['level'] == 1:
            # 主标题 - 在最右侧作为大标题
            title = section['title']
            # 标题竖排
            title_y = margin_y + 60
            for char in title:
                draw.text((current_x, title_y), char, font=title_font, fill='#8B0000')
                bbox = title_font.getbbox(char)
                title_y += (bbox[3] - bbox[1]) + 8 if bbox else 50
            
            # 标题后加间距
            current_x -= col_width + col_gap
            current_y = margin_y + 50
            
        elif section['level'] == 2:
            # 章节标题
            if current_y > margin_y + 200:
                # 换列
                current_x -= col_width + col_gap
                current_y = margin_y + 50
            
            # 检查是否超出左边界
            if current_x < margin_x + col_width:
                break
            
            title = f"【{section['title']}】"
            title_y = current_y
            for char in title:
                draw.text((current_x, title_y), char, font=section_font, fill='#2F4F4F')
                bbox = section_font.getbbox(char)
                title_y += (bbox[3] - bbox[1]) + 6 if bbox else 30
            
            current_y = title_y + 20
        
        # 处理内容
        for item in section['content']:
            # 检查是否需要换列
            if current_y > height - margin_y - 100:
                current_x -= col_width + col_gap
                current_y = margin_y + 50
                
                if current_x < margin_x + col_width:
                    break
            
            if item['type'] == 'p':
                text = item['text']
                text_y = current_y
                for char in text:
                    draw.text((current_x, text_y), char, font=body_font, fill='#000000')
                    bbox = body_font.getbbox(char)
                    text_y += (bbox[3] - bbox[1]) + 4 if bbox else 24
                    
                    # 检查是否到列底
                    if text_y > height - margin_y - 60:
                        current_x -= col_width + col_gap
                        text_y = margin_y + 50
                        if current_x < margin_x + col_width:
                            break
                
                current_y = text_y + 15
                
            elif item['type'] == 'h3':
                text_y = current_y
                for char in item['text']:
                    draw.text((current_x, text_y), char, font=section_font, fill='#2F4F4F')
                    bbox = section_font.getbbox(char)
                    text_y += (bbox[3] - bbox[1]) + 4 if bbox else 28
                current_y = text_y + 15
                
            elif item['type'] == 'bold':
                text_y = current_y
                text = f"【{item['text']}】"
                for char in text:
                    draw.text((current_x, text_y), char, font=body_font, fill='#8B0000')
                    bbox = body_font.getbbox(char)
                    text_y += (bbox[3] - bbox[1]) + 4 if bbox else 24
                current_y = text_y + 10
                
            elif item['type'] == 'list':
                text_y = current_y
                text = f"·{item['text']}"
                for char in text:
                    draw.text((current_x, text_y), char, font=body_font, fill='#000000')
                    bbox = body_font.getbbox(char)
                    text_y += (bbox[3] - bbox[1]) + 4 if bbox else 24
                    
                    if text_y > height - margin_y - 60:
                        current_x -= col_width + col_gap
                        text_y = margin_y + 50
                        if current_x < margin_x + col_width:
                            break
                current_y = text_y + 10
                
            elif item['type'] == 'quote':
                text_y = current_y
                text = f"「{item['text']}」"
                for char in text:
                    draw.text((current_x, text_y), char, font=small_font, fill='#666666')
                    bbox = small_font.getbbox(char)
                    text_y += (bbox[3] - bbox[1]) + 3 if bbox else 20
                    
                    if text_y > height - margin_y - 60:
                        current_x -= col_width + col_gap
                        text_y = margin_y + 50
                        if current_x < margin_x + col_width:
                            break
                current_y = text_y + 10
                
            elif item['type'] == 'hr':
                current_y += 20
        
        if current_x < margin_x + col_width:
            break
    
    # 页脚 - 左下角
    footer_text = "永乐小典·解缙奉敕编纂"
    footer_x = margin_x + 20
    footer_y = height - margin_y + 5
    draw.text((footer_x, footer_y), footer_text, font=small_font, fill='#888888')
    
    # 保存图片
    img.save(output_file, 'PNG', quality=95)
    print(f"竖版图片已生成: {output_file}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python yongle_vertical.py <input.md> [output.png]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    if len(sys.argv) >= 3:
        output_file = sys.argv[2]
    else:
        output_file = input_file.replace('.md', '.png')
    
    create_yongle_vertical_image(input_file, output_file)
