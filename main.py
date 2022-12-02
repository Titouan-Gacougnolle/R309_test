import sys, threading, time, socket
from PyQt5.QtCore import QCoreApplication, pyqtSlot
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QGridLayout, QCheckBox, QComboBox, QDateEdit, QSlider, \
    QLabel, QMainWindow, QLineEdit, QPushButton

class Fenetre(QMainWindow):

    def __init__(self,  host: str = '127.0.0.1', port: int = 10000):
        super().__init__()
        self.__host = host
        self.__port = port
        self.__socket_client = None

        widget = QWidget()
        self.setCentralWidget(widget)
        self.__arret_thread = False
        self.__t1 = None

        self.__grid = QGridLayout()
        widget.setLayout(self.__grid)
        self.setWindowTitle('Chronomètre')

        self.__lab = QLabel("Compteur")
        self.__lab2 = QLineEdit("")
        self.__startbutn = QPushButton("START")
        self.__stopbutn = QPushButton("STOP")
        self.__reset = QPushButton("RESET")
        self.__connectbutn = QPushButton("CONNECT")
        self.__quit = QPushButton("QUITTER")


        self.__grid.addWidget(self.__lab, 0, 0, 1, 1,)
        self.__grid.addWidget(self.__lab2, 1, 0, 1, 2)
        self.__grid.addWidget(self.__startbutn, 2, 0, 1, 2)
        self.__grid.addWidget(self.__stopbutn, 3 , 0, 1, 1)
        self.__grid.addWidget(self.__reset, 3, 1, 1, 1)
        self.__grid.addWidget(self.__connectbutn, 4, 0, 1, 1)
        self.__grid.addWidget(self.__quit, 4, 1, 1, 1)

        self.__startbutn.clicked.connect(self.start)
        self.__reset.clicked.connect(self.reset)
        self.__quit.clicked.connect(self.quit)
        self.__stopbutn.clicked.connect (self.stop)
        self.__connectbutn.clicked.connect(self.connect)

    def connect(self):
        if self.__socket_client == None:
            self.__socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print(f"Le client tente de se connecter au serveur {self.__host}")
            try:
                self.__socket_client.connect((self.__host, self.__port))
                print(f"Le client s'est connecté au serveur {self.__host} \n")

            except ConnectionRefusedError:
                print(f"La connexion au serveur {self.__host} n'a pas pu se faire \n")
        else:
            print('Vous êtes déja connecté')

    def stop(self):
        if self.__socket_client == None:
            pass
        else:
            message = 'Le client a appuyé sur "STOP"'
            try:
                self.__socket_client.send(message.encode())
            except:
                pass
        self.__arret_thread = True
        if self.__t1 == None:
            pass
        else:
            self.__t1.join()


    def quit(self):
        if self.__socket_client == None:
            pass
        else:
            message = 'bye'
            print('fin de la connexion')
            self.__socket_client.send(message.encode())
        self.stop()
        QCoreApplication.exit(0)

    def reset(self):
        if self.__socket_client == None:
            pass
        else:
            message = 'Le client a appuyé sur "RESET"'
            self.__socket_client.send(message.encode())
        self.__arret_thread = True
        self.__t1.join()
        self.__lab2.setText('')


    def start(self):
        if self.__socket_client == None:
            pass
        else:
            message = 'Le client a appuyé sur "START"'
            self.__socket_client.send(message.encode())
        self.__t1 = threading.Thread(target=self.__start, args=[])
        self.__t1.start()

    def __start(self):
        self.__arret_thread = False
        compteur = 0 #self.__lab2.text()
        while not self.__arret_thread:
            compteur = compteur+1
            self.__lab2.setText(str(compteur))
            if self.__socket_client == None:
                pass
            else:
                message = str(compteur)
                try:
                    self.__socket_client.send(message.encode())
                except OSError:
                    self.__socket_client = None
                    pass
            time.sleep(1)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Fenetre()
    window.show()
    sys.exit(app.exec_())


#https://github.com/Titouan-Gacougnolle/R309_test