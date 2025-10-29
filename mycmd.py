import cmd
from search import *
from tdt3_data import totaltext, transtext
import shutil
from pathlib import Path

# MyCLI 类
class MyCLI(cmd.Cmd):
    prompt = 'test> '
    
    def __init__(self):
        super().__init__()
        self.indexer = None  # 初始化索引器
        self.index_dir = "indexdir"
        

    def do_build(self, arg):
        """按指定路径文件构建索引"""
        if not arg:
            if Path(self.index_dir).exists():
                print("未输入参数但索引文件已存在，加载已有文件")
                self.indexer = WhooshIndexer(index_dir=self.index_dir)
            else:
                print("请输入索引的文件路径")
                return
        else:                                   # 加载文档并构建索引
            print(f"从指定路径{arg}加载该文件")
            documents = totaltext(arg)
            self.indexer = WhooshIndexer(index_dir=self.index_dir)
            self.indexer.add_documents(documents)
            print("索引构建完成")

    def do_search(self, arg):
        """执行查询"""
        if not self.indexer:
            print("请先构建索引")
            return
        # 解析查询参数
        args = arg.split(" ")
        hits = 10
        query =" ".join(args)

        if len(args) > 2 and args[-2] == "-h":
            hits = int(args[-1]) 
            query = " ".join(args[:-2])  # 查询字符串
        
        # 对查询进行处理
        query_str = query
        results = self.indexer.query_top_bm25f(query_str, top_n=hits)
        import time
        start_time = time.time()
        results = self.indexer.query_top_bm25f(query_str, top_n=hits)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"q = {query_str}, took {elapsed_time:.4f} seconds")
        print('-'*73)
        for i in range(len(results)):
            result = results[i]
            print(f"|NO: {i + 1}\t\t\t\t|score: {result['score']:.4f}\t\t\t\t|")
            print('-'*73)
            print(f"|docno: {result['docno']} | doctype: {result['doctype']}\t| txttype: {result['txttype']}\t|")
            print('-'*73)
            print(result['text'][:200]+'...')
            print('-'*73)


    def do_show(self, arg):
        print(f"索引目录：{self.index_dir}")

    def do_exit(self, arg):
        """退出程序"""
        print("退出程序")
        if Path(self.index_dir).exists() and arg:
            shutil.rmtree(self.index_dir)  # 删除目录及其子目录
            print("索引已清除")
        else:
            print("默认保留当前索引")
        return True  

    def do_help(self, arg):
        """帮助信息"""
        print("""
        Available commands:
        build [path]                - 构建索引; path为可选参数,数据集的路径
        search <word> [-h hits]     - 查询; h为可选参数,规定返回结果条数
        show                        - 展示当前数据集特征
        exit [-d]                   - 退出程序; d为可选参数,删除索引文件
        """)

if __name__ == '__main__':
    cli = MyCLI()
    cli.cmdloop()