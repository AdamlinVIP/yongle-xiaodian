#!/usr/bin/env python3
"""
永樂小典目錄 - 豎版古籍開本
高>宽，模仿《永樂大典》真本豎頁格式
從右至左，從上至下
"""

from PIL import Image, ImageDraw, ImageFont
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

def create_vertical_directory(output_file):
    """創建豎版目錄古籍"""
    
    # 竖页格式 - 高>宽
    width = 1600
    height = 2400
    
    # 創建圖片
    img = Image.new('RGB', (width, height), color='#E8E0D0')
    draw = ImageDraw.Draw(img)
    
    # 添加紙張紋理
    for _ in range(4000):
        x = random.randint(0, width-1)
        y = random.randint(0, height-1)
        offset = random.randint(-10, 10)
        base_color = (232 + offset, 224 + offset, 208 + offset)
        draw.point((x, y), fill=base_color)
    
    # 加載字體
    title_font = get_font(72, 'large')
    subtitle_font = get_font(42, 'title')
    section_font = get_font(32, 'title')
    body_font = get_font(24, 'regular')
    small_font = get_font(22, 'regular')
    footer_font = get_font(20, 'regular')
    
    # 邊距
    margin_x = 100
    margin_y = 100
    
    # 列寬
    col_width = 40
    col_gap = 35
    
    border_color = '#3A0000'
    
    # 邊框
    draw.rectangle(
        [(margin_x-35, margin_y-35), (width-margin_x+35, height-margin_y+35)],
        outline=border_color, width=3
    )
    draw.rectangle(
        [(margin_x-18, margin_y-18), (width-margin_x+18, height-margin_y+18)],
        outline=border_color, width=1
    )
    
    # 書根標籤（右下角）
    label_font = get_font(26, 'title')
    draw.text((width - margin_x - 50, height - margin_y + 5), "目", font=label_font, fill=border_color)
    draw.text((width - margin_x - 50, height - margin_y + 38), "錄", font=label_font, fill=border_color)
    
    # 從最右邊開始
    current_x = width - margin_x - col_width
    current_y = margin_y + 50
    
    # 大標題
    title = "永樂小典"
    y = current_y
    for char in title:
        draw.text((current_x, y), char, font=title_font, fill=border_color)
        bbox = title_font.getbbox(char)
        y += (bbox[3] - bbox[1]) + 12 if bbox else 80
    
    # 副標題
    subtitle = "目錄"
    y += 35
    for char in subtitle:
        draw.text((current_x, y), char, font=subtitle_font, fill=border_color)
        bbox = subtitle_font.getbbox(char)
        y += (bbox[3] - bbox[1]) + 8 if bbox else 50
    
    # 分隔線
    line_x = current_x - col_width - 25
    draw.line([(line_x, margin_y + 50), (line_x, height - margin_y - 50)], fill=border_color, width=2)
    
    # 凡例列
    current_x = line_x - col_gap
    y = current_y
    
    fanli_title = "凡例"
    for char in fanli_title:
        draw.text((current_x, y), char, font=section_font, fill=border_color)
        bbox = section_font.getbbox(char)
        y += (bbox[3] - bbox[1]) + 8 if bbox else 40
    
    # 凡例內容
    current_x -= col_width + col_gap
    y = current_y
    
    fanli_lines = [
        "一、本典仿︽永樂大典︾",
        "之體例，以洪武正韻為",
        "綱，采輯公元二〇〇〇",
        "年後之新知新學。",
        "",
        "二、本典依︽洪武正韻︾",
        "七十六韻編排，分平聲",
        "二十二韻、上聲二十二",
        "韻、去聲二十二韻、入",
        "聲十韻。",
        "",
        "三、每韻以字系事，以",
        "事明理。",
        "",
        "四、新學名詞，依聲定",
        "韻。",
        "",
        "五、一詞跨韻者，於各",
        "韻互見。",
    ]
    
    for line in fanli_lines:
        if line == "":
            y += 20
            continue
        for char in line:
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
    
    # 韻目總覽標題
    if current_x > margin_x + col_width * 2:
        current_x -= col_width + col_gap
        y = current_y
        yunmu_title = "韻目總覽"
        for char in yunmu_title:
            draw.text((current_x, y), char, font=section_font, fill=border_color)
            bbox = section_font.getbbox(char)
            y += (bbox[3] - bbox[1]) + 8 if bbox else 40
    
    # 平聲標題
    current_x -= col_width + col_gap
    y = current_y
    ping_title = "平聲"
    for char in ping_title:
        draw.text((current_x, y), char, font=section_font, fill='#5A0000')
        bbox = section_font.getbbox(char)
        y += (bbox[3] - bbox[1]) + 6 if bbox else 35
    
    # 每個韻部獨立一列
    yunmu_data = [
        ("一東", "東同童籠蓬蒙恩宗"),
        ("二支", "支枝知馳池移離"),
        ("三齊", "齊西溪低泥啼題"),
        ("四魚", "魚余居諸除書疏"),
        ("五模", "模謨圖都徒奴盧"),
        ("六皆", "皆街諧懷乖排埋"),
        ("七灰", "灰回雷枚杯堆推"),
        ("八真", "真辰人身神臣仁"),
        ("九寒", "寒安丹殘闌看端"),
        ("十刪", "刪山關還環蠻閒"),
        ("十一先", "先前千煙田年顛"),
        ("十二蕭", "蕭消朝樵潮橋迢"),
        ("十三爻", "爻交郊包茅嘲泡"),
        ("十四豪", "豪高勞毛桃曹遨"),
        ("十五歌", "歌柯波多羅何呵"),
        ("十六麻", "麻華沙車斜遮奢"),
        ("十七陽", "陽章昌堂郎長航"),
        ("十八庚", "庚更生橫兵京英"),
        ("十九青", "青清星靈冥屏經"),
        ("二十尤", "尤由游休囚求浮"),
        ("廿一侵", "侵音心金針深林"),
        ("廿二覃", "覃談南甘藍蠶含"),
    ]
    
    for yun_num, yun_chars in yunmu_data:
        current_x -= col_width + col_gap
        if current_x < margin_x + col_width:
            break
            
        y = current_y
        
        # 韻部數字（紅色）
        for char in yun_num:
            draw.text((current_x, y), char, font=small_font, fill='#8B0000')
            bbox = small_font.getbbox(char)
            y += (bbox[3] - bbox[1]) + 4 if bbox else 26
        
        y += 15  # 間隔
        
        # 韻部代表字
        for char in yun_chars:
            draw.text((current_x, y), char, font=small_font, fill='#3A0000')
            bbox = small_font.getbbox(char)
            y += (bbox[3] - bbox[1]) + 3 if bbox else 24
    
    # 頁腳
    footer = "永樂小典編修局奉敕編纂"
    footer_x = margin_x + 30
    footer_y = height - margin_y + 5
    draw.text((footer_x, footer_y), footer, font=footer_font, fill='#666666')
    
    # 保存
    img.save(output_file, 'PNG', quality=95)
    print(f"豎頁目錄已生成: {output_file}")

if __name__ == '__main__':
    output_file = sys.argv[1] if len(sys.argv) > 1 else '目錄.png'
    create_vertical_directory(output_file)
