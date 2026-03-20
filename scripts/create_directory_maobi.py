#!/usr/bin/env python3
"""
永樂小典目錄 - 豎版古籍開本（大號毛筆字風格）
使用超大字號模擬毛筆字效果
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import sys
import os
import random

def get_font(size, style='regular'):
    """獲取中文字體"""
    if style == 'title':
        font_paths = ['/usr/share/fonts/google-noto-cjk/NotoSerifCJK-Bold.ttc']
    elif style == 'large':
        font_paths = ['/usr/share/fonts/google-noto-cjk/NotoSerifCJK-Bold.ttc']
    else:
        font_paths = ['/usr/share/fonts/google-noto-cjk/NotoSerifCJK-Regular.ttc']
    
    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                return ImageFont.truetype(font_path, size)
            except:
                continue
    return ImageFont.load_default()

def draw_text_with_shadow(draw, x, y, char, font, fill, shadow_color='#00000020'):
    """繪製帶陰影的文字，模擬毛筆字效果"""
    # 繪製陰影
    draw.text((x+2, y+2), char, font=font, fill=shadow_color)
    # 繪製主文字
    draw.text((x, y), char, font=font, fill=fill)

def create_vertical_directory(output_file):
    """創建豎版目錄古籍（大號字體）"""
    
    # 更大的豎頁格式
    width = 2000
    height = 3200
    
    # 創建圖片
    img = Image.new('RGB', (width, height), color='#E8E0D0')
    draw = ImageDraw.Draw(img)
    
    # 添加紙張紋理
    for _ in range(5000):
        x = random.randint(0, width-1)
        y = random.randint(0, height-1)
        offset = random.randint(-10, 10)
        base_color = (232 + offset, 224 + offset, 208 + offset)
        draw.point((x, y), fill=base_color)
    
    # 加載字體 - 超大字號模擬毛筆字
    title_font = get_font(120, 'large')     # 超大標題
    subtitle_font = get_font(72, 'title')   # 大副標題
    section_font = get_font(48, 'title')    # 章節標題
    body_font = get_font(36, 'regular')     # 正文大字
    small_font = get_font(32, 'regular')    # 韻目大字
    footer_font = get_font(28, 'regular')   # 頁腳
    
    # 邊距
    margin_x = 120
    margin_y = 120
    
    # 列寬
    col_width = 60
    col_gap = 45
    
    border_color = '#2A0000'
    
    # 邊框
    draw.rectangle(
        [(margin_x-45, margin_y-45), (width-margin_x+45, height-margin_y+45)],
        outline=border_color, width=4
    )
    draw.rectangle(
        [(margin_x-22, margin_y-22), (width-margin_x+22, height-margin_y+22)],
        outline=border_color, width=2
    )
    
    # 書根標籤
    label_font = get_font(36, 'title')
    draw.text((width - margin_x - 70, height - margin_y + 8), "目", font=label_font, fill=border_color)
    draw.text((width - margin_x - 70, height - margin_y + 55), "錄", font=label_font, fill=border_color)
    
    # 從最右邊開始
    current_x = width - margin_x - col_width
    current_y = margin_y + 60
    
    # 大標題
    title = "永樂小典"
    y = current_y
    for char in title:
        draw_text_with_shadow(draw, current_x, y, char, title_font, border_color)
        bbox = title_font.getbbox(char)
        y += (bbox[3] - bbox[1]) + 20 if bbox else 140
    
    # 副標題
    subtitle = "目錄"
    y += 50
    for char in subtitle:
        draw_text_with_shadow(draw, current_x, y, char, subtitle_font, border_color)
        bbox = subtitle_font.getbbox(char)
        y += (bbox[3] - bbox[1]) + 12 if bbox else 85
    
    # 分隔線
    line_x = current_x - col_width - 35
    draw.line([(line_x, margin_y + 60), (line_x, height - margin_y - 60)], fill=border_color, width=3)
    
    # 凡例列
    current_x = line_x - col_gap
    y = current_y
    
    fanli_title = "凡例"
    for char in fanli_title:
        draw_text_with_shadow(draw, current_x, y, char, section_font, border_color)
        bbox = section_font.getbbox(char)
        y += (bbox[3] - bbox[1]) + 12 if bbox else 60
    
    # 凡例內容
    current_x -= col_width + col_gap
    y = current_y
    
    fanli_lines = [
        "一、本典仿︽永樂大典︾之體",
        "例，以洪武正韻為綱，采輯",
        "公元二〇〇〇年後之新知新",
        "學。",
        "",
        "二、本典依︽洪武正韻︾七十",
        "六韻編排，分平聲二十二韻、",
        "上聲二十二韻、去聲二十二韻、",
        "入聲十韻。",
        "",
        "三、每韻以字系事，以事明",
        "理。",
        "",
        "四、新學名詞，依聲定韻。",
        "",
        "五、一詞跨韻者，於各韻互",
        "見。",
    ]
    
    for line in fanli_lines:
        if line == "":
            y += 30
            continue
        for char in line:
            draw.text((current_x, y), char, font=body_font, fill='#2A0000')
            bbox = body_font.getbbox(char)
            y += (bbox[3] - bbox[1]) + 6 if bbox else 42
            if y > height - margin_y - 100:
                current_x -= col_width + col_gap
                y = current_y
                if current_x < margin_x + col_width:
                    break
        y += 18
        if current_x < margin_x + col_width:
            break
    
    # 韻目總覽標題
    if current_x > margin_x + col_width * 2:
        current_x -= col_width + col_gap
        y = current_y
        yunmu_title = "韻目總覽"
        for char in yunmu_title:
            draw_text_with_shadow(draw, current_x, y, char, section_font, border_color)
            bbox = section_font.getbbox(char)
            y += (bbox[3] - bbox[1]) + 12 if bbox else 60
    
    # 平聲標題
    current_x -= col_width + col_gap
    y = current_y
    ping_title = "平聲"
    for char in ping_title:
        draw_text_with_shadow(draw, current_x, y, char, section_font, '#5A0000')
        bbox = section_font.getbbox(char)
        y += (bbox[3] - bbox[1]) + 10 if bbox else 55
    
    # 每個韻部獨立一列
    yunmu_data = [
        ("一東", "東同童籠"),
        ("二支", "支枝知馳"),
        ("三齊", "齊西溪低"),
        ("四魚", "魚余居諸"),
        ("五模", "模謨圖都"),
        ("六皆", "皆街諧懷"),
        ("七灰", "灰回雷枚"),
        ("八真", "真辰人身"),
        ("九寒", "寒安丹殘"),
        ("十刪", "刪山關還"),
        ("十一先", "先前千煙"),
        ("十二蕭", "蕭消朝樵"),
        ("十三爻", "爻交郊包"),
        ("十四豪", "豪高勞毛"),
        ("十五歌", "歌柯波多"),
        ("十六麻", "麻華沙車"),
        ("十七陽", "陽章昌堂"),
        ("十八庚", "庚更生橫"),
        ("十九青", "青清星靈"),
        ("二十尤", "尤由游休"),
        ("廿一侵", "侵音心金"),
        ("廿二覃", "覃談南甘"),
    ]
    
    for yun_num, yun_chars in yunmu_data:
        current_x -= col_width + col_gap
        if current_x < margin_x + col_width:
            break
            
        y = current_y
        
        # 韻部數字（紅色）
        for char in yun_num:
            draw_text_with_shadow(draw, current_x, y, char, small_font, '#8B0000')
            bbox = small_font.getbbox(char)
            y += (bbox[3] - bbox[1]) + 6 if bbox else 38
        
        y += 20  # 間隔
        
        # 韻部代表字
        for char in yun_chars:
            draw.text((current_x, y), char, font=small_font, fill='#3A0000')
            bbox = small_font.getbbox(char)
            y += (bbox[3] - bbox[1]) + 5 if bbox else 36
    
    # 頁腳
    footer = "永樂小典編修局奉敕編纂"
    footer_x = margin_x + 40
    footer_y = height - margin_y + 8
    draw.text((footer_x, footer_y), footer, font=footer_font, fill='#666666')
    
    # 保存
    img.save(output_file, 'PNG', quality=95)
    print(f"大號字體目錄已生成: {output_file}")

if __name__ == '__main__':
    output_file = sys.argv[1] if len(sys.argv) > 1 else '目錄.png'
    create_vertical_directory(output_file)
