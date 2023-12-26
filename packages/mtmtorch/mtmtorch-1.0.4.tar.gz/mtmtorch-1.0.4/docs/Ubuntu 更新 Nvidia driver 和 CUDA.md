
# 0. 卸载 nvidia 驱动和 cuda
下面两行是卸载Ubuntu的Nvidia驱动，如果是其他系统，请自行查找卸载命令
```
apt-get remove --purge nvidia* # 卸载 nvidia 驱动
apt-get remove --purge "*cublas*" "cuda*" # 卸载 cuda
apt-get autoremove # 卸载不再需要的库
```
下面两行是卸载Nvidia官方安装的驱动和cuda
```
/usr/bin/nvidia-uninstall # 卸载 nvidia 驱动
/usr/local/cuda-11.8/bin/cuda-uninstaller # 卸载 cuda
```

# 1. 关闭 nouveau 模块
如果要安装nvidia官方驱动，需要关闭 nouveau 模块
```
lsmod | grep nouveau # 检查是否开启 nouveau 模块
```
具体关闭流程可查阅参考链接，使用nvidia驱动安装程序安装时也可自动添加配置文件去关闭nouveau（该次安装失败），再次重启后即可正式关闭nouveau
# 2. 杀死所有占用 nvidia 设备的进程，卸载 nvidia 模块
检查是否有进程占用 nvidia 设备，如果有，请全部kill
```
lsof -n -w /dev/nvidia* # 
```
卸载 nvidia 模块， 如果提示 nvidia 模块正在使用，可以根据提示卸载前置模块，如 nvidia_uvm
```
rmmod nvidia
```


# 3. 安装 nvidia 驱动
安装 cuda 和 driver
```
bash cuda_12.2.2_535.104.05_linux.run
```
界面中的X号表示选择该组件  

---
安装成功后输出以下内容

```
===========
= Summary =
===========

Driver:   Installed
Toolkit:  Installed in /usr/local/cuda-12.2/

Please make sure that
 -   PATH includes /usr/local/cuda-12.2/bin
 -   LD_LIBRARY_PATH includes /usr/local/cuda-12.2/lib64, or, add /usr/local/cuda-12.2/lib64 to /etc/ld.so.conf and run ldconfig as root

To uninstall the CUDA Toolkit, run cuda-uninstaller in /usr/local/cuda-12.2/bin
To uninstall the NVIDIA Driver, run nvidia-uninstall
Logfile is /var/log/cuda-installer.log
```

# 参考链接
- [nvidia-smi出现Failed to initialize NVML: Driver/library version mismatch的超级详细可靠解决方法而且不用重启)](https://blog.csdn.net/qq_41616600/article/details/131420684)
- [Ubuntu 卸载 Nvidia 驱动和安装最新驱动](https://blog.csdn.net/wm9028/article/details/110268030)