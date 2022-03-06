from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
from PyQt5 import QtWidgets,uic
from PyQt5.QtWidgets import QApplication
import mysql.connector as c
import pandas as pd
from PyQt5.QtWidgets import QMessageBox
import re
#from AdminClass import SetComboData

class CRUDCashProcess(QDialog):
    def __init__(self,user_id):
        super(CRUDCashProcess,self).__init__()
        uic.loadUi("CRUDcashier.ui",self)
        self.setWindowTitle("CRUD Employee")
        
        self.LoadData(user_id)
        self.mydb=None
        self.updatebtn.clicked.connect(self.UpdateData)
        self.addbtn.clicked.connect(self.AddData)
        self.deletebtn.clicked.connect(self.DeleteData)
        self.clearbtn.clicked.connect(self.ClearData)

    def ClearData(self):
        self.idtxt.clear()
        self.nametxt.clear()
        self.roletxt.clear()   
        self.usernametxt.clear()
        self.passwordtxt.clear() 
        self.addresstxt.clear()
        self.phtxt.clear()
        self.emailtxt.clear() 
        self.banktxt.clear()
        self.idtxt.setEnabled(True)

    def check(self):
        regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        
        email=self.emailtxt.toPlainText()

        if(re.fullmatch(regex, email)):
            print("Valid Email")
        else:
            print("Invalid Email")

    def UpdateData(self):
        uid=self.idtxt.toPlainText()
        username= self.nametxt.toPlainText()
        role=self.roletxt.toPlainText()
        role=role.lower().strip()
        log_name= self.usernametxt.toPlainText()
        log_pass=self.passwordtxt.toPlainText()
        address=self.addresstxt.toPlainText()
        phone=self.phtxt.toPlainText().strip()
        bankacc=self.banktxt.toPlainText()

        email=self.emailtxt.toPlainText()
        regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        if(re.fullmatch(regex,email)):
            if role=="cashier" or role=="admin":
                if len(phone)==11:
                    if len(uid)<=0 or len(username)<=0 or len(role)<=0 or len(log_name)<=0 or len(log_pass)<=0 or len(address)<=0 or len(phone)<=0 or len(email)<=0 or len(bankacc)<=0:
                        QMessageBox.about(self,"No Entry Data","Please Fill all data completely.")
                    
                    else:
                        reply=QMessageBox.question(self,"Quit","Are you sure to update this product?",
                            QMessageBox.Yes|QMessageBox.No,QMessageBox.No) 
                        if reply==QMessageBox.Yes:
                            self.DBConnect()
                            cursor=self.mydb.cursor()
                            sqlstr="update userinfo_tb set userinfo_tb.username ='"+username+"', userinfo_tb.role='"+role+"', userinfo_tb.address='"+address+"',userinfo_tb.phone_number='"+phone+"',userinfo_tb.email='"+email+"', userinfo_tb.bankacc='"+bankacc+"' where user_id="+str(uid)
                            log_sqlstr="update login_tb set login_tb.username ='"+log_name+"', login_tb.password='"+log_pass+"' where user_id="+str(uid)
                            print(sqlstr,log_sqlstr)
                            cursor.execute(sqlstr)
                            cursor.execute(log_sqlstr)
                            
                            self.mydb.commit()
                            print(cursor.rowcount," record affected.")   
                            QMessageBox.about(self,"Success","Your Data are updated successfully.")
                            self.idtxt.setEnabled(True)
                else:
                    QMessageBox.about(self,"Invalid Phone Number","Please fill up to 11 digits")
            else:
                QMessageBox.about(self,"Invalid Role","Please fill cashier or admin")
        else:
            QMessageBox.about(self,"Invalid Email","Please end with @gmail.com")


    def AddData(self):
        self.idtxt.setEnabled(True)
        uid=self.idtxt.toPlainText()
        username= self.nametxt.toPlainText()
        role=self.roletxt.toPlainText()
        role=role.lower().strip()
        print(role)
        
        log_name= self.usernametxt.toPlainText()
        log_pass=self.passwordtxt.toPlainText()
        address=self.addresstxt.toPlainText()
        phone=self.phtxt.toPlainText().strip()

        bankacc=self.banktxt.toPlainText()

        email=self.emailtxt.toPlainText()
        regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        if(re.fullmatch(regex,email)):
            if role=="cashier" or role=="admin":
                if len(phone)==11:
                    if len(uid)<1 or len(username)<1 or len(role)<1 or len(log_name)<1 or len(log_pass)<1 or len(address)<1 or len(phone)<1 or len(email)<1 or len(bankacc)<1:
                        QMessageBox.about(self,"No Entry Data","Please Fill all data completely.")
                        
                    else:
                        result=self.SearchID(uid)
                        log_result=self.SearchLogID(uid)
                    if result==False and log_result==False:
                        QMessageBox.about(self,"Duplicate UserId","Please Enter Another User Id that you want to add")
                    else:
                        username= self.nametxt.toPlainText()
                        role=self.roletxt.toPlainText()
                        log_name= self.usernametxt.toPlainText()
                        log_pass=self.passwordtxt.toPlainText()
                        address=self.addresstxt.toPlainText()
                        phone=self.phtxt.toPlainText()
                        email=self.emailtxt.toPlainText()
                        bankacc=self.banktxt.toPlainText()

                        self.DBConnect()
                        cursor=self.mydb.cursor()

                        sqlstr="insert into userinfo_tb(user_id,username,role,address,phone_number,email,bankacc) values(%s,%s,%s,%s,%s,%s,%s)"
                        val=(str(uid),username,role,address,phone,email,bankacc)
                        cursor.execute(sqlstr,val)

                        log_sqlstr="insert into login_tb(username,password,user_id) values(%s,%s,%s)"
                        log_val=(log_name,log_pass,str(uid))
                        cursor.execute(log_sqlstr,log_val)

                        self.mydb.commit()
                        QMessageBox.about(self,"Success","New data is inserted successfully.")
                else:
                    QMessageBox.about(self,"Invalid Phone Number","Please fill up to 11 digits")
            else:
                QMessageBox.about(self,"Invalid Role","Please fill cashier or admin")       
        else:
            QMessageBox.about(self,"Invalid Email","Please end with @gmail.com")


    def DeleteData(self):
        self.DBConnect()
        uid=self.idtxt.toPlainText()
        if len(uid)<1:
            QMessageBox.about(self,"Entry Data","Please Enter Product Id that you want to delete.")
        else:
            result=self.SearchID(uid)
            log_result=self.SearchLogID(uid)
            if result==True and log_result==True:
                QMessageBox.about(self,"No Data Found","Please Enter Product Id that you want to delete")
            else:
                reply=QMessageBox.question(self,"Quit","Are you sure to delete this product?",
                        QMessageBox.Yes|QMessageBox.No,QMessageBox.No) 
                if reply==QMessageBox.Yes:
                    cursor=self.mydb.cursor()
                    sqlstr="delete from userinfo_tb where user_id="+str(uid)
                    cursor.execute(sqlstr)

                    log_sqlstr="delete from login_tb where user_id="+str(uid)
                    cursor.execute(log_sqlstr)

                    self.mydb.commit()
                    QMessageBox.about(self,"Success","Your Product is deleted successfully.")
                    self.ClearData()
        

    def SearchID(self,uid): 
        self.DBConnect()
        sign=False
        cursor=self.mydb.cursor()
        sqlstr="select * from userinfo_tb where user_id="+str(uid)
        cursor.execute(sqlstr)
        result=cursor.fetchone()
        if result==None:
            sign=True
        return sign

    def SearchLogID(self,uid):
        self.DBConnect()
        sign=False
        cursor=self.mydb.cursor()
        log_sqlstr="select * from login_tb where user_id="+str(uid)
        cursor.execute(log_sqlstr)
        log_result=cursor.fetchone()
        if log_result==None:
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

    def LoadData(self,user_id):
        self.DBConnect()
        cursor=self.mydb.cursor()
        sqlstr="select * from userinfo_tb where user_id="+str(user_id)
        print(sqlstr)
        cursor.execute(sqlstr)
        result=cursor.fetchone()
        self.idtxt.setPlainText(str(result[0]))
        self.nametxt.setPlainText(str(result[1]))
        self.roletxt.setPlainText(str(result[2]))
        self.addresstxt.setPlainText(str(result[3]))
        self.phtxt.setPlainText(str(result[4]))
        self.emailtxt.setPlainText(str(result[5]))
        self.banktxt.setPlainText(str(result[6]))

        log_sqlstr="select * from login_tb where user_id="+str(user_id)
        cursor.execute(log_sqlstr)
        log_result=cursor.fetchone()
        self.usernametxt.setPlainText(str(log_result[1]))
        self.passwordtxt.setPlainText(str(log_result[2]))

        self.idtxt.setEnabled(False)



"""app=QApplication(sys.argv)
stu=CRUDProcess(1002)
stu.show()
app.exec_()"""