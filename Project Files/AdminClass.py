from datetime import datetime
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
from PyQt5 import QtWidgets,uic
from PyQt5.QtWidgets import QApplication
import mysql.connector as c
import pandas as pd
from PyQt5.QtWidgets import QMessageBox

class Admin_Process_Class(QDialog):
    def __init__(self,id,role,name):
        super(Admin_Process_Class,self).__init__()
        uic.loadUi("adminform.ui",self)
        self.setWindowTitle("Admin Dashboard")
        self.adminlbl.setText("Admin Name :"+name)
        self.UserId=id
        

        self.mydb=None
        end_date = datetime.now()
        text=end_date.strftime("%Y, %m, %d")
        self.datetimelbl.setText("Date : "+ str(text))

        self.SetComboData()
        self.showsoldbtn.clicked.connect(self.ShowSoldData)
        self.showproductbtn.clicked.connect(self.ShowProductData)
        self.updateproductbtn.clicked.connect(self.UpdateProductData)
        self.updatecashierbtn.clicked.connect(self.UpdateCashierData)
        self.showallpdbtn.clicked.connect(self.ShowAllProduct)
        self.showallembtn.clicked.connect(self.ShowEmployeeData)
        self.changepricebtn.clicked.connect(self.ChangePriceData)
        self.exitbtn.clicked.connect(self.ExitForm)


        self.tableView.clicked.connect(self.TableSelect)
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
        
    def TableSelect(self):
        self.updateproductbtn.setEnabled(True)
        self.updatecashierbtn.setEnabled(True)

    def ExitForm(self, event):
        reply=QMessageBox.question(self,"window Close","Are you sure you want to close the window?",
                            QMessageBox.Yes|QMessageBox.No,QMessageBox.No)

        if reply==QMessageBox.Yes:
            QMessageBox.exec_()

    def SetComboData(self):
        self.cashiercombo.addItem("All")
        self.DBConnect()
        cursor=self.mydb.cursor()
        #self.cashiercombo.clear() #to remove items and avoid duplicate
        sqlcmd="select username from userinfo_tb where role='"+str("cashier")+"'"
        cursor.execute(sqlcmd)

        for i in cursor: 
            self.cashiercombo.addItem(str(i[0]))
            
    def ShowSoldData(self):
        combodata=self.GetData()
        combodata=combodata.lower().strip()
        self.ShowProdctCashier(combodata)

    def GetData(self):
        combodata=self.cashiercombo.currentText()
        return combodata

    def ShowProdctCashier(self,combodata):
        self.DBConnect()
        cursor=self.mydb.cursor()

        if combodata=="all":
            sqlstr="""
            select userinfo_tb.user_id as UserID,userinfo_tb.username as Name,userinfo_tb.role as Role,product_tb.product_name as Product_Name,product_tb.category_name as Category,sale_tb.sale_date_time as Sale_Date_Time
            from sale_tb,userinfo_tb,product_tb
            where sale_tb.user_id=userinfo_tb.user_id 
            and sale_tb.product_id=product_tb.product_id"""
        else:
            sqlstr="""
            select userinfo_tb.user_id as UserID,userinfo_tb.username as Name,userinfo_tb.role as Role,product_tb.product_name as Product_Name,product_tb.category_name as Category,sale_tb.sale_date_time as Sale_Date_Time
            from sale_tb,userinfo_tb,product_tb
            where sale_tb.user_id=userinfo_tb.user_id 
            and sale_tb.product_id=product_tb.product_id
            and userinfo_tb.username='"""+combodata+"'"

        SQL_Query=pd.read_sql_query(sqlstr,self.mydb)
        df=pd.DataFrame(SQL_Query,columns=["UserID","Name","Role","Product_Name","Category","Sale_Date_Time"])

        if len(df)<1:
            QMessageBox.about(self,"Not Found","Please Try Again.")
        from TableModel import pandasModel
        model= pandasModel(df)
        self.tableView.setModel(model)

    
    def GetProductData(self):
        useroption=None
        if self.allproductbtn.isChecked():
            useroption="all_product"
        elif self.soldoutbtn.isChecked():
            useroption="soldout_product"
        else:
            useroption="instock_product"
        return useroption

    def ShowProductData(self):
        useroption=self.GetProductData()
        if useroption=="all_product":
            self.ShowAllProduct()
        elif useroption=="soldout_product":
            self.ShowSoldOutProduct()
        else:
            self.ShowInstockProduct()

    def ShowAllProduct(self):
        self.DBConnect()
        cursor=self.mydb.cursor()
        sqlstr="select * from product_tb"
        
        SQL_Query=pd.read_sql_query(sqlstr,self.mydb)
        df=pd.DataFrame(SQL_Query,columns=["product_id","product_name","category_name","unitprice","previous_price","num_product","left_product"])
            
        if len(df)<1:
            QMessageBox.about(self,"Not Found","Please Try Again")
        from TableModel import pandasModel
        model= pandasModel(df)
        self.tableView.setModel(model)
    
    def ShowSoldOutProduct(self):
        self.DBConnect()
        cursor=self.mydb.cursor()
        sqlstr="select * from product_tb where left_product='"+str(0)+"'";
        
        SQL_Query=pd.read_sql_query(sqlstr,self.mydb)
        df=pd.DataFrame(SQL_Query,columns=["product_id","product_name","category_name","unitprice","previous_price","num_product","left_product"])
            
        if len(df)<1:
            QMessageBox.about(self,"Not Found","There is no sold out product!")
            #QMessageBox.setStyleSheet("QLabel{color:white}")
        from TableModel import pandasModel
        model= pandasModel(df)
        self.tableView.setModel(model)

    def ShowInstockProduct(self):
        self.DBConnect()
        cursor=self.mydb.cursor()
        sqlstr="select * from product_tb where left_product >'"+str(0)+"'";
        
        SQL_Query=pd.read_sql_query(sqlstr,self.mydb)
        df=pd.DataFrame(SQL_Query,columns=["product_id","product_name","category_name","unitprice","previous_price","num_product","left_product"])
            
        if len(df)<1:
            QMessageBox.about(self,"Not Found","There is no instock product!")
            #QMessageBox.setStyleSheet(self,"QLabel{color:white}")
        from TableModel import pandasModel
        model= pandasModel(df)
        self.tableView.setModel(model)
    
    def ShowEmployeeData(self):
        self.DBConnect()
        cursor=self.mydb.cursor()
        sqlstr="select * from userinfo_tb"
        
        SQL_Query=pd.read_sql_query(sqlstr,self.mydb)
        df=pd.DataFrame(SQL_Query,columns=["user_id","username","role","address","phone_number","email","bankacc"])
            
        if len(df)<1:
            QMessageBox.about(self,"Not Found","Please Try Again")
        from TableModel import pandasModel
        model= pandasModel(df)
        self.tableView.setModel(model)
        self.cashiercombo.clear()
        self.SetComboData()

    def UpdateProductData(self):
        self.updateproductbtn.setEnabled(False)
        
        index=self.tableView.selectionModel().currentIndex()
        value=index.sibling(index.row(),index.column()).data()
        print(str(value))

        self.DBConnect()
        self.mydb.cursor()
        sqlstr="select * from product_tb "  
        SQL_Query=pd.read_sql_query(sqlstr,self.mydb)
        df=pd.DataFrame(SQL_Query,columns=["product_id","product_name","category_name","unitprice","previous_price","num_product","left_product"])
        pid=list(df["product_id"])
        for x in pid:
            if str(x) == str(value):
                
                from CRUDProductProcess import CRUDPProcess
                crud=CRUDPProcess(value)
                crud.show()
                crud.exec_()


    def UpdateCashierData(self):
        self.updatecashierbtn.setEnabled(False)
        self.cashiercombo.clear()
        self.SetComboData()

        index=self.tableView.selectionModel().currentIndex()
        value=index.sibling(index.row(),index.column()).data()
        print(str(value))
        
        self.DBConnect()
        self.mydb.cursor()
        sqlstr="select * from userinfo_tb " 
        SQL_Query=pd.read_sql_query(sqlstr,self.mydb)
        df=pd.DataFrame(SQL_Query,columns=["user_id","username","role","address","phone_number","email","bankacc"])
        
        uid=list(df["user_id"])
        print(uid)
        
        if str(value) not in str(uid):
            QMessageBox.about(self,"Wrong Selection","Please Select only ID!")
        else:
            from CRUDCashierProcess import CRUDCashProcess
            crud=CRUDCashProcess(value)
            crud.show()
            crud.exec_()
    
    def ChangePriceData(self):
        value=self.UserId
        from ChangePriceProcess import ChangePrice
        change=ChangePrice(value)
        change.show()
        change.exec_()
    
"""app=QApplication(sys.argv)
#stu=Student_Teacher_Class(3,"student","Soe Mtint")
admin=Admin_Process_Class(3,"admin","Hla Hla")
admin.show()
app.exec_()"""