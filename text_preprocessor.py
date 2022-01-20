import os
import re
import time
from dataclasses import dataclass

from base import BaseTextProcessor, BaseDataAccess

"""
全局变量
"""
# 检索文件的相对路径
dataset_path = "hyatt-k"


@dataclass
class Document():
    """
    文件内容及地址
    """
    id: str #文件ID（相对地址）
    content: str #文件内容


class TEXTPreprocessor(BaseTextProcessor):
    """

    """

    def __init__(self) -> None:
        self._dataset = dataset_path
        self._docs = []  # 单个文件列表

        super().__init__()


    def run(self):
        """
        第一次读取数据
        解析多层文件夹下文件，存储相对路径
        读取单个文本内容，对应文本ID
        文本预处理操作
        """

        start_parsing = time.perf_counter()  # 返回性能计数器的值（以分秒为单位）
        #全部文件路径，包含多层文件
        text_files = []
        for root, dirs, files in os.walk(dataset_path):
            for name in files:
                text_files.append(os.path.join(root, name))#每个文件的相对路径，从hyatt—k开始
        #输出文件相对路径ID
        # for item in text_files:
        #     print(item)

        # 返回一个由文件名和目录名组成的列表
        for text in text_files:
            text_content = self.data.read(text, encoding='latin-1')#读取文件内容
            document = Document(text, text_content)
            self._docs.append(document)

        end_parsing = time.perf_counter()
        print(f"\033[36m[Done]文件内容读取完毕，用时 {end_parsing - start_parsing:0.4f} 秒\033[0m")

        for doc in self._docs:  # 进行base中的预处理
            self._text = doc.content
            self.case_folding()
            self.punctuation_remove()
            self.num_remove()
            doc.content = self._text

        end_preprocess = time.perf_counter()
        print(f"\033[36m[Done]文件预处理完毕，用时 {end_preprocess - end_parsing:0.4f} 秒\033[0m")

    @property
    def docs(self):
        """
        返回文件列表
        """
        return self._docs
