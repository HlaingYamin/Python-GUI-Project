from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
from PyQt5 import QtWidgets,uic
from PyQt5.QtWidgets import QApplication
import mysql.connector as c
import pandas as pd
from PyQt5.QtWidgets import QMessageBox

class ChangePrice(QDialog):
    def __init__(self,product_id):
        super(ChangePrice,self).__init__()
        uic.loadUi("changeprice.ui",self)
        self.setWindowTitle("Change All Product Price")
        self.mydb=None
        self.enterbtn.clicked.connect(self.ShowUpdatePrice)

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
    
    
    
    def ShowUpdatePrice(self):
        useroption,percent=self.GetData()
        print(f"{useroption} and {percent}")
        if len(useroption)>0 and len(percent)>0 and len(percent)<3:
            self.CalculatePrice(useroption,percent)
        else:
            QMessageBox.about(self,"Invalid Data","Please Fill no more than two digits!")

    def GetData(self):
        useroption=None
        if self.inbtn.isChecked():
            useroption="increase"
        else:
            useroption="decrease"
        
        percent=self.percentTxt.toPlainText()
        return useroption,percent
    
    def CalculatePrice(self,useroption,percent):
        percent=percent.strip()
        upd_percent=int(percent)/100
        print(upd_percent)

        if len(percent)==0:
            QMessageBox.about(self,"No Data","Please Fill Data!")
        else:
            self.DBConnect()
            cursor=self.mydb.cursor()

            sqlstr="select * from product_tb "
            
            SQL_Query=pd.read_sql_query(sqlstr,self.mydb)
            df=pd.DataFrame(SQL_Query,columns=["product_id","product_name","category_name","unitprice","previous_price","num_product","left_product"])
            
            for x in range(len(df)):
                
                if useroption=="increase":
                    previous_price=int(df.loc[x,"unitprice"])
                    update=previous_price+(previous_price*upd_percent)
                    pid=int(df.loc[x,"product_id"])
                    sqlstr="Update product_tb set unitprice="+str(update)+" , previous_price="+str(previous_price)+" where product_id="+str(pid)+";"
                    cursor.execute(sqlstr)
                    self.mydb.commit()
                    print(cursor.rowcount,"records affected into product table.")
                else:
                    previous_price=int(df.loc[x,"unitprice"])
                    update=previous_price-(previous_price*upd_percent)
                    pid=int(df.loc[x,"product_id"])
                    sqlstr="Update product_tb set unitprice="+str(update)+" , previous_price="+str(previous_price)+" where product_id="+str(pid)+";"
                    cursor.execute(sqlstr)
                    self.mydb.commit()
                    print(cursor.rowcount,"records affected into product table.")

            
            upd_sqlstr="select * from product_tb " 
            SQL_Query=pd.read_sql_query(upd_sqlstr,self.mydb)
            upd_all_df=pd.DataFrame(SQL_Query,columns=["product_id","product_name","category_name","unitprice","previous_price","num_product","left_product"])
            
            if len(upd_all_df)<1:
                QMessageBox.about(self,"Not Found","Please Try Another Product.")
            from TableModel import pandasModel
            model= pandasModel(upd_all_df)
            self.tableView.setModel(model)
            
    
                
                



