import os
from query_processor import QueryProcessor

if __name__ == "__main__":

    qp = QueryProcessor()

    while True:
        # 输入检索词项
        query = input("\033[34m请输入要查询的内容 (布尔检索操作符：AND，OR，NOT，输入q退出系统): \033[0m")
        # 输入q结束
        if query != 'q':
            print("\033[34m检索结果: \033[0m")
            for item in sorted(qp.process(query)):# 对结果按照文档名称进行排序
                print(item)
        else:
            break
