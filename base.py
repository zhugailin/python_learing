# ## 1.Python中Gevent的使用
# """
# 1、可以通过gevent轻松实现并发同步或异步编程。gevent中使用的主要模式是Greenlet，它是以C扩展模块的形式访问Python的轻量级协程。
# 2、Greenlet全部运行在主程序操作系统的过程中，但是它们是协作调度
# """
# from gevent import monkey # 为了能识别time模块的io
# monkey.patch_all()  #必须放到被打补丁者的前面，如 time，socket 模块之前
# import gevent
# # pip install gevent
# from time import time,sleep
 
# def gf(name):
#     print(f'{name}:我想打王者！！')
#     # gevent.sleep(2)
#     sleep(0)
#     print(f'{name}:我想吃大餐！！！')
#     sleep(1)
#     print(f'{name}: ！！')
 
# def bf(name):
#     print(f'{name}:一起打！！！')
#     # gevent.sleep(2)
#     sleep(0)
#     print(f'{name}:一快去吃！！')
 
# if __name__ == "__main__":
#     start = time()
#     # 创建协程对象
#     g1 = gevent.spawn(gf,'貂蝉')
#     g2 = gevent.spawn(bf,'吕布')
#     # 开启任务
#     g1.join()
#     g2.join()
#     # gf('貂蝉')
#     # bf('吕布')
#     end = time()
#     print(end-start)


# # 2.Python使用协程的缺点

# """
# 1、多核资源不能使用：协程的本质是单线程，它不能同时使用单个CPU的多核、协程。
# 2、在多CPU上运行程需要与过程配合。当然，每天编写的大多数应用程序都没有必要。除非是cpu密集型应用。
# 3、阻塞(Blocking)操作(如IO)会阻塞整个程序。"""

# # 协程的基本使用
# # 实现两个任务的切换  yield和 next来回切换
# def func1():
#     for i in range(11):
#         print(f"一班打印第{i}次数据")
#         yield
 
# def func2():
#     g = func1()
#     next(g)
#     for i in range(10):
#         print(f"二班打印第{i}次数据")
#         next(g)
 
# if __name__ == "__main__":
#     func2()

# next的用法
"""
next() 返回迭代器的下一个项目。
next() 函数要和生成迭代器的 iter() 函数一起使用。
"""
