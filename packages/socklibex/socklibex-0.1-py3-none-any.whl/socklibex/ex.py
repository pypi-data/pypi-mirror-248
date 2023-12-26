def show_info():
    return "Информация о написании кода на разных языках..."

#C#
# using System.Collections.Generic;
# using System.IO;
# using System.Linq;
# using System.Text.Json;
# using MARATHON2._0.Classes;

# namespace MARATHON2._0
# {
#     public class JsonDatabase
#     {
#         public const string filename1 = "Database.json";
#         public const string filename2 = "Database2.json";
#         public const string filename3 = "Database3.json";

#         private static List<User> _users;
#         private static List<Item> _items;
#         private static List<Category> _categories;

#         public static List<User> GetAllUsers()
#         {
#             if (_users == null)
#             {
#                 if (new FileInfo(filename1).Exists)
#                 {
#                     using (FileStream fs = new FileStream(filename1, FileMode.Open))
#                     {
#                         _users = JsonSerializer.Deserialize<List<User>>(fs);
#                     }
#                 }
#                 else
#                 {
#                     _users = new List<User>();
#                 }
#             }
#             return _users;
#         }

#         public static List<Item> GetAllItems()
#         {
#             if (_items == null)
#             {
#                 if (new FileInfo(filename2).Exists)
#                 {
#                     using (FileStream fs = new FileStream(filename2, FileMode.Open))
#                     {
#                         _items = JsonSerializer.Deserialize<List<Item>>(fs);
#                     }
#                 }
#                 else
#                 {
#                     _items = new List<Item>();
#                 }
#             }
#             return _items;
#         }

#         public static List<Category> GetAllCategory()
#         {
#             if (_categories == null)
#             {
#                 if (new FileInfo(filename3).Exists)
#                 {
#                     using (FileStream fs = new FileStream(filename3, FileMode.Open))
#                     {
#                         _categories = JsonSerializer.Deserialize<List<Category>>(fs);
#                     }
#                 }
#                 else
#                 {
#                     _categories = new List<Category>();
#                 }
#             }
#             return _categories;
#         }


#         public static Category GetCategoryByName(string name)
#         {
#             return GetAllCategory().FirstOrDefault(u => u.Name == name);
#         }

#         public static Item GetItemByID(int id)
#         {
#             return GetAllItems().FirstOrDefault(u => u.Id == id);
#         }

#         public static User GetUserByEmail(string email)
#         {
#             return GetAllUsers().FirstOrDefault(u => u.Email == email);
#         }

#         public static Item AddItem(Item item)
#         {
#             var items = GetAllItems();
#             items.RemoveAll(v => v.Id == item.Id);
#             items.Add(item);
#             SaveToFile(filename2, items);
#             return item;
#         }

#         public static User AddUser(User user)
#         {
#             var users = GetAllUsers();
#             users.RemoveAll(v => v.Email == user.Email);
#             users.Add(user);
#             SaveToFile(filename1, users);
#             return user;
#         }

#         public static Item EditItem(Item item)
#         {
#             var items = GetAllItems();
#             var dbItem = items.FirstOrDefault(u => u.Id == item.Id);
#             if (dbItem != null)
#             {
#                 dbItem.Name = item.Name;
#                 dbItem.Description = item.Description;
#                 dbItem.Price = item.Price;
#                 SaveToFile(filename2, items);
#             }
#             return dbItem;
#         }

#         public static User EditUser(User user)
#         {
#             var users = GetAllUsers();
#             var dbUser = users.FirstOrDefault(u => u.Email == user.Email);
#             if (dbUser != null)
#             {
#                 dbUser.Email = user.Email;
#                 dbUser.Password = user.Password;
#                 dbUser.productIds = user.productIds;
#                 SaveToFile(filename1, users);
#             }
#             return dbUser;
#         }

#         public static void DeleteItem(int Id)
#         {
#             var items = GetAllItems();
#             items.RemoveAll(u => u.Id == Id);
#             SaveToFile(filename2, items);
#         }

