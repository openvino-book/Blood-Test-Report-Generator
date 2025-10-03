import random
from datetime import datetime, timedelta
from faker import Faker
import os
from PIL import Image, ImageDraw, ImageFont

class BloodReportGenerator:
    def __init__(self):
        self.fake = Faker('zh_CN')
        # A4横向尺寸
        self.width, self.height = 2480, 1748
        
        # 字体配置
        self.setup_fonts()
        
        # 严格定义项目信息 - 使用正确的医学标准
        self.projects_left = [
            (1, "WBC", "白细胞", "10^9/L", "4-10", self.generate_wbc),
            (2, "RBC", "红细胞", "10^12/L", "3.5-5.5", self.generate_rbc),
            (3, "HGB", "血红蛋白", "g/L", "110-160", self.generate_hgb),
            (4, "HCT", "红细胞压积", "%", "36-50", self.generate_hct),
            (5, "MCV", "红细胞平均体积", "fL", "82-100", self.generate_mcv),
            (6, "MCH", "平均血红蛋白量", "pg", "25-32", self.generate_mch),
            (7, "MCHC", "平均血红蛋白浓度", "g/L", "320-360", self.generate_mchc),
            (8, "PLT", "血小板", "10^9/L", "100-300", self.generate_plt),
            (9, "LYMPH%", "淋巴细胞比率", "%", "20-40", self.generate_lymph_percent),
            (10, "NEUT%", "中性细胞比率", "%", "50-70", self.generate_neut_percent),
            (11, "MONO%", "单核细胞比率", "%", "3-8", self.generate_mono_percent),
            (12, "EO%", "嗜酸性粒细胞比率", "%", "0.5-5", self.generate_eo_percent),
            (13, "BASO%", "嗜碱性粒细胞比率", "%", "0-1", self.generate_baso_percent)
        ]
        
        self.projects_right = [
            (14, "LYMPH#", "淋巴细胞数", "10^9/L", "0.8-4", self.generate_lymph),
            (15, "NEUT#", "中性细胞数", "10^9/L", "2-7", self.generate_neut),
            (16, "MONO#", "单核细胞", "10^9/L", "0-0.8", self.generate_mono),
            (17, "EO#", "嗜酸性粒细胞", "10^9/L", "0.05-0.5", self.generate_eo),
            (18, "BASO#", "嗜碱性粒细胞", "10^9/L", "0-0.1", self.generate_baso),
            (19, "RDW-CV", "红细胞分布宽度CV", "%", "10.9-15.4", self.generate_rdw_cv),
            (20, "RDW-SD", "红细胞分布宽度SD", "fL", "37-54", self.generate_rdw_sd),
            (21, "PDW", "血小板分布宽度", "fL", "9-17", self.generate_pdw),
            (22, "MPV", "平均血小板体积", "fL", "9-13", self.generate_mpv),
            (23, "PCT", "血小板压积", "%", "0.17-0.35", self.generate_pct),
            (24, "P-LCR", "大型血小板比率", "%", "13-43", self.generate_plcr),
            (25, "ESR", "血沉", "mm/h", "男：0-15", self.generate_esr)
        ]
    
    def setup_fonts(self):
        """设置字体"""
        try:
            font_paths = [
                "C:/Windows/Fonts/simsun.ttc",
                "C:/Windows/Fonts/msyh.ttc", 
                "C:/Windows/Fonts/simhei.ttf",
            ]
            
            font_path = None
            for path in font_paths:
                if os.path.exists(path):
                    font_path = path
                    break
            
            if font_path:
                print(f"使用字体: {font_path}")
                self.title_font = ImageFont.truetype(font_path, 48)
                self.header_font = ImageFont.truetype(font_path, 32)
                self.normal_font = ImageFont.truetype(font_path, 28)
                self.table_font = ImageFont.truetype(font_path, 26)
                self.small_font = ImageFont.truetype(font_path, 24)
            else:
                raise Exception("No Chinese font found")
                
        except Exception as e:
            print(f"字体加载失败: {e}")
            self.title_font = ImageFont.load_default()
            self.header_font = ImageFont.load_default()
            self.normal_font = ImageFont.load_default()
            self.table_font = ImageFont.load_default()
            self.small_font = ImageFont.load_default()
    
    def parse_reference_range(self, ref_str, gender="男"):
        """解析参考值范围"""
        # 处理性别特定的参考值
        if "：" in ref_str:
            if gender == "男" and "男" in ref_str:
                parts = ref_str.split("：")
                if len(parts) > 1:
                    ref_str = parts[1]
            elif gender == "女" and "女" in ref_str:
                parts = ref_str.split("：")
                if len(parts) > 1:
                    ref_str = parts[1]
            elif "：" in ref_str:
                # 如果没有明确性别，取通用值
                parts = ref_str.split("：")
                if len(parts) > 1:
                    ref_str = parts[1]
        
        if "-" in ref_str:
            try:
                low, high = map(float, ref_str.split("-"))
                return low, high
            except:
                return 0, 100
        return 0, 100
    
    def generate_value_with_variation(self, ref_str, gender="男", variation_chance=0.2):
        """生成值"""
        low, high = self.parse_reference_range(ref_str, gender)
        
        if low >= high:
            low, high = high, low
        
        if random.random() < variation_chance:
            if random.random() < 0.5:
                # 偏高
                return round(random.uniform(high * 1.05, high * 1.3), 2), 1
            else:
                # 偏低
                return round(random.uniform(low * 0.7, low * 0.95), 2), -1
        else:
            # 正常值
            return round(random.uniform(low * 0.98, high * 1.02), 2), 0
    
    # 项目生成函数 - 确保使用正确的单位
    def generate_wbc(self, gender="男"): return self.generate_value_with_variation("4-10", gender)
    def generate_rbc(self, gender="男"): return self.generate_value_with_variation("3.5-5.5", gender)
    def generate_hgb(self, gender="男"): return self.generate_value_with_variation("110-160", gender)
    def generate_hct(self, gender="男"): return self.generate_value_with_variation("36-50", gender)
    def generate_mcv(self, gender="男"): return self.generate_value_with_variation("82-100", gender)
    def generate_mch(self, gender="男"): return self.generate_value_with_variation("25-32", gender)
    def generate_mchc(self, gender="男"): return self.generate_value_with_variation("320-360", gender)
    def generate_plt(self, gender="男"): return self.generate_value_with_variation("100-300", gender)
    def generate_lymph_percent(self, gender="男"): return self.generate_value_with_variation("20-40", gender)
    def generate_neut_percent(self, gender="男"): return self.generate_value_with_variation("50-70", gender)
    def generate_mono_percent(self, gender="男"): return self.generate_value_with_variation("3-8", gender)
    def generate_eo_percent(self, gender="男"): return self.generate_value_with_variation("0.5-5", gender)
    def generate_baso_percent(self, gender="男"): return self.generate_value_with_variation("0-1", gender)
    def generate_lymph(self, gender="男"): return self.generate_value_with_variation("0.8-4", gender)
    def generate_neut(self, gender="男"): return self.generate_value_with_variation("2-7", gender)
    def generate_mono(self, gender="男"): return self.generate_value_with_variation("0-0.8", gender)
    def generate_eo(self, gender="男"): return self.generate_value_with_variation("0.05-0.5", gender)
    def generate_baso(self, gender="男"): return self.generate_value_with_variation("0-0.1", gender)
    def generate_rdw_cv(self, gender="男"): return self.generate_value_with_variation("10.9-15.4", gender)
    def generate_rdw_sd(self, gender="男"): return self.generate_value_with_variation("37-54", gender)
    def generate_pdw(self, gender="男"): return self.generate_value_with_variation("9-17", gender)
    def generate_mpv(self, gender="男"): return self.generate_value_with_variation("9-13", gender)
    def generate_pct(self, gender="男"): return self.generate_value_with_variation("0.17-0.35", gender)
    def generate_plcr(self, gender="男"): return self.generate_value_with_variation("13-43", gender)
    def generate_esr(self, gender="男"): 
        # 血沉有性别差异
        if gender == "男":
            return self.generate_value_with_variation("0-15", gender)
        else:
            return self.generate_value_with_variation("0-20", gender)
    
    def generate_patient_info(self):
        """生成患者信息"""
        gender = random.choice(["男", "女"])
        if gender == "男":
            name = self.fake.name_male()
        else:
            name = self.fake.name_female()
        
        return {
            "姓名": name,
            "病案": f"BA{random.randint(100000, 999999)}",
            "费别": random.choice(["医保", "自费", "公费"]),
            "标本编号": str(random.randint(30, 50)),
            "性别": gender,
            "申请科室": random.choice(["门诊抽血室", "急诊科", "内科", "外科"]),
            "送检医师": self.fake.name(),
            "条码编号": f"TM{random.randint(100000, 999999)}",
            "年龄": f"{random.randint(18, 80)}",
            "床号": f"{random.randint(1, 50)}-{random.randint(1, 10)}",
            "标本种类": "全血",
            "临床诊断": random.choice(["健康体检", "上呼吸道感染", "高血压", "糖尿病", "贫血待查"])
        }
    
    def get_text_size(self, text, font):
        """获取文本尺寸"""
        try:
            bbox = font.getbbox(text)
            return bbox[2] - bbox[0], bbox[3] - bbox[1]
        except:
            try:
                return font.getsize(text)
            except:
                return len(text) * 15, 25
    
    def draw_text(self, draw, text, position, font=None, color=(0, 0, 0)):
        """绘制文本"""
        if font is None:
            font = self.normal_font
        draw.text(position, text, font=font, fill=color)
    
    def create_report_image(self, patient_info, left_results, right_results):
        """创建报告单图片"""
        image = Image.new('RGB', (self.width, self.height), 'white')
        draw = ImageDraw.Draw(image)
        
        margin = 80
        y_position = margin
        
        # 标题
        title = "知己知医血常规报告单"
        title_width, title_height = self.get_text_size(title, self.title_font)
        self.draw_text(draw, title, ((self.width - title_width) // 2, y_position), self.title_font)
        y_position += title_height + 60
        
        # 患者信息 - 两列布局
        col_width = (self.width - 3 * margin) // 2
        left_x, right_x = margin, margin + col_width + 50
        line_height = 45
        
        # 左列信息
        left_info = [
            f"姓    名：{patient_info['姓名']}",
            f"病    案：{patient_info['病案']}",
            f"费    别：{patient_info['费别']}",
            f"标本编号：{patient_info['标本编号']}",
            f"性    别：{patient_info['性别']}",
            f"申请科室：{patient_info['申请科室']}",
            f"送检医师：{patient_info['送检医师']}"
        ]
        
        # 右列信息
        right_info = [
            f"条码编号：{patient_info['条码编号']}",
            f"年    龄：{patient_info['年龄']}",
            f"床    号：{patient_info['床号']}",
            f"标本种类：{patient_info['标本种类']}",
            f"临床诊断：{patient_info['临床诊断']}"
        ]
        
        # 绘制患者信息
        for i, line in enumerate(left_info):
            self.draw_text(draw, line, (left_x, y_position + i * line_height))
        
        for i, line in enumerate(right_info):
            self.draw_text(draw, line, (right_x, y_position + i * line_height))
        
        y_position += max(len(left_info), len(right_info)) * line_height + 80
        
        # 表格设置 - 增加列宽避免重叠
        col_widths = [160, 250, 120, 120, 140]
        left_table_start = margin
        right_table_start = self.width // 2 - 60
        
        # 绘制统一的表头（只绘制一次）
        headers = ["序号代码", "项目名称", "结果", "单位", "参考值"]
        
        # 左表表头
        x = left_table_start
        for i, header in enumerate(headers):
            self.draw_text(draw, header, (x, y_position), self.header_font)
            x += col_widths[i]
        
        # 右表表头
        x = right_table_start
        for i, header in enumerate(headers):
            self.draw_text(draw, header, (x, y_position), self.header_font)
            x += col_widths[i]
        
        y_position += 60
        
        # 表头分隔线
        draw.line([(margin, y_position), (self.width - margin, y_position)], fill='black', width=2)
        y_position += 40
        
        # 绘制表格内容
        max_lines = max(len(left_results), len(right_results))
        row_height = 42
        
        for i in range(max_lines):
            current_y = y_position + i * row_height
            
            # 左列项目
            if i < len(left_results):
                self.draw_table_row(draw, left_results[i], left_table_start, current_y, col_widths)
            
            # 右列项目
            if i < len(right_results):
                self.draw_table_row(draw, right_results[i], right_table_start, current_y, col_widths)
        
        y_position += (max_lines + 2) * row_height + 60
        
        # 底部信息
        report_time = datetime.now()
        modify_time = report_time - timedelta(hours=random.randint(1, 6))
        
        bottom_info = [
            f"修改时间：{modify_time.strftime('%Y-%m-%d %H:%M:%S')}",
            f"报告时间：{report_time.strftime('%Y-%m-%d %H:%M:%S')}",
            f"检验者：{self.fake.name()}",
            f"审核者：{self.fake.name()}",
            "",
            "备注：",
            "此结果仅对本样本负责！"
        ]
        
        for i, line in enumerate(bottom_info):
            self.draw_text(draw, line, (margin, y_position + i * line_height))
        
        return image
    
    def draw_table_row(self, draw, row_data, start_x, y, col_widths):
        """绘制表格行 - 箭头放在结果与单位中间"""
        seq, code, name, result, unit, ref, status = row_data
        x = start_x
        
        # 序号代码
        code_text = f"{seq} {code}"
        self.draw_text(draw, code_text, (x + 10, y), self.table_font)
        x += col_widths[0]
        
        # 项目名称
        self.draw_text(draw, name, (x + 10, y), self.table_font)
        x += col_widths[1]
        
        # 结果
        if isinstance(result, float):
            result_text = f"{result:.2f}"
        else:
            result_text = str(result)
        
        # 计算结果的宽度
        result_width, _ = self.get_text_size(result_text, self.table_font)
        result_x = x + (col_widths[2] - result_width) // 2 -20 # 结果居中
        self.draw_text(draw, result_text, (result_x, y), self.table_font)
        
        # 在结果和单位之间绘制箭头
        if status != 0:
            # 计算箭头位置 - 在结果列和单位列中间
            arrow_x = x + col_widths[2] - 30  # 结果列结束后向右偏移10px
            arrow_text = "↑" if status == 1 else "↓"
            self.draw_text(draw, arrow_text, (arrow_x, y), self.table_font)
        
        x += col_widths[2]
        
        # 单位
        unit_x = x + 10
        self.draw_text(draw, unit, (unit_x, y), self.table_font)
        x += col_widths[3]
        
        # 参考值
        self.draw_text(draw, ref, (x + 10, y), self.table_font)
    
    def generate_report(self, patient_count=1, output_dir="blood_reports"):
        """生成报告单"""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        for i in range(patient_count):
            patient_info = self.generate_patient_info()
            
            # 生成左列项目结果
            left_results = []
            for project in self.projects_left:
                seq, code, name, unit, ref, func = project
                value, status = func(patient_info['性别'])
                left_results.append((seq, code, name, value, unit, ref, status))
            
            # 生成右列项目结果
            right_results = []
            for project in self.projects_right:
                seq, code, name, unit, ref, func = project
                value, status = func(patient_info['性别'])
                right_results.append((seq, code, name, value, unit, ref, status))
            
            # 创建图片
            image = self.create_report_image(patient_info, left_results, right_results)
            
            # 保存图片
            filename = f"{output_dir}/血常规报告_{patient_info['姓名']}_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
            image.save(filename, dpi=(200, 200))
            
            print(f"已生成报告: {filename}")

# 使用示例
if __name__ == "__main__":
    generator = BloodReportGenerator()
    
    print("开始生成血常规报告单...")
    generator.generate_report(patient_count=3, output_dir="blood_reports")
    print("报告单生成完成！")