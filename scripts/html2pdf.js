const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

async function htmlToPdf(htmlFile, pdfFile) {
    const browser = await puppeteer.launch({
        headless: 'new',
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    
    const page = await browser.newPage();
    
    // 读取 HTML 内容
    const htmlContent = fs.readFileSync(htmlFile, 'utf-8');
    
    // 设置内容
    await page.setContent(htmlContent, {
        waitUntil: 'networkidle0'
    });
    
    // 等待字体加载
    await new Promise(resolve => setTimeout(resolve, 3000));
    
    // 生成 PDF
    await page.pdf({
        path: pdfFile,
        format: 'A4',
        printBackground: true,
        margin: {
            top: '0mm',
            right: '0mm',
            bottom: '0mm',
            left: '0mm'
        }
    });
    
    await browser.close();
    console.log(`PDF 已生成: ${pdfFile}`);
}

// 主函数
const htmlFile = process.argv[2] || 'chapters/一东/互联网.html';
const pdfFile = process.argv[3] || htmlFile.replace('.html', '.pdf');

htmlToPdf(htmlFile, pdfFile).catch(console.error);
