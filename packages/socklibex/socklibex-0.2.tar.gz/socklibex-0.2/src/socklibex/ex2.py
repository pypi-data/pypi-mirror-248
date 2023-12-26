def show_new_info():
    return "Информация о написании кода на разных языках..."


#kotlin
#add_product
# package com.example.lab_work_first

# import android.content.Context
# import android.content.Intent
# import android.net.Uri
# import android.os.Bundle
# import android.provider.MediaStore
# import android.widget.Button
# import android.widget.EditText
# import android.widget.TextView
# import android.widget.Toast
# import androidx.appcompat.app.AppCompatActivity
# import org.json.JSONObject
# import java.io.File
# import java.util.*

# class Add_product: AppCompatActivity() {
#     override fun onCreate(savedInstanceState: Bundle?) {
#         super.onCreate(savedInstanceState)
#         setContentView(R.layout.add_product)


#         var nameField = findViewById<EditText>(R.id.name)
#         var idField = findViewById<EditText>(R.id.id)
#         var discriptionfield = findViewById<EditText>(R.id.discription)

#         val file = File(filesDir, "products.json")

#         val jsonString = if (file.exists()) {
#             file.bufferedReader().use {
#                 it.readText()
#             }
#         } else {
#             "{\"products\":[]}"
#         }

#         val jsonObject = JSONObject(jsonString)
#         val productArray = jsonObject.getJSONArray("products")

#         val productt = mutableSetOf<String>()
#         for (i in 0 until productArray.length()){
#             val contactObject = productArray.getJSONObject(i)
#             productt.add(contactObject.getString("name"))
#         }

#         var save = findViewById<Button>(R.id.button2)
#         save.setOnClickListener {

#             if(nameField.text==null || nameField.text==null || discriptionfield.text==null) {
#                 Toast.makeText(baseContext,"заполни все поля",Toast.LENGTH_SHORT).show()
#             } else if (productt.contains(nameField.text.toString())) {
#                 Toast.makeText(baseContext,"товар с таким названием уже существует",Toast.LENGTH_SHORT).show()
#             } else {
#                 val newUser = JSONObject().apply {
#                     put("id", idField.text)
#                     put("name", nameField.text)
#                     put("description",discriptionfield.text)
#                 }
#                 productArray.put(newUser)
#                 jsonObject.put("products", productArray)

#                 try {
#                     val fileOutputStream = openFileOutput("products.json", Context.MODE_PRIVATE)
#                     fileOutputStream.write(jsonObject.toString().toByteArray())
#                     fileOutputStream.close()
#                     val intent = Intent(this@Add_product, Items::class.java)
#                     startActivity(intent);
#                     finish();
#                     Toast.makeText(this, "товар зареган", Toast.LENGTH_SHORT).show()
#                 } catch (e: java.lang.Exception) {
#                     e.printStackTrace()
#                     Toast.makeText(this, "ошибка регистрации", Toast.LENGTH_SHORT).show()
#                 }
#             }
#         }
#     }

# }

#add_user
# package com.example.lab_work_first

# import android.content.Context
# import android.content.Intent
# import androidx.appcompat.app.AppCompatActivity
# import android.os.Bundle
# import android.view.animation.AnimationUtils
# import android.widget.Button
# import android.widget.EditText
# import android.util.Log
# import android.widget.TextView
# import android.widget.Toast
# import org.json.JSONObject
# import java.io.BufferedWriter
# import java.io.File
# import java.io.FileWriter
# import java.io.Writer


# class create_account : AppCompatActivity() {

#     override fun onCreate(savedInstanceState: Bundle?) {
#         super.onCreate(savedInstanceState)
#         setContentView(R.layout.create_account)

#         val buttonReg: Button = findViewById(R.id.buttonLogin)

#         loginBox = findViewById(R.id.editTextEmail)
#         passBox = findViewById(R.id.editTextPassword)

#         buttonReg.setOnClickListener {
#             register()
#         }
#     }


#     private var loginBox: EditText? = null
#     private var passBox: EditText? = null

#     fun register() {
#         val login = loginBox?.text.toString()
#         val pass = passBox?.text.toString()


#         val file = File(filesDir, "users.json")
#         val jsonString = if (file.exists()) {
#             file.bufferedReader().use {
#                 it.readText()
#             }
#         } else {
#             "{\"users\":[]}"
#         }

#         val jsonObject = JSONObject(jsonString)
#         val usersArray = jsonObject.getJSONArray("users")

#         for (i in 0 until usersArray.length()) {
#             val userObject = usersArray.getJSONObject(i)
#             val existingLogin = userObject.getString("login")
#             if (existingLogin == login) {
#                 Toast.makeText(this, "Пользователь уже существует", Toast.LENGTH_SHORT).show()
#                 return
#             }
#         }

