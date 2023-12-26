import os

remote_data = [
    {
        "name": '测试',
        "childer": [
            {
                'name': '哈哈.text',
                "file_path": 'https://www.baidu.com'
            },
            {
                'name': '李四.text',
                "file_path": 'https://www.baidu.com'
            },
            {
                "name": '测试',
                "childer": [
                    {
                        "name": '测试文件.txt',
                        "file_path": 'https://www.baidu.com'
                    }
                ]
            }
        ]
    }
]

def check_file(path):
    if os.path.isdir(path):
        return False
    else:
        return True

def update_files(remote_data, parent_path):
    contents = os.listdir(parent_path)
    for item in contents:
        is_file = check_file(os.path.join(parent_path, item))
        flag = False
        if is_file:
            for i in remote_data:
                if i['name'] == item and i.get('file_url'):
                    flag = True
            if not flag:
                os.remove(os.path.join(parent_path, item))
        else:
            for i in remote_data:
                if i['name'] == item and not i.get('file_url'):
                    flag = True
                res_path = i.get('childer', [])
                update_files(res_path, os.path.join(parent_path, item))
            if not flag:
                os.rmdir(os.path.join(parent_path, item))
update_files(remote_data, 'D:\course')