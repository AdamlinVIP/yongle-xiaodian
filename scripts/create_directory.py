#!/usr/bin/env python3
"""
永乐小典目录 - 影印本风格
模仿《永乐大典》真本版式
"""

from PIL import Image, ImageDraw, ImageFont
import sys
import os

def get_font(size, style='regular'):
    """获取中文字体 - 使用宋体模拟古籍"""
    if style == 'title':
        font_paths = [
            '/usr/share/fonts/google-noto-cjk/NotoSerifCJK-Bold.ttc',
            '/usr/share/fonts/google-noto-cjk/NotoSerifCJK-Regular.ttc',
        ]
    elif style == 'large':
        font_paths = [
            '/usr/share/fonts/google-noto-cjk/NotoSerifCJK-Bold.ttc',
        ]
    else:
        font_paths = [
            '/usr/share/fonts/google-noto-cjk/NotoSerifCJK-Regular.ttc',
            '/usr/share/fonts/google-noto-cjk/NotoSerifCJK-Light.ttc',
        ]
    
    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                return ImageFont.truetype(font_path, size)
            except:
                continue
    
    return ImageFont.load_default()

def create_directory_image(output_file):
    """创建目录影印本"""
    
    # 图片尺寸 - 古籍开本比例
    width = 1600
    height = 2400
    
    # 创建图片（米黄色古籍纸张，略带旧感）
    img = Image.new('RGB', (width, height), color='#E8E0D0')
    draw = ImageDraw.Draw(img)
    
    # 添加纸张纹理效果（随机噪点模拟旧纸）
    import random
    for _ in range(5000):
        x = random.randint(0, width-1)
        y = random.randint(0, height-1)
        # 轻微的颜色变化
        offset = random.randint(-10, 10)
        base_color = (232 + offset, 224 + offset, 208 + offset)
        draw.point((x, y), fill=base_color)
    
    # 加载字体
    title_font = get_font(72, 'large')      # 大标题
    subtitle_font = get_font(36, 'title')   # 副标题
    section_font = get_font(28, 'title')    # 章节标题
    body_font = get_font(22, 'regular')     # 正文
    small_font = get_font(18, 'regular')    # 小字
    
    # 边距
    margin_x = 120
    margin_y = 100
    
    # 当前位置
    y = margin_y
    
    # 绘制边框 - 双线框
    border_color = '#4A0000'  # 深褐色，模拟古籍墨色
    
    # 外框
    draw.rectangle(
        [(margin_x-40, margin_y-40), (width-margin_x+40, height-margin_y+40)],
        outline=border_color, width=3
    )
    # 内框
    draw.rectangle(
        [(margin_x-25, margin_y-25), (width-margin_x+25, height-margin_y+25)],
        outline=border_color, width=1
    )
    
    # 顶部装饰 - 象鼻纹简化
    y += 20
    draw.line([(margin_x, y), (width-margin_x, y)], fill=border_color, width=2)
    y += 15
    
    # 大标题 - 永乐小典
    title = "永乐小典"
    bbox = title_font.getbbox(title)
    title_width = bbox[2] - bbox[0] if bbox else 200
    x = (width - title_width) // 2
    draw.text((x, y), title, font=title_font, fill=border_color)
    y += 100
    
    # 副标题 - 目录
    subtitle = "目　录"
    bbox = subtitle_font.getbbox(subtitle)
    sub_width = bbox[2] - bbox[0] if bbox else 100
    x = (width - sub_width) // 2
    draw.text((x, y), subtitle, font=subtitle_font, fill=border_color)
    y += 70
    
    # 分隔线
    draw.line([(margin_x + 100, y), (width - margin_x - 100, y)], fill=border_color, width=2)
    y += 40
    
    # 凡例
    draw.text((margin_x, y), "凡例", font=section_font, fill=border_color)
    y += 45
    
    fanli_text = [
        "一、本典仿《永乐大典》之体例，以洪武正韵为纲，",
        "　　采辑公元二〇〇〇年后之新知新学。",
        "二、本典依《洪武正韵》七十六韵编排，分平声二十",
        "　　二韵、上声二十二韵、去声二十二韵、入声十韵。",
        "三、每韵以字系事，以事明理。词条之下，详载释义、",
        "　　出处、演变、关联。",
        "四、新学名词，有音无字者，依声定韵；有字者，依",
        "　　字定韵。",
        "五、一词跨韵者，于各韵互见，以便检索。",
    ]
    
    for line in fanli_text:
        draw.text((margin_x, y), line, font=body_font, fill='#2A0000')
        y += 32
    
    y += 30
    
    # 分隔线
    draw.line([(margin_x + 100, y), (width - margin_x - 100, y)], fill=border_color, width=1)
    y += 30
    
    # 韵目总览
    draw.text((margin_x, y), "韵目总览", font=section_font, fill=border_color)
    y += 45
    
    # 平声
    draw.text((margin_x, y), "平声二十二韵", font=section_font, fill='#5A0000')
    y += 40
    
    ping_sheng = [
        "一东　东、同、童、笼、蓬、蒙",
        "二支　支、枝、知、驰、池、移",
        "三齐　齐、西、溪、低、泥、啼",
        "四鱼　鱼、余、居、诸、除、书",
        "五模　模、谟、图、都、徒、奴",
        "六皆　皆、街、谐、怀、乖、排",
        "七灰　灰、回、雷、枚、杯、堆",
        "八真　真、辰、人、身、神、臣",
        "九寒　寒、安、丹、残、阑、看",
        "十删　删、山、关、还、环、蛮",
        "十一先　先、前、千、烟、田、年",
        "十二萧　萧、消、朝、樵、潮、桥",
        "十三肴　肴、交、郊、包、茅、嘲",
        "十四豪　豪、高、劳、毛、桃、曹",
        "十五歌　歌、柯、波、多、罗、何",
        "十六麻　麻、华、沙、车、斜、遮",
        "十七阳　阳、章、昌、堂、郎、长",
        "十八庚　庚、更、生、横、兵、京",
        "十九青　青、清、星、灵、冥、屏",
        "二十尤　尤、由、游、休、囚、求",
        "二十一侵　侵、音、心、金、针、深",
        "二十二覃　覃、谈、南、甘、蓝、蚕",
    ]
    
    for line in ping_sheng:
        draw.text((margin_x + 20, y), line, font=small_font, fill='#3A0000')
        y += 26
    
    y += 20
    
    # 上声
    draw.text((margin_x, y), "上声二十二韵", font=section_font, fill='#5A0000')
    y += 40
    
    shang_sheng = [
        "一董　董、动、孔、总、汞、桶",
        "二纸　纸、旨、止、齿、侈、豕",
        "三荠　荠、礼、体、米、弟、洗",
        "四语　语、与、巨、吕、侣、许",
    ]
    
    for line in shang_sheng[:4]:  # 只显示部分，避免过长
        draw.text((margin_x + 20, y), line, font=small_font, fill='#3A0000')
        y += 26
    
    draw.text((margin_x + 20, y), "......", font=small_font, fill='#666666')
    y += 30
    
    # 分隔线
    draw.line([(margin_x + 100, y), (width - margin_x - 100, y)], fill=border_color, width=1)
    y += 30
    
    # 采辑领域
    draw.text((margin_x, y), "采辑领域", font=section_font, fill=border_color)
    y += 45
    
    fields = [
        "科技门　人工智能、区块链、量子计算、基因编辑",
        "　　　　新能源、深空探测、互联网、物联网",
        "文化门　网络文化、弹幕、网红经济、元宇宙",
        "商业门　金融科技、数字货币、移动支付、订阅制",
    ]
    
    for line in fields:
        draw.text((margin_x, y), line, font=body_font, fill='#2A0000')
        y += 32
    
    y += 30
    
    # 分隔线
    draw.line([(margin_x + 100, y), (width - margin_x - 100, y)], fill=border_color, width=1)
    y += 40
    
    # 编纂职官
    draw.text((margin_x, y), "编纂职官", font=section_font, fill=border_color)
    y += 45
    
    officials = [
        "总裁官　　　解缙",
        "副总裁　　　姚广孝、胡广",
        "纂修官　　　待补",
        "缮写官　　　待补",
    ]
    
    for line in officials:
        draw.text((margin_x, y), line, font=body_font, fill='#2A0000')
        y += 32
    
    # 底部装饰
    y = height - margin_y - 60
    draw.line([(margin_x, y), (width-margin_x, y)], fill=border_color, width=2)
    y += 20
    
    # 页脚
    footer = "永乐小典编修局　奉敕编纂"
    bbox = small_font.getbbox(footer)
    footer_width = bbox[2] - bbox[0] if bbox else 200
    x = (width - footer_width) // 2
    draw.text((x, y), footer, font=small_font, fill='#666666')
    
    # 保存图片
    img.save(output_file, 'PNG', quality=95)
    print(f"目录影印本已生成: {output_file}")

if __name__ == '__main__':
    output_file = sys.argv[1] if len(sys.argv) > 1 else '目录.png'
    create_directory_image(output_file)