#         public static Category AddCategory(Category category)
#         {
#             var categories = GetAllCategory();
#             categories.RemoveAll(v => v.Id == category.Id);
#             categories.Add(category);
#             SaveToFile(filename3, categories);
#             return category;
#         }

#         public static Category EditCategory(Category category)
#         {
#             var categories = GetAllCategory();
#             var dbCategory = categories.FirstOrDefault(u => u.Id == category.Id);
#             if (dbCategory != null)
#             {
#                 dbCategory.Name = category.Name;
#                 SaveToFile(filename3, categories);
#             }
#             return dbCategory;
#         }

#         public static void DeleteCategory(int Id)
#         {
#             var categories = GetAllCategory();
#             categories.RemoveAll(u => u.Id == Id);
#             SaveToFile(filename3, categories);
#         }

#         public static void DeleteUser(string email)
#         {
#             var users = GetAllUsers();
#             users.RemoveAll(u => u.Email == email);
#             SaveToFile(filename1, users);
#         }

#         private static void SaveToFile<T>(string filename, List<T> data)
#         {
#             using (FileStream fs = new FileStream(filename, FileMode.Create))
#             {
#                 JsonSerializer.Serialize(fs, data);
#             }
#         }
#     }
# }
# using System;
# using System.Collections.Generic;
# using System.ComponentModel.Composition;
# using System.Linq;
# using System.Text;
# using System.Threading.Tasks;
# using System.Net.Sockets;
# using MARATHON2._0.Classes;
# using System.Net;
# using System.Windows;
# using System.Net.Http.Headers;
# using System.Text.Json;
# using System.Windows.Markup;

# namespace MARATHON2._0.Classes
# {
#     public class Server
#     {
#         public static List<Socket> clients = new List<Socket>();
#         public static async void starts_server()
#         {
#             IPEndPoint ipPoint = new IPEndPoint(IPAddress.Any, 8080);
#             Socket socket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
#             socket.Bind(ipPoint);
#             while(true)
#             {
#                 socket.Listen(100);
                
#                 Socket client = await socket.AcceptAsync();
#                 ItemInfo info = new ItemInfo(JsonDatabase.GetAllItems(), JsonDatabase.GetAllCategory());

#                 string json = JsonSerializer.Serialize(info);

#                 byte[] data = Encoding.ASCII.GetBytes(json);
                

#                 byte[] data1 = new byte[1]; data1[0] = 1;
#                 client.Send(data.Concat(data1).ToArray());

#                 clients.Add(client);
#             }
            
#         }

#         public static void SendData()
#         {
#             try
#             {
#                 ItemInfo info = new ItemInfo(JsonDatabase.GetAllItems(), JsonDatabase.GetAllCategory());
#                 string json = JsonSerializer.Serialize(info);
#                 byte[] data = Encoding.ASCII.GetBytes(json);
#                 byte[] data1 = new byte[1]; data1[0] = 1;
#                 foreach (var client in clients)
#                 {
#                     client.Send(data.Concat(data1).ToArray());
#                 }
#             }
#             catch (SocketException)
#             {
#                 MessageBox.Show("Ошибка");
#             };
           
#         }
#     }

#     public class ItemInfo
#     {
#         public List<Item> item { get; set; }
#         public List<Category> categories { get; set; }

#         public ItemInfo(List<Item> item, List<Category> categories)
#         {
#             this.item = item;
#             this.categories = categories;
#         }
#     }
    
# }
# using System;
# using System.Collections.Generic;
# using System.Linq;
# using System.Net.Sockets;
# using System.Text;
# using System.Text.Json.Serialization;
# using System.Text.Json;
# using System.Threading.Tasks;
# using System.Windows;

# namespace MARATHON2._0
# {



#     public class Client
#     {
#         private TcpClient client;
#         private NetworkStream stream;

#         public Client(string serverAddress, int serverPort)
#         {            
#             client = new TcpClient(serverAddress, serverPort);
#             stream = client.GetStream();                                      
#         }

#         public async Task<string> SendOrderDataAsync(object orderData)
#         {
#             try
#             {
                
