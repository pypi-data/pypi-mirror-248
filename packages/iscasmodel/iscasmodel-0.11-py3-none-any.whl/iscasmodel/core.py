import os
import shutil
import urllib.request
import urllib.parse
import zipfile
from accelerate_iscas.utils import calculate_maximum_sizes


class ModelUtils:

    def __init__(self):
        self.svc_ip = os.getenv("svc_ip")
        self.model_id = os.getenv("model_id")
        self.dataset_id = os.getenv("dataset_id")
        self.user_id = os.getenv("user_id")
        self.modelApi = os.getenv("modelApi")
        # self.gitAddr = os.getenv("git_addr")
        self.memory = os.getenv("memory")
        self.batch = os.getenv("batch")
        self.mutilType = os.getenv("mutil_ype")

    # 发送准确率
    def send_acc(self, acc):
        data = {'modelId': self.model_id, "acc": acc}
        data = urllib.parse.urlencode(data).encode('utf-8')
        address = f"http://{self.svc_ip}:8080/train/addAcc"
        req = urllib.request.Request(url=address, data=data, method='POST')
        response = urllib.request.urlopen(req)
        # 根据需要，你可以添加处理响应或错误的代码。

    # 发送验证准确率
    def sent_validation_acc(self, acc):

        data = {'modelId': self.model_id, "validationAccuracy": acc}
        data = urllib.parse.urlencode(data).encode('utf-8')
        address = "http://" + self.svc_ip + ":8080/model/addValidationAcc"
        req = urllib.request.Request(url=address, data=data, method='POST')
        response = urllib.request.urlopen(req)
        print('Accuracy:', acc, '%')

    # 获得数据集地址
    def get_dataset_path(self):
        return f"/dataset/{self.user_id}/{self.dataset_id}"

    # 获得验证时需要的api地址
    def get_validation_url(self):
        return self.modelApi

    # 保存模型结果
    def save_result(self, *source_files):
        destination_path = '/result'
        zip_filename = f"/download/{self.model_id}/results.zip"

        # 确保/download/model_id目录存在
        model_id_path = os.path.join('/download', self.model_id)
        if not os.path.exists(model_id_path):
            os.makedirs(model_id_path)

        # 创建一个新的zip文件
        with zipfile.ZipFile(zip_filename, 'w') as zipf:
            for source_file in source_files:
                # 将文件复制到/result目录
                shutil.copy2(source_file, destination_path)
                # 将文件加入到zip包中
                zipf.write(os.path.join(destination_path, os.path.basename(source_file)), os.path.basename(source_file))

    def model_memory_usage(self, model, batch_size):
        if self.memory is not None:
            if self.batch is not None:
                batch_size = self.batch
                return batch_size
            else:
                return batch_size

        total_size, largest_layer = calculate_maximum_sizes(model)
        DTYPE_MODIFIER = {"float32": 1, "float16/bfloat16": 2, "int8": 4, "int4": 8}

        data = []

        dtype_total_size = total_size
        dtype_largest_layer = largest_layer[0]

        modifier = DTYPE_MODIFIER["float32"]
        dtype_total_size /= modifier
        dtype_largest_layer /= modifier

        # batch_size = 16

        # print(dtype_total_size)
        # dtype_training_size = convert_bytes()
        dtype_training_size = round(((dtype_total_size * 4 * batch_size) / (1024 ** 3)), 2)

        # dtype_total_size = convert_bytes(dtype_total_size)
        # dtype_largest_layer = convert_bytes(dtype_largest_layer)
        # data.append(
        #     {
        #         "dtype": "float32",
        #         "Largest Layer or Residual Group": dtype_largest_layer,
        #         "Total Size": dtype_total_size,
        #         "Training using Adam": dtype_training_size,
        #     }
        # )
        #
        # print(data)
        data = {'modelId': self.model_id, "memory": dtype_training_size}
        data = urllib.parse.urlencode(data).encode('utf-8')
        address = f"http://{self.svc_ip}:8080/train/memory"
        req = urllib.request.Request(url=address, data=data, method='POST')
        response = urllib.request.urlopen(req)
        return batch_size
