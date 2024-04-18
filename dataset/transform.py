import json

def transform_jsonl(input_file_path, output_file_path):
    # 打开原始的 JSONL 文件进行读取
    with open(input_file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    # 准备新的数据集
    transformed_data = []
    
    # 遍历每一行数据
    for line in lines:
        # 解析 JSON 数据
        data = json.loads(line)
        
        # 提取需要的字段
        instruction = data['instruction']
        input_text = data['instances'][0]['input']  # 假设每个任务只有一个实例
        output = data['instances'][0]['output']
        
        # 构建新的 JSON 对象
        transformed_entry = {
            'instruction': instruction,
            'input': input_text,
            'output': output
        }
        transformed_data.append(transformed_entry)
    
    # 打开输出文件，写入转换后的数据
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        for item in transformed_data:
            json_line = json.dumps(item) + '\n'
            output_file.write(json_line)

# 调用函数进行文件转换
input_file_path = 'seed_tasks_test.jsonl'
output_file_path = 'seed_transfromed.jsonl'
transform_jsonl(input_file_path, output_file_path)