#                 // Конвертация данных в JSON
#                 string jsonOrderData = JsonSerializer.Serialize(orderData);                
#                 // Отправка данных
#                 byte[] data = Encoding.UTF8.GetBytes(jsonOrderData);
#                 await stream.WriteAsync(data, 0, data.Length);

#                 // Получение ответа
#                 data = new byte[256];
#                 int bytes = await stream.ReadAsync(data, 0, data.Length);
#                 return Encoding.UTF8.GetString(data, 0, bytes);
#             }
#             catch (Exception ex)
#             {
#                 return $"Ошибка: {ex.Message}";
#             }
#         }

#         public void CloseConnection()
#         {
#             stream.Close();
#             client.Close();
#         }
#     }
# }


####Python



# from PyQt5.QtWidgets import *
# from PyQt5.QtCore import *
# from PyQt5.QtGui import *
# import server
# from win_to_show_items import DetailsWindow
# from order import Order

# class TableWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()

#         # Создание центрального виджета
#         central_widget = QWidget()
#         self.setCentralWidget(central_widget)

#         # Создание календаря
#         self.calendar = QCalendarWidget()
#         self.calendar.selectionChanged.connect(self.data_filter)

#         # Создание таблицы
#         self.table = QTableWidget()
#         self.table.setColumnCount(100) 

#         # Размещение календаря и таблицы в вертикальном макете
#         layout = QVBoxLayout()
#         layout.addWidget(self.calendar)  
#         layout.addWidget(self.table)     
#         central_widget.setLayout(layout)

#         # Настройка размера окна
#         self.setGeometry(300, 300, 600, 400)
#         self.setMinimumSize(770, 400)
#         self.setWindowTitle("Просмотр данных")
        
#         self.start_server()
        
        
#     def data_filter(self):
#         selected_date = self.calendar.selectedDate().toString("yyyy-MM-dd")
#         for row in range(self.table.rowCount()):
#             date_item = self.table.item(row, 4) 
#             if date_item and selected_date in date_item.text():
#                 self.table.setRowHidden(row, False)
#             else:
#                 self.table.setRowHidden(row, True)


#     def start_server(self):
#         self.server_signals = server.ServerSignals()
    
#         self.server_signals.new_data.connect(self.load_data)    

#         self.server_thread = server.ServerThread(self.server_signals)
#         self.server_thread.start()

    
#     def load_data(self, received_data):        
#         data = received_data
#         print(data)
#         order = Order.from_dict(data)
#         self.update_table(order)

#     def update_table(self, order):
#         user = order.user
#         items = order.products
#         print(items)       

#         self.table.setRowCount(1)
#         self.table.setColumnCount(6)

#         self.table.setHorizontalHeaderLabels(["Email", "Общая стоимость", "Подробнее", "ID заказа", "Дата", "Время"])

#         email_item = QTableWidgetItem(user.get('Name', ''))  
#         email_item.setFlags(email_item.flags() & ~Qt.ItemIsEditable)
#         self.table.setItem(0, 0, email_item)

#         total_cost_item = QTableWidgetItem(str(sum(item.Price * item.Count for item in items)))
#         total_cost_item.setFlags(total_cost_item.flags() & ~Qt.ItemIsEditable)
#         self.table.setItem(0, 1, total_cost_item)

#         order_id_item = QTableWidgetItem(order.id)
#         order_id_item.setFlags(order_id_item.flags() & ~Qt.ItemIsEditable)
#         self.table.setItem(0, 3, order_id_item)

#         re_order_date_item = QTableWidgetItem(order.date.split('T')[0])
#         re_order_date_item.setFlags(re_order_date_item.flags() & ~Qt.ItemIsEditable)
#         self.table.setItem(0, 4, re_order_date_item)

#         re_order_time_item = QTableWidgetItem(order.date.split('T')[1].split('.')[0])
#         re_order_time_item.setFlags(re_order_time_item.flags() & ~Qt.ItemIsEditable)
#         self.table.setItem(0, 5, re_order_time_item)

