# GUI_socket_python
通过wifi监听多机器人状态的服务器端程序

##注意事项:
pyqt和twisted模块都是事件驱动型，都一直在run然后监听动作并响应。因此，它俩要同时运行，有两种方式:
1. 是开俩线程
2. 使用专门针对qt和twisted的qt4reactor。到网上下载qt4reactor的相关文件，在将主程序中将调用qt4reactor模块。


在我们的程序中，使用了qt4reactor模块

##程序说明:
twisted_serv_qt4为简单的服务器GUI测试程序，它完成如下功能：
1. 构建服务器，监听端口的连接请求
2. 新连接的client，命名为unname，并把该client第一次发送的数据当做他的名字。将该client以及name保存到字典里，方便服务器通过名字查询和调用。
3. 通过字典名可以给指定的client发送命令(如停止某一台机器人)

ref：这部分程序主要完成一个类似聊天功能的服务器，参考http://twistedmatrix.com/documents/13.0.0/core/howto/servers.html
