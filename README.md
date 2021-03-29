# 搜索记录频繁模式挖掘

这是一个《大数据挖掘技术》@复旦课程项目，试图从搜狗实验室用户查询日志数据（2008）中找出搜索记录中有较高支持度关键词的频繁二项集。在实现层面上，我搭建了一个由五台服务器组成的微型 Hadoop 集群，并且用 Python 实现了 Parallel FP-Growth 算法中的三个 MapReduce 过程。

## 一、Demo

### 1.1 快速开始

请确保 Python 以及 jieba 中文分词库已安装。

若没有安装 jieba ，在命令行中：

```shell
pip install jieba # for python
pip3 install jieba # for python3
```

或者直接运行无 jieba 版本 `find_pair_nojieba.py`（会没有关键词近似匹配功能）。

不修改任何文件，运行 `.src/demo/find_pair.py`。

输入想要匹配的查询词即可。

### 1.2 自定义

将 MR3 的结果（所有 `part-*` 文件） 取回本地，存放在同一目录下（比如 `./result/res3/` ）。

修改 `./src/demo/combine_parts.py` 中的两个参数（输入文件目录和输出文件路径），然后运行 `./src/demo/combine_parts.py` ，即可合并所有的 `part-*` 文件。

然后将 `./src/demo/find_pair.py` 中的参数修改为刚才得到的合并结果的路径，运行 `./src/demo/find_pair.py`。

接下来输入想要查询的关键词，就会返回其频繁二项集。

## 二、频繁模式挖掘

请确保 Hadoop 集群已经完成配置并且工作正常。

以下的所有相对路径均以工程根目录为当前目录 `./` 。

### 2.1 建立工程目录

为了方便地直接按照默认参数运行预处理文件，请按照如下目录树建立一些空的 `data` 和 `log` 目录：

```text
./
|
+-- data/
|    |
|    +---- raw/ # 原始数据集文件目录
|    |      |
|    |      +-- SogouQ/ # 搜狗数据集原始文件目录
|    |
|    +---- temp/ # 临时文件目录，用于存放转码后的数据文件
|    |
|    +---- clean/ # 存放清洗后的数据文件
|    |
|    +---- BD_jieba/ # 存放关键词提取的结果，这也是第一个 MapReduce 的输入文件目录
|    |
|    +---- result/ # 存放分组结果，即 F-list 和 G-list
|
+-- log/ # 预处理输出日志目录
|
...
```

### 2.2 获取数据集

于搜狗实验室[https://www.sogou.com/labs/resource/q.php](https://www.sogou.com/labs/resource/q.php)下载数据集，请下载完整版数据集，因为三个大小的数据集的格式并不一致。

将下载得到的数据集中共 31 个文件解压到 `./data/raw/SogouQ` 中。

### 2.3 预处理

依次运行以下 Python 代码：

1. `./src/preprocess/gb2utf8.py`
2. `./src/preprocess/format_file_v2.py`
3. `./src/preprocess/to_db_jieba.py`

### 2.4 将数据上传至 HDFS

接下来将 `./data/DB_jieba` 目录下所有需要的文件上传到 HDFS 中。

首先从本地把数据文件上传到 Master 中，假设 Master 服务器（ `hadoop@master` ）中我们的工作目录为 `~/pj/` ，其中有 `data` 和 `src` 两个子目录。

```shell
scp ./data/DB_jieba/*.txt hadoop@master:~/pj/data/
```

然后在 Master 上将数据文件存入 HDFS：

```shell
hadoop fs -mkdir /pj
hadoop fs -mkdir /pj/data
hadoop fs -put ~/pj/data/*.txt /pj/data
```

可以通过

```shell
hadoop fs -ls /pj/data
```

确认文件是否上传成功。

### 2.5 上传源代码

将以下代码文件上传到 Master 的 `~/pj/src/` 目录下：

- `./src/mapper1.py`
- `./src/mapper3.py`
- `./src/reducer1.py`
- `./src/reducer2.py`
- `./src/reducer3.py`

然后在 Master 给予它们执行权限：

```shell
chmod +x ~/pj/src/*.py
```

### 2.6 运行 MR1: 并行计数

请确认 Hadoop Streaming `hadoop/share/hadoop/tools/lib/hadoop-streaming-{版本号}.jar` 的路径，此处以 `/home/hadoop/cluster/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.8.5.jar` 为例。

在 Master 上使用以下命令执行第一个 MapReduce:

```shell
yarn jar /home/hadoop/cluster/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.8.5.jar -file ~/pj/src/mapper1.py -file ~/pj/src/reducer1.py -mapper ~/pj/src/mapper1.py -reducer ~/pj/src/reducer1.py -input /pj/data/*.txt -output /pj/res1/
```

执行完毕后，首先在 Master 上将结果从 HDFS 中取出：

```shell
hadoop fs -get /pj/res1/part-* ./data/
```

然后在本地，将结果传回来：

```shell
scp hadoop@master:~/pj/data/part-* ./data/result/
```

### 2.7 项目分组

修改 `./src/sort_kv.py` 中主函数里 `sort_file()` 函数的第一个输入参数为上一步得到的结果的相对路径（如 `../data/result/part-00000` ），然后运行 `./src/sort_kv.py` 。

将得到的 `./data/result/G-list.json` 文件内容全部复制，粘贴为 `./src/mapper2.py` 中 `G-list` 变量的值。

然后上传 `./src/mapper2.py` 到 Master 的 `~/pj/src/` 目录下，并给予权限：

```shell
chmod +x ~/pj/src/mapper2.py
```

### 2.8 运行 MR2: 并行 FP-Growth

在 Master 上使用以下命令执行第二个 MapReduce:

```shell
yarn jar /home/hadoop/cluster/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.8.5.jar -D mapreduce.job.reduces=30 -file ~/pj/src/mapper2.py -file ~/pj/src/reducer2.py -mapper ~/pj/src/mapper2.py -reducer ~/pj/src/reducer2.py -input /pj/data/*.txt -output /pj/res2/
```

上述命令中 `-D mapreduce.job.reduces=N` 参数的 `N` 指的是要分配的 Reducer 数目，官方推荐数值为 (0.95 或 1.75) * 所有 Slave 节点总核数。比如对于 Slave 一共 32 核的集群，可以选择 30 （计算效率最高）或 56 （计算稳定性最好）。

### 2.9 运行 MR3: 汇总

在 Master 上使用以下命令执行第三个 MapReduce:

```shell
yarn jar /home/hadoop/cluster/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.8.5.jar -D mapreduce.job.reduces=30 -file ~/pj/src/mapper3.py -file ~/pj/src/reducer3.py -mapper ~/pj/src/mapper3.py -reducer ~/pj/src/reducer3.py -input /pj/res2/part-* -output /pj/res3/
```

若有需要可以将得到的结果按照类似 2.6 节的方法取回 Master 或本地。

## 三、项目文档

本项目的详细项目文档在[这里](https://github.com/CLDXiang/Mining-Frequent-Pattern-from-Search-History/blob/master/doc/%E6%90%9C%E7%B4%A2%E8%AE%B0%E5%BD%95%E9%A2%91%E7%B9%81%E6%A8%A1%E5%BC%8F%E6%8C%96%E6%8E%98.pdf)。

如果对您有帮助就请在右上角 Star 一下这个仓库吧~