#         details_button = QPushButton('Подробнее')
#         details_button.clicked.connect(lambda: self.show_purchase_details(items))
#         self.table.setCellWidget(0, 2, details_button)


    
#     def show_purchase_details(self, items):
#         details_window = DetailsWindow(items, self)
#         details_window.exec_()


#     def closeEvent(self, event):
#         self.server_thread.stop_server()
#         self.server_thread.join()  
#         super().closeEvent(event)


# """Dummy docstring."""
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
                
###Kotlin
# package com.example.lab_work_first

# import android.content.Intent
# import android.os.Bundle
# import android.widget.Button
# import android.widget.EditText
# import android.widget.Toast
# import androidx.appcompat.app.AppCompatActivity
# import org.json.JSONObject
# import java.io.File


# class MainActivity : AppCompatActivity() {

#     private var logBox: EditText? = null
#     private var passBox: EditText? = null
#     fun userLogin() {
#         if (logBox == null || passBox == null){
#             Toast.makeText(this, "поля пустые",
#                 Toast.LENGTH_SHORT).show()
#             return
#         }
#         else {

#         }
#         val login = logBox?.text.toString()
#         val pass = passBox?.text.toString()

#         val file = File(filesDir, "users.json")

#         val jsonString = if (file.exists()) {
#             file.bufferedReader().use {
#                 it.readText()
#             }
#         }
#         else {
#             "{\"users\":[]}"
#         }

#         val jsonObject = JSONObject(jsonString)
#         val usersArray = jsonObject.getJSONArray("users")
#         var isAuth = false

#         for (i in 0 until usersArray.length()) {
#             val userObject = usersArray.getJSONObject(i)
#             val userJSON = userObject.getString("login")
#             val passJSON = userObject.getString("password")
#             if (userJSON == login && passJSON == pass) {
#                 Toast.makeText(this, "успех",
#                     Toast.LENGTH_SHORT).show()
#                 isAuth = true
#                 val newPage = Intent(this, Items::class.java)
#                 startActivity(newPage)
#                 Security.user = User(userJSON, mutableListOf())
#                 break
#             }
#         }
#         if (isAuth == false) {
#             Toast.makeText(this, "Неуспех",
#                 Toast.LENGTH_SHORT).show()

#         }
#     }

#     override fun onCreate(savedInstanceState: Bundle?) {
#         super.onCreate(savedInstanceState)
#         setContentView(R.layout.activity_main)

#         val btnReg: Button = findViewById(R.id.buttonCreateAccount)
#         val btnSign: Button = findViewById(R.id.buttonLogin)
#         logBox = findViewById(R.id.editTextEmail)
#         passBox = findViewById(R.id.editTextPassword)

#         btnReg.setOnClickListener {
#             val intent = Intent(this@MainActivity, create_account::class.java)
#             startActivity(intent);finish();
#             }

#         btnSign.setOnClickListener {
#             userLogin()
#         }
#     }
# }
           

    

# package com.example.lab_work_first

# import android.annotation.SuppressLint
# import android.content.Intent
# import android.graphics.Color
# import android.os.Bundle
# import android.os.Handler
# import android.os.Looper
# import android.util.Log
# import android.view.Gravity
# import android.view.KeyEvent
# import android.view.View
# import android.widget.AdapterView
# import android.widget.ArrayAdapter
# import android.widget.Button
# import android.widget.EditText
# import android.widget.ImageButton
# import android.widget.LinearLayout
# import android.widget.Spinner
# import android.widget.TextView
# import android.widget.Toast
# import androidx.appcompat.app.AppCompatActivity
# import com.google.gson.Gson
# import org.json.JSONObject
# import java.io.File
# import java.io.IOException
# import java.net.InetSocketAddress
# import java.net.Socket
# import java.net.SocketTimeoutException
# import java.nio.charset.Charset
# import java.time.LocalDateTime
# import java.util.UUID
# import java.util.concurrent.Executors

# class Items<SocketException : Any> : AppCompatActivity() {

