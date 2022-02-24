# ##os模块:操作系统接口
import os
print(os.getcwd())# 返回当前的工作目录
os.chdir('/data/home/zgl/Github/python_learing/')# 修改当前的工作目录
# os.system('mkdir today') # 执行系统命令 mkdir 
# os.system('rm -r today')

# ##shutil :针对日常的文件和目录管理任务

# import shutil
# shutil.copyfile('README.md', 'README2.md') # 复制
# shutil.move('README.md', 'README.txt') #