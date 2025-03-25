import re
import urllib.parse
from pathlib import Path


def custom_quote(url, safe='/'):
    # 定义不需要编码的字符，除了默认的'/'外，还可以添加其他字符
    # 注意：这里我们特意不将中文字符加入到safe中，因为我们想保留它们
    # 但是通过手动控制哪些字符被编码，我们可以达到保留中文的目的

    # 首先对url进行标准的quote操作
    quoted_url = urllib.parse.quote(url, safe=safe)

    # 然后恢复中文字符部分
    # 这里假设url中只有中文字符是我们想要保留且不在safe中的
    # 实际应用中可能需要更复杂的逻辑来识别和处理中文
    for char in url:
        if '\u4e00' <= char <= '\u9fff':  # 判断是否为中文字符
            quoted_url = quoted_url.replace(urllib.parse.quote(char), char)

    return quoted_url


md_h1_pattern = re.compile(r'^#\s+(.*)$')


def extract_h1_titles(file_path: Path) -> list[str]:
    h1_titles = []
    with file_path.open('r', encoding='utf-8') as file:
        for line in file:
            match = md_h1_pattern.match(line)
            if match:
                h1_titles.append(match.group(1))
    return h1_titles
