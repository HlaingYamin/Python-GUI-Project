from os import name
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QDate, QTime, QDateTime, Qt
from PyQt5 import QtWidgets,uic
import mysql.connector as c

class Login_Class(QDialog):
    def __init__(self):
        super(Login_Class,self).__init__()
        uic.loadUi("loginform.ui",self) #Connect with designer(LoginForm.ui) 
        self.logo.setScaledContents(True);
        self.logo.setPixmap(QPixmap("keyIcon.png"))
        self.logo.setStyleSheet("background-image:url(ketIcon.png);")

        self.loginBtn.clicked.connect(self.LoginProcess)
        #self.signUpBtn.clicked.connect(self.SignUpProcess)
        self.mydb=None

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
        
    def LoginProcess(self):
        usr=self.userTxtBox.toPlainText().strip()
        pwd=self.passTxtBox.text().strip()

        print(f"Username {usr} and Password {pwd}")
        self.CheckLogin(usr,pwd)

    def GetUserRole(self,user_id):
        mycursor1=self.mydb.cursor()
        mycursor1.execute("select * from userinfo_tb where user_id="+str(user_id))
        value=mycursor1.fetchall()
        print("In User Role")
        role=None
        name=None
        for x in value:
            role=x[2]
            name=x[1]
        return role,name  

    def CheckLogin(self,usr,pwd):
        self.DBConnect()
        mycursor=self.mydb.cursor()
        mycursor.execute("Select * from login_tb")
        rows=mycursor.fetchall()
        found=0
        for x in rows:
            if usr==x[1] and pwd==x[2]:
                print("Login Successful")
                found=1
                user_id=x[3]
                role,name=self.GetUserRole(user_id)
                if role.lower()=="admin":
                    
                    from AdminClass import Admin_Process_Class
                    admin=Admin_Process_Class(user_id,role,name)
                    admin.showMaximized()
                    admin.exec_()
                else:
                    role=role.lower()                  
                    from CashierClass import Cashier_Process_Class
                    stu=Cashier_Process_Class(user_id,role,name)
                    stu.showMaximized()
                    stu.exec_()  
                break
        if found==0:
                from PyQt5.QtWidgets import QMessageBox
                self.userTxtBox.clear()
                self.passTxtBox.clear()

                msg=QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Username and password does not exist.Please Try Again.")
                msg.setWindowTitle("Login Error")
                msg.setInformativeText("Next Login")
                msg.exec_()

    
    """def SignUpProcess(self):
        print("In Sign Up")
"""
if __name__=="__main__":
    app = QApplication(sys.argv)
    login = Login_Class()
    login.showMaximized()
    app.exec_()
