## 1.Python中Gevent的使用
"""
1、可以通过gevent轻松实现并发同步或异步编程。gevent中使用的主要模式是Greenlet，它是以C扩展模块的形式访问Python的轻量级协程。
2、Greenlet全部运行在主程序操作系统的过程中，但是它们是协作调度
"""
from gevent import monkey # 为了能识别time模块的io
monkey.patch_all()  #必须放到被打补丁者的前面，如 time，socket 模块之前
import gevent
from time import time,sleep
 
def gf(name):
    print(f'{name}:我想打王者！！')
    # gevent.sleep(2)
    sleep(0)
    print(f'{name}:我想吃大餐！！！')
    sleep(1)
    print(f'{name}: ！！')
 
def bf(name):
    print(f'{name}:一起打！！！')
    # gevent.sleep(2)
    sleep(0)
    print(f'{name}:一快去吃！！')
 
if __name__ == "__main__":
    start = time()
    # 创建协程对象
    g1 = gevent.spawn(gf,'貂蝉')
    g2 = gevent.spawn(bf,'吕布')
    # 开启任务
    g1.join()
    g2.join()
    # gf('貂蝉')
    # bf('吕布')
    end = time()
    print(end-start)


## 2.Python使用协程的缺点

"""
1、多核资源不能使用：协程的本质是单线程，它不能同时使用单个CPU的多核、协程。
2、在多CPU上运行程需要与过程配合。当然，每天编写的大多数应用程序都没有必要。除非是cpu密集型应用。
3、阻塞(Blocking)操作(如IO)会阻塞整个程序。"""

    # 协程的基本使用
    # 实现两个任务的切换  yield和 next来回切换
def func1():
    for i in range(11):
        print(f"一班打印第{i}次数据")
        yield
 
def func2():
    g = func1()
    next(g)
    for i in range(10):
        print(f"二班打印第{i}次数据")
        next(g)
 
if __name__ == "__main__":
    func2()

# next的用法:https://www.runoob.com/python/python-func-next.html
"""
next() 返回迭代器的下一个项目。
next() 函数要和生成迭代器的 iter() 函数一起使用。
next(iterable[, default])
参数说明：
iterable -- 可迭代对象
default -- 可选，用于设置在没有下一个元素时返回该默认值，如果不设置，又没有下一个元素则会触发 StopIteration 异常。
"""
    # 首先获得Iterator对象:
it = iter([1, 2, 3, 4, 5])
    # 循环:
while True:
    try:
        # 获得下一个值:
        x = next(it)
        print(x)
    except StopIteration:
        # 遇到StopIteration就退出循环
        break
    # 如果传入第二个参数, 获取最后一个元素之后, 下一次next返回该默认值, 而不会抛出 StopIteration:   
while True:
    x = next(it, 'a')
    print(x)
    if x == 'a':
        break

## 3.python检查文件是否有软连接
"""
1、对于python 3.4及更高版本，可以使用Path类。
2、使用is_symlink()方法时必须小心。只要命名对象是符号链接，即使链接的目标不存在，它也会返回True。
ln -s ../nonexistentfile flnk"""
from pathlib import Path
    # rpd is a symbolic link
Path('test.ipynb').is_symlink()
Path('README').is_symlink()

## 4.python静态web服务器如何实现
"""
1、编写TCP服务器程序。
2、获取浏览器发送的http请求消息数据。
3、读取固定的页面数据，将页面数据组装成HTTP响应消息数据并发送给浏览器。
4、HTTP响应报文数据发送完成后，关闭服务于客户端的套接字。"""

import socket
if __name__ == '__main__':
    # 创建tcp服务端套接字
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 设置端口号复用, 程序退出端口立即释放
    tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    # 绑定端口号
    tcp_server_socket.bind(("", 5003))  ##浏览器访问http://192.168.57.159:5003/
    # 设置监听
    tcp_server_socket.listen(128)
    while True:
        # 等待接受客户端的连接请求
        new_socket, ip_port = tcp_server_socket.accept()
        # 代码执行到此，说明连接建立成功
        recv_client_data = new_socket.recv(4096)
        # 对二进制数据进行解码
        recv_client_content = recv_client_data.decode()
        print(recv_client_content)
        
        # 响应行
        response_line = "HTTP/1.1 200 OK\r\n"
        # 响应头
        response_header = "Server: py1.0\r\n"
 
        # 响应体
        response_body = "Hello,guys!"
 
        # 拼接响应报文
        response_data = (response_line + response_header + "\r\n"+ response_body).encode()

        # 发送数据
        new_socket.send(response_data)
        # 关闭服务与客户端的套接字
        new_socket.close()

