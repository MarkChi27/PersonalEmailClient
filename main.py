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
        options = QFileDialog.Option.ReadOnly | QFileDialog.Option.DontUseNativeDialog
        filenames, _ = QFileDialog.getOpenFileNames(self, "Open File", "", "All Files (*.*)", options=options)
        if filenames != []:
            for filename in filenames:
                attachment = open(filename, 'rb')
                filename = filename[filename.rfind("/")+1:]

                p = MIMEBase('application', 'octet-stream')
                p.set_payload(attachment.read())
                encoders.encode_base64(p)
                p.add_header("Content-Disposition", f"attachment; filename={filename}")
                self.msg.attach(p)
                if not self.attachments.text().endswith(":"):
                    self.attachments.setText(self.attachments.text() + ",")
                self.attachments.setText(self.attachments.text() + " " + filename)

    def sendEmail(self):
        button = QMessageBox.question(
            self,
            "Question",
            "Do you wish to send this email?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if button == QMessageBox.StandardButton.Yes:
            try:
                self.msg['From'] = "Jason Yang"
                self.msg['To'] = self.to.text()
                self.msg['Subject'] = self.subject.text()
                self.msg.attach(MIMEText(self.mainContent.toPlainText(), 'plain'))
                text = self.msg.as_string()
                self.server.sendmail(self.emailAddress.text(), self.to.text(), text)

                message_box = QMessageBox()
                message_box.setText("Email has been sent!")
                message_box.exec()
            except:
                message_box = QMessageBox()
                message_box.setText("Failed to send email!")
                message_box.exec()

app = QApplication([])
window = MyGUI()
sys.exit(app.exec())