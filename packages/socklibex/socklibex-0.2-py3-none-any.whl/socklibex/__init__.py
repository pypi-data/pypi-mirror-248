#C# 
# namespace Exam_test_try
# {
#     public class JsonDB
#     {
#         public const string filename1 = "Database.json";        
        
#         private static List<Item> items;
        

#         public static List<Item> GetAllItems()
#         {
#             if (items == null)
#             {
#                 if (new FileInfo(filename1).Exists)
#                 {
#                     using (FileStream fs = new FileStream(filename1, FileMode.Open))
#                     {
#                         items = JsonSerializer.Deserialize<List<Item>>(fs);
#                     }
#                 }
#                 else
#                 {
#                     items = new List<Item>();
#                 }
#             }
#             return items;
#         }

#         public static Item AddItem(Item item)
#         {
#             var items = GetAllItems();
#             items.RemoveAll(v => v.Id == item.Id);
#             items.Add(item);
#             SaveToFile(filename1, items);
#             return item;
#         }

#         public static Item EditItem(Item item)
#         {
#             var items = GetAllItems();
#             var dbItem = items.FirstOrDefault(u => u.Id == item.Id);
#             if (dbItem != null)
#             {
#                 dbItem.Id = item.Id;
#                 dbItem.Name = item.Name;
#                 dbItem.Description = item.Description;                
#                 SaveToFile(filename1, items);
#             }
#             return dbItem;
#         }

#         public static void DeleteItem(int Id)
#         {
#             var items = GetAllItems();
#             items.RemoveAll(u => u.Id == Id);
#             SaveToFile(filename1, items);
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


# namespace Exam_test_try
# {
#     public class Server
#     {
#         public static List<Socket> clients = new List<Socket>();
#         public static async void starts_server()
#         {
#             IPEndPoint ipPoint = new IPEndPoint(IPAddress.Any, 8080);
#             Socket socket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
#             socket.Bind(ipPoint);
#             while (true)
#             {
#                 socket.Listen(100);

#                 Socket client = await socket.AcceptAsync();
#                 ItemInfo info = new ItemInfo(JsonDB.GetAllItems());

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
#                 ItemInfo info = new ItemInfo(JsonDB.GetAllItems());
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

#         public ItemInfo(List<Item> item)
#         {
#             this.item = item;            
#         }
#     }

# }



# namespace Exam_test_try
# {
#     /// <summary>
#     /// Логика взаимодействия для MainWindow.xaml
#     /// </summary>
#     public partial class MainWindow : Window
#     {
#         User user = new User();
#         public MainWindow()
#         {
#             InitializeComponent();
#             MainFrame.Navigate(new Auth(MainFrame));
#         }

#         private void Click_back(object sender, RoutedEventArgs e)
#         {
#             if (MainFrame.CanGoBack)
#                 MainFrame.GoBack();
#         }

#         private void MainFrame_CR(object sender, EventArgs e)
#         {
#             if (MainFrame.CanGoBack)
#             {
#                 back.Visibility = Visibility.Visible;
#             }
#             else
#             {
#                 back.Visibility = Visibility.Hidden;
#             }            
#         }


#     }
# }

# <Grid>
#         <Grid.RowDefinitions>
#             <RowDefinition Height="50"></RowDefinition>
#             <RowDefinition Height="*"></RowDefinition>
#         </Grid.RowDefinitions>
#         <Grid Grid.Row="0">
#             <Grid.RowDefinitions>
#                 <RowDefinition Height="Auto"></RowDefinition>
#             </Grid.RowDefinitions>
#             <Button x:Name="back" Grid.Row="0" Content="Назад" VerticalAlignment="Center" HorizontalAlignment="Left" Width="80" Height="30"  />
#         </Grid>
#         <Frame NavigationUIVisibility="Hidden" Grid.Row="1" Name="MainFrame" ContentRendered="MainFrame_CR"/>

#     </Grid>


# <Grid Background="White">
#         <Grid.ColumnDefinitions>
#             <ColumnDefinition></ColumnDefinition>
#             <ColumnDefinition></ColumnDefinition>
#         </Grid.ColumnDefinitions>
#         <Grid.RowDefinitions>
#             <RowDefinition Height ="Auto" ></RowDefinition>
#             <RowDefinition Height="*"/>
#         </Grid.RowDefinitions>
#         <StackPanel Grid.Row="1" HorizontalAlignment="Center" VerticalAlignment="Center">
#             <Button Content="Добавить товар" HorizontalAlignment="Left" VerticalAlignment="Center" Click="Add_item"></Button>
#             <Button Content="Изменить товар" VerticalAlignment="Center" HorizontalAlignment="Center" Click="Change_item"/>
#             <Button Content="Удалить товар" HorizontalAlignment="Right" VerticalAlignment="Center" Click="Del_item"/>
#         </StackPanel>
        
