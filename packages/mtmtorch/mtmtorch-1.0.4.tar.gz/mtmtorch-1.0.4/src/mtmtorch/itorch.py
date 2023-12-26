import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
from sklearn.model_selection import train_test_split

import random

# Set seed for reproducibility
def same_seeds(seed=0, reproducibility=False):
    # 参考链接: [Pytorch设置随机数种子，使训练结果可复现。](https://zhuanlan.zhihu.com/p/76472385)
    # 参考链接: [pytorch模型可复现设置(cudnn.benchmark 加速卷积运算 & cudnn.deterministic)(随机种子seed)(torch.backends)](https://blog.csdn.net/hxxjxw/article/details/1201601355)

    # Set the seed for all random generators.
    random.seed(seed)  # Python random module.
    np.random.seed(seed)  # Numpy module.
    torch.manual_seed(seed)

    # cuda 为 GPU 加速，如果可用，设置为固定种子
    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)  # if you are using multi-GPU.
    
    # 基于参数 reproducibility 的值，设置 torch.backends.cudnn.benchmark 和 torch.backends.cudnn.deterministic
    # https://pytorch.org/docs/stable/notes/randomness.html
    if reproducibility: # 使得每次运行结果相同，但降低模型推理速度
        torch.backends.cudnn.benchmark = False # 使用默认的确定性算法，保证每次卷积算法一致，加快速度，但不保证结果一致
        torch.backends.cudnn.deterministic = True # 保证每次结果一样，但是会降低速度
    else: # 不强求每次运行结果相同， 但提高模型推理速度
        torch.backends.cudnn.benchmark = True # 寻找最适合网络的卷积算法，选择最快的一个
        torch.backends.cudnn.deterministic = False # 不保证每次结果一样，但是会提高速度

same_seeds(0)