#         val newUser = JSONObject().apply {
#             put("login", login)
#             put("password", pass)
#         }

#         usersArray.put(newUser)
#         jsonObject.put("users", usersArray)

#         try {
#             val fileOutputStream = openFileOutput("users.json", Context.MODE_PRIVATE)
#             fileOutputStream.write(jsonObject.toString().toByteArray())
#             fileOutputStream.close()
#             Toast.makeText(this, "Пользователь зарегистрирован", Toast.LENGTH_SHORT).show()
#             val newPage = Intent(this, Items::class.java)
#             startActivity(newPage)
#         } catch (e: java.lang.Exception) {
#             e.printStackTrace()
#             Toast.makeText(this, "Ошибка регистрации", Toast.LENGTH_SHORT).show()
#         }
#     }
# }



###class item


# package com.example.lab_work_first

# class item(
#     var id: Int,
#     var name: String,
#     var discription: String,

# )

###Items

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

#     override fun onCreate(savedInstanceState: Bundle?) {
#         super.onCreate(savedInstanceState)
#         setContentView(R.layout.items)

#         val btn_plus: Button = findViewById(R.id.add_item)
#         btn_plus.setOnClickListener {
#             val intent = Intent(this@Items, Add_product::class.java)
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

#                                             setProducts("")

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
#         editText.setOnKeyListener(object : View.OnKeyListener {
#             override fun onKey(v: View?, keyCode: Int, event: KeyEvent): Boolean {
#                 if (event.action == KeyEvent.ACTION_DOWN &&
#                     keyCode == KeyEvent.KEYCODE_ENTER
#                 ) {
#                     editText.clearFocus()
#                     editText.isCursorVisible = false

#                     search = editText.text.toString()
#                     linearLayout.removeAllViews()

#                     setProducts(search)

#                     return true
#                 }
#                 return false
#             }
#         })


#         var order = findViewById<Button>(R.id.order)
#         order.setOnClickListener {
#             makeOrder()
#         }


#     }

#     companion object {
#         fun jsonToJsonObject(buffer: MutableList<Byte>): JSONObject {
#             val tmpMeassage =
#                 String(buffer.toByteArray(), 0, buffer.size)

#             return JSONObject(tmpMeassage);
#         }

#         fun getProducts(search: String,jsonObject1: JSONObject): MutableList<Product> {
#             val productsArray1 = jsonObject1.getJSONArray("item")

#             var products = mutableListOf<Product>()

#             for (i in 0 until productsArray1.length()) {
#                 val userObject = productsArray1.getJSONObject(i)
#                 val id = userObject.getInt("Id")
#                 val name = userObject.getString("Name")
#                 val discription = userObject.getString("Discription")
#                 if (name.contains(search)) {
#                     products.add(
#                         Product(
#                             id,
#                             name,
#                             discription,
#                         )
#                     )
#                 }
#             }
#             return products;
#         }
#     }


#     fun makeOrder() {
#         val file = File(filesDir, "products.json")
#         if (file.exists()) {
#             val jsonString = file.bufferedReader().use { it.readText() }

#             Thread {
#                 try {
#                     val socket = Socket()
#                     socket.connect(InetSocketAddress("10.0.2.2", 12345), 500)
#                     val outputStream = socket.getOutputStream()
#                     outputStream.write(jsonString.toByteArray(Charset.defaultCharset()))
#                     socket.close()
#                 } catch (e: Exception) {
#                     e.printStackTrace()
#                     runOnUiThread {
#                         Toast.makeText(baseContext, e.message, Toast.LENGTH_SHORT).show()
#                     }
#                 }
#             }.start()
#         } else {
#             runOnUiThread {
#                 Toast.makeText(baseContext, "File not found", Toast.LENGTH_SHORT).show()
#             }
#         }
#     }


#     fun setProducts(search: String) {
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
#             products = getProducts(search,jsonObject1)

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
#                 productsPrice.text = item.Name.toString()
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
#                 productsCount.text = item.Description.toString()
#                 productsCount.setTextColor(Color.BLACK)
#                 productsCount.textSize = 16f
#                 linearLayout7.addView(productsCount)



#                 linearLayout.addView(linearLayout1)
#             }
#         }
#     }

# }

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
#     var Description: String,

# )


###вход



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



