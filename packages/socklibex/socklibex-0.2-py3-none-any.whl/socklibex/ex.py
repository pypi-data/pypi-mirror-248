def show_info():
    return "Информация о написании кода на разных языках..."

#Python
# import socket
# import threading
# import json
# from PyQt5.QtCore import pyqtSignal, QObject


# class ServerSignals(QObject):
#     new_data = pyqtSignal(object)
    
# class ServerThread(threading.Thread):
#     def __init__(self, signals):
#         super().__init__()
#         self.signals = signals
#         self.running = True

#     def run(self):
#         self.start_server(self.signals)
        
    
#     def stop_server(self):
#         self.running = False  
    

#     def start_server(self, signals, host='0.0.0.0', port=12345):
#             server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#             server.bind((host, port))
#             server.listen()
#             print(f"Server listening on {host}:{port}")

#             server.settimeout(1)
            
#             try:
#                 while self.running:                    
#                     try:
#                         conn, addr = server.accept()
#                         client_thread = threading.Thread(target=self.handle_client, args=(conn, addr, self.signals))
#                         client_thread.start()
#                     except socket.timeout:
#                         continue
#             except KeyboardInterrupt:
#                 print("Server is shutting down")
#             finally:
#                 server.close()
    
    
#     def work_with_json(self, data):
#         try:
#             received_json = data.decode('utf-8')
#             received_data = json.loads(received_json)
#             return received_data
#         except Exception as e:
#             print("Error handling data from")
           
                                                  
#     def handle_client(self, connection, address, signals):
#             print(f"Connected by {address}")
#             try:
#                 while True:
#                     data = connection.recv(10024)
#                     # print(data)
#                     if not data:
#                         break
                   
#                     received_data = self.work_with_json(data)                  
#                     connection.sendall(b"Data received")                   
                  
#                     signals.new_data.emit(received_data)

#             except Exception as e:
#                 print(f"Error handling data from {address}: {e}")
#             finally:
#                 connection.close()
                

# from PyQt5.QtWidgets import *
# from PyQt5.QtCore import *
# from PyQt5.QtGui import *
# import server
# from win_to_show_items import DetailsWindow
# import json
# from order import OrderItem

# class TableWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()

#         # Создание центрального виджета
#         central_widget = QWidget()
#         self.setCentralWidget(central_widget)   
        
#         #Строка поиcка
#         self.searchBar = QLineEdit()
#         self.searchBar.setPlaceholderText("Поиск товаров...")
#         self.searchBar.textChanged.connect(self.search_item)
            

#         # Создание таблицы
#         self.table = QTableWidget()
#         self.table.setColumnCount(100) 

#         # Размещение календаря и таблицы в вертикальном макете
#         layout = QVBoxLayout()  
#         layout.addWidget(self.searchBar)      
#         layout.addWidget(self.table)     
#         central_widget.setLayout(layout)

#         # Настройка размера окна
#         self.setGeometry(300, 300, 600, 400)
#         self.setMinimumSize(770, 400)
#         self.setWindowTitle("Просмотр данных")
        
#         self.start_server()      
        
#     def search_item(self, text):
#         for row in range(self.table.rowCount()):
#             item = self.table.item(row, 1) 
#             self.table.setRowHidden(row, text.lower() not in item.text().lower() if item else False)      


#     def start_server(self):
#         self.server_signals = server.ServerSignals()
    
#         self.server_signals.new_data.connect(self.load_data)    

#         self.server_thread = server.ServerThread(self.server_signals)
#         self.server_thread.start()

    
#     def load_data(self, received_data):
#         products_data = received_data['products']
#         self.update_table(products_data)

        
#     def update_table(self, products):
#         self.table.setRowCount(len(products))
#         self.table.setColumnCount(3)  # У нас есть 3 столбца: ID, Name, Description

#         self.table.setHorizontalHeaderLabels(["ID", "Name", "Description"])

#         for row, item in enumerate(products):
#             self.table.setItem(row, 0, QTableWidgetItem(item['id']))
#             self.table.setItem(row, 1, QTableWidgetItem(item['name']))
#             self.table.setItem(row, 2, QTableWidgetItem(item['description']))


#     def closeEvent(self, event):
#         self.server_thread.stop_server()
#         self.server_thread.join()  
#         super().closeEvent(event)
                                  
                                  
                                  
# import sys
# from PyQt5.QtWidgets import QApplication
# from window_to_show_items import TableWindow 
# from PyQt5 import QtWidgets


# def main():
#     app = QtWidgets.QApplication(sys.argv)
#     mainWin = TableWindow()       
#     mainWin.show()
#     sys.exit(app.exec_())
    
    
    
# if __name__ == "__main__":
#     main()