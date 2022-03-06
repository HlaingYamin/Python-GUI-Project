from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
from PyQt5 import QtWidgets,uic
from PyQt5.QtWidgets import QApplication
import mysql.connector as c
import pandas as pd
from PyQt5.QtWidgets import QMessageBox
from datetime import datetime 


class Cashier_Process_Class(QDialog):
    def __init__(self,id,role,name):
        super(Cashier_Process_Class,self).__init__()
        uic.loadUi("cashierform.ui",self)
        self.setWindowTitle("Sale Products")
        self.cashierlbl.setText("Cashier Name :"+name)
    
        self.UserID=id
        self.role=role
        self.name=name

        self.searchbtn.clicked.connect(self.SearchBut)
        self.addcartbtn.clicked.connect(self.AddCartItem)
        self.viewbtn.clicked.connect(self.ViewItem)

        self.detailclearbtn.clicked.connect(self.ClearData)
        self.tableView.clicked.connect(self.TableSelect)

        self.mydb=None

        self.end_date = datetime.now()
        self.text=self.end_date.strftime("%Y, %m, %d")
        self.datetimelbl.setText("Date : "+ str(self.text))
        
    def ClearData(self):
        self.searchtxt.clear()
        self.pidtxt.clear()
        self.pnametxt.clear()
        self.categorytxt.clear()
        self.pricetxt.clear()
        self.stocktxt.clear()
        self.qtytxt.clear()
        

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
            
    def SearchBut(self):
        inputdata=self.GetData()
        print(f"{inputdata}")
        self.ProductSearch(inputdata)
    
    def GetData(self):  
        inputdata=self.searchtxt.toPlainText()
        return inputdata

    def GetIDData(self):
        productId=self.pidtxt.toPlainText()
        return productId

    def ProductSearch(self,inputdata):
        inputdata=inputdata.strip()
        if len(inputdata)==0:
            QMessageBox.about(self,"No Data","Please Fill Product Id(eg;1001)!")
            self.searchtxt.clear()
        else:
            #self.CheckProductID(inputdata)
            self.DBConnect()
            cursor=self.mydb.cursor
            sqlstr="select * from product_tb where product_id="+str(inputdata)
            SQL_Query=pd.read_sql_query(sqlstr,self.mydb)
            df=pd.DataFrame(SQL_Query,columns=["product_id","product_name","category_name","unitprice","num_product","left_product"])
            print(df)
            if len(df)<1:
                QMessageBox.about(self,"No Match Product","Please Try Another Product.")
                self.ClearData()
            else: 
                self.LoadData(inputdata)
                


    def LoadData(self,pid):
        self.DBConnect()
        cursor=self.mydb.cursor()
        sqlstr="select * from product_tb where product_id="+str(pid)
        cursor.execute(sqlstr)
        result=cursor.fetchone()
        self.pidtxt.setPlainText(str(result[0]))
        self.pnametxt.setPlainText(str(result[1]))
        self.categorytxt.setPlainText(str(result[2]))
        self.pricetxt.setPlainText(str(result[3]))
        self.stocktxt.setPlainText(str(result[6]))
        self.pidtxt.setEnabled(False)
        self.pnametxt.setEnabled(False)
        self.categorytxt.setEnabled(False)
        self.pricetxt.setEnabled(False)
        self.stocktxt.setEnabled(False)


    def AddCartItem(self):
        self.qtytxt.setEnabled(True)
        inputIDdata=self.GetIDData()
        if len(inputIDdata)<1:
            QMessageBox.about(self,"No Data","Please Search by Product ID!")
            #QMessageBox.setStyleSheet("QLabel{ color: white}")
            inputIDdata=self.GetIDData()

        else:
            #self.qtytxt.setEnabled(False)
            self.DBConnect()
            cursor=self.mydb.cursor

            sqlstr="select * from product_tb where product_id="+str(inputIDdata)
            SQL_Query=pd.read_sql_query(sqlstr,self.mydb)
            df=pd.DataFrame(SQL_Query,columns=["product_id","product_name","category_name","unitprice","num_product","left_product"])
            
            left_copy=list(df["left_product"])
            left_copy=int(left_copy[0])
            print(str(left_copy))
            #copy_num=int(df.loc[0,"left_product"])
            qty_amt=self.qtytxt.toPlainText()
            if len(qty_amt)<1:
                QMessageBox.about(self,"Fill Quantity","Please Fill Desired quantity!")
                self.qtytxt.clear()
            else:

                if left_copy<1:
                    QMessageBox.about(self,"Sold Out Product!","Please try another product")
                    self.qtytxt.clear()
                elif (int(qty_amt)>left_copy):
                    QMessageBox.about(self,"Invalid Stock!!","Try another quantity")
                    self.qtytxt.clear()
                else:
                    reply=QMessageBox.question(self,"Add to cart","Are you sure to buy this product?",
                            QMessageBox.Yes|QMessageBox.No,QMessageBox.No)
                    
                    if reply==QMessageBox.Yes:
                        #count minus to product_tb
                        self.MinusProduct(df)
                        self.qtytxt.clear()
                        #add information to borrow_tb
                        self.UpdateSaleProduct(df)
                        QMessageBox.about(self,"Dear "+self.name,"Finished!The product is bought.")
                    
    def MinusProduct(self,df):
        copy_num=int(df.loc[0,"left_product"])
        qty_amt=self.qtytxt.toPlainText()

        copy_num=copy_num-int(qty_amt)
        product_id=int(df.loc[0,"product_id"])
        cursor=self.mydb.cursor()
        sqlstr="Update product_tb set left_product="+str(copy_num)+" where product_id="+str(product_id)+";"
        print(sqlstr)
        cursor.execute(sqlstr)
        self.mydb.commit()
        print(cursor.rowcount,"records affected into product table.")
        

    def UpdateSaleProduct(self,df):
        product_id=int(df.loc[0,"product_id"])
        user_id=self.UserID 

        from datetime import datetime
        current=datetime.now()
        #matchdate=current.strftime("%Y, %m, %d")

        cursor=self.mydb.cursor()

        sql="insert into sale_tb(user_id,product_id,sale_date_time) values(%s,%s,%s)"
        val=(user_id,product_id,str(current))
        cursor.execute(sql,val)
        self.mydb.commit()
        print(cursor.rowcount,"records affected into Sale table.")
        
    def ViewItem(self):
        #self.user_id
        self.DBConnect()
        cursor=self.mydb.cursor()
        sqlstr="select product_tb.product_id,product_tb.product_name,product_tb.category_name,product_tb.unitprice,product_tb.left_product,sale_tb.sale_date_time from product_tb,sale_tb where sale_tb.user_id="+str(self.UserID)+" and sale_tb.product_id=product_tb.product_id"
        print(sqlstr)

        SQL_Query=pd.read_sql_query(sqlstr,self.mydb)
        #all_df=pd.DataFrame(SQL_Query,columns=["title","author","published_year","left_copies"])
        df=pd.DataFrame(SQL_Query,columns=["product_id","product_name","category_name","unitprice","left_product","sale_date_time"])

        if len(df)<1:
            QMessageBox.about(self,"Not Found")
        from TableModel import pandasModel
        model= pandasModel(df)
        self.tableView.setModel(model)

    def TableSelect(self):
        self.addcartbtn.setEnabled(True)

    

"""app=QApplication(sys.argv)
#stu=Student_Teacher_Class(3,"student","Soe Mtint")
stu=Cashier_Process_Class(2,"cashier","Hla Hla")
stu.show()
app.exec_()"""
