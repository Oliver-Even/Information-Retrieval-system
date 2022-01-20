from typing import List
from inverted_intex import InvertedIndex
from base import BaseTextProcessor


class QueryProcessor:
    def __init__(self) -> None:

        # 第一次创建倒排索引，加载倒排索引
        self._index = InvertedIndex()

        # 不能加载则进行创建
        if not self._index.load():
            self._index.build()

        # 创建文本处理器处理词项
        self._preprocessor = BaseTextProcessor()

        # 定义布尔检索操作符
        self._operands = ["AND", "OR", "NOT"]

    def process(self, q) -> List:
        """
        用于解析和运行查询的处理函数
        查询内容作为输入
        """

        q = self._preprocess(q)

        bag = [] #分隔后的词项文档ID
        q_tokens = q.split()
        operand = None

        for token in q_tokens:
            if token in self._operands:
                if not bag:#操作符开头，前面没有词项
                    print("\033[31m请输入正确检索内容，没有词项无法进行布尔检索!\033[0m")
                    exit()
                operand = token#操作符
            else:
                bag.append(self._index.get(token.casefold()))#得到文档ID
                if len(bag) > 1 and operand != None:#含有操作符
                    sub_result = self._operation(bag, operand)
                    if sub_result == None:
                        exit()
                    bag.append(sub_result)
                elif len(bag) > 2 and operand == None:#操作符错误
                    print("\033[31m请输入正确检索内容，操作符错误!\033[0m")
                    exit()

        return bag.pop()

    def _preprocess(self, q) -> str:
        """
        用于在处理之前预处理检索内容
        """
        self._preprocessor._text = q
        self._preprocessor.punctuation_remove()
        self._preprocessor.num_remove()

        return self._preprocessor._text

    def _operation(self, bag, operand) -> List:
        """
        布尔检索
        进行操作子操作
        返回结果列表
        """
        #pop(0)处理队列(FIFO)
        if operand == 'AND':
            return self._index.merge(bag.pop(0), bag.pop(0))
        elif operand == 'OR':
            return self._index.union(bag.pop(0), bag.pop(0))
        elif operand == 'NOT':
            return self._index.difference(bag.pop(0), bag.pop(0))
        else:
            print("\033[31m错误操作符!\033[0m")
            return None
