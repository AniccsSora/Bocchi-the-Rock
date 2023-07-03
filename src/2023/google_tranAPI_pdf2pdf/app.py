import PyPDF2
from google.cloud import translate_v2 as translate
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.ttfonts import TTFont


margin_x = 20  # 水平邊距
margin_y = 20  # 垂直邊距
# 計算可用的列印區域
width, height = A4
available_width = width - 2 * margin_x
available_height = height - 2 * margin_y

# 每行文字的高度
line_height = 14  # 可根據需要調整

# 讀取 PDF 文件
with open('iso-iec9899.pdf', 'rb') as f:
    reader = PyPDF2.PdfReader(f)
    translate_client = translate.Client()

    # text = reader.pages[0].extract_text()  # 只讀取第一頁

    c = canvas.Canvas("iso-iec9899_output.pdf", pagesize=A4)

    # 在創建Canvas物件之後，設定所需的字體
    # 設定中文字型
    font_path = "NotoSansMonoCJKtc-VF.ttf"  # 字型文件的路徑
    font_name = "NotoSansMonoCJKtc"  # 字型名稱，可以自行指定
    pdfmetrics.registerFont(TTFont(font_name, font_path))

    for page_num in range(len(reader.pages)):
        text = reader.pages[page_num].extract_text()  # 只讀取某一頁
        fff = text.split('\n')
        translation = translate_client.translate(fff, target_language='zh-tw')

        # 當前繪製的文字位置
        x = margin_x
        y = height - margin_y

        # 設定字形
        c.setFont(font_name, 12)

        each_line_h = available_height // len(translation)
        for line in translation:
            t_text = line['translatedText']
            # debug show
            # print(t_text)
            #
            c.drawString(x, y, t_text)

            # 更新文字位置
            y -= each_line_h
        c.showPage()

        # 測試時記得開啟
        # if page_num >= 2:
        #     break
c.save()
