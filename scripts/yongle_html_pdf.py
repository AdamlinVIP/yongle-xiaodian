#!/usr/bin/env python3
"""
永乐大典风格 HTML + PDF 生成器
使用 Playwright 生成古籍风格的 PDF 图片
"""

import sys
import os

def create_html(input_md, output_html):
    """将 Markdown 转换为永乐大典风格的 HTML"""
    
    with open(input_md, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # 简单的 Markdown 解析
    lines = md_content.split('\n')
    html_body = []
    in_list = False
    
    for line in lines:
        line = line.strip()
        if not line:
            if in_list:
                html_body.append('</ul>')
                in_list = False
            continue
        
        # 主标题
        if line.startswith('# '):
            if in_list:
                html_body.append('</ul>')
                in_list = False
            html_body.append(f'<h1 class="main-title">{line[2:]}</h1>')
        # 章节标题
        elif line.startswith('## '):
            if in_list:
                html_body.append('</ul>')
                in_list = False
            html_body.append(f'<h2 class="section-title">{line[3:]}</h2>')
        # 小标题
        elif line.startswith('### '):
            if in_list:
                html_body.append('</ul>')
                in_list = False
            html_body.append(f'<h3 class="sub-title">{line[4:]}</h3>')
        # 分隔线
        elif line == '---':
            if in_list:
                html_body.append('</ul>')
                in_list = False
            html_body.append('<hr class="divider">')
        # 列表项
        elif line.startswith('- '):
            if not in_list:
                html_body.append('<ul class="content-list">')
                in_list = True
            html_body.append(f'<li>{line[2:]}</li>')
        # 粗体
        elif line.startswith('**') and line.endswith('**'):
            if in_list:
                html_body.append('</ul>')
                in_list = False
            html_body.append(f'<p class="highlight">【{line[2:-2]}】</p>')
        # 普通段落
        else:
            if in_list:
                html_body.append('</ul>')
                in_list = False
            html_body.append(f'<p>{line}</p>')
    
    if in_list:
        html_body.append('</ul>')
    
    # 永乐大典风格 HTML 模板
    html_template = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>永乐小典 · 互联网</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600;700&display=swap');
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: "Noto Serif SC", "SimSun", "STSong", serif;
            background: linear-gradient(135deg, #f5f0e8 0%, #e8e0d0 100%);
            color: #2c2c2c;
            line-height: 1.8;
            padding: 40px;
            max-width: 210mm;
            margin: 0 auto;
            min-height: 297mm;
        }}
        
        /* 古籍纸张纹理效果 */
        body::before {{
            content: "";
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
            opacity: 0.03;
            pointer-events: none;
            z-index: -1;
        }}
        
        /* 边框装饰 */
        .page-border {{
            border: 3px double #8B0000;
            padding: 30px;
            position: relative;
            min-height: 257mm;
        }}
        
        .page-border::before {{
            content: "";
            position: absolute;
            top: 8px;
            left: 8px;
            right: 8px;
            bottom: 8px;
            border: 1px solid #8B0000;
            pointer-events: none;
        }}
        
        /* 主标题 */
        .main-title {{
            font-size: 36px;
            font-weight: 700;
            color: #8B0000;
            text-align: center;
            margin-bottom: 10px;
            letter-spacing: 8px;
            border-bottom: 2px solid #8B0000;
            padding-bottom: 15px;
        }}
        
        /* 章节标题 */
        .section-title {{
            font-size: 20px;
            font-weight: 600;
            color: #2F4F4F;
            margin-top: 25px;
            margin-bottom: 15px;
            padding-left: 15px;
            border-left: 4px solid #8B0000;
        }}
        
        /* 小标题 */
        .sub-title {{
            font-size: 16px;
            font-weight: 600;
            color: #4A4A4A;
            margin-top: 20px;
            margin-bottom: 10px;
        }}
        
        /* 段落 */
        p {{
            text-align: justify;
            text-indent: 2em;
            margin-bottom: 12px;
            font-size: 14px;
        }}
        
        /* 高亮文本 */
        .highlight {{
            color: #8B0000;
            font-weight: 600;
            text-indent: 0;
            margin: 15px 0;
        }}
        
        /* 列表 */
        .content-list {{
            margin-left: 2em;
            margin-bottom: 15px;
        }}
        
        .content-list li {{
            margin-bottom: 8px;
            font-size: 14px;
        }}
        
        /* 分隔线 */
        .divider {{
            border: none;
            border-top: 1px solid #ccc;
            margin: 20px 0;
        }}
        
        /* 页脚 */
        .footer {{
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #8B0000;
            font-size: 12px;
            color: #666;
        }}
        
        .footer p {{
            text-indent: 0;
            margin-bottom: 5px;
        }}
        
        /* 打印优化 */
        @media print {{
            body {{
                background: #f5f0e8;
                padding: 20px;
            }}
        }}
    </style>
</head>
<body>
    <div class="page-border">
        {''.join(html_body)}
        
        <div class="footer">
            <p>永乐小典 · 一东 · 互联网</p>
            <p>解缙奉敕编纂 · 公元二〇〇〇年后之新学</p>
        </div>
    </div>
</body>
</html>'''
    
    with open(output_html, 'w', encoding='utf-8') as f:
        f.write(html_template)
    
    print(f"HTML 已生成: {output_html}")
    return output_html

async def html_to_pdf(html_file, pdf_file):
    """使用 Playwright 将 HTML 转换为 PDF"""
    from playwright.async_api import async_playwright
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        # 加载 HTML 文件
        await page.goto(f'file://{os.path.abspath(html_file)}')
        
        # 等待字体加载
        await page.wait_for_timeout(2000)
        
        # 生成 PDF
        await page.pdf(
            path=pdf_file,
            format='A4',
            print_background=True,
            margin={
                'top': '0mm',
                'right': '0mm', 
                'bottom': '0mm',
                'left': '0mm'
            }
        )
        
        await browser.close()
    
    print(f"PDF 已生成: {pdf_file}")

def main():
    if len(sys.argv) < 2:
        print("用法: python yongle_html_pdf.py <input.md> [output.pdf]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    if len(sys.argv) >= 3:
        output_file = sys.argv[2]
    else:
        output_file = input_file.replace('.md', '.pdf')
    
    # 生成 HTML
    html_file = input_file.replace('.md', '.html')
    create_html(input_file, html_file)
    
    # 生成 PDF
    import asyncio
    asyncio.run(html_to_pdf(html_file, output_file))
    
    # 可选：删除临时 HTML 文件
    # os.remove(html_file)
    
    print(f"\n完成！输出文件: {output_file}")

if __name__ == '__main__':
    main()
