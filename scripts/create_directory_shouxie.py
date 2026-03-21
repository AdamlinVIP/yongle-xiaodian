#!/usr/bin/env python3
"""
永樂小典目錄 - 毛筆手寫風格
使用圖像處理模擬手寫毛筆字效果
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

def create_brush_char(char, font, size, ink_color=(30, 20, 10)):
    """創建單個毛筆字 - 使用多層疊加模擬墨跡"""
    # 獲取字體尺寸
    bbox = font.getbbox(char)
    if not bbox:
        w, h = size, size
    else:
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    
    # 創建足大的畫布
    canvas_w, canvas_h = w + 40, h + 40
    
    # 第一層：主體（濃墨）
    layer1 = Image.new('RGBA', (canvas_w, canvas_h), (0, 0, 0, 0))
    draw1 = ImageDraw.Draw(layer1)
    draw1.text((20, 20), char, font=font, fill=ink_color + (220,))
    
    # 第二層：暈染（淡墨）
    layer2 = Image.new('RGBA', (canvas_w, canvas_h), (0, 0, 0, 0))
    draw2 = ImageDraw.Draw(layer2)
    draw2.text((20, 20), char, font=font, fill=ink_color + (80,))
    layer2 = layer2.filter(ImageFilter.GaussianBlur(radius=3))
    
    # 第三層：飛白（最淡）
    layer3 = Image.new('RGBA', (canvas_w, canvas_h), (0, 0, 0, 0))
    draw3 = ImageDraw.Draw(layer3)
    draw3.text((22, 22), char, font=font, fill=ink_color + (40,))
    layer3 = layer3.filter(ImageFilter.GaussianBlur(radius=6))
    
    # 合併圖層
    result = Image.new('RGBA', (canvas_w, canvas_h), (0, 0, 0, 0))
    result = Image.alpha_composite(result, layer3)
    result = Image.alpha_composite(result, layer2)
    result = Image.alpha_composite(result, layer1)
    
    # 添加隨機墨點
    pixels = result.load()
    for py in range(5, canvas_h-5):
        for px in range(5, canvas_w-5):
            r, g, b, a = pixels[px, py]
            if a > 100 and random.random() > 0.98:
                # 隨機添加小墨點
                pixels[px, py] = ink_color + (min(255, a + 30),)
    
    return result

def draw_brush_text(draw, x, y, text, font, ink_color=(30, 20, 10)):
    """繪製毛筆文字"""
    current_y = y
    for char in text:
        char_img = create_brush_char(char, font, font.size, ink_color)
        # 粘貼到主圖片
        draw._image.paste(char_img, (x - 10, current_y - 10), char_img)
        
        # 計算下一個字的位置
        bbox = font.getbbox(char)
        if bbox:
            char_h = bbox[3] - bbox[1]
            current_y += char_h + 15
        else:
            current_y += font.size + 15

def create_old_paper(width, height):
    """創建做舊紙張"""
    # 基礎顏色
    img = Image.new('RGB', (width, height), color='#E8E0D0')
    draw = ImageDraw.Draw(img)
    
    # 添加紙張紋理
    for _ in range(10000):
        x = random.randint(0, width-1)
        y = random.randint(0, height-1)
        base_r, base_g, base_b = 232, 224, 208
        offset = random.randint(-25, 15)
        r = max(190, min(250, base_r + offset))
        g = max(185, min(245, base_g + offset))
        b = max(170, min(230, base_b + offset))
        draw.point((x, y), fill=(r, g, b))
    
    # 添加輕微褶皺線
    for _ in range(25):
        x = random.randint(0, width)
        y = random.randint(0, height)
        length = random.randint(40, 120)
        angle = random.random() * math.pi
        
        for i in range(length):
            px = int(x + i * math.cos(angle))
            py = int(y + i * math.sin(angle))
            if 0 <= px < width and 0 <= py < height:
                if random.random() > 0.5:
                    c = (210, 200, 185) if random.random() > 0.5 else (195, 185, 170)
                    draw.point((px, py), fill=c)
    
    # 邊緣磨損
    for y in range(height):
        for x in range(15):
            if random.random() > 0.85:
                draw.point((x, y), fill=(205, 195, 180))
        for x in range(width-15, width):
            if random.random() > 0.85:
                draw.point((x, y), fill=(205, 195, 180))
    
    return img

def create_directory(output_file):
    """創建目錄"""
    
    width = 1800
    height = 2800
    
    # 創建紙張
    img = create_old_paper(width, height)
    draw = ImageDraw.Draw(img)
    
    # 字體
    title_font = get_font(100, 'title')
    subtitle_font = get_font(60, 'title')
    section_font = get_font(40, 'title')
    body_font = get_font(28, 'regular')
    small_font = get_font(26, 'regular')
    
    margin_x = 100
    margin_y = 100
    col_width = 50
    col_gap = 40
    
    border_color = (45, 35, 25)
    
    # 邊框
    draw.rectangle(
        [(margin_x-40, margin_y-40), (width-margin_x+40, height-margin_y+40)],
        outline=border_color, width=3
    )
    draw.rectangle(
        [(margin_x-20, margin_y-20), (width-margin_x+20, height-margin_y+20)],
        outline=border_color, width=1
    )
    
    # 書根
    label_font = get_font(30, 'title')
    draw.text((width - margin_x - 60, height - margin_y + 5), "目", font=label_font, fill=border_color)
    draw.text((width - margin_x - 60, height - margin_y + 45), "錄", font=label_font, fill=border_color)
    
    # 從右開始
    current_x = width - margin_x - col_width
    current_y = margin_y + 50
    
    # 大標題
    draw_brush_text(draw, current_x, current_y, "永樂小典", title_font)
    
    # 計算副標題位置
    bbox = title_font.getbbox("永")
    title_h = (bbox[3] - bbox[1] + 15) * 4 if bbox else 460
    subtitle_y = current_y + title_h + 40
    draw_brush_text(draw, current_x, subtitle_y, "目錄", subtitle_font)
    
    # 分隔線
    line_x = current_x - col_width - 30
    draw.line([(line_x, margin_y + 50), (line_x, height - margin_y - 50)], fill=border_color, width=2)
    
    # 凡例
    current_x = line_x - col_gap
    draw_brush_text(draw, current_x, current_y, "凡例", section_font)
    
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
            y += 25
            continue
        draw_brush_text(draw, current_x, y, line, body_font, (40, 30, 20))
        
        # 計算下一行位置
        bbox = body_font.getbbox("永")
        line_h = (bbox[3] - bbox[1] + 15) * len(line) if bbox else len(line) * 35
        y += line_h + 15
        
        if y > height - margin_y - 80:
            current_x -= col_width + col_gap
            y = current_y
            if current_x < margin_x + col_width:
                break
    
    # 韻目總覽
    if current_x > margin_x + col_width * 2:
        current_x -= col_width + col_gap
        draw_brush_text(draw, current_x, current_y, "韻目總覽", section_font)
    
    # 平聲
    current_x -= col_width + col_gap
    draw_brush_text(draw, current_x, current_y, "平聲", section_font)
    
    # 韻部
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
        draw_brush_text(draw, current_x, y, yun_num, small_font, (150, 40, 30))
        
        bbox = small_font.getbbox("永")
        num_h = (bbox[3] - bbox[1] + 15) * len(yun_num) if bbox else len(yun_num) * 35
        y += num_h + 20
        
        # 韻部代表字
        draw_brush_text(draw, current_x, y, yun_chars, small_font, (40, 30, 20))
    
    # 頁腳
    footer_font = get_font(24, 'regular')
    draw.text((margin_x + 30, height - margin_y + 5), "永樂小典編修局奉敕編纂", 
              font=footer_font, fill=(120, 110, 100))
    
    # 輕微模糊
    img = img.filter(ImageFilter.GaussianBlur(radius=0.2))
    
    img.save(output_file, 'PNG', quality=95)
    print(f"毛筆字目錄已生成: {output_file}")

if __name__ == '__main__':
    output_file = sys.argv[1] if len(sys.argv) > 1 else '目錄.png'
    create_directory(output_file)
