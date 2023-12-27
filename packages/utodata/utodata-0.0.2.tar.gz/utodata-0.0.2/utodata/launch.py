from utodata.dataset import TrainDataset


class DataEngine:
    @staticmethod
    def sync_dataset(input_dir):
        dataset = TrainDataset(input_dir=input_dir)
        response = dataset.sync_data()
        if not response or response["code"] != 200:
            print("请求失败: ", response)
            exit(1)
        print("请求成功: ", response)
        exit(0)