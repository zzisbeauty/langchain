import requests
import time
import json
import os



# 请求参数
url = "http://10.0.15.21:5627/hanwei/docProcess"  # 替换成你的真实地址
payload = {
    "dataset_id": "2252d06e-b335-46e2-bec7-c47101e65072",
    "batch": "20250702073600105213"
}

# 日志路径
log_file_path = "./cdify/utils/loggers/temp.log"

# 已记录的状态集合
logged_status_set = set()

# 如果日志存在，初始化已记录的值
if os.path.exists(log_file_path):
    with open(log_file_path, "r", encoding="utf-8") as f:
        for line in f:
            status = line.strip().split("indexing_status:")[-1].strip()
            logged_status_set.add(status)

def log_status_if_new(status_value):
    if status_value not in logged_status_set:
        with open(log_file_path, "a", encoding="utf-8") as f:
            f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] indexing_status: {status_value}\n")
        logged_status_set.add(status_value)

def poll_doc_process():
    while True:
        try:
            response = requests.post(url, json=payload, timeout=10)
            if response.status_code == 200:
                resp_json = response.json()
                data_list = resp_json.get("data", {}).get("data", [])
                if data_list:
                    indexing_status = data_list[0].get("indexing_status")
                    if indexing_status:
                        log_status_if_new(indexing_status)
                        print(f"[✓] 当前 indexing_status: {indexing_status}")
            else:
                print(f"[!] 请求失败，状态码: {response.status_code}")
        except Exception as e:
            print(f"[X] 请求异常: {e}")
        time.sleep(20)  # 每 20 秒轮询一次





if __name__ == "__main__":
    poll_doc_process()