#     private var products = mutableListOf<Product>()
#     private var views = mutableListOf<MutableList<View>>()

#     override fun onCreate(savedInstanceState: Bundle?) {
#         super.onCreate(savedInstanceState)
#         setContentView(R.layout.items)

#         val btn_plus: Button = findViewById(R.id.add_item)
#         btn_plus.setOnClickListener {
#             val intent = Intent(this@Items, Add_product::class.java)
#             startActivity(intent);finish();
#         }

#         val btn_chat: ImageButton = findViewById(R.id.btn_search)
#         btn_chat.setOnClickListener {
#             val intent = Intent(this@Items, Chat::class.java)
#             startActivity(intent);finish();
#         }

#         val btn_cart: ImageButton = findViewById(R.id.btn_cart)
#         btn_cart.setOnClickListener {
#             val intent = Intent(this@Items, Items::class.java)
#             startActivity(intent);finish();
#         }
#         val btnprf: ImageButton = findViewById(R.id.btn_profile)

#         btnprf.setOnClickListener {
#             val intent = Intent(this@Items, UserProfile::class.java)
#             startActivity(intent);finish();
#         }

#         Thread() {
#             try {
#                 var socket = Socket()
#                 socket.connect(InetSocketAddress("10.0.2.2", 8080), 500)
#                 var inputStream = socket.getInputStream()

#                 val executor = Executors.newSingleThreadExecutor()
#                 var handler = Handler(Looper.getMainLooper())

#                 executor.execute(kotlinx.coroutines.Runnable {
#                     kotlin.run {
#                         while (true) {
#                             try {
#                                 var byte = 0;
#                                 var buffer = mutableListOf<Byte>()
#                                 while (true) {
#                                     var temp = inputStream.read()
#                                     if (temp == 1 && byte == 125) {
#                                         break;
#                                     }
#                                     byte = temp;
#                                     buffer.add(byte.toByte())
#                                 }

#                                 handler.post(Runnable {
#                                     kotlin.run {
#                                         try {
#                                             Log.i("client", buffer.toString())

#                                             val jsonObject = jsonToJsonObject(buffer)
#                                             Log.i("client", jsonObject.toString())

#                                             val usersFile =
#                                                 File(
#                                                     applicationContext.filesDir,
#                                                     "products.json"
#                                                 )
#                                             usersFile.writeText(jsonObject.toString())

#                                             val categories = getCategoriesFromJsonObject(jsonObject);

#                                             val s = findViewById<Spinner>(R.id.spinner)
#                                             val adapter: ArrayAdapter<String> =
#                                                 ArrayAdapter<String>(
#                                                     this,
#                                                     androidx.appcompat.R.layout.support_simple_spinner_dropdown_item,
#                                                     categories
#                                                 )
#                                             s.adapter = adapter

#                                             setProducts("", "")

#                                         } catch (e: ConcurrentModificationException) {
#                                             Log.e("client", "ConcurrentModificationException")
#                                         } finally {
#                                             buffer.clear()
#                                         }
#                                     }
#                                 })
#                             } catch (ex: IOException) {
#                                 ex.printStackTrace()
#                                 break;
#                             }
#                         }
#                     }
#                 })
#             } catch (ex: SocketTimeoutException) {
#                 ex.printStackTrace();
#             }
#         }.start()


#         val linearLayout = findViewById<LinearLayout>(R.id.list)

#         var editText = findViewById<EditText>(R.id.search)
#         var search = ""
#         var sort = ""
#         editText.setOnKeyListener(object : View.OnKeyListener {
#             override fun onKey(v: View?, keyCode: Int, event: KeyEvent): Boolean {
#                 if (event.action == KeyEvent.ACTION_DOWN &&
#                     keyCode == KeyEvent.KEYCODE_ENTER
#                 ) {
#                     editText.clearFocus()
#                     editText.isCursorVisible = false

#                     search = editText.text.toString()
#                     linearLayout.removeAllViews()

#                     setProducts(search, sort)

#                     return true
#                 }
#                 return false
#             }
#         })

