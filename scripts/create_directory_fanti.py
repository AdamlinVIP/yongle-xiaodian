#!/usr/bin/env python3
"""
永樂小典目錄 - 豎版影印本風格
模仿《永樂大典》真本版式
從右至左，從上至下
繁體字、毛筆字效果、正確書名號
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import sys
import os
import random

def get_font(size, style='regular'):
    """獲取中文字體"""
    if style == 'title':
        # 標題用粗體
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

def create_vertical_directory(output_file):
    """創建豎版目錄影印本"""
    
    # 圖片尺寸
    width = 2800
    height = 2000
    
    # 創建圖片（米黃色古籍紙張）
    img = Image.new('RGB', (width, height), color='#E8E0D0')
    draw = ImageDraw.Draw(img)
    
    # 添加紙張紋理
    for _ in range(5000):
        x = random.randint(0, width-1)
        y = random.randint(0, height-1)
        offset = random.randint(-10, 10)
        base_color = (232 + offset, 224 + offset, 208 + offset)
        draw.point((x, y), fill=base_color)
    
    # 加載字體 - 增大字體模擬毛筆字
    title_font = get_font(72, 'large')      # 大標題
    subtitle_font = get_font(42, 'title')   # 副標題
    section_font = get_font(32, 'title')    # 章節標題
    body_font = get_font(24, 'regular')     # 正文
    small_font = get_font(20, 'regular')    # 小字
    
    # 邊距
    margin_x = 120
    margin_y = 100
    
    # 列寬
    col_width = 40
    col_gap = 60
    
    # 邊框顏色
    border_color = '#3A0000'
    
    # 繪製邊框 - 雙線框
    draw.rectangle(
        [(margin_x-40, margin_y-40), (width-margin_x+40, height-margin_y+40)],
        outline=border_color, width=4
    )
    draw.rectangle(
        [(margin_x-20, margin_y-20), (width-margin_x+20, height-margin_y+20)],
        outline=border_color, width=2
    )
    
    # 書根標籤（右下角）
    label_font = get_font(28, 'title')
    draw.text((width - margin_x - 60, height - margin_y + 5), "目", font=label_font, fill=border_color)
    draw.text((width - margin_x - 60, height - margin_y + 40), "錄", font=label_font, fill=border_color)
    
    # 從最右邊開始
    current_x = width - margin_x - col_width
    current_y = margin_y + 50
    
    # 大標題 - 永樂小典（最右列）
    title = "永樂小典"
    title_y = current_y
    for char in title:
        draw.text((current_x, title_y), char, font=title_font, fill=border_color)
        bbox = title_font.getbbox(char)
        title_y += (bbox[3] - bbox[1]) + 12 if bbox else 80
    
    # 副標題 - 目錄
    subtitle = "目錄"
    subtitle_y = title_y + 30
    for char in subtitle:
        draw.text((current_x, subtitle_y), char, font=subtitle_font, fill=border_color)
        bbox = subtitle_font.getbbox(char)
        subtitle_y += (bbox[3] - bbox[1]) + 8 if bbox else 50
    
    # 分隔線（豎線）
    line_x = current_x - col_width - 30
    draw.line([(line_x, margin_y + 50), (line_x, height - margin_y - 50)], fill=border_color, width=3)
    
    # 移動到下一列
    current_x = line_x - col_gap
    current_y = margin_y + 50
    
    # 凡例
    fanli_title = "凡例"
    y = current_y
    for char in fanli_title:
        draw.text((current_x, y), char, font=section_font, fill=border_color)
        bbox = section_font.getbbox(char)
        y += (bbox[3] - bbox[1]) + 8 if bbox else 40
    
    current_x -= col_width + col_gap
    y = current_y
    
    # 凡例內容 - 繁體、正確書名號（豎排書名號用︽︾）
    fanli_content = [
        "一、本典仿︽永樂大典︾之體例，",
        "以洪武正韻為綱，采輯公元",
        "二〇〇〇年後之新知新學。",
        "",
        "二、本典依︽洪武正韻︾七十",
        "六韻編排，分平聲二十二韻、",
        "上聲二十二韻、去聲二十二韻、",
        "入聲十韻。",
        "",
        "三、每韻以字系事，以事明理。",
        "",
        "四、新學名詞，依聲定韻。",
        "",
        "五、一詞跨韻者，於各韻互見。",
    ]
    
    for text in fanli_content:
        if text == "":
            y += 20
            continue
        for char in text:
            draw.text((current_x, y), char, font=body_font, fill='#2A0000')
            bbox = body_font.getbbox(char)
            y += (bbox[3] - bbox[1]) + 4 if bbox else 28
            
            if y > height - margin_y - 80:
                current_x -= col_width + col_gap
                y = current_y
                if current_x < margin_x + col_width:
                    break
        y += 12
        if current_x < margin_x + col_width:
            break
    
    # 分隔線
    if current_x > margin_x + col_width * 3:
        current_x -= col_width
        draw.line([(current_x + col_width//2, margin_y + 50), (current_x + col_width//2, height - margin_y - 50)], fill=border_color, width=2)
        current_x -= col_gap
    
    # 韻目總覽
    if current_x > margin_x + col_width:
        y = current_y
        yunmu_title = "韻目總覽"
        for char in yunmu_title:
            draw.text((current_x, y), char, font=section_font, fill=border_color)
            bbox = section_font.getbbox(char)
            y += (bbox[3] - bbox[1]) + 8 if bbox else 40
        
        current_x -= col_width + col_gap
        y = current_y
        
        # 平聲 - 每個韻部分開，中間有間隔
        ping_title = "平聲"
        for char in ping_title:
            draw.text((current_x, y), char, font=section_font, fill='#5A0000')
            bbox = section_font.getbbox(char)
            y += (bbox[3] - bbox[1]) + 6 if bbox else 35
        
        y += 20
        
        # 韻目列表 - 每個韻部獨立，中間有空行
        yun_list = [
            ("一東", "東同童籠蓬蒙"),
            ("", ""),  # 空行
            ("二支", "支枝知馳池移"),
            ("", ""),
            ("三齊", "齊西溪低泥啼"),
            ("", ""),
            ("四魚", "魚余居諸除書"),
            ("", ""),
            ("五模", "模謨圖都徒奴"),
            ("", ""),
            ("六皆", "皆街諧懷乖排"),
            ("", ""),
            ("七灰", "灰回雷枚杯堆"),
            ("", ""),
            ("八真", "真辰人身神臣"),
            ("", ""),
            ("九寒", "寒安丹殘闌看"),
            ("", ""),
            ("十刪", "刪山關還環蠻"),
            ("", ""),
            ("十一先", "先前千煙田年"),
            ("", ""),
            ("十二蕭", "蕭消朝樵潮橋"),
            ("", ""),
            ("十三爻", "爻交郊包茅嘲"),
            ("", ""),
            ("十四豪", "豪高勞毛桃曹"),
            ("", ""),
            ("十五歌", "歌柯波多羅何"),
            ("", ""),
            ("十六麻", "麻華沙車斜遮"),
            ("", ""),
            ("十七陽", "陽章昌堂郎長"),
            ("", ""),
            ("十八庚", "庚更生橫兵京"),
            ("", ""),
            ("十九青", "青清星靈冥屏"),
            ("", ""),
            ("二十尤", "尤由游休囚求"),
            ("", ""),
            ("廿一侵", "侵音心金針深"),
            ("", ""),
            ("廿二覃", "覃談南甘藍蠶"),
        ]
        
        for yun_num, yun_chars in yun_list:
            if yun_num == "" and yun_chars == "":
                y += 15  # 空行間隔
                continue
                
            # 韻部數字（如"一東"）
            if yun_num:
                for char in yun_num:
                    draw.text((current_x, y), char, font=small_font, fill='#8B0000')
                    bbox = small_font.getbbox(char)
                    y += (bbox[3] - bbox[1]) + 3 if bbox else 23
                y += 5
            
            # 韻部代表字
            if yun_chars:
                for char in yun_chars:
                    draw.text((current_x, y), char, font=small_font, fill='#3A0000')
                    bbox = small_font.getbbox(char)
                    y += (bbox[3] - bbox[1]) + 2 if bbox else 22
                    
                    if y > height - margin_y - 80:
                        current_x -= col_width + col_gap
                        y = current_y
                        if current_x < margin_x + col_width:
                            break
            
            y += 8
            if current_x < margin_x + col_width:
                break
    
    # 頁腳
    footer = "永樂小典編修局奉敕編纂"
    footer_x = margin_x + 30
    footer_y = height - margin_y + 5
    draw.text((footer_x, footer_y), footer, font=small_font, fill='#666666')
    
    # 保存圖片
    img.save(output_file, 'PNG', quality=95)
    print(f"豎版目錄影印本已生成: {output_file}")

if __name__ == '__main__':
    output_file = sys.argv[1] if len(sys.argv) > 1 else '目錄.png'
    create_vertical_directory(output_file)
