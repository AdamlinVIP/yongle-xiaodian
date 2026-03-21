#!/usr/bin/env python3
"""
永樂小典目錄 - 台閣體手寫風格
明代官方書體，橫平豎直，端莊匀稱
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import sys
import os
import random
import math

def get_font(size, style='regular'):
    """獲取字體 - 使用宋體模擬台閣體"""
    if style == 'title':
        # 標題用粗體
        font_paths = ['/usr/share/fonts/google-noto-cjk/NotoSerifCJK-Bold.ttc']
    else:
        # 正文用常規體
        font_paths = ['/usr/share/fonts/google-noto-cjk/NotoSerifCJK-Regular.ttc']
    
    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                return ImageFont.truetype(font_path, size)
            except:
                continue
    return ImageFont.load_default()

def create_taige_char(char, font, ink_color=(25, 18, 12)):
    """創建台閣體單字 - 端莊匀稱，墨跡飽滿"""
    bbox = font.getbbox(char)
    if not bbox:
        w, h = font.size, font.size
    else:
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    
    canvas_w, canvas_h = w + 30, h + 30
    
    # 主體層 - 飽滿濃墨
    main_layer = Image.new('RGBA', (canvas_w, canvas_h), (0, 0, 0, 0))
    draw_main = ImageDraw.Draw(main_layer)
    draw_main.text((15, 15), char, font=font, fill=ink_color + (240,))
    
    # 暈染層 - 台閣體暈染較均勻
    blur_layer = Image.new('RGBA', (canvas_w, canvas_h), (0, 0, 0, 0))
    draw_blur = ImageDraw.Draw(blur_layer)
    draw_blur.text((15, 15), char, font=font, fill=ink_color + (60,))
    blur_layer = blur_layer.filter(ImageFilter.GaussianBlur(radius=2))
    
    # 合併
    result = Image.new('RGBA', (canvas_w, canvas_h), (0, 0, 0, 0))
    result = Image.alpha_composite(result, blur_layer)
    result = Image.alpha_composite(result, main_layer)
    
    return result

def draw_taige_text(draw, x, y, text, font, ink_color=(25, 18, 12)):
    """繪製台閣體文字"""
    current_y = y
    for char in text:
        char_img = create_taige_char(char, font, ink_color)
        draw._image.paste(char_img, (x - 5, current_y - 5), char_img)
        
        bbox = font.getbbox(char)
        if bbox:
            char_h = bbox[3] - bbox[1]
            current_y += char_h + 12
        else:
            current_y += font.size + 12

def create_xuan_paper(width, height):
    """創建宣紙效果 - 米黃色，細膩紋理"""
    img = Image.new('RGB', (width, height), color='#EDE5D5')
    draw = ImageDraw.Draw(img)
    
    # 細膩紋理
    for _ in range(15000):
        x = random.randint(0, width-1)
        y = random.randint(0, height-1)
        base_r, base_g, base_b = 237, 229, 213
        offset = random.randint(-15, 10)
        r = max(215, min(250, base_r + offset))
        g = max(210, min(245, base_g + offset))
        b = max(195, min(230, base_b + offset))
        draw.point((x, y), fill=(r, g, b))
    
    # 輕微纖維紋理（橫向）
    for _ in range(100):
        y = random.randint(0, height)
        length = random.randint(50, 200)
        x_start = random.randint(0, width - length)
        for i in range(length):
            if random.random() > 0.7:
                gray = random.randint(200, 220)
                draw.point((x_start + i, y), fill=(gray, gray-3, gray-8))
    
    # 輕微纖維紋理（豎向）
    for _ in range(100):
        x = random.randint(0, width)
        length = random.randint(50, 200)
        y_start = random.randint(0, height - length)
        for i in range(length):
            if random.random() > 0.7:
                gray = random.randint(200, 220)
                draw.point((x, y_start + i), fill=(gray, gray-3, gray-8))
    
    # 邊緣自然磨損
    for y in range(height):
        for x in range(10):
            if random.random() > 0.8:
                draw.point((x, y), fill=(210, 200, 185))
        for x in range(width-10, width):
            if random.random() > 0.8:
                draw.point((x, y), fill=(210, 200, 185))
    
    return img

def draw_seal(draw, x, y, size=80):
    """繪製印章 - 永樂小典"""
    # 印章底色
    seal_color = (180, 50, 40)  # 硃砂紅
    
    # 方形印章
    draw.rectangle([x, y, x+size, y+size], fill=seal_color, outline=seal_color)
    
    # 印章文字（簡化版，用線條模擬）
    seal_font = get_font(size//3, 'title')
    
    # 永
    draw.text((x+size//4, y+size//8), "永", font=seal_font, fill=(240, 220, 200))
    # 樂
    draw.text((x+size//4, y+size//2), "樂", font=seal_font, fill=(240, 220, 200))

def create_directory(output_file):
    """創建台閣體目錄"""
    
    width = 1800
    height = 2800
    
    # 創建宣紙
    img = create_xuan_paper(width, height)
    draw = ImageDraw.Draw(img)
    
    # 台閣體字體
    title_font = get_font(90, 'title')
    subtitle_font = get_font(55, 'title')
    section_font = get_font(38, 'title')
    body_font = get_font(26, 'regular')
    small_font = get_font(24, 'regular')
    
    margin_x = 100
    margin_y = 100
    col_width = 48
    col_gap = 35
    
    border_color = (40, 30, 22)
    
    # 雙線邊框
    draw.rectangle(
        [(margin_x-38, margin_y-38), (width-margin_x+38, height-margin_y+38)],
        outline=border_color, width=3
    )
    draw.rectangle(
        [(margin_x-18, margin_y-18), (width-margin_x+18, height-margin_y+18)],
        outline=border_color, width=1
    )
    
    # 書根標籤
    label_font = get_font(28, 'title')
    draw.text((width - margin_x - 55, height - margin_y + 5), "目", font=label_font, fill=border_color)
    draw.text((width - margin_x - 55, height - margin_y + 40), "錄", font=label_font, fill=border_color)
    
    # 從右開始
    current_x = width - margin_x - col_width
    current_y = margin_y + 50
    
    # 大標題
    draw_taige_text(draw, current_x, current_y, "永樂小典", title_font)
    
    bbox = title_font.getbbox("永")
    title_h = (bbox[3] - bbox[1] + 12) * 4 if bbox else 400
    subtitle_y = current_y + title_h + 35
    draw_taige_text(draw, current_x, subtitle_y, "目錄", subtitle_font)
    
    # 分隔線
    line_x = current_x - col_width - 25
    draw.line([(line_x, margin_y + 50), (line_x, height - margin_y - 50)], fill=border_color, width=2)
    
    # 凡例
    current_x = line_x - col_gap
    draw_taige_text(draw, current_x, current_y, "凡例", section_font)
    
    # 凡例內容
    current_x -= col_width + col_gap
    y = current_y
    
    fanli = [
        "一、本典仿︽永樂大典︾之",
        "體例，以洪武正韻為綱，",
        "采輯公元二〇〇〇年後之",
        "新知新學。",
        "",
        "二、本典依︽洪武正韻︾七",
        "十六韻編排，分平聲二十",
        "二韻、上聲二十二韻、去",
        "聲二十二韻、入聲十韻。",
        "",
        "三、每韻以字系事，以事",
        "明理。",
        "",
        "四、新學名詞，依聲定韻。",
        "",
        "五、一詞跨韻者，於各韻",
        "互見。",
    ]
    
    for line in fanli:
        if line == "":
            y += 22
            continue
        draw_taige_text(draw, current_x, y, line, body_font)
        
        bbox = body_font.getbbox("永")
        line_h = (bbox[3] - bbox[1] + 12) * len(line) if bbox else len(line) * 32
        y += line_h + 12
        
        if y > height - margin_y - 80:
            current_x -= col_width + col_gap
            y = current_y
            if current_x < margin_x + col_width:
                break
    
    # 韻目總覽
    if current_x > margin_x + col_width * 2:
        current_x -= col_width + col_gap
        draw_taige_text(draw, current_x, current_y, "韻目總覽", section_font)
    
    # 平聲
    current_x -= col_width + col_gap
    draw_taige_text(draw, current_x, current_y, "平聲", section_font)
    
    # 韻部列表
    yunmu = [
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
    
    for yun_num, yun_chars in yunmu:
        current_x -= col_width + col_gap
        if current_x < margin_x + col_width:
            break
        
        y = current_y
        
        # 韻部數字（硃紅色）
        draw_taige_text(draw, current_x, y, yun_num, small_font, (160, 45, 35))
        
        bbox = small_font.getbbox("永")
        num_h = (bbox[3] - bbox[1] + 12) * len(yun_num) if bbox else len(yun_num) * 32
        y += num_h + 18
        
        # 韻部代表字
        draw_taige_text(draw, current_x, y, yun_chars, small_font)
    
    # 印章（右下角上方）
    seal_x = width - margin_x - 150
    seal_y = height - margin_y - 250
    draw_seal(draw, seal_x, seal_y, 100)
    
    # 頁腳
    footer_font = get_font(22, 'regular')
    draw.text((margin_x + 25, height - margin_y + 5), "永樂小典編修局奉敕編纂", 
              font=footer_font, fill=(115, 105, 95))
    
    # 輕微模糊模擬掃描效果
    img = img.filter(ImageFilter.GaussianBlur(radius=0.15))
    
    img.save(output_file, 'PNG', quality=95)
    print(f"台閣體目錄已生成: {output_file}")

if __name__ == '__main__':
    output_file = sys.argv[1] if len(sys.argv) > 1 else '目錄.png'
    create_directory(output_file)
