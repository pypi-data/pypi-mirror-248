import math
import numpy as np
import torch
import torch.nn as nn

__all__ = ["autopad",]

def autopad(kernel, padding=None, dilation=1):
    """自动计算填充大小，以使输出具有与输入相同的形状
    :param k: kernel
    :param p: padding
    :param d: dilation
    :return: 自动计算得到的填充大小
    """
    k, p, d = kernel, padding, dilation
    if d > 1:
        k = d * (k - 1) + 1 if isinstance(k, int) else [d * (x - 1) + 1 for x in k]  # actual kernel-size
    if p is None:
        p = k // 2 if isinstance(k, int) else [x // 2 for x in k]  # auto-pad
    return p


def _make_divisible(v, divisor, min_value=None):
    """
    此函数取自TensorFlow代码库.它确保所有层都有一个可被8整除的通道编号
    在这里可以看到:
    https://github.com/tensorflow/models/blob/master/research/slim/nets/mobilenet/mobilenet.py
    通过四舍五入和增加修正，确保通道编号是可被 divisor 整除的最接近的值，并且保证结果不小于指定的最小值。
    """
    if min_value is None:
        min_value = divisor
    new_v = max(min_value, int(v + divisor / 2) // divisor * divisor)
    # 确保四舍五入的下降幅度不超过10%.
    if new_v < 0.9 * v:
        new_v += divisor
    return new_v