#         var spinner = findViewById<Spinner>(R.id.spinner)
#         spinner.setOnItemSelectedListener(object : AdapterView.OnItemSelectedListener {
#             override fun onItemSelected(
#                 parentView: AdapterView<*>?,
#                 selectedItemView: View?,
#                 position: Int,
#                 id: Long
#             ) {
#                 sort = (selectedItemView as TextView).text as String
#                 linearLayout.removeAllViews()
#                 setProducts(search, sort)
#             }

#             override fun onNothingSelected(parentView: AdapterView<*>?) {

#             }
#         })

#         var order = findViewById<Button>(R.id.order)
#         order.setOnClickListener {
#             makeOrder()
#         }


#     }

#     companion object {
#         fun getCategoriesFromJsonObject(jsonObject: JSONObject): MutableList<String> {
#             val categories = mutableListOf<String>()
#             categories.add("Без фильтра")
#             val categoryArray = jsonObject.getJSONArray("categories")
#             for (i in 0 until categoryArray.length()) {
#                 val categoryObject = categoryArray.getJSONObject(i)
#                 val nameJSON = categoryObject.getString("Name")
#                 categories.add(nameJSON);
#             }
#             return categories
#         }
#         fun jsonToJsonObject(buffer: MutableList<Byte>): JSONObject {
#             val tmpMeassage =
#                 String(buffer.toByteArray(), 0, buffer.size)

#             return JSONObject(tmpMeassage);
#         }

#         fun createOrder(products: MutableList<Product>): String {
#             var id = UUID.randomUUID().toString();
#             var date = LocalDateTime.now()

#             var prods = mutableListOf<Product>()

#             for (i in Security.user?.productsId!!) {
#                 var product = products.filter { it.Id == i }[0].copy()
#                 if (prods.filter { it.Id == i }.isEmpty()) {
#                     product.Count = 1
#                     prods.add(product)
#                 } else {
#                     prods.filter { it.Id == i }[0].Count += 1
#                 }
#             }

#             var gson = Gson();
#             var json =
#                 gson.toJson(Order(id, prods, date.toString(), UserJson(Security.user!!.login)))

#             return json
#         }
#         fun getProducts(search: String,jsonObject1: JSONObject,sort: String): MutableList<Product> {
#             val productsArray1 = jsonObject1.getJSONArray("item")

#             var products = mutableListOf<Product>()

#             for (i in 0 until productsArray1.length()) {
#                 val userObject = productsArray1.getJSONObject(i)
#                 val id = userObject.getInt("Id")
#                 val url = userObject.getString("Photo")
#                 val name = userObject.getString("Name")
#                 val price = userObject.getInt("Price")
#                 val count = userObject.getInt("Count")
#                 val category = userObject.getJSONObject("Category");
#                 if (name.contains(search)) {
#                     products.add(
#                         Product(
#                             id,
#                             name,
#                             url,
#                             price,
#                             Category(category.getString("Name")),
#                             count
#                         )
#                     )
#                 }
#             }

#             if (sort != "Без фильтра") products = products.filter { it.Category.Name == sort }.toMutableList()

#             return products;
#         }
#     }


#     fun makeOrder() {
#         if (Security.user?.productsId?.size!! > 0) {
#             var json = createOrder(products)

#             Thread() {
#                 try {
#                     var socket1 = Socket()
#                     socket1.connect(InetSocketAddress("10.0.2.2", 12345), 500)
#                     var outputStream = socket1.getOutputStream()
#                     outputStream.write(json.toByteArray(Charset.defaultCharset()))
#                     runOnUiThread {
#                         views.forEach {
#                             (it[0] as LinearLayout).removeAllViews();
#                             (it[0] as LinearLayout).addView(it[1])
#                         }
#                         Security.user!!.productsId = mutableListOf()
#                     }
#                     socket1.close()
#                     outputStream.close()
#                 } catch (e: Exception) {
#                     e.printStackTrace()
#                     runOnUiThread {
#                         Toast.makeText(baseContext, e.message, Toast.LENGTH_SHORT).show()
#                     }
#                 } catch (e: SocketTimeoutException) {
#                     runOnUiThread {
#                         Toast.makeText(baseContext, e.message, Toast.LENGTH_SHORT).show()
#                     }
#                 }
#             }.start()
#         }
#     }

