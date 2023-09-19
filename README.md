## 一、框架介绍

本框架是基于Python+Pytest+Playwright+BDD的UI自动化测试框架。

* git地址: [https://gitlink.org.cn/floraachy/uiautotest_playwright.git](https://gitlink.org.cn/floraachy/uiautotest_playwright.git)
* 项目参与者: floraachy
* 个人主页： [https://www.gitlink.org.cn/floraachy](https://www.gitlink.org.cn/floraachy)
* 测试社区地址:  [https://www.gitlink.org.cn/zone/tester](https://www.gitlink.org.cn/zone/tester)
* 入群二维码：[https://www.gitlink.org.cn/floraachy/apiautotest/issues/1](https://www.gitlink.org.cn/floraachy/apiautotest/issues/1)

对于框架任何问题，欢迎联系我！

## 二、实现功能
- 支持通过命令行指定浏览器，选择需要运行的浏览器。
- 支持通过命令行指定运行环境，实现环境一键切换，解决多环境相互影响问题。
- 采用loguru管理日志，可以输出更为优雅，简洁的日志
- 钉钉、企业微信通知: 支持多种通知场景，执行成功之后，可选择发送钉钉、或者企业微信、邮箱通知
- 使用pipenv管理虚拟环境和依赖文件，可以使用pipenv install一键安装依赖包。

## 三、依赖库
```
pytest = "==6.2.5"
requests = "==2.26.0"
loguru = "*"
pytest-rerunfailures = "*"
faker = "*"
yagmail = "*"
pywinauto = "*"
allure-pytest = "*"
requests-toolbelt = "*"
pytest-bdd = "*"
sttable = "*"
playwright = "*"
pytest-playwright = "*"
```

## 四、安装教程
1. 通过Git工具clone代码到本地 或者 直接下载压缩包ZIP
```
https://gitlink.org.cn/floraachy/uiautotest_playwright.git
```

2. 本地电脑搭建好 python环境，我使用的python版本是3.9


3. 安装pipenv
```
# 建议在项目根目录下执行命令安装
pip install pipenv
```

4. 使用pipenv管理安装环境依赖包：pipenv install （必须在项目根目录下执行）
```
   注意：使用pipenv install会自动安装Pipfile里面的依赖包，该依赖包仅安装在虚拟环境里，不安装在测试机。
```
如上环境都已经搭建好了，包括框架依赖包也都安装好了。

## 五、如何创建用例
### 1. 修改配置文件  `config.settings.py`
1）确认RunConfig的各项参数，可以调整失败重跑次数`rerun`， 失败重跑间隔时间`reruns_delay`，当达到最大失败数，停止执行`max_fail`
2）确认测试完成后是否发送测试结果，由SEND_RESULT_TYPE控制，并填充对应邮件/钉钉/企业微信配置信息
3）指定日志收集级别，由LOG_LEVEL控制


### 2. 修改全局变量，增加测试数据  `config.global_vars.py`
1) ENV_VARS["common"]是一些公共参数，如报告标题，报告名称，测试者，测试部门。后续会显示在测试报告上。如果还有其他，可自行添加
2）ENV_VARS["test"]是保存test环境的一些测试数据。ENV_VARS["live"]是保存live环境的一些测试数据。如果还有其他环境可以继续增加，例如增加ENV_VARS["dev"] = {"host": "", ......}

### 3. 删除框架中的示例用例数据
1）删除 `test_cases`目录下所有`test`开头的文件
2）删除`test_features`目录下所有文件
注意：如果想先体验一下框架，可以先保留我写的示例用例。

### 4. 编写测试用例
#### 1. 在`test_features`目录新建一个`.feature`文件，按照BDD模式编写测试用例


#### 2. 基于`.feature`文件， 在 `test_cases`目录下新建一个`test_*py`文件，实现测试用例

此处需要对BDD知识有一定的了解，可以参考文章：[Pytest-BDD行为驱动开发测试](https://www.gitlink.org.cn/zone/tester/newdetail/301)


## 六、运行自动化测试
### 1.  激活已存在的虚拟环境
- （如果不存在会创建一个）：pipenv shell （必须在项目根目录下执行）

### 2. 运行
```
在pycharm>terminal或者电脑命令窗口，进入项目根路径，执行如下命令（如果依赖包是安装在虚拟环境中，需要先启动虚拟环境）。
  > python run.py  (默认在test环境运行测试用例, 报告采用allure)
  > python run.py -m demo 在test环境仅运行打了标记demo用例， 默认报告采用allure
  > python run.py -env live 在live环境运行测试用例
  > python run.py -env=test 在test环境运行测试用例
  > python run.py -browser webkit 使用webkit浏览器运行测试用例
  > python run.py -browser chromium webkit 使用chromium和webkit浏览器运行测试用例
```
注意：
- 如果pycharm.interpreter拥有了框架所需的所有依赖包，可以通过pycharm直接在`run.py`中右键运行

## 七 、、初始化项目可能遇到的问题
- [测试机安装的是python3.7，但是本框架要求3.9.5，怎么办？](https://www.gitlink.org.cn/zone/tester/newdetail/245)
- [无法安装依赖包或者安装很慢，怎么办？](https://www.gitlink.org.cn/zone/tester/newdetail/244)