# <?xml version="1.0" encoding="utf-8"?>
# <LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
#     xmlns:app="http://schemas.android.com/apk/res-auto"
#     xmlns:tools="http://schemas.android.com/tools"
#     android:layout_width="match_parent"
#     android:layout_height="match_parent"
#     android:orientation="vertical"
#     tools:context=".Items">
#     <LinearLayout
#         android:layout_width="match_parent"
#         android:gravity="center"
#         android:orientation="horizontal"
#         android:layout_height="wrap_content">
#         <EditText
#             android:id="@+id/search"
#             android:layout_width="wrap_content"
#             android:layout_height="50dp"
#             android:inputType="text"
#             android:hint="Product name" />

#         <Button
#             android:id="@+id/order"
#             android:layout_width="wrap_content"
#             android:layout_height="wrap_content"
#             android:text="Купить"/>

#         <Button
#             android:id="@+id/add_item"
#             android:layout_width="wrap_content"
#             android:layout_height="wrap_content"
#             android:text="+"/>
#     </LinearLayout>

#     <ScrollView
#         android:layout_width="match_parent"
#         android:layout_height="0dp"
#         android:layout_weight="1">
#         <LinearLayout
#             android:id="@+id/list"
#             android:layout_width="match_parent"
#             android:gravity="center"
#             android:orientation="vertical"
#             android:layout_height="wrap_content">

#         </LinearLayout>
#     </ScrollView>



# </LinearLayout>


# <LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
# android:layout_width="match_parent"
# android:layout_height="match_parent"
# android:orientation="vertical"
# android:gravity="center_horizontal"
# android:padding="16dp">


# <EditText
#     android:id="@+id/editTextEmail"
#     android:layout_width="371dp"
#     android:layout_height="46dp"
#     android:layout_marginTop="50dp"
#     android:hint="@string/email"
#     android:inputType="textEmailAddress" />

# <EditText
#     android:id="@+id/editTextPassword"
#     android:layout_width="371dp"
#     android:layout_height="46dp"
#     android:layout_marginTop="20dp"
#     android:hint="@string/password"
#     android:inputType="textPassword" />


# <androidx.appcompat.widget.AppCompatButton
#     android:id="@+id/buttonLogin"
#     android:layout_width="370dp"
#     android:layout_height="wrap_content"
#     android:layout_marginTop="30dp"

#     android:text="@string/login" />

# </LinearLayout>


# <LinearLayout
#     xmlns:android="http://schemas.android.com/apk/res/android"
#     android:layout_width="match_parent"
#     android:layout_height="match_parent"
#     android:orientation="vertical"
#     android:padding="16dp">

#     <!-- EditText для ввода названия продукта -->
#     <EditText
#         android:id="@+id/name"
#         android:layout_width="match_parent"
#         android:layout_height="wrap_content"
#         android:hint="Название продукта"/>

#     <!-- EditText для ввода количества продукта -->
#     <EditText
#         android:id="@+id/id"
#         android:layout_width="match_parent"
#         android:layout_height="wrap_content"
#         android:hint="id"
#         android:inputType="number"/>

#     <!-- EditText для ввода цены продукта -->
#     <EditText
#         android:id="@+id/discription"
#         android:layout_width="match_parent"
#         android:layout_height="wrap_content"
#         android:hint="Описание"/>


#     <Button
#         android:id="@+id/button2"
#         android:layout_width="match_parent"
#         android:layout_height="wrap_content"
#         android:text="Сохранить"/>

# </LinearLayout>


# <LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
#     android:layout_width="match_parent"
#     android:layout_height="match_parent"
#     android:orientation="vertical"
#     android:gravity="center_horizontal"
#     android:padding="16dp">

#     <EditText
#         android:id="@+id/editTextEmail"
#         android:layout_width="371dp"
#         android:layout_height="46dp"
#         android:layout_marginTop="50dp"
#         android:hint="@string/email"
#         android:inputType="textEmailAddress" />

#     <EditText
#         android:id="@+id/editTextPassword"
#         android:layout_width="371dp"
#         android:layout_height="46dp"
#         android:layout_marginTop="20dp"
#         android:hint="@string/password"
#         android:inputType="textPassword" />

#     <androidx.appcompat.widget.AppCompatButton
#         android:id="@+id/buttonLogin"
#         android:layout_width="370dp"
#         android:layout_height="wrap_content"
#         android:layout_marginTop="30dp"
#         android:text="@string/signin" />

#     <LinearLayout
#         android:layout_width="wrap_content"
#         android:layout_height="wrap_content"
#         android:orientation="horizontal"
#         android:layout_gravity="center_horizontal"
#         android:layout_marginTop="16dp">

#         <Button
#             android:id="@+id/buttonCreateAccount"
#             android:layout_width="wrap_content"
#             android:layout_height="wrap_content"
#             android:layout_marginStart="10dp"
#             android:background="@android:color/transparent"
#             android:text="@string/create_account"
#             android:textColor="@color/black" />
#     </LinearLayout>

# </LinearLayout>
