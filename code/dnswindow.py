# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dnswindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import threading

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QListWidgetItem, QTreeWidgetItem

from analysis_dns import analysis_dns


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(932, 641)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.listWidget = QtWidgets.QListWidget(self.splitter)
        self.listWidget.setMinimumSize(QtCore.QSize(300, 0))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.listWidget.setFont(font)
        self.listWidget.setObjectName("listWidget")
        self.treeWidget = QtWidgets.QTreeWidget(self.splitter)
        self.treeWidget.setMinimumSize(QtCore.QSize(500, 0))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.treeWidget.setFont(font)
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.headerItem().setText(0, "1")
        self.horizontalLayout.addWidget(self.splitter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 932, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # init
        self.init_GUI()
        self.pro = []
        self.dns = []
        self.info = []
        self.listWidget.itemSelectionChanged.connect(self.show)

    def init_GUI(self):
        self.treeWidget.setHeaderHidden(True)
        self.listWidget.clear()
        self.statusbar.showMessage('分析中 ...')

    def analysis(self):
        if not self.pro:
            return
        self.listWidget.setEnabled(False)
        t1 = threading.Thread(target=self.dns_info)
        t1.setDaemon(True)
        t1.start()

    def dns_info(self):
        for p in self.pro:
            if 'DNS' in p.protocol:
                name = p.info.split(' ')[-1]
                if name not in self.dns:
                    self.dns.append(name)
        for name in self.dns:
            res = analysis_dns(name)
            self.info.append(res)
            if res and 'country' in res and res['country']:
                local = res['country']
            else:
                local = 'unknown'
            item = QListWidgetItem(QIcon(':/img/' + local + '.png'), name)
            self.listWidget.addItem(item)
        self.statusbar.showMessage('分析完成')
        self.listWidget.setEnabled(True)

    def show(self):
        self.treeWidget.clear()
        index = self.listWidget.currentIndex().row()
        res = self.info[index]
        if not res:
            return
        name = self.listWidget.item(index).text()
        root = QTreeWidgetItem()
        root.setText(0, name)
        self.treeWidget.addTopLevelItem(root)
        if 'domain_name' in res and res['domain_name']:
            domain_name = QTreeWidgetItem()
            domain_name.setText(0, 'domain_name')
            self.treeWidget.addTopLevelItem(domain_name)
            if type(res['domain_name']).__name__ == 'list':
                for it in res['domain_name']:
                    tmp = QTreeWidgetItem()
                    tmp.setText(0, it)
                    domain_name.addChild(tmp)
            else:
                tmp = QTreeWidgetItem()
                tmp.setText(0, res['domain_name'])
                domain_name.addChild(tmp)
        if 'registrar' in res and res['registrar']:
            registrar = QTreeWidgetItem()
            registrar.setText(0, res['registrar'])
            self.treeWidget.addTopLevelItem(registrar)
        if 'updated_date' in res and res['updated_date']:
            updated_date = QTreeWidgetItem()
            updated_date.setText(0, 'updated_date')
            if type(res['updated_date']).__name__ == 'list':
                for it in res['updated_date']:
                    tmp = QTreeWidgetItem()
                    tmp.setText(0, str(it))
                    updated_date.addChild(tmp)
            else:
                tmp = QTreeWidgetItem()
                tmp.setText(0, str(res['updated_date']))
                updated_date.addChild(tmp)
            self.treeWidget.addTopLevelItem(updated_date)
        if 'creation_date' in res and res['creation_date']:
            creation_date = QTreeWidgetItem()
            creation_date.setText(0, 'creation_date: ' + str(res['creation_date']))
            self.treeWidget.addTopLevelItem(creation_date)
        if 'expiration_date' in res and res['expiration_date']:
            expiration_date = QTreeWidgetItem()
            expiration_date.setText(0, 'expiration_date: ' + str(res['expiration_date']))
            self.treeWidget.addTopLevelItem(expiration_date)
        if 'name_servers' in res and res['name_servers']:
            name_servers = QTreeWidgetItem()
            name_servers.setText(0, 'name_servers')
            if type(res['name_servers']).__name__ == 'list':
                for it in res['name_servers']:
                    tmp = QTreeWidgetItem()
                    tmp.setText(0, it)
                    name_servers.addChild(tmp)
            else:
                tmp = QTreeWidgetItem()
                tmp.setText(0, res['name_servers'])
                name_servers.addChild(tmp)
            self.treeWidget.addTopLevelItem(name_servers)
        if 'dnssec' in res and res['dnssec']:
            dnssec = QTreeWidgetItem()
            dnssec.setText(0, res['dnssec'])
            self.treeWidget.addTopLevelItem(dnssec)
        if 'name' in res and res['name']:
            name = QTreeWidgetItem()
            name.setText(0, res['name'])
            self.treeWidget.addTopLevelItem(name)
        if 'org' in res and res['org']:
            org = QTreeWidgetItem()
            org.setText(0, res['org'])
            self.treeWidget.addTopLevelItem(org)
        if 'address' in res and res['address']:
            address = QTreeWidgetItem()
            address.setText(0, res['address'])
            self.treeWidget.addTopLevelItem(address)
        if 'city' in res and res['city']:
            city = QTreeWidgetItem()
            city.setText(0, res['city'])
            self.treeWidget.addTopLevelItem(city)
        if 'state' in res and res['state']:
            state = QTreeWidgetItem()
            state.setText(0, res['state'])
            self.treeWidget.addTopLevelItem(state)
        if 'zipcode' in res and res['zipcode']:
            zipcode = QTreeWidgetItem()
            zipcode.setText(0, res['zipcode'])
            self.treeWidget.addTopLevelItem(zipcode)
        if 'country' in res and res['country']:
            country = QTreeWidgetItem()
            country.setText(0, res['country'])
            self.treeWidget.addTopLevelItem(country)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "DNS结果分析"))