## 6.python偏函数
"""
1、偏函数，是对原始函数的二次封装，是将现有函数的部分参数预先绑定到指定值，从而获得新的函数。
2、定义偏函数，需要使用partial关键字(位于functools模块中"""

from functools import partial
from unicodedata import name
def display(name, age):
    print("name:", name,"age：", age)
    #定义偏函数
fun = partial(display,name="gary")
fun(age=12)

## 7. python调用函数和打印函数的区别
"""
1、当你调用一个返回某些东西的函数时，应该为函数调用分配一个变量来存储返回值。
调用函数并忽略其返回值，或者你返回值存储在变量，也可以打印出来，或者记录它，或者把它传递给另一个函数的参数。
2、在打印函数调用的情况下，返回值不需要存储，直接打印。"""
def get_favorite_food():
     food = input("What's your favorite food?")
     return 'Your favorite food' + ' ' + food + ' ' + 'is ready!'
 
result = get_favorite_food()
print(result)

## 8.python静态方法的用法
"""
1、通过装饰器@staticmethod定义静态方法。
2、@staticmethod必须写在方法上。
3、在静态方法中访问实例属性和实例方法会导致错误。
4、调用格式：“类名.静态方法名(参数列表) """
class Person:
    # 类属性
    school = "国际学校"
    tuition = 100000
    count = 0
    # 实例属性
    def __init__(self,name,age):
        self.name = name
        self.age = age
        Person.count = Person.count+1
     # 静态实例 :类和实例对象都可以调用,
    @staticmethod
    def addNum(a,b):
      print("{0}+{1}={2}".format(a,b,a+b))
      return a+b
    # 实例方法 :类的实例能够使用的方法,只能由实例对象调用。
    # 第一个参数必须是实例对象，该参数名一般约定为“self”，通过它来传递实例的属性和方法
    def get_score(self):
        print("姓名：{0}；年龄：{1}".format(self.name,self.age))
 
stu1 = Person("sue", 22)
stu1.get_score()
Person.addNum(1,2)
stu1.addNum(1,2)

## 9.Python 中的 [:-1] 和 [::-1]
a='python'
b=a[::-1] # 每隔一位逆序输出
print(b) #nohtyp
c=a[::-2]
print(c) #nhy 
d=a[:-1]  #从位置0到位置-1之前的数, 从后往前数的话，最后一个位置为-1
print(d)


## 10. Python 实例方法、类方法、静态方法的区别与作用 :https://www.cnblogs.com/wcwnina/p/8644892.html
class ClassTest(object):
    __num = 0

    @classmethod   #类方法 使用装饰器@classmethod。
    def addNum(cls):
        cls.__num += 1

    @classmethod
    def getNum(cls):
        return cls.__num

    # 这里用到魔术方法__new__，主要是为了在创建实例的时候调用累加方法:https://www.cnblogs.com/zyxnhr/p/12344977.html
    def __new__(self):
        ClassTest.addNum()
        return super(ClassTest, self).__new__(self)

class Student(ClassTest):
    def __init__(self):
        self.name = ''

a = Student()
b = Student()
print(ClassTest.getNum())  # 2

import time

class TimeTest(object):
    def __init__(self, hour, minute, second):
        self.hour = hour
        self.minute = minute
        self.second = second

    @staticmethod
    def showTime():
        return time.strftime("%H:%M:%S", time.localtime())


print(TimeTest.showTime())
t = TimeTest(2, 10, 10)
nowTime = t.showTime()
print(nowTime)

class Person:
 
    # 类属性
    school = "国际学校"
    tuition = 100000
    count = 0
 
    # 实例属性
    def __init__(self,name,age,gender):
        self.name = name
        self.age = age
        self.gender = gender
        Person.count = Person.count+1
 
    @classmethod
    def printSchool(cls):
        print(cls)
        print(cls.school)
        print(cls.count)
 
    # 实例方法
    def get_score(self):
        print("姓名：{0}；年龄：{1}；性别：{2}".format(self.name,self.age,self.gender))
 
stu1 = Person("sue", 22, "male")
stu1.get_score()
Person.printSchool()

## 11.python实例方法的使用注意
class getMin():
    # 实例方法
    def fun(self, arr, n):
        print(arr[n-1])
    # 类方法
    @classmethod
    def class_fun(cls):
        print("this is class function")
 
if __name__ == "__main__":
    arr = input().strip().split(" ")
    int_arr = []
    for item in arr:
        int_arr.append(int(item))
    n = int(input())
 
    instance = getMin()
    # 用实例调用实例方法
    instance.fun(int_arr, n)
    # 用类调用方法
    getMin.fun(instance, int_arr, n)
    # 实例调用类方法
    instance.class_fun()
    # 类调用类方法
    getMin.class_fun()



