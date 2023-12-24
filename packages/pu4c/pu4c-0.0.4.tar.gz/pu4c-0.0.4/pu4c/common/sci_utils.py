import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


def draw_hist(data_dict: dict, min, max, num_bins, 
              xticks=5, colormap=['blue', 'green', 'red'],
              input_hist=None, normlize=False, save_fname=None,
              title=None, xlabel=None, ylabel=None, figsize=None,
              ):
    """
    Args:
        data_dict: {图例: 直方图数据, ...}
        min, max, num_bins: 截断统计值(x 轴)的范围，以及柱子数量
        xticks: x 轴刻度数
        colormap: 柱子颜色
        normlize: 柱子高度为统计个数还是所占百分比
    值域闭括号 [min, max] 可取最值，xticks 根据 num_bins 的值计算，xticks 的值为真实值，并非均匀选取
    Example:
        hist = draw_hist({'arr': np.array([0,1,2,3,4,5,5,5,8,9])}, 0, 9, 10, xticks=10)
    """
    plt.clf()
    if figsize: plt.figure(figsize=figsize)
    
    x = np.linspace(min, max, num_bins)
    for i, (key, data) in enumerate(data_dict.items()):
        if input_hist:
            hist = data
        else:
            hist, bins = np.histogram(data, bins=num_bins, range=(min, max))
        if normlize: hist = hist / sum(hist) * 100
    
        dataframe = pd.DataFrame({'x':x, key:hist})
        sns.barplot(x='x', y=key, data=dataframe, color=colormap[i], alpha=0.5, label=key)

    # 设置 x 轴刻度显示
    show_ticks = xticks  # 设置要显示的刻度数量
    x_ticks = np.linspace(0, x.shape[0] - 1, show_ticks).astype(int)
    x_ticklabels = np.round(x[x_ticks])
    plt.xticks(x_ticks, x_ticklabels)
        
    if title: plt.title(title)
    if xlabel: plt.xlabel(xlabel)
    if ylabel: plt.ylabel(ylabel)
    
    plt.legend()
    if save_fname:
        plt.savefig(save_fname)
    else:
        plt.show()
    
    return hist