#         <StackPanel Grid.Row="1" Grid.Column="1">
#             <StackPanel HorizontalAlignment="Right" Orientation="Horizontal" Margin="0,10,0,0">
#                 <TextBlock VerticalAlignment="Center"  Text="Поиск: " HorizontalAlignment="Left"/>
#                 <TextBox x:Name="search" Width="200" Height="25" TextChanged="TextBox_TextChanged"></TextBox>
#             </StackPanel>
#         </StackPanel>
#         <StackPanel Grid.Row="1" Grid.Column="1" VerticalAlignment="Top" Margin="10,134,-10,0">
#             <StackPanel>
#                 <ListView Grid.Row="1" HorizontalAlignment="Center" x:Name="ListViewItems" ScrollViewer.HorizontalScrollBarVisibility="Disabled" ItemsSource="{Binding Items}" Width="338">
#                     <ListView.View>
#                         <GridView>
#                             <GridViewColumn Header="ID" DisplayMemberBinding="{Binding Id}" />
#                             <GridViewColumn Header="Name" DisplayMemberBinding="{Binding Name}" />
#                             <GridViewColumn Header="Description" DisplayMemberBinding="{Binding Description}" />
#                         </GridView>
#                     </ListView.View>
#                 </ListView>
#             </StackPanel>
#         </StackPanel>
# </Grid>


# namespace Exam_test_try
# {
#     /// <summary>
#     /// Логика взаимодействия для Admin.xaml
#     /// </summary>
#     public partial class Admin : Page
#     {
#         private Frame frame = null;
#         public ObservableCollection<Item> Items { get; set; }

#         // Исходный список всех элементов для фильтрации
#         private List<Item> originalItemsList;

#         public Admin(Frame frame)
#         {
#             InitializeComponent();
#             this.frame = frame;
#             LoadItems();
#             this.DataContext = this;
#         }

#         private void LoadItems()
#         {            
#             originalItemsList = JsonDB.GetAllItems() ?? new List<Item>();
#             Items = new ObservableCollection<Item>(originalItemsList);
#         }

#         private void TextBox_TextChanged(object sender, TextChangedEventArgs e)
#         {
#             loadItem();
#         }

#         private void loadItem()
#         {
#             if (!string.IsNullOrEmpty(search.Text))
#             {
#                 string searchQuery = search.Text.Trim().ToLower();
#                 var filteredItems = originalItemsList.Where(v => v.Name.ToLower().Contains(searchQuery)).ToList();

#                 // Обновление Items для отображения в ListView
#                 Items.Clear();
#                 foreach (var item in filteredItems)
#                 {
#                     Items.Add(item);
#                 }
#             }
#             else
#             {
#                 // Возвращаем все элементы, если строка поиска пуста
#                 Items.Clear();
#                 foreach (var item in originalItemsList)
#                 {
#                     Items.Add(item);
#                 }
#             }
#         }

#         private void Del_item(object sender, RoutedEventArgs e)
#         {
#             frame.Navigate(new Del_item(frame));
#         }

#         private void Add_item(object sender, RoutedEventArgs e)
#         {
#             frame.Navigate(new add_item(frame));
#         }

#         private void Change_item(object sender, RoutedEventArgs e)
#         {
#             frame.Navigate(new Change_item(frame));
#         }
#     }
# }


# namespace Exam_test_try
# {
#     /// <summary>
#     /// Логика взаимодействия для add_item.xaml
#     /// </summary>
#     public partial class add_item : Page
#     {
#         public Frame frame;
#         private Item item = new Item();
#         public add_item(Frame frame)
#         {
#             InitializeComponent();
#             this.frame = frame;
#         }
#         private void add_item_to_json(object sender, RoutedEventArgs e)
#         {            
#             var allItems = JsonDB.GetAllItems();

#             if (allItems != null && allItems.Any(i => i.Id == int.Parse(id.Text)))
#             {
#                 MessageBox.Show("Данный id уже используется");
#                 return;
#             }
#             item.Id = int.Parse(id.Text);
#             item.Name = name.Text;            
#             item.Description = description.Text;            

#             if (JsonDB.GetAllItems() != null && item == null)
#             {
#                 MessageBox.Show("Данный id уже используется");
#                 return;
#             }

#             else
#             {
#                 JsonDB.AddItem(item);
#                 Server.SendData();
#             }

#             frame.Navigate(new Admin(frame));

#         }
#     }
# }


# namespace Exam_test_try
# {
#     /// <summary>
#     /// Логика взаимодействия для Change_item.xaml
#     /// </summary>
#     public partial class Change_item : Page
#     {
#         public Frame frame;

#         private Item item = new Item();
#         public Change_item(Frame frame)
#         {
#             InitializeComponent();
#             this.frame = frame;
#         }

#         private void add_item_to_json(object sender, RoutedEventArgs e)
#         {            
#             item.Id = int.Parse(id.Text);
#             item.Name = name.Text;            
#             item.Description = description.Text;            
            
#             var existingItem = JsonDB.GetAllItems()?.FirstOrDefault(i => i.Id == item.Id);

#             if (existingItem != null)
#             {
#                 JsonDB.EditItem(item);
#             }
#             else
#             {
#                 JsonDB.AddItem(item);
#                 Server.SendData();
#             }

#             frame.Navigate(new Admin(frame));
#         }
#     }
# }
