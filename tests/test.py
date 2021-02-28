# -*- coding: utf-8 -*-
# @Time      : 2021/2/22 17:39
# @Author    : JianjinL
# @eMail     : jianjinlv@163.com
# @File      : test
# @Software  : PyCharm
# @Dscription: 测试文件

import os
import tensorflow as tf
from configs.config import params
from crnn.metrics import Accuracy
from crnn.losses.ctc_loss import CTCLoss
from crnn.data.postprocess.decode import Decoder
from crnn.data.preprocess.dataset_preprocess import Preprocess
from tests.accuracy import acc

def test(param):
    # 构建训练集
    dataset = Preprocess(param)
    ds, labels = dataset.build_test()
    # 加载模型
    model_path = os.path.join(param['save_path'], "crnn_{0}.h5".format(str(param["test_epoch"])))
    model = tf.keras.models.load_model(model_path, compile=False)
    # 编译模型
    model.compile(
        optimizer=tf.keras.optimizers.Adam(param["learning_rate"]),
        loss=CTCLoss(),
        metrics=[Accuracy()]
    )
    # 查看模型结构
    model.summary()
    # 预测
    test_ds = next(iter(ds))
    result = model.predict(test_ds)
    decoder = Decoder(param)
    y_pred = decoder.decode(result, method='greedy')
    acc_1, acc_2 = acc(labels, y_pred)
    print("Predict: ", acc_1)
    print("Accuracy: ", acc_2)


if __name__ == '__main__':
    test(params)
