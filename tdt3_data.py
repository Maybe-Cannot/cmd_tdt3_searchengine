# 2025-10-28
# 本文件的作用：
# 从指定路径加载数据
# 统计相关信息
# 构建文档合集


from pathlib import Path

# 传入路径，返回路径下的可选文件
def textpath(root:str) -> list[str]:
    p = Path(root)
    if not p.exists():
        raise FileNotFoundError(f"路径不存在: {root}")
    if not p.is_dir():
        raise NotADirectoryError(f"不是目录: {root}")
    files: list[str] = []
    for child in p.iterdir():
        try:
            if child.is_dir():
                # 递归时传入子目录 Path 对象或字符串均可
                files += textpath(child)
            elif child.is_file():
                # 使用 resolve() 获取绝对路径并转为字符串
                files.append(str(child.resolve()))
        except PermissionError:
            # 忽略无权限访问的项
            continue
    return files

# 解析文件并返回格式化内容
def textcontent(path: str) -> dict:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"路径不存在: {path}")
    if not p.is_file():
        # 使用内置的 IsADirectoryError 来表示不是文件的错误
        raise IsADirectoryError(f"并非文件: {path}")
    # 读取文件内容并返回一个简单的字典：{"path": <绝对路径>, "content": <文本内容>}
    try:
        text = p.read_text(encoding="utf-8", errors="replace")
    except PermissionError:
        # 明确抛出权限错误，调用者可捕获并处理
        raise
    import re
    # print('='*10)
    dno = re.search(r"<DOCNO>\s*(.*?)\s*</DOCNO>", text, re.DOTALL)
    # print(dno)
    dtype = re.search(r"<DOCTYPE>\s*(.*?)\s*</DOCTYPE>", text, re.DOTALL)
    ctype = re.search(r"<TXTTYPE>\s*(.*?)\s*</TXTTYPE>", text, re.DOTALL)
    ct = re.search(r"<TEXT>\s*(.*?)\s*</TEXT>", text, re.DOTALL)
    s = {
        "path": str(path), 
        "docno": dno.group(1).strip(),
        "doctype": dtype.group(1).strip(),
        "txttype": ctype.group(1).strip(),
        "text": ct.group(1).strip()
        }
    return s
    

def totaltext(root:str) -> list[dict]:
    pt = textpath(root)
    doc = []
    for p in pt:
        doc.append(textcontent(p))
    return doc

def transtext(prompt:str) -> str:
    import re
    pattern = r'"(.*?)"'
    # 使用 re.sub 替换匹配的内容
    result = re.sub(pattern, r'{\1}', prompt)
    return result

if __name__ == "__main__":
    f = textpath(r"D:\code\lab\cmd_tdt3_searchengine\data\tdt3")
    print("文件:", f[:10],sep = "\n")
    t = textcontent(f[0])
    print(t)