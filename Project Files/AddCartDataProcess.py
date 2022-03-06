from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
from PyQt5 import QtWidgets,uic
from PyQt5.QtWidgets import QApplication
import mysql.connector as c
import pandas as pd
from PyQt5.QtWidgets import QMessageBox

class AddCartProcess(QDialog):
    def __init__(self,product_id):
        super(AddCartProcess,self).__init__()
        uic.loadUi("addcartform.ui",self)
        self.setWindowTitle("Add to Cart")
        self.LoadData(product_id)
        self.mydb=None
        self.savebtn.clicked.connect(self.SaveData)
        #self.detailclearbtn.clicked.connect(self.ClearData)
        
    def DBConnect(self):
        try:
            self.mydb=c.connect(
                host="localhost",
                user="root",
                password="",
                database="project_db"
            )
        except c.Error as err:
            print("Something went wrong {}".format(err))  

    """def ClearData(self):
        self.pidtxt.clear()
        self.pnametxt.clear()
        self.pricetxt.clear()
        self.stocktxt.clear()
        self.qtytxt.clear()
        self.pidtxt.setEnabled(True)
        self.pnametxt.setEnabled(True)
        self.pricetxt.setEnabled(True)
        self.stocktxt.setEnabled(True)"""


    def SaveData(self):
        pid=self.pidtxt.toPlainText()
        pname= self.pnametxt.toPlainText()
        price=self.pricetxt.toPlainText()
        stock=self.stocktxt.toPlainText()
        qty=self.qtytxt.toPlainText()

        self.DBConnect()
        cursor=self.mydb.cursor()

        sqlstr="update product_tb set product_id='"+pid+"', product_name='"+pname+"', unitprice='"+price+"', left_product="+str(stock)+" where product_id="+str(pid)
        cursor.execute(sqlstr)
        self.mydb.commit()
        print(cursor.rowcount," record affected.")   
        QMessageBox.about(self,"Success","Your Data are updated successfully.")
        self.pidtxt.setEnabled(True)

    def LoadData(self,pid):
        self.DBConnect()
        cursor=self.mydb.cursor()
        sqlstr="select * from product_tb where product_id="+str(pid)
        cursor.execute(sqlstr)
        result=cursor.fetchone()
        self.pidtxt.setPlainText(str(result[1]))
        self.pnametxt.setPlainText(str(result[2]))
        self.pricetxt.setPlainText(str(result[3]))
        self.stocktxt.setPlainText(str(result[5]))
        self.pidtxt.setEnabled(False)
        self.pnametxt.setEnabled(False)
        self.pricetxt.setEnabled(False)
        self.stocktxt.setEnabled(False)

    def ShowData(self):
        pid,pname,price,stock,qty=self.GetData()
        self.ShowSelectedItem(pid,pname,price,stock,qty)

    def GetData(self):  
        pid=self.pidtxt.toPlainText()
        pname= self.pnametxt.toPlainText()
        price=self.pricetxt.toPlainText()
        stock=self.stocktxt.toPlainText()
        qty=self.qtytxt.toPlainText()
        return pid,pname,price,stock,qty
    
    def ShowSelectedItem(self,pid,pname,price,stock,qty):
        pass

"""app=QApplication(sys.argv)
stu=CRUDProcess(1002)
stu.show()
app.exec_()"""