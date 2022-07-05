
# #理解下类和继承
# # 1.创建父类 
# class Person:
#   def __init__(self, fname, lname):
#     self.firstname = fname
#     self.lastname = lname

#   def printname(self):
#     print(self.firstname, self.lastname)

#   # 使用 Person 来创建对象，然后执行 printname 方法：
# x = Person("Bill", "Gates")
# x.printname()
# # 2.子类继承
# class Student(Person):
#   pass
# x = Student("woll", "Gates")
# x.printname()

# #3.添加__init__()
# class Student(Person):
#   def __init__(self, fname, lname): #当您添加 __init__() 函数时，子类将不再继承父的 __init__() 函数。
#       # 添加属性等
#       Person.__init__(self, fname, lname) #保留对父类的__init__() 函数继承

# # super() 函数：使子类从其父继承所有方法和属性

# class Student(Person):
#   def __init__(self, fname, lname, year):
#     super().__init__(fname, lname)
#     self.year = year #把名为year 的属性添加到 Student 类
#   def printname(self):
#     print(self.firstname, self.lastname, self.year) #类的方法重写 在子类中添加一个与父类中的函数同名的方法，则将覆盖父方法的继承。
#   def welcome(self): #添加新的方法
#     print("Welcome", self.firstname, self.lastname, "to the class of", self.year)

# y = Student("Elon", "Musk", 2019)
# y.printname()



## 变量
# """在函数外部创建的变量称为全局变量。
# 全局变量可以被函数内部和外部的每个人使用。"""
# x = "awesome"

# def myfunc():
#   print("Python is " + x)

# myfunc()

# """在函数内部创建具有相同名称的变量，则该变量将是局部变量，并且只能在函数内部使用。具有相同名称的全局变量将保留原样，并拥有原始值。"""
# x = "awesome"

# def myfunc():
#         # global x #要在函数内部更改全局变量的值，请使用 global 关键字引用该变量：
#     x = "fantastic"
#     print("Python is " + x)

# myfunc()
# print("Python is " + x)

# """
# 文本类型：	str
# 数值类型：	int, float, complex
# 序列类型：	list, tuple, range
# 映射类型：	dict
# 集合类型：	set, frozenset
# 布尔类型：	bool
# 二进制类型：bytes, bytearray, memoryview"""
# x = memoryview(bytes(5))
# print(type(x))

#字符串
# strip() 方法删除开头和结尾的空白字符：
# split() 方法在找到分隔符的实例时将字符串拆分为子字符串：
# a = " Hello,World!   "
# print(a.strip()) # returns "Hello, World!"
# print(a.split(",") ) # returns "Hello, World!"


# quantity = 3
# itemno = 567
# price = 49.95545
# myorder = "I want {} pieces of item {} for {} dollars."
# print(myorder.format(quantity, itemno, price))
##递归
# def tri_recursion(k):
#   if(k>1):
#     result = tri_recursion(k)+tri_recursion(k-1)
#     print(result)
#   else:
#     result = 0
#   return result

# print("\n\nRecursion Example Results")
# tri_recursion(6)

# import json

# x = {
#   "name": "Bill",
#   "age": 63,
#   "married": True,
#   "divorced": False,
#   "children": ("Jennifer","Rory","Phoebe"),
#   "pets": None,
#   "cars": [
#     {"model": "Porsche", "mpg": 38.2},
#     {"model": "BMW M5", "mpg": 26.9}
#   ]
# }
# print(json.dumps(x,indent=4))

import os
data_path = "/data/home/zgl/datasets/robot/"
name_ = os.path.basename(data_path)
print(name_)