#     fun setProducts(search: String, sort: String) {
#         val linearLayout = findViewById<LinearLayout>(R.id.list)

#         linearLayout.removeAllViews()

#         val file1 = File(filesDir, "products.json")

#         val jsonString1 = if (file1.exists()) {
#             file1.bufferedReader().use {
#                 it.readText()
#             }
#         } else {
#             "{\"products\":[]}"
#         }

#         val jsonObject1 = JSONObject(jsonString1)
#         if (jsonObject1.length() > 0) {
#             products = getProducts(search,jsonObject1,sort)

#             for (item in products) {
#                 val linearLayout1 = LinearLayout(this)
#                 linearLayout1.layoutParams = LinearLayout.LayoutParams(
#                     LinearLayout.LayoutParams.MATCH_PARENT,
#                     220
#                 )
#                 linearLayout1.gravity = Gravity.CENTER or Gravity.LEFT
#                 linearLayout1.orientation = LinearLayout.HORIZONTAL

#                 val linearLayout2 = LinearLayout(this)
#                 linearLayout2.layoutParams = LinearLayout.LayoutParams(
#                     LinearLayout.LayoutParams.WRAP_CONTENT,
#                     LinearLayout.LayoutParams.MATCH_PARENT
#                 )
#                 linearLayout2.gravity = Gravity.CENTER or Gravity.LEFT
#                 linearLayout1.addView(linearLayout2)
#                 val textView = TextView(this)
#                 textView.layoutParams = LinearLayout.LayoutParams(
#                     LinearLayout.LayoutParams.WRAP_CONTENT,
#                     LinearLayout.LayoutParams.WRAP_CONTENT
#                 )
#                 textView.setPadding(20, 0, 0, 0)
#                 textView.text = item.Name
#                 textView.setTextColor(Color.BLACK)
#                 textView.textSize = 20f
#                 linearLayout2.addView(textView)

#                 val linearLayout6 = LinearLayout(this)
#                 linearLayout6.layoutParams = LinearLayout.LayoutParams(
#                     LinearLayout.LayoutParams.WRAP_CONTENT,
#                     LinearLayout.LayoutParams.MATCH_PARENT
#                 )
#                 linearLayout6.gravity = Gravity.CENTER or Gravity.LEFT
#                 linearLayout1.addView(linearLayout6)
#                 val productsPrice = TextView(this)
#                 productsPrice.layoutParams = LinearLayout.LayoutParams(
#                     LinearLayout.LayoutParams.WRAP_CONTENT,
#                     LinearLayout.LayoutParams.WRAP_CONTENT
#                 )
#                 productsPrice.setPadding(20, 0, 0, 0)
#                 productsPrice.text = item.Price.toString()
#                 productsPrice.setTextColor(Color.BLACK)
#                 productsPrice.textSize = 16f
#                 linearLayout6.addView(productsPrice)

#                 val linearLayout7 = LinearLayout(this)
#                 linearLayout7.layoutParams = LinearLayout.LayoutParams(
#                     LinearLayout.LayoutParams.WRAP_CONTENT,
#                     LinearLayout.LayoutParams.MATCH_PARENT
#                 )
#                 linearLayout7.gravity = Gravity.CENTER or Gravity.LEFT
#                 linearLayout1.addView(linearLayout7)
#                 val productsCount = TextView(this)
#                 productsCount.layoutParams = LinearLayout.LayoutParams(
#                     LinearLayout.LayoutParams.WRAP_CONTENT,
#                     LinearLayout.LayoutParams.WRAP_CONTENT
#                 )
#                 productsCount.setPadding(20, 0, 0, 0)
#                 productsCount.text = item.Count.toString()
#                 productsCount.setTextColor(Color.BLACK)
#                 productsCount.textSize = 16f
#                 linearLayout7.addView(productsCount)


