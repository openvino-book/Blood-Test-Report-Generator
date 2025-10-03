from PIL import Image, ImageDraw, ImageFont
import os
import datetime
import random

class BloodReportGenerator:
    def __init__(self, width=1000, height=1800):
        self.width = width
        self.height = height
        self.margin = 50
        self.line_height = 50
        self.bg_color = "white"
        self.text_color = "black"
        self.table_line_color = "black"

        # 字体检测（Windows 优先）
        font_candidates = [
            r"C:\Windows\Fonts\msyh.ttc",   # 微软雅黑
            r"C:\Windows\Fonts\simhei.ttf", # 黑体
            r"C:\Windows\Fonts\arial.ttf",  # Arial
        ]
        self.font_path = next((f for f in font_candidates if os.path.exists(f)), None)
        if not self.font_path:
            raise RuntimeError("没有找到可用字体，请检查 Windows 字体目录")

        print("使用字体：", self.font_path)

        # 字体大小
        self.title_font = ImageFont.truetype(self.font_path, 50)
        self.header_font = ImageFont.truetype(self.font_path, 28)
        self.text_font   = ImageFont.truetype(self.font_path, 26)
        self.small_font  = ImageFont.truetype(self.font_path, 22)

        # 25 项血常规指标 (参考范围)
        self.data_template = [
            ("白细胞计数 WBC", "10^9/L", 3.5, 9.5),
            ("红细胞计数 RBC", "10^12/L", 4.3, 5.8),
            ("血红蛋白 HGB", "g/L", 130, 175),
            ("红细胞压积 HCT", "%", 40, 50),
            ("平均红细胞体积 MCV", "fL", 80, 100),
            ("平均血红蛋白含量 MCH", "pg", 27, 34),
            ("平均血红蛋白浓度 MCHC", "g/L", 320, 360),
            ("红细胞体积分布宽度 RDW-CV", "%", 11, 16),
            ("血小板计数 PLT", "10^9/L", 125, 350),
            ("平均血小板体积 MPV", "fL", 7.5, 11.5),
            ("血小板分布宽度 PDW", "%", 10, 18),
            ("大血小板比率 P-LCR", "%", 13, 43),
            ("中性粒细胞比率 NEUT%", "%", 40, 75),
            ("中性粒细胞绝对值 NEUT#", "10^9/L", 1.8, 6.3),
            ("淋巴细胞比率 LYM%", "%", 20, 50),
            ("淋巴细胞绝对值 LYM#", "10^9/L", 1.1, 3.2),
            ("单核细胞比率 MONO%", "%", 3, 10),
            ("单核细胞绝对值 MONO#", "10^9/L", 0.1, 0.6),
            ("嗜酸细胞比率 EOS%", "%", 0.5, 5),
            ("嗜酸细胞绝对值 EOS#", "10^9/L", 0.02, 0.5),
            ("嗜碱细胞比率 BASO%", "%", 0, 1),
            ("嗜碱细胞绝对值 BASO#", "10^9/L", 0, 0.06),
            ("红细胞分布宽度 SD-RDW", "fL", 35, 56),
            ("血沉 ESR", "mm/h", 0, 15),
            ("C反应蛋白 CRP", "mg/L", 0, 8),
        ]

    def random_value(self, low, high):
        """生成带轻微异常的随机值"""
        # 大部分在正常范围内，少数超过范围
        if random.random() < 0.8:
            return round(random.uniform(low, high), 2)
        else:
            shift = (high - low) * random.uniform(0.2, 0.5)
            if random.random() < 0.5:
                return round(low - shift, 2)  # 偏低
            else:
                return round(high + shift, 2)  # 偏高

    def generate_one(self, patient_name="张三", output_path="blood_report.png"):
        # 创建画布
        img = Image.new("RGB", (self.width, self.height), self.bg_color)
        draw = ImageDraw.Draw(img)

        # ===== 报告单标题 =====
        title_text = "血 常 规 检 验 报 告 单"
        draw.text((self.width//2 - 250, 40), title_text, fill=self.text_color, font=self.title_font)

        # ===== 病人基本信息 =====
        patient_info = [
            f"姓名: {patient_name}", "性别: 男", "年龄: " + str(random.randint(18,70)),
            f"病员号: {random.randint(10000,99999)}", "科室: 门诊抽血室", "标本: 静脉血"
        ]
        for i, text in enumerate(patient_info):
            draw.text((self.margin, 120 + i*30), text, fill=self.text_color, font=self.small_font)

        # 报告时间
        report_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        draw.text((self.width-400, 120), f"送检时间: {report_time}", fill=self.text_color, font=self.small_font)
        draw.text((self.width-400, 160), f"报告时间: {report_time}", fill=self.text_color, font=self.small_font)

        # ===== 表头 =====
        headers = ["序号", "项目名称", "结果", "单位", "参考值", "提示"]
        col_widths = [70, 280, 160, 120, 220, 120]  # 每列宽度
        col_x = [self.margin]
        for w in col_widths:
            col_x.append(col_x[-1] + w)

        y_start = 320
        for i, header in enumerate(headers):
            draw.text((col_x[i] + 5, y_start), header, fill=self.text_color, font=self.header_font)
        draw.line((self.margin, y_start+40, col_x[-1], y_start+40), fill=self.table_line_color, width=2)

        # ===== 数据填充 =====
        y = y_start + 60
        for idx, (name, unit, low, high) in enumerate(self.data_template, 1):
            value = self.random_value(low, high)
            tip = ""
            if value < low:
                tip = "↓"
            elif value > high:
                tip = "↑"
            row = (str(idx), name, str(value), unit, f"{low}-{high}", tip)
            for i, val in enumerate(row):
                draw.text((col_x[i] + 5, y), val, fill=self.text_color, font=self.text_font)
            y += self.line_height
            draw.line((self.margin, y-10, col_x[-1], y-10), fill="#999", width=1)

        # ===== 底部说明 =====
        draw.text((self.margin, self.height-120), "检验者: 李技师", fill=self.text_color, font=self.small_font)
        draw.text((self.margin+300, self.height-120), "审核者: 曹大夫", fill=self.text_color, font=self.small_font)
        draw.text((self.margin, self.height-80), "本报告仅对本次送检标本负责", fill=self.text_color, font=self.small_font)

        # 保存
        img.save(output_path)
        print(f"报告已生成：{output_path}")

    def generate_batch(self, n=5, output_dir="reports"):
        """批量生成 N 个报告"""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        for i in range(1, n+1):
            name = f"病人{i}"
            file_path = os.path.join(output_dir, f"report_{i}.png")
            self.generate_one(patient_name=name, output_path=file_path)
        print(f"批量生成完成，共 {n} 份报告，目录: {output_dir}")

if __name__ == "__main__":
    generator = BloodReportGenerator()
    # 生成单个报告
    # generator.generate_one(patient_name="张三", output_path="report_single.png")

    # 批量生成 10 个报告
    generator.generate_batch(n=10, output_dir="batch_reports")
