"""
包含基本类和一些基本操作
"""
import os
import re
import string
from abc import abstractmethod
from typing import List

"""
全局变量
"""
# 停用词文档路径
stopword_path = "doctxt\\stopwords.txt"


class BaseDataAccess:
    """
    用于数据读/写操作的类
    """
    # 读文件
    def read(self, read_path, encoding='utf-8', mode='r'):
        """
        使用默认 utf-8 编码和 read（'r'） 模式从给定read_path读取数据。
        """
        # 系统路径加上文件相对路径
        with open(os.path.join(os.getcwd(), read_path), encoding=encoding, mode=mode) as f:
            data = f.read().replace('\n', ' ')
            # 将\n替换成空格
            f.close()
            # 返回文件内容
        return data


    # 写文件
    def write(self, data, write_path, mode='w'):
        """
        使用默认模式 write（'w） 将给定数据写入给定write_path。
        """
        # 系统路径加上文件相对路径
        with open(os.path.join(os.getcwd(), write_path), mode=mode) as f:
            f.write(data)
            f.close()


class BaseTextProcessor():
    """
    用于必要预处理的基本文本预处理类
    """

    def __init__(self) -> None:  # 返回类型None
        # 类的对象
        self.data = BaseDataAccess()
        self._text = None

    # 词项
    def tokenize(self, text=None) -> List[str]:
        """
        用于将字符串转换为词项的操作
        """
        if text:
            return text.split()  # 使用空字符分隔
        else:
            return self.text.split()

    # 去除标点符号
    def punctuation_remove(self):
        """
        去除文本中的标点符号，转换为空
        """
        to_remove = string.punctuation + "\n"  # 句子中的标点符号
        mapper = str.maketrans('', '', to_remove)
        self._text = self._text.translate(mapper)  # 替换为空

    # 去除文本中的数字
    def num_remove(self):
        """
        删除文本中数字，替换为空
        """
        self._text = re.sub(r'\d+',"",self._text)

    # 去除停用词
    @property
    def stopwords(self) -> List:
        """
        去除停用词，读取和拆分非索引字
        """
        return self.data.read(stopword_path).split() if stopword_path else None

    # 小写
    def case_folding(self):
        """
        将文本全部转换为小写字符
        """
        self._text = self._text.casefold()  # 变为小写
        # self._text = self._text.lower()


class BaseInvertedIndex:
    """
    倒排索引基本操作的基类。
    作为字典保存
    """

    def __init__(self) -> None:
        self.dictionary = {}

    # 返回文档ID
    def get(self, token) -> List:
        """
        返回指定键的值
        """
        value = self.dictionary.get(token)
        return value if value else []

    # 添加（词项，文档ID）
    def add(self, token, id) -> None:
        """
        将给定键值和value添加到字典中，即（词项，文档ID）
        """
        if token in self.dictionary.keys():
            self._insert(token, id)#字典中已出现词项
        else:
            self._update(token, [id])#字典中未出现词项

    # 更新字典
    def _update(self, key, value=[]) -> None:
        """
        使用给定的键值对字典进行更新
        （词项，文档ID）如果没有给出ID使用空列表初始化。
        """
        self.dictionary.update({key: value})

    def _insert(self, key, id) -> None:
        """
        对于已出现的词项在字典中进行插入其文档ID
        """
        posting = self.dictionary.get(key) # 查找显示应将此 ID 添加到的位置的索引

        start = 0
        end = len(posting) - 1

        while start <= end:
            middle = int((start + end) / 2)

            if posting[middle] > id:
                end = middle - 1
            else:
                start = middle + 1

        posting.insert(start, id)