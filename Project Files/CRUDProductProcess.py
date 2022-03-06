from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
from PyQt5 import QtWidgets,uic
from PyQt5.QtWidgets import QApplication
import mysql.connector as c
import pandas as pd
from PyQt5.QtWidgets import QMessageBox

class CRUDPProcess(QDialog):
    def __init__(self,product_id):
        super(CRUDPProcess,self).__init__()
        uic.loadUi("CRUDproduct.ui",self)
        self.setWindowTitle("CRUD Product")
        
        self.LoadData(product_id)
        self.mydb=None
        self.updatebtn.clicked.connect(self.UpdateData)
        self.addbtn.clicked.connect(self.AddData)
        self.deletebtn.clicked.connect(self.DeleteData)
        self.clearbtn.clicked.connect(self.ClearData)

    def ClearData(self):
        self.idtxt.clear()
        self.nametxt.clear()
        self.categorytxt.clear()
        self.pricetxt.clear()
        self.ppricetxt.clear()
        self.copytxt.clear()
        self.lefttxt.clear()
        self.idtxt.setEnabled(True)


    def UpdateData(self):
        pid=self.idtxt.toPlainText()
        productname= self.nametxt.toPlainText()
        categoryname=self.categorytxt.toPlainText()
        price=self.pricetxt.toPlainText()
        pprice=self.ppricetxt.toPlainText()
        copy=self.copytxt.toPlainText()
        left=self.lefttxt.toPlainText()
        if len(pid)<=0 or len(productname)<=0 or len(categoryname)<=0 or len(price)<=0 or len(pprice)<=0 or len(copy)<=0 or len(left)<=0:
            QMessageBox.about(self,"No Entry Data","Please Fill all data completely.")
        else:
            reply=QMessageBox.question(self,"Quit","Are you sure to update this product?",
                        QMessageBox.Yes|QMessageBox.No,QMessageBox.No) 
            if reply==QMessageBox.Yes:
                self.DBConnect()
                cursor=self.mydb.cursor()
                sqlstr="update product_tb set product_name='"+productname+"', category_name='"+categoryname+"', unitprice='"+price+"', previous_price='"+pprice+"', num_product="+str(copy)+", left_product="+str(left)+" where product_id="+str(pid)
                cursor.execute(sqlstr)
                self.mydb.commit()
                print(cursor.rowcount," record affected.")   
                QMessageBox.about(self,"Success","Your Data are updated successfully.")
                self.idtxt.setEnabled(True)

    def AddData(self):
        self.idtxt.setEnabled(True)
        pid=self.idtxt.toPlainText()
        productname= self.nametxt.toPlainText()
        categoryname=self.categorytxt.toPlainText()
        price=self.pricetxt.toPlainText()
        pprice=self.ppricetxt.toPlainText()
        copy=self.copytxt.toPlainText()
        left=self.lefttxt.toPlainText()

        if len(pid)<=0 or len(productname)<=0 or len(categoryname)<=0 or len(price)<=0 or len(pprice)<=0 or len(copy)<=0 or len(left)<=0:
            QMessageBox.about(self,"No Entry Data","Please Fill all data completely.")
        else:
            result=self.SearchID(pid)
            if result==False:
                QMessageBox.about(self,"Duplicate Product ID","Please Enter Another Product Id that you want to add")
            else:
                reply=QMessageBox.question(self,"Quit","Are you sure to insert this product?",
                        QMessageBox.Yes|QMessageBox.No,QMessageBox.No) 
                if reply==QMessageBox.Yes:
                    productname= self.nametxt.toPlainText()
                    categoryname=self.categorytxt.toPlainText()
                    price=self.pricetxt.toPlainText()
                    pprice=self.ppricetxt.toPlainText()
                    copy=self.copytxt.toPlainText()
                    left=self.lefttxt.toPlainText()

                    self.DBConnect()
                    cursor=self.mydb.cursor()

                    sqlstr="insert into product_tb(product_id,product_name,category_name,unitprice,previous_price,num_product,left_product) values(%s,%s,%s,%s,%s,%s,%s)"
                    val=(str(pid),productname,categoryname,price,pprice,str(copy),str(left))
                    cursor.execute(sqlstr,val)
                    self.mydb.commit()
                    QMessageBox.about(self,"Success","A new product is inserted successfully.")


    def DeleteData(self):
        self.DBConnect()
        pid=self.idtxt.toPlainText()
        if len(pid)<1:
            QMessageBox.about(self,"Entry Data","Please Enter Product Id that you want to delete.")
        else:
            result=self.SearchID(pid)
            if result==True:
                QMessageBox.about(self,"No Data Found","Please Enter Correct Product Id that you want to delete")
            else:
                
                reply=QMessageBox.question(self,"Quit","Are you sure to delete this product?",
                        QMessageBox.Yes|QMessageBox.No,QMessageBox.No) 
                if reply==QMessageBox.Yes:
                    cursor=self.mydb.cursor()
                    sqlstr="delete from product_tb where product_id="+str(pid)
                    cursor.execute(sqlstr)
                    self.mydb.commit()
                    QMessageBox.about(self,"Success","Your Product is deleted successfully.")
                    #QMessageBox.setStyleSheet("QLabel{ color: white}")
                    self.ClearData()

    def SearchID(self,pid):
        self.DBConnect()
        sign=False
        cursor=self.mydb.cursor()
        sqlstr="select * from product_tb where product_id="+str(pid)
        cursor.execute(sqlstr)
        result=cursor.fetchone()
        if result==None:
            sign=True
        return sign

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

    def LoadData(self,product_id):
        self.DBConnect()
        cursor=self.mydb.cursor()
        
        sqlstr="select * from product_tb where product_id="+str(product_id)
        print(sqlstr)
        
        cursor.execute(sqlstr)
        result=cursor.fetchone()
        self.idtxt.setPlainText(str(result[0]))
        self.nametxt.setPlainText(str(result[1]))
        self.categorytxt.setPlainText(str(result[2]))
        self.pricetxt.setPlainText(str(result[3]))
        self.ppricetxt.setPlainText(str(result[4]))
        self.copytxt.setPlainText(str(result[5]))
        self.lefttxt.setPlainText(str(result[6]))
        self.idtxt.setEnabled(False)
        

"""app=QApplication(sys.argv)
stu=CRUDProcess(1002)
stu.show()
app.exec_()"""