import json
import os

import cv2
import time
import torch
import numpy as np
from PyQt6.QtWidgets import QProgressDialog
from weasyprint import HTML
from bs4 import BeautifulSoup
from PyQt6.QtCore import QRunnable, QDir, QObject, pyqtSignal

from frame_singleton import FrameListManager
from report_singleton import ReportListManager
from progress_singleton import ProgressValueManager



class FrameHandlePdf(QRunnable):
    def __init__(self, cap=None, model=None):
        super().__init__()
        self.frame = None
        self.cap = cap
        self.last_capture_pic_name = ""
        self.model = model
        self.frame_list_manager = FrameListManager()
        self.report_list_manager = ReportListManager()
        self.progress_value_manager = ProgressValueManager()



    def run(self):
        self.progress_value_manager.show_progress_dialog()
        try:
            self.generate_report()
        except:
            self.progress_value_manager.cancel_progress_dialog()
            pass

    def generate_report(self):
        self.load_case()

        now = int(time.time())
        timeArray = time.localtime(now)
        nowtime_str = time.strftime("%Y-%m-%d-%H-%M-%S", timeArray)
        year, month, day = nowtime_str.split('-')[:3]
        dataset_path = "output/dataset"
        capture_path = "output/capture"
        pdf_path = "output/pdf"

        self.progress_value_manager.set_progress_value(10)

        if not self.check_path_exist(pdf_path):
            os.makedirs(pdf_path)
        self.progress_value_manager.set_progress_value(20)

        frame_info = self.frame_list_manager.get_last_frame()
        if frame_info is None:
            raise Exception('未找到最新照片')

        self.last_capture_pic_name = frame_info[0]
        self.frame = frame_info[1]
        self.dframe = frame_info[2]

        self.progress_value_manager.set_progress_value(30)



        # 获取当天capture目录中保存的最新一张照片，用于生成pdf文件
        latest_jpg_file = capture_path + "/" + self.last_capture_pic_name
        print(f'latest_jpg_file:{latest_jpg_file}')

        self.progress_value_manager.set_progress_value(40)

        # 获取当天dataset目录中保存的最新一张照片，用于生成pdf文件
        latest_dataset_jpg_file = dataset_path + "/" + self.last_capture_pic_name
        print(f'latest_dataset_jpg_file:{latest_dataset_jpg_file}')

        self.progress_value_manager.set_progress_value(50)

        # 生成pdf文件名和保存路径
        pdf_file_name = self.replace_extension(os.path.basename(latest_jpg_file), 'pdf')
        pdf_file_path = pdf_path + "/" + pdf_file_name

        # 计算最新一张照片的概率
        score = self.classify_disease()
        # 生成最大值序列
        disease_probability_index = np.argsort(score)[::-1]

        self.progress_value_manager.set_progress_value(60)


        # 取最大概率名称
        name = self.disease_category_name[disease_probability_index[0]]
        # 取最大概率报告
        name = self.all_case_info_dict[name][0]['名称']
        report = self.all_case_info_dict[name][0]['分析结果']
        reason = self.all_case_info_dict[name][0]['原因']
        complication = self.all_case_info_dict[name][0]['影响']
        treatment = self.all_case_info_dict[name][0]['康养建议']

        # 指定 HTML 文件和输出的 PDF 文件名
        html_file = 'html/html2pdf.html'


        # 读取HTML文件并使用BeautifulSoup解析
        with open(html_file, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')

        self.progress_value_manager.set_progress_value(70)


        # 找到div_container标签
        div_container = soup.find('div', class_='div-container')

        # 创建两张图片标签
        img1 = soup.new_tag('img')
        img1['src'] = latest_dataset_jpg_file  # 替换为你的图片路径或URL
        img1['alt'] = 'real picture'  # 添加alt属性，描述图片内容（可选）

        # 对比图片文件
        case_path = "case"
        case_pic_path = case_path + "/" + name + ".jpg"
        img2 = soup.new_tag('img')
        img2['src'] = case_pic_path  # 替换为你的图片路径或URL
        img2['alt'] = 'contrast picture'  # 添加alt属性，描述图片内容（可选）

        # 将图片添加到div_container中
        div_container.append(img1)
        div_container.append(img2)

        # 找到div_result标签
        div_result = soup.find('div', class_='div-result')
        # 创建4段文本
        paragraph_1 = soup.new_tag('h3')
        paragraph_1.string = '分析结果:'
        content_1 = soup.new_tag('p')
        content_1.string = report

        paragraph_2 = soup.new_tag('h3')
        paragraph_2.string = '原因:'
        content_2 = soup.new_tag('p')
        content_2.string = reason

        paragraph_3 = soup.new_tag('h3')
        paragraph_3.string = '影响:'
        content_3 = soup.new_tag('p')
        content_3.string = complication

        paragraph_4 = soup.new_tag('h3')
        paragraph_4.string = '康养建议:'
        content_4 = soup.new_tag('p')
        content_4.string = treatment

        div_result.append(paragraph_1)
        div_result.append(content_1)
        div_result.append(paragraph_2)
        div_result.append(content_2)
        div_result.append(paragraph_3)
        div_result.append(content_3)
        div_result.append(paragraph_4)
        div_result.append(content_4)

        self.progress_value_manager.set_progress_value(80)

        # 将修改后的 HTML 转换回字符串
        modified_html = str(soup)

        self.progress_value_manager.set_progress_value(90)

        # 将 HTML 转换为 PDF
        HTML(string=modified_html, base_url='./').write_pdf(pdf_file_path)
        print(f'save pdf: {pdf_file_path}')

        # 把pdf长文件名写入列表
        self.report_list_manager.add_report(pdf_file_name)
        self.progress_value_manager.set_progress_value(100)

    def check_path_exist(self, path_s):
        return os.path.isdir(path_s)

    # 更换文件拓展名后缀
    def replace_extension(self, filename, new_extension):
        # 使用os.path.splitext()分割文件名和扩展名
        base_name, extension = os.path.splitext(filename)

        # 确保新的扩展名以'.'开头，如果不是，则添加它
        if not new_extension.startswith('.'):
            new_extension = '.' + new_extension

            # 重新组合文件名和新的扩展名
        new_filename = base_name + new_extension

        return new_filename

    def load_case(self):
        self.all_case_info_dict = {}
        self.disease_category_name = []
        self.disease_category_num = 0

        # 使用 Qt 的方式来遍历目录
        dir_path = QDir('case')
        entries = dir_path.entryInfoList(['*.json'], QDir.Filter.Files)

        for entry in entries:
            # 读取json文件
            filename = entry.absoluteFilePath()
            with open(filename, 'r', encoding='utf-8') as file:
                try:
                    case = json.load(file)
                except Exception as e:
                    print(f"Error loading {filename}: {e}")
                else:
                    keys = case.keys()
                    name = list(keys)[0]
                    self.all_case_info_dict[name] = case[name]

        # 所有病例名称列表
        self.disease_category_name = list(self.all_case_info_dict.keys())
        # 病例名称种类个数
        self.disease_category_num = len(self.disease_category_name)

    def classify_disease(self):
        self.frame = cv2.resize(self.frame, (0, 0), fx=0.25, fy=0.25, interpolation=cv2.INTER_NEAREST)
        target_img = torch.from_numpy(cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY).astype(np.float32).reshape((1, 1, 270, 480)))
        with torch.no_grad():
            self.model.eval()
            output = self.model(target_img)

            disease_probability = output.numpy()[0]
            disease_probability_index = np.argsort(disease_probability)[::-1]

            return disease_probability
