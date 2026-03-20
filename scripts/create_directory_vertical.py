#!/usr/bin/env python3
"""
永乐小典目录 - 竖版影印本风格
模仿《永乐大典》真本竖版版式
从右至左，从上至下
"""

from PIL import Image, ImageDraw, ImageFont
import sys
import os
import random

def get_font(size, style='regular'):
    """获取中文字体 - 使用宋体模拟古籍"""
    if style == 'title':
        font_paths = [
            '/usr/share/fonts/google-noto-cjk/NotoSerifCJK-Bold.ttc',
        ]
    elif style == 'large':
        font_paths = [
            '/usr/share/fonts/google-noto-cjk/NotoSerifCJK-Bold.ttc',
        ]
    else:
        font_paths = [
            '/usr/share/fonts/google-noto-cjk/NotoSerifCJK-Regular.ttc',
        ]
    
    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                return ImageFont.truetype(font_path, size)
            except:
                continue
    
    return ImageFont.load_default()

def draw_vertical_text(draw, text, x, y, font, fill, spacing=4):
    """绘制竖排文字（从上至下）"""
    for char in text:
        draw.text((x, y), char, font=font, fill=fill)
        bbox = font.getbbox(char)
        char_height = (bbox[3] - bbox[1]) if bbox else 20
        y += char_height + spacing
    return y

