# detail
这个库是项目实现交互界面的主要部分
dbmain.py是主函数入口，用于启动项目
login是登录界面，用户和管理员将可以从这个界面登入
enroll是注册界面，新用户可以在这个界面注册
我们通过admin_container打开管理员界面，通过user_container打开用户界面
管理员将能看到cfile、cuser、logger三个视图选项，能在cfile中上传和下载文件，在cuser中管理用户和在库中移除文件，在logger中看到日志记录
而用户只能看到cfile和logger两个视图
cfile从系统或者Input文件夹中获取数据上传到服务器的Data中，下载时则也从Data中寻找目标文件下载到Output文件夹中
登入和注册都会访问架设在服务器上的数据库，对用户权限和文件的修改也会访问和修改数据库数据并记录在日志中
