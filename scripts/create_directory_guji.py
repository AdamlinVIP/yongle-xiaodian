#!/usr/bin/env python3
"""
永樂小典目錄 - 古籍影印本
栅格化文字 + 毛筆字效果 + 做舊紙張
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import sys
import os
import random
import math

def get_font(size, style='regular'):
    """獲取中文字體"""
    if style == 'title':
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

def create_ink_effect(draw, x, y, char, font, fill, intensity=0.8):
    """創建墨跡效果 - 模擬毛筆字"""
    # 直接繪製文字，但使用RGB模式
    if isinstance(fill, tuple):
        color = fill
    else:
        color = (40, 30, 20)  # 深褐色墨
    
    # 繪製主文字
    draw.text((x, y), char, font=font, fill=color)
    
    # 添加輕微模糊模擬墨跡暈染
    # 這裡簡化處理，直接繪製即可

def create_old_paper_texture(width, height):
    """創建做舊紙張紋理"""
    img = Image.new('RGB', (width, height), color='#E5DCC8')
    draw = ImageDraw.Draw(img)
    
    # 基礎紙張顏色變化 - 更明顯的斑駁
    for _ in range(12000):
        x = random.randint(0, width-1)
        y = random.randint(0, height-1)
        # 隨機顏色變化 - 模擬舊紙的斑駁
        base_r, base_g, base_b = 225, 215, 195
        offset = random.randint(-40, 25)
        r = max(170, min(250, base_r + offset))
        g = max(160, min(240, base_g + offset))
        b = max(140, min(225, base_b + offset))
        draw.point((x, y), fill=(r, g, b))
    
    # 添加輕微水漬/污漬效果（非常淡）
    for _ in range(10):
        cx = random.randint(0, width)
        cy = random.randint(0, height)
        radius = random.randint(10, 30)
        for r in range(radius):
            fade = r / radius
            gray = int(210 - fade * 15)
            draw.ellipse([cx-r, cy-r, cx+r, cy+r], 
                        outline=(gray, gray-5, gray-10), width=1)
    
    # 添加褶皺/裂痕效果
    for _ in range(20):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        length = random.randint(30, 150)
        angle = random.random() * math.pi * 2
        
        # 繪製細微裂痕
        for i in range(length):
            px = int(x1 + i * math.cos(angle))
            py = int(y1 + i * math.sin(angle))
            if 0 <= px < width and 0 <= py < height:
                if random.random() > 0.6:
                    draw.point((px, py), fill=(170, 160, 140))
    
    # 邊緣磨損效果
    for y in range(height):
        for x in range(min(20, width)):
            if random.random() > 0.8:
                draw.point((x, y), fill=(200, 190, 170))
        for x in range(max(0, width-20), width):
            if random.random() > 0.8:
                draw.point((x, y), fill=(200, 190, 170))
    
    return img

def create_vertical_directory(output_file):
    """創建古籍影印本目錄"""
    
    # 豎頁開本
    width = 2000
    height = 3200
    
    # 創建做舊紙張
    img = create_old_paper_texture(width, height)
    draw = ImageDraw.Draw(img)
    
    # 加載字體
    title_font = get_font(120, 'title')
    subtitle_font = get_font(72, 'title')
    section_font = get_font(48, 'title')
    body_font = get_font(36, 'regular')
    small_font = get_font(32, 'regular')
    footer_font = get_font(28, 'regular')
    
    # 邊距
    margin_x = 120
    margin_y = 120
    col_width = 60
    col_gap = 45
    
    border_color = (45, 35, 25)  # 深褐色邊框
    
    # 繪製邊框 - 雙線
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
    draw.text((width - margin_x - 70, height - margin_y + 8), "目", 
              font=label_font, fill=border_color)
    draw.text((width - margin_x - 70, height - margin_y + 55), "錄", 
              font=label_font, fill=border_color)
    
    # 從最右開始
    current_x = width - margin_x - col_width
    current_y = margin_y + 60
    
    # 大標題 - 使用墨跡效果
    title = "永樂小典"
    y = current_y
    for char in title:
        create_ink_effect(draw, current_x, y, char, title_font, border_color)
        bbox = title_font.getbbox(char)
        y += (bbox[3] - bbox[1]) + 20 if bbox else 140
    
    # 副標題
    subtitle = "目錄"
    y += 50
    for char in subtitle:
        create_ink_effect(draw, current_x, y, char, subtitle_font, border_color)
        bbox = subtitle_font.getbbox(char)
        y += (bbox[3] - bbox[1]) + 12 if bbox else 85
    
    # 分隔線
    line_x = current_x - col_width - 35
    draw.line([(line_x, margin_y + 60), (line_x, height - margin_y - 60)], 
              fill=border_color, width=3)
    
    # 凡例
    current_x = line_x - col_gap
    y = current_y
    
    fanli_title = "凡例"
    for char in fanli_title:
        create_ink_effect(draw, current_x, y, char, section_font, border_color)
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
            # 正文使用稍淡的墨色
            create_ink_effect(draw, current_x, y, char, body_font, (50, 40, 30), 0.7)
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
    
    # 韻目總覽
    if current_x > margin_x + col_width * 2:
        current_x -= col_width + col_gap
        y = current_y
        yunmu_title = "韻目總覽"
        for char in yunmu_title:
            create_ink_effect(draw, current_x, y, char, section_font, border_color)
            bbox = section_font.getbbox(char)
            y += (bbox[3] - bbox[1]) + 12 if bbox else 60
    
    # 平聲
    current_x -= col_width + col_gap
    y = current_y
    ping_title = "平聲"
    for char in ping_title:
        create_ink_effect(draw, current_x, y, char, section_font, (90, 30, 20))
        bbox = section_font.getbbox(char)
        y += (bbox[3] - bbox[1]) + 10 if bbox else 55
    
    # 韻部列表
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
        
        # 韻部數字（硃紅色）
        for char in yun_num:
            create_ink_effect(draw, current_x, y, char, small_font, (140, 30, 20))
            bbox = small_font.getbbox(char)
            y += (bbox[3] - bbox[1]) + 6 if bbox else 38
        
        y += 20
        
        # 韻部代表字
        for char in yun_chars:
            create_ink_effect(draw, current_x, y, char, small_font, (50, 40, 30), 0.75)
            bbox = small_font.getbbox(char)
            y += (bbox[3] - bbox[1]) + 5 if bbox else 36
    
    # 頁腳
    footer = "永樂小典編修局奉敕編纂"
    footer_x = margin_x + 40
    footer_y = height - margin_y + 8
    draw.text((footer_x, footer_y), footer, font=footer_font, fill=(120, 110, 100))
    
    # 最後添加整體模糊和對比度調整，模擬古籍掃描效果
    img = img.filter(ImageFilter.GaussianBlur(radius=0.3))
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(0.95)
    
    # 保存
    img.save(output_file, 'PNG', quality=95)
    print(f"古籍影印本目錄已生成: {output_file}")

if __name__ == '__main__':
    output_file = sys.argv[1] if len(sys.argv) > 1 else '目錄.png'
    create_vertical_directory(output_file)