def create_vertical_directory(output_file):
    """创建竖版目录影印本"""
    
    # 图片尺寸 - 古籍开本（宽>高，横向排列多列）
    width = 2400
    height = 1600
    
    # 创建图片（米黄色古籍纸张）
    img = Image.new('RGB', (width, height), color='#E8E0D0')
    draw = ImageDraw.Draw(img)
    
    # 添加纸张纹理
    for _ in range(3000):
        x = random.randint(0, width-1)
        y = random.randint(0, height-1)
        offset = random.randint(-8, 8)
        base_color = (232 + offset, 224 + offset, 208 + offset)
        draw.point((x, y), fill=base_color)
    
    # 加载字体
    title_font = get_font(56, 'large')      # 大标题
    subtitle_font = get_font(32, 'title')   # 副标题
    section_font = get_font(26, 'title')    # 章节标题
    body_font = get_font(20, 'regular')     # 正文
    small_font = get_font(16, 'regular')    # 小字
    
    # 边距
    margin_x = 100
    margin_y = 80
    
    # 列宽
    col_width = 32
    col_gap = 45
    
    # 边框颜色
    border_color = '#4A0000'
    
    # 绘制边框 - 双线框
    draw.rectangle(
        [(margin_x-30, margin_y-30), (width-margin_x+30, height-margin_y+30)],
        outline=border_color, width=3
    )
    draw.rectangle(
        [(margin_x-15, margin_y-15), (width-margin_x+15, height-margin_y+15)],
        outline=border_color, width=1
    )
    
    # 书根标签（右下角）
    label_font = get_font(24, 'title')
    draw.text((width - margin_x - 50, height - margin_y + 5), "目", font=label_font, fill=border_color)
    
    # 从最右边开始
    current_x = width - margin_x - col_width
    current_y = margin_y + 40
    
    # 大标题 - 永乐小典（最右列）
    title = "永乐小典"
    title_y = current_y
    for char in title:
        draw.text((current_x, title_y), char, font=title_font, fill=border_color)
        bbox = title_font.getbbox(char)
        title_y += (bbox[3] - bbox[1]) + 10 if bbox else 60
    
    # 副标题 - 目录
    subtitle = "目录"
    subtitle_y = title_y + 20
    for char in subtitle:
        draw.text((current_x, subtitle_y), char, font=subtitle_font, fill=border_color)
        bbox = subtitle_font.getbbox(char)
        subtitle_y += (bbox[3] - bbox[1]) + 6 if bbox else 35
    
    # 分隔线（竖线）
    line_x = current_x - col_width - 20
    draw.line([(line_x, margin_y + 40), (line_x, height - margin_y - 40)], fill=border_color, width=2)
    
    # 移动到下一列
    current_x = line_x - col_gap
    current_y = margin_y + 40
    
    # 凡例
    fanli_title = "凡例"
    y = current_y
    for char in fanli_title:
        draw.text((current_x, y), char, font=section_font, fill=border_color)
        bbox = section_font.getbbox(char)
        y += (bbox[3] - bbox[1]) + 6 if bbox else 30
    
    current_x -= col_width + col_gap
    y = current_y
    
    # 凡例内容
    fanli_content = [
        "一、本典仿《永乐大典》之体例，",
        "以洪武正韵为纲，采辑公元",
        "二〇〇〇年后之新知新学。",
        "二、本典依《洪武正韵》七十",
        "六韵编排，分平声二十二韵、",
        "上声二十二韵、去声二十二韵、",
        "入声十韵。",
        "三、每韵以字系事，以事明理。",
        "四、新学名词，依声定韵。",
        "五、一词跨韵者，于各韵互见。",
    ]
    
    for text in fanli_content:
        for char in text:
            draw.text((current_x, y), char, font=body_font, fill='#2A0000')
            bbox = body_font.getbbox(char)
            y += (bbox[3] - bbox[1]) + 3 if bbox else 23
            
            if y > height - margin_y - 60:
                current_x -= col_width + col_gap
                y = current_y
                if current_x < margin_x + col_width:
                    break
        y += 10
        if current_x < margin_x + col_width:
            break
    
    # 分隔线
    current_x -= col_width
    if current_x > margin_x:
        draw.line([(current_x + col_width//2, margin_y + 40), (current_x + col_width//2, height - margin_y - 40)], fill=border_color, width=1)
    
    current_x -= col_gap
    y = current_y
    
    # 韵目总览
    if current_x > margin_x:
        yunmu_title = "韵目总览"
        for char in yunmu_title:
            draw.text((current_x, y), char, font=section_font, fill=border_color)
            bbox = section_font.getbbox(char)
            y += (bbox[3] - bbox[1]) + 6 if bbox else 30
        
        current_x -= col_width + col_gap
        y = current_y
        
        # 平声
        ping_title = "平声"
        for char in ping_title:
            draw.text((current_x, y), char, font=section_font, fill='#5A0000')
            bbox = section_font.getbbox(char)
            y += (bbox[3] - bbox[1]) + 4 if bbox else 28
        
        y += 10
        
        ping_yun = [
            "一东东同童",
            "二支支枝知",
            "三齐齐西溪",
            "四鱼鱼余居",
            "五模模谟图",
            "六皆皆街谐",
            "七灰灰回雷",
            "八真真辰人",
            "九寒寒安丹",
            "十删删山关",
            "十一先先前千",
            "十二萧萧消朝",
            "十三肴肴交郊",
            "十四豪豪高劳",
            "十五歌歌柯波",
            "十六麻麻华沙",
            "十七阳阳章昌",
            "十八庚庚更生",
            "十九青青清星",
            "二十尤尤由游",
            "二十一侵侵音心",
            "二十二覃覃谈南",
        ]
        
        for text in ping_yun:
            for char in text:
                draw.text((current_x, y), char, font=small_font, fill='#3A0000')
                bbox = small_font.getbbox(char)
                y += (bbox[3] - bbox[1]) + 2 if bbox else 18
                
                if y > height - margin_y - 60:
                    current_x -= col_width + col_gap
                    y = current_y + 40
                    if current_x < margin_x + col_width:
                        break
            if current_x < margin_x + col_width:
                break
            y += 5
    
    # 页脚
    footer = "永乐小典编修局奉敕编纂"
    footer_x = margin_x + 20
    footer_y = height - margin_y + 5
    draw.text((footer_x, footer_y), footer, font=small_font, fill='#666666')
    
    # 保存图片
    img.save(output_file, 'PNG', quality=95)
    print(f"竖版目录影印本已生成: {output_file}")

if __name__ == '__main__':
    output_file = sys.argv[1] if len(sys.argv) > 1 else '目录.png'
    create_vertical_directory(output_file)
