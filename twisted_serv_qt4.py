#!/usr/bin/env python
# -*- coding:utf-8 -*-
from PyQt4 import QtGui
 
from twisted.internet.protocol import ServerFactory
from twisted.protocols.basic import LineOnlyReceiver

import socket

 
class Core(LineOnlyReceiver):  #or class Core(Protocol):
    def getId(self):
        return str(self.transport.getPeer())
 
    def connectionMade(self):
        '''初次连接的时候，随便命名这个客户，客户第一次发送数据的时候，需要自报姓名，我们将保存他的名字'''
        self.name = 'unnamed'
        self.state = "GETNAME"
        self.factory.window.protocol = self
        #self.factory.addClient(self)
        
        self.log('New User Login:%s!' % self.getId())
 
    def connectionLost(self, reason):
        if self.factory.clients !={} and (self.name in self.factory.clients):
            self.factory.clients.pop(self.name)
 
    def dataReceived(self, data):
        '''客户第一次通信的时候需要自报姓名'''
        
        if self.state == 'GETNAME':
            self.handle_GETNAME(data)
        else:
            self.handle_CHAT(data)
        
    def handle_GETNAME(self, data):        
        self.name = data
        if self.factory.clients.has_key(self.name):
            self.factory.clients[self.name].transport.write('error name')
            return
        else:
            self.factory.clients[self.name]=self   # 通过字典名来保存客户端 
            self.factory.clients[self.name].transport.write('ok,I remeber you ')
            self.state = "CHAT"
            self.log('IP:%s User name:%s' % (self.transport.getPeer().host, self.name))
            
#        msg = "%s:%s" % (self.transport.client[0], data)
#        self.factory.sendAll(msg)
#        self.log(msg)
 
    def handle_CHAT(self, data):
        pass
        
    def log(self, msg):
        self.factory.window.sendMessage(msg)
        
 
class CoreFactory(ServerFactory):
    protocol = Core
    def __init__(self, window):
        self.window = window
        self.clients = {}   # 用一个字典来保存和查找相应的客户端
 
    def sendAll(self, data):
        for x in self.clients:
            x.transport.write(data)
    
    def sendsomeone(self, name, data):
        if name in self.clients:
            self.clients[name].transport.write(data)
        else:
            self.window.sendMessage('wrong name')
 
class Frame(QtGui.QFrame):
    def __init__(self, reactor):
        super(Frame, self).__init__()
        self.reactor = reactor
        
        myname = socket.getfqdn(socket.gethostname())
        myaddr = socket.gethostbyname(myname)
        
        self.btn_listen = QtGui.QPushButton(u'侦听', self)
        self.btn_listen.clicked.connect(self.btn_listen_click)
 
        self.btn_stop = QtGui.QPushButton(u'停止', self)
        self.btn_stop.clicked.connect(self.btn_stop_click)
 
        self.btn_radio = QtGui.QPushButton(u"广播", self)
        self.btn_radio.clicked.connect(self.btn_radio_click)
 
        self.text_port = QtGui.QLineEdit("5000", self)
        self.text_msg = QtGui.QLineEdit("hello", self)
 
        self.view = QtGui.QTextEdit(self)
 
        layout = QtGui.QGridLayout()
        layout.addWidget(self.text_port, 0, 0)
        layout.addWidget(self.btn_listen, 0, 1)
        layout.addWidget(self.btn_stop, 0, 2)
        layout.addWidget(self.view, 1, 0, 1, 0)
        layout.addWidget(self.text_msg, 2, 0)
        layout.addWidget(self.btn_radio, 2, 1, 1, 2)
        
        self.ip_addr = QtGui.QLineEdit(myaddr, self)
        layout.addWidget(self.ip_addr, 3, 0)
        
        self.username = QtGui.QLineEdit('', self)
        layout.addWidget(self.username, 3, 1)
        
        self.setLayout(layout)
 
        self.core_factory = CoreFactory(self)
        self.protocol = None
 
    def sendMessage(self, msg):
        self.view.append(msg)
 
    def btn_listen_click(self):
        port = int(self.text_port.text())
        self.reactor.listenTCP(port, self.core_factory)
        print "start running..."
        #self.reactor.run()
 
    def btn_stop_click(self):
       
        if self.reactor.running:
            self.reactor.stop()
 
    def btn_radio_click(self):
        msg = str(self.text_msg.text()) + '\r\n'
        name = str(self.username.text())        self.core_factory.sendsomeone(name, msg)
        #self.core_factory.sendAll(msg)
         
    def closeEvent(self, event):
        print('Attempting to close the main window!')
        self.btn_stop_click()
        event.accept()
 
if __name__ == '__main__':
    import sys, qt4reactor
    app = QtGui.QApplication(sys.argv)
    qt4reactor.install()
    from twisted.internet import reactor
    
    frm = Frame(reactor)
    frm.show()
    reactor.run()
    sys.exit(app.exec_())
