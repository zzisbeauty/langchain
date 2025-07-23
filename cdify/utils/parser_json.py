def extract_and_concat_content(data_dict, debug=False):
    try:
        # 检查 records 是否存在
        records = data_dict.get("records")
        if not isinstance(records, list):
            if debug:
                print("错误：'records' 字段缺失或不是列表")
            return ""

        # 提取每个 record 中 segment 的 content
        contents = []
        for idx, item in enumerate(records):
            if not isinstance(item, dict):
                if debug:
                    print(f"第 {idx} 项不是字典")
                continue

            segment = item.get("segment")
            if not isinstance(segment, dict):
                if debug:
                    print(f"第 {idx} 项中 'segment' 字段缺失或不是字典")
                continue

            content = segment.get("content")
            if not isinstance(content, str):
                if debug:
                    print(f"第 {idx} 项中 'content' 字段缺失或不是字符串")
                continue

            contents.append(content)

        # 拼接所有 content
        return "".join(contents)

    except Exception as e:
        if debug:
            print(f"解析出错: {e}")
        return ""