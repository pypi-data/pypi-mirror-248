import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
import time
import warnings
import numpy as np
from torch.utils.tensorboard import SummaryWriter


class CommonTrainer:
    def __init__(self, log_dir: str = None, **kwargs):
        super().__init__()
        if log_dir is not None:
            writer_kwargs_keys = ["comment", "filename_suffix", "purge_step", "flush_secs", "max_queue"]
            writer_kwargs = {key: kwargs[key] for key in writer_kwargs_keys if key in kwargs}
            self.writer = SummaryWriter(log_dir=log_dir, **writer_kwargs)
        else:
            self.writer = None
        pass

    def split_datas(self, datas):
        inputs, targets = datas[:-1], datas[-1]  # 获取输入和目标
        return inputs, targets

    def calculate_loss(self, outputs, targets, criterion):
        # 计算损失
        # 在 outputs 和 targets 若为 tuple 且长度为 1 的情况下，取出其中的元素，进行计算
        if isinstance(outputs, tuple) and len(outputs) == 1:
            outputs = outputs[0]
        if isinstance(targets, tuple) and len(targets) == 1:
            targets = targets[0]
        loss = criterion(outputs, targets)
        return loss

    def train(
        self,
        model,
        train_loader: DataLoader,
        optimizer,
        criterion,
        scheduler=None,
        device: torch.device = None,
        **kwargs,
    ):
        # 获取迭代次数上限
        max_loader_len = len(train_loader)
        max_epoch = kwargs.get("max_epoch", None)
        max_iteraiton = kwargs.get("max_iteraiton", None)
        if max_epoch is None and max_iteraiton is None:
            raise ValueError("max_epoch and max_iteraiton cannot be both None")
        if max_epoch is None and max_iteraiton is not None:
            max_epoch = max_iteraiton // max_loader_len + 1

        # 获取要在哪个设备上运行, 默认为 cuda:0 或 cpu
        if device is None:
            device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

        # 设置模型为训练模式
        model.train()

        # 初始化损失列表
        loss_array = np.zeros(max_epoch * max_loader_len)
        loss_array[:] = np.nan

        # 中间变量
        t_start = time.time()
        n_samples = 0
        n_batches = 0
        flag_break = False
        outputs_list = []
        targets_list = []

        for epoch in range(1, max_epoch + 1):
            for idx, datas in enumerate(train_loader, 1):
                nums = datas[0].shape[0]  # 获取 此次 batch 的 大小
                datas = tuple([i.to(device) for i in datas])  # 将数据放到指定设备上

                # 分离输入和目标
                inputs, targets = self.split_datas(datas)

                # 优化器梯度清零
                optimizer.zero_grad()

                # 前向传播
                outputs = model(*inputs)

                # 计算损失
                loss = self.calculate_loss(outputs, targets, criterion)

                # 记录损失
                loss_array[n_batches] = loss.item()

                # 反向传播，计算梯度
                loss.backward()

                # 更新网络参数
                optimizer.step()

                # 更新中间变量
                n_samples += nums  # 更新已训练的样本数量
                n_batches += 1  # 更新已训练的batch数量
                outputs_list.append(outputs.cpu().detach().numpy())
                targets_list.append(targets.cpu().detach().numpy())

                # 退出条件
                if max_iteraiton is not None and n_samples >= max_iteraiton:
                    flag_break = True
                    break
            if flag_break:
                break

        # 更新学习率
        if scheduler is not None:
            scheduler.step()

        # 记录训练时间
        t_end = time.time()

        # 记录训练信息
        loss_array_real = loss_array[:n_batches]  # 获取真实的损失列表
        mean_loss = np.nanmean(loss_array_real)  # 计算平均损失
        infos = {
            "run_time": t_end - t_start,
            "iteration": n_samples,
            "epoch": epoch,
            "loss_array": loss_array_real,
            "mean_loss": mean_loss,
            "outputs": np.concatenate(outputs_list, axis=0),
            "targets": np.concatenate(targets_list, axis=0),
        }

        return infos

    def validate(self, model, validate_loader: DataLoader, criterion, device: torch.device = None, **kwargs):
        # 获取迭代次数上限
        max_loader_len = len(validate_loader)

        # 获取要在哪个设备上运行, 默认为 cuda:0 或 cpu
        if device is None:
            device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

        # 设置模型为评估模式
        model.eval()

        # 初始化损失列表
        loss_array = np.zeros(1 * max_loader_len)
        loss_array[:] = np.nan

        # 中间变量
        t_start = time.time()
        n_samples = 0
        n_batches = 0
        outputs_list = []
        targets_list = []

        with torch.no_grad():  # 不计算梯度
            for idx, datas in enumerate(validate_loader, 1):
                nums = datas[0].shape[0]  # 获取 此次 batch 的 大小
                datas = tuple([i.to(device) for i in datas])  # 将数据放到指定设备上

                # 分离输入和目标
                inputs, targets = self.split_datas(datas)

                # 前向传播
                outputs = model(*inputs)

                # 计算损失
                loss = self.calculate_loss(outputs, targets, criterion)

                # 记录损失
                loss_array[n_batches] = loss.item()

                # 更新中间变量
                n_samples += nums  # 更新已训练的样本数量
                n_batches += 1  # 更新已训练的batch数量
                outputs_list.append(outputs.cpu().detach().numpy())
                targets_list.append(targets.cpu().detach().numpy())
        # 记录训练时间
        t_end = time.time()

        # 记录训练信息
        loss_array_real = loss_array[:n_batches]  # 获取真实的损失列表
        mean_loss = np.nanmean(loss_array_real)  # 计算平均损失
        infos = {
            "run_time": t_end - t_start,
            "iteration": n_samples,
            "epoch": 1,
            "loss_array": loss_array_real,
            "mean_loss": mean_loss,
            "outputs": np.concatenate(outputs_list, axis=0),
            "targets": np.concatenate(targets_list, axis=0),
        }

        return infos

    def test(self, model, test_loader: DataLoader, criterion, device: torch.device = None, **kwargs):
        # 获取迭代次数上限
        max_loader_len = len(test_loader)

        # 获取要在哪个设备上运行, 默认为 cuda:0 或 cpu
        if device is None:
            device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

        # 设置模型为评估模式
        model.eval()

        # 初始化损失列表
        loss_array = np.zeros(1 * max_loader_len)
        loss_array[:] = np.nan

        # 中间变量
        t_start = time.time()
        n_samples = 0
        n_batches = 0
        outputs_list = []
        targets_list = []

        with torch.no_grad():  # 不计算梯度
            for idx, datas in enumerate(test_loader, 1):
                nums = datas[0].shape[0]  # 获取 此次 batch 的 大小
                datas = tuple([i.to(device) for i in datas])  # 将数据放到指定设备上

                # 分离输入和目标
                inputs, targets = self.split_datas(datas)

                # 前向传播
                outputs = model(*inputs)

                # 计算损失
                loss = self.calculate_loss(outputs, targets, criterion)

                # 记录损失
                loss_array[n_batches] = loss.item()

                # 更新中间变量
                n_samples += nums  # 更新已训练的样本数量
                n_batches += 1  # 更新已训练的batch数量
                outputs_list.append(outputs.cpu().detach().numpy())
                targets_list.append(targets.cpu().detach().numpy())

        # 记录训练时间
        t_end = time.time()

        # 记录训练信息
        loss_array_real = loss_array[:n_batches]  # 获取真实的损失列表
        mean_loss = np.nanmean(loss_array_real)  # 计算平均损失
        infos = {
            "run_time": t_end - t_start,
            "iteration": n_samples,
            "epoch": 1,
            "loss_array": loss_array_real,
            "mean_loss": mean_loss,
            "outputs": np.concatenate(outputs_list, axis=0),
            "targets": np.concatenate(targets_list, axis=0),
        }

        return infos

    def __del__(self):
        if self.writer is not None and isinstance(self.writer, SummaryWriter):
            self.writer.close()
        if hasattr(super(), "__del__"):
            super().__del__()
