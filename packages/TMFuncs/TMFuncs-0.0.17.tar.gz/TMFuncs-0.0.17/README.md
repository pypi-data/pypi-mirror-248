> 这里介绍如何通过自定义代码，上传到pypi，以供Databricks加载外部库使用。
> 下面以本项目中notebook/wheels为例说明操作过程。
> 后续可以搭建私有PyPi仓库。

# 1. 前置依赖

## 1.1 包安装以及升级

    pip install twine
    python -m pip install --user --upgrade setuptools wheel

## 1.2 注册pypi

提前在 [pypi](https://pypi.org) 上注册账户，并验证邮箱。


# 2. 创建程序代码

## 2.1 创建项目

该步骤略，具体功能自定义。项目中包含如下程序结构：

    TMFuncs
        __init__.py
        batch_read.py
        op_log.py

## 2.2 修改 __init__.py 文件

在文件中，写入如下代码：

    from .batch_read import *
    from .op_log import *
    
    name = 'TMFuncs'


# 3. 创建setup所需文件

## 3.1 setup.py

在项目的**平行**目录下（即与TMFuncs处于相同目录），创建 setup.py，写入如下代码：

    from setuptools import setup, find_packages
    
    with open("README.md", "r") as fh:
        long_description = fh.read()
    
    setup(name='TMFuncs',
          version='0.0.1',
          description='Databricks common functions, written by TrueMetrics.',
          long_description=long_description,
          long_description_content_type="text/markdown",
          url='https://www.truemetrics.cn/',
          author='TSO',
          author_email='tlsong@truemetrics.cn',
          packages=find_packages(),
          classifiers=[
              "Programming Language :: Python :: 3.9",
              "License :: OSI Approved :: MIT License",
              "Operating System :: OS Independent",
          ],
          )

其中：
 - name是包的分发名称。只要包含字母，数字_和，就可以是任何名称-。它也不能在pypi.org上使用。请务必使用您的用户名更新此内容，因为这可确保您在上传程序包时不会遇到任何名称冲突。
 - version 是包版本看 PEP 440有关版本的更多详细信息。
 - author并author_email用于识别包的作者。
 - description 是一个简短的，一句话的包的总结。
 - long_description是包的详细说明。这显示在Python Package Index的包详细信息包中。在这种情况下，加载长描述README.md是一种常见模式。
 - long_description_content_type告诉索引什么类型的标记用于长描述。在这种情况下，它是Markdown。
 - url是项目主页的URL。对于许多项目，这只是一个指向GitHub，GitLab，Bitbucket或类似代码托管服务的链接。
 - packages是应包含在分发包中的所有Python 导入包的列表。我们可以使用 自动发现所有包和子包，而不是手动列出每个包。
 - classifiers告诉索引并点一些关于你的包的其他元数据。在这种情况下，该软件包仅与Python 3兼容，根据MIT许可证进行许可，并且与操作系统无关。您应始终至少包含您的软件包所使用的Python版本，软件包可用的许可证以及您的软件包将使用的操作系统。有关分类器的完整列表，请参阅[https://pypi.org/classifiers/](https://pypi.org/classifiers/)。

除了这里提到的还有很多。有关详细信息，请参阅 打包和分发项目。

## 3.2 README.md

这里是自定义的说明，markdown格式，根据需求撰写。

## 3.3 LICENSE

上传到Python Package Index的每个包都包含许可证，这一点很重要。这告诉用户安装你的软件包可以使用您的软件包的条款。有关选择许可证的帮助，请访问 [https://choosealicense.com/](https://choosealicense.com/)。


# 4. 项目打包及上传

## 4.1 打包项目

现在从setup.py位于的同一目录运行此命令：

    python setup.py sdist bdist_wheel

> 如果您在安装它们时遇到问题，请参阅 [安装包教程](https://link.zhihu.com/?target=https%3A//packaging.python.org/tutorials/installing-packages/)

此命令应输出大量文本，一旦完成，应在dist目录中生成两个文件：

    dist/
      TMFuncs-0.0.1-py3-none-any.whl
      TMFuncs-0.0.1.tar.gz


## 4.2 上传 PYPI

在该项目命令行下输入

    twine upload dist/*

然后输入注册时的用户名和密码即可。成功后，会输出如下信息：

    Uploading distributions to https://upload.pypi.org/legacy/
    Enter your username: tonysong
    Enter your password: gbu00pF7!^gZkoUl$DWo6iy&m2XSAjjL
    Uploading TMFuncs-0.0.1-py3-none-any.whl
    100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 7.2/7.2 kB • 00:01 • ?
    WARNING  Error during upload. Retry with the --verbose option for more details.
    100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 6.5/6.5 kB • 00:00 • ?
    
    View at:
    https://pypi.org/project/TMFuncs/0.0.1/
