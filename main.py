from PyQt6.QtWidgets import *
from PyQt6 import uic
import sys
import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

class MyGUI(QMainWindow):

    def __init__(self):
        super(MyGUI, self).__init__()
        uic.loadUi("EmailClientGUI.ui", self)
        self.show()

        self.userLogin.clicked.connect(self.login)
        self.addAttachment.clicked.connect(self.attachFile)
        self.send.clicked.connect(self.sendEmail)

    def login(self):
        try:
            self.server = smtplib.SMTP(self.smtpServer.text(), self.port.text())
            self.server.ehlo()
            self.server.starttls()
            self.server.ehlo()
            self.server.login(self.emailAddress.text(), self.password.text())

            self.emailAddress.setEnabled(False)
            self.password.setEnabled(False)
            self.smtpServer.setEnabled(False)
            self.port.setEnabled(False)
            self.userLogin.setEnabled(False)

            self.to.setEnabled(True)
            self.subject.setEnabled(True)
            self.addAttachment.setEnabled(True)
            self.mainContent.setEnabled(True)
            self.send.setEnabled(True)

            self.msg = MIMEMultipart()
        except smtplib.SMTPAuthenticationError:
            message_box = QMessageBox()
            message_box.setText("Invalid Login Info!")
            message_box.exec()
        except:
            message_box = QMessageBox()
            message_box.setText("Login Failed!")
            message_box.exec()

    def attachFile(self):
        pass

    def sendEmail(self):
        pass

app = QApplication([])
window = MyGUI()
sys.exit(app.exec())