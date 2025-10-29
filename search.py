# 2025-10-28
# 本文件的作用
# 1.构建索引
# 2.提供两种查询

import os
from whoosh import index
from whoosh.fields import Schema, TEXT, ID
from whoosh.analysis import StemmingAnalyzer
from whoosh.qparser import QueryParser
from whoosh.scoring import BM25F


class WhooshIndexer:
    def __init__(self, index_dir="indexdir"):
        self.index_dir = index_dir
        self.schema = Schema(
            docno=ID(stored=True),  # 文档编号
            doctype=TEXT(stored=True),  # 文档类型
            txttype=TEXT(stored=True),  # 文本类型
            text=TEXT(analyzer=StemmingAnalyzer(), stored=True)  # 文本内容
        )
        if not os.path.exists(self.index_dir):
            os.mkdir(self.index_dir)
        # 创建Whoosh索引
        if not index.exists_in(self.index_dir):
            self.ix = index.create_in(self.index_dir, self.schema)
        else:
            self.ix = index.open_dir(self.index_dir)


    def add_documents(self, documents):
        writer = self.ix.writer()
        from tqdm import tqdm  # 导入 tqdm
        # 使用 tqdm 显示加载进度条
        for doc in tqdm(documents, desc="Adding documents", unit="doc"):
            # 从字典中提取字段信息
            docno = doc.get("docno")
            doctype = doc.get("doctype")
            txttype = doc.get("txttype")
            text = doc.get("text")
            # 将文档添加到索引中
            writer.add_document(docno=docno, doctype=doctype, txttype=txttype, text=text)
        writer.commit()

    def query_top_bm25f(self, query_str, top_n):
        field_weights = {
            "docno": 0.1,     # 文档编号权重
            "doctype": 0.2,   # 文档类型权重
            "txttype": 0.2,   # 文本类型权重
            "text": 2.0       # 文本内容权重（可以设置较高的权重）
        }
        # 使用BM25F评分模型
        searcher = self.ix.searcher(weighting=BM25F(field_weights = field_weights))
        # 使用Whoosh的QueryParser解析查询字符串
        query_parser = QueryParser("text", schema=self.schema)
        query = query_parser.parse(query_str)
        # 执行查询，按BM25F评分返回前top_n个结果
        results = searcher.search(query, limit=top_n)
        # 构建查询结果列表
        result_list = [
            {
                "docno": result['docno'],
                "doctype": result['doctype'],
                "txttype": result['txttype'],
                "text": result['text'],
                "score": result.score
            } 
            for result in results
            ]
        return result_list
    


