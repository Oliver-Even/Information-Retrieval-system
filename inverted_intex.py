import time
import pickle

from base import BaseInvertedIndex
import text_preprocessor as sp


class InvertedIndex(BaseInvertedIndex):
    """
    倒排索引的类以及布尔检索基础类
    形成、存储、加载倒排记录表
    布尔检索基础操作
    """

    def __init__(self) -> None:
        super().__init__()
        self.textp = sp.TEXTPreprocessor()

    def build(self):
        """
        形成倒排索引表
        """
        #第一次运行进行文本处理
        self.textp.run()

        start_building = time.perf_counter()

        for doc in self.textp.docs:
            #得到倒排记录表
            tokens = self.textp.tokenize(doc.content)
            tokens = list(set(tokens) - set(self.textp.stopwords))#去停用词
            #添加词项
            for token in tokens:
                self.add(token, doc.id)

        end_building = time.perf_counter()
        # 按照键值进行排序
        sorted_dictionary = sorted(self.dictionary.items(), key=lambda d: d[0], reverse=False)
        # 输出倒排记录表，每列一项
        for key, value in sorted_dictionary:
            print(str(key) + ": " + str(value))
        print(f"\033[36m[Done]倒排记录表建立成功，用时{end_building - start_building:0.4f} 秒\033[0m")
        #保存倒排记录表
        self.save()
    #保存倒排记录表
    def save(self):
        with open("dictionary.pkl", "wb") as f:#二进制写入文件
            pickle.dump(self.dictionary, f)
            f.close()
        print("\033[36m[Done]倒排记录表保存成功!\033[0m")
    #加载倒排记录表
    def load(self) -> bool:
        try:
            with open("dictionary.pkl", "rb") as f:#二进制读取倒排记录表
                self.dictionary = pickle.load(f)
                #按照键值进行排序
                sorted_dictionary = sorted(self.dictionary.items(), key=lambda d: d[0], reverse=False)
                #输出倒排记录表，每列一项
                for key, value in sorted_dictionary:
                    print(str(key) + ": " + str(value))

                f.close
            print("\033[36m[Done]倒排记录表加载成功！\033[0m")
            return True
        except(FileNotFoundError):
            print("\033[31m[FAIL]未找到倒排记录表！\033[0m")
            return False

    def merge(self, l, r):
        """
        为进行AND操作求取合并结果
        """
        #将指针和合并结果初始化为空列表
        #i 表示长列表的指针，j 表示短列表的指针
        i, j = 0, 0
        result = []

        short, long = (l, r) if len(l) < len(r) else (r, l)
        while i < len(long) and j < len(short):
            if long[i] == short[j]:
                result.append(long[i])
                j += 1
                i += 1
            elif long[i] > short[j]:
                j += 1
            else:
                i += 1

        return result

    def union(self, l, r):
        """
        为进行OR操作求取交结果
        """
        # 将指针和交结果初始化为空列表
        # i 表示长列表的指针，j 表示短列表的指针
        i, j = 0, 0
        result = []

        short, long = (l, r) if len(l) < len(r) else (r, l)
        #此循环遍历以短词项结束
        while i < len(long) and j < len(short):
            if long[i] <= short[j]:
                result.append(long[i])
                if long[i] == short[j]:
                    j += 1
                i += 1
            else:
                result.append(short[j])
                j += 1

        #仍然有长列表或短列表中的元素。这些剩余元素将添加到结果中
        return result + long[i:] + short[j:]

    def difference(self, l, r):
        """
        为进行NOT操作求取差结果
        """
        result = l.copy()

        for i in r:
            if i in result:
                result.remove(i)

        return result