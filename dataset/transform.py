import json

def convert_jsonl_to_custom_format(input_file, output_file):
    # 打开输入文件和输出文件
    with open(input_file, 'r', encoding='utf-8') as infile, \
         open(output_file, 'w', encoding='utf-8') as outfile:
        
        # 创建一个空列表用于存储转换后的数据
        converted_data = []
        
        # 逐行读取JSONL数据
        for line in infile:
            # 将每行数据从JSON格式转换为Python字典
            data = json.loads(line)
            
            # 创建新的格式字典
            new_format = {
                "instruction": data["instruction"],
                "input": data["input"],  # 使用get来处理可选字段
                "output": data["output"],
            }
            
            # 将新格式的字典添加到列表中
            converted_data.append(new_format)
        
        # 将整个列表转换为JSON格式，并写入输出文件
        json.dump(converted_data, outfile, ensure_ascii=False, indent=2)

# 调用函数进行转换
convert_jsonl_to_custom_format('all_generated_instances.jsonl', 'data.json')