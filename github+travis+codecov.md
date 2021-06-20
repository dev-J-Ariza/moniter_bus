# Github集成Travis与CodeCov

## Travis、CodeCov简介

Travis是一个CI（持续集成）框架，使用它可以在每次提交自动对代码库进行测试、部署等工作，这些工作都可以通过自己写脚本定制。

CodeCov是用来统计单元测试代码覆盖率的，它的功能很多。 可以检测出每次提交的覆盖率变动，也可以检测出远程仓库或者本地分支整体的覆盖率。

~~另外，Travis对Github是免费的。~~ 并不是，free plan每个用户有10000个credits，每次build就得消耗10个。用完为止。。

后续会考虑迁移到Github自家的Github Action。

## 搭建环境

### 配置Travis
前提，要注册一个Github账号，在上面有某个repo。

打开[Travis官网](https://travis-ci.com)，同步Github上面的repo，然后打开开关，各种授权。

![screenshot](https://www.ruanyifeng.com/blogimg/asset/2017/bg2017121902.png)

到这为止，环境上的许可都有了，只剩下代码上的阻碍。

### 配置CodeCov
登录[CodeCov官网](codecov.io)，完成用户注册。

点击Repositories面板，点击Add new repository, 把Github上面的Repo添加进来。

最后，为了在CI脚本中上传代码覆盖率到CodeCov，我们需要一个CodeCov的token。这个token每个用户都可以生成多个，需要记录token的内容。

在CodeCov个人主页 -> Settings -> Access, 点击Generate Token.

## 编写Travis CI代码

要使用Travis作为CI工具，需要在项目根目录下新建一个```.travis.yml```文件，不需要其它额外的关联工作。
这个文件就是所有CI脚本的入口了， 然后你的每次提交就会在travis的环境中跑你的脚本。

Travis为不同语言的项目写了一些模板yml文件，具体可以参考[travis官方文档](https://docs.travis-ci.com/user/languages/python/) 。
原理都是一致的，这里简单介绍一下如何编写这个```.travis.yml```。

首先，```.travis.yml```里面有几个重要的入口，类似生命周期，它们是：
- before_install
- install
- before_script
- script
- after_success or after_failure
- [OPTIONAL] before_deploy
- [OPTIONAL] deploy
- [OPTIONAL] after_deploy
- after_script

我们可以在```before_install```里面做一些准备工作， 在```install```里面安装项目需要的requirements.txt.
在```script```里面完成CI的主要工作，比如各种检查（语法规范，代码覆盖率），生成文件（比如apk）以及你想干的其它事情。
在```deploy```里面做部署，把结果部署到服务器上。

**有一点值得注意**
Travis可以使用环境变量，也可以加密变量。 [Travis环境变量](https://docs.travis-ci.com/user/environment-variables/).
如果脚本中有敏感信息，不能直接明文写到Travis脚本中，可以使用加密后的环境变量。
步骤：
1. ```brew install travis```（或者gem install travis）
2. 在Github个人主页，进入Setting页面，进入Developer settings，进入Person Token，点击生成token
3. ```travis login --pro --github-token yourGitHubTokenHere```
4. cd到项目根目录，```travis encrypt MY_SECRET_ENV=super_secret --add env.global```

之后你就可以在脚本里面，通过 ${MY_SECRET_ENV} 代替之前的明文value了。

## 编写CodeCov代码
首先是[CodeCov的上传功能](https://docs.codecov.com/docs/about-the-codecov-bash-uploader) ，也就是在每次CI成功构建之后，将新的代码覆盖率上传到CodeCov。
CodeCov会自动接收项目中跟代码覆盖率有关的文件，这里使用pytest生成的xml文件。

## 完整的CI脚本

```shell
    env:
      global:
        secure: super_secret
        
    language: python
    before_install:
      - pip install -U pip
    install: bash ./coverage/install-dependencies.sh
    script: python -m pytest tests/ --cov=moniter_bus --cov-report xml:cov.xml
    after_success: bash <(curl -s https://codecov.io/bash) -t ${MY_SECRET_ENV}
    after_failure: pip list
```

## TODO

使用Travis.deploy和CodeCov的获取、diff功能。

## 参考

[ryf travis简介](http://www.ruanyifeng.com/blog/2017/12/travis_ci_tutorial.html)