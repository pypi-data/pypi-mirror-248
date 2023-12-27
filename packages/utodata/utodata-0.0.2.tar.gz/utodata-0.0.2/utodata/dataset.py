import os
import json
import requests


class TrainDataset:
    """
    ENV: 数据集名称，描述，项目location，标签，TOKEN，disk_name,
    手填：input_dir


    {
    "inputDir": [
        "/数据闭环开发/数据迁移输入/bev_gt/5508_2023_11_04-18_44_41_raw_rtg穿行"
    ],
    "diskName": "minio_dataplatform",
    "batchName": "transfer_test1",
    "project": "AIVLJ",
    "wf_template_name": "data-transfer-only-wf",
    "metadata": {
        "dataName": "5508_2023_11_04-18_44_41_raw_rtg穿行-zjw",
        "type": "0",
        "location": "AIVLJ",
        "desc": "bevgt_data",
        "label": "1"
        }
    }
    """

    # env
    data_name = os.getenv("datasetname")
    desc = os.getenv("datasetdesc")
    location = os.getenv("datasetproject")
    label_str = os.getenv("datasetlabels")
    token = os.getenv("token")
    disk_name = os.getenv("folderpath")  # 本地盘符
    argo_env = os.getenv("argoenv", "dev")  # dev:测试  production:开发

    if data_name is None:
        print("null for datasetname")
        exit(1)
    if desc is None:
        print("null for datasetdesc")
        exit(1)
    if location is None:
        print("null for datasetproject")
        exit(1)
    if label_str is None:
        print("null for datasetlabels")
        exit(1)
    if token is None:
        print("null for token")
        exit(1)
    if disk_name is None:
        print("null for folderpath")
        exit(1)
    if argo_env is None:
        print("null for argoenv, use dev as default")
        argo_env = "dev"

    wf_template_name = "data-transfer-only-wf"
    data_type = "0"
    batch_name = f"trainingSet_{data_name}"

    def __init__(self, input_dir):
        # user input
        self.input_dir = [input_dir]

    def sync_data(self):

        params = {
            "inputDir": self.input_dir,
            "diskName": "api",
            "batchName": TrainDataset.batch_name,
            "project": TrainDataset.location,
            "wf_template_name": TrainDataset.wf_template_name,
            "metadata": {
                "dataName": TrainDataset.data_name,
                "type": TrainDataset.data_type,
                "location": TrainDataset.location,
                "desc": TrainDataset.desc,
                "label": TrainDataset.label_str,
                "token": TrainDataset.token,
                "diskName": TrainDataset.disk_name,
            }
        }

        print(f"请求参数: ", params)

        header = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {TrainDataset.token}",
            'Accept': '*/*',
        }

        url = "https://ad.saicmaxus.com/api/data_pipeline/batch/submit/"
        if TrainDataset.argo_env == "dev":
            url = "http://10.65.198.27:8008/api/data_pipeline/batch/submit/"

        try:
            res = requests.post(url=url, data=json.dumps(params), headers=header, verify=False)
            return res.json()
        except Exception as e:
            print(f"Error '{e}' when post request to {url}")
            return {}