#                 val linearLayout3 = LinearLayout(this)
#                 linearLayout3.layoutParams = LinearLayout.LayoutParams(
#                     LinearLayout.LayoutParams.MATCH_PARENT,
#                     LinearLayout.LayoutParams.MATCH_PARENT
#                 )
#                 linearLayout3.gravity = Gravity.CENTER or Gravity.RIGHT
#                 linearLayout1.addView(linearLayout3)
#                 val productsUserCount = TextView(this)
#                 productsUserCount.layoutParams = LinearLayout.LayoutParams(
#                     LinearLayout.LayoutParams.WRAP_CONTENT,
#                     LinearLayout.LayoutParams.WRAP_CONTENT
#                 )
#                 productsUserCount.setPadding(20, 0, 0, 0)
#                 productsUserCount.text =
#                     Security.user?.productsId?.count { it == item.Id }.toString()
#                 productsUserCount.setTextColor(Color.BLACK)
#                 productsUserCount.textSize = 16f
#                 val minus = Button(this)
#                 minus.text = "-"
#                 minus.layoutParams = LinearLayout.LayoutParams(
#                     LinearLayout.LayoutParams.WRAP_CONTENT,
#                     LinearLayout.LayoutParams.WRAP_CONTENT
#                 )

#                 val plus = Button(this)
#                 plus.text = "+"
#                 plus.layoutParams = LinearLayout.LayoutParams(
#                     LinearLayout.LayoutParams.WRAP_CONTENT,
#                     LinearLayout.LayoutParams.WRAP_CONTENT
#                 )
#                 plus.setOnClickListener {
#                     if (item.Count >= 1) {
#                         item.Count = (item.Count - 1)
#                         productsCount.text = item.Count.toString()
#                         Security.user?.productsId?.add(item.Id);
#                         productsUserCount.text =
#                             Security.user?.productsId?.count { it == item.Id }.toString()

#                     }
#                 }
#                 val buy = Button(this)
#                 buy.text = "купить"
#                 buy.layoutParams = LinearLayout.LayoutParams(
#                     LinearLayout.LayoutParams.WRAP_CONTENT,
#                     LinearLayout.LayoutParams.WRAP_CONTENT
#                 )
#                 buy.setOnClickListener {
#                     if (item.Count >= 1) {
#                         item.Count = (item.Count - 1)
#                         productsCount.text = item.Count.toString()
#                         Security.user?.productsId?.add(item.Id);
#                         productsUserCount.text =
#                             Security.user?.productsId?.count { it == item.Id }.toString()
#                         linearLayout3.removeAllViews()
#                         linearLayout3.addView(minus)
#                         linearLayout3.addView(productsUserCount)
#                         linearLayout3.addView(plus)
#                     }
#                 }
#                 if (item.Count > 0) linearLayout3.addView(buy)

#                 views.add(mutableListOf(linearLayout3, buy))

#                 minus.setOnClickListener {
#                     if (Security.user?.productsId?.contains(item.Id) == true) {
#                         item.Count = (item.Count + 1)
#                         productsCount.text = item.Count.toString()
#                         Security.user?.productsId?.remove(item.Id);
#                         productsUserCount.text =
#                             Security.user?.productsId?.count { it == item.Id }.toString()

#                         if (Security.user?.productsId?.count { it == item.Id } == 0) {
#                             linearLayout3.removeAllViews()
#                             linearLayout3.addView(buy)
#                         }
#                     }
#                 }

#                 linearLayout.addView(linearLayout1)
#             }
#         }
#     }

# }

# private fun <SocketException> SocketException.printStackTrace() {
#     TODO("Not yet implemented")
# }

# data class Category(var Name: String)
# data class UserJson(var Name: String)
# data class Order(
#     var id: String,
#     var products: MutableList<Product>,
#     val date: String,
#     val user: UserJson
# )

# data class Product(
#     var Id: Int,
#     var Name: String,
#     var Url: String,
#     var Price: Int,
#     var Category: Category,
#     var Count: Int
# )


