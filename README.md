# About The Project

[![Build Status](https://travis-ci.com/dev-J-Ariza/moniter_bus.svg?token=oXwGPfT7t3rxFMeiYgjs&branch=main)](https://travis-ci.com/dev-J-Ariza/moniter_bus)
[![codecov](https://codecov.io/gh/dev-J-Ariza/moniter_bus/branch/main/graph/badge.svg?token=ZM7LQUISZ6)](https://codecov.io/gh/dev-J-Ariza/moniter_bus)

- 这个项目是为了获取北京公交的公开信息，例如所有的公交线路，某个公交线路的所有站点，以及某线路的实时公交。
- 这个项目的成品是一个python package，导入这个这个package，就可以获取这些信息。
- 这个项目参考了github上的两个开源项目（链接在后面）

![screenshot](/screenshot.png)

实时公交到站情况：

![实时公交到站图片](/real_time_bus.png)



## Quick start

1. Clone the repo
   ```sh
   git clone https://github.com/github_username/repo_name.git
   ```
   
2. 安装依赖
   ```python 
    pip install -r requirements
   ```
3. 在你的.py中
   ```python
    from moniter_bus import bus
   
    bus.print_help()    # 查看使用帮助
    bus.get_station(509) # 获取某条线路
    bus.get_all_buses() # 获取所有线路
    bus.get_real_time_bus(509) # 获取这条线路上的实时公交到站情况
   ```

# Reference 参考
- [Harpsichord1207 / BeiJingRealBus](https://github.com/Harpsichord1207/BeiJingRealBus.git)
  
- [Python实现命令行监控北京实时公交之一](https://segmentfault.com/a/1190000014324320)

- [Zoutianjian/Beijing_Bus_realtime_query](https://github.com/Zoutianjian/Beijing_Bus_realtime_query)


# License

Distributed under the MIT License. 
