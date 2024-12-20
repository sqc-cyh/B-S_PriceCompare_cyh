这是BS体系软件设计项目商品比价网站的仓库，其中包含了docker以及前后端的相关代码。

## Project setup
1. 首先克隆仓库到本地
```git
git clone https://github.com/sqc-cyh/B-S_PriceCompare_cyh/.git
```

2. 在根目录下运行`docker-compose up`进行部署

3. 打开本地浏览器并通过localhost访问8080端口即可访问网站内容

## Bug solve
以下是一些可能出现的运行bug：

* 镜像拉取失败：
    1. mysql:8.0
    2. python:3.12
    前往docker官网拉取镜像即可
    ![alt text](./img/image.png)

* 爬虫时edgedriver相关报错：
    在backend的`Dockerfile`中解除以下注释，获取linux版本的edgedriver并配置到docker的`/usr/local/bin/`路径中：
    ```dockerfile
    # RUN apt-get update && apt-get install -y libgl1 unzip
    # RUN wget https://msedgedriver.azureedge.net/132.0.2957.48/edgedriver_linux64.zip\
    #     && unzip edgedriver_linux64.zip -d /usr/local/bin/ \
    #     && chmod +x /usr/local/bin/msedgedriver \
    #     && echo "Download successful"
    ```
    如果仍存在报错，请检查浏览器版本是否与edgedriver驱动版本一致。

## 附录
* 关于git管理：由于个人疏忽，直到快完成项目才从任务要求中看到需要使用git管理以展示项目的修改流程。目前只能通过一些其他方法跟踪本地的历史修改记录，以下是一些历史版本的证明：
    1. vscode中文件的创建和修改日期截图：
        * 文件创建日期在10月11日：
            ![alt text](./img/image-1.png)
        * 在10月11日到三周前（11月24日）一直有修改
            ![alt text](./img/image-3.png)
        * 最后修改日期在12月9日：
            ![alt text](./img/image-2.png)
    2. 后通过vscode的历史文件夹找到相关代码的历史版本记录，路径如下：`C:\Users\金银白黑红\AppData\Roaming\Code\User\History\`，但由于该文件夹下保存的各个文件都是通过16进制代码保存：
            ![alt text](./img/image-4.png)
        因此只能通过人肉查找里面哪些文件对应源代码中哪些文件的历史记录，我将部分找到的较为重要的文件的历史记录保存在了仓库的历史记录文件夹中，可以进行修改日期以及内容的查看。
    
   