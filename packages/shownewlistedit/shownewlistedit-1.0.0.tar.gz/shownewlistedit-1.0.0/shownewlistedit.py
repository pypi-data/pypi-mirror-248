def show_info():
    return "Информация о написании кода на разных языках..."


##############WPF_C####################




###CatalogProducts.xaml###

# <Page x:Class="PrizivaNet.CatalogProducts"
#       xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
#       xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
#       xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
#       xmlns:d="http://schemas.microsoft.com/expression/blend/2008"
#       xmlns:local="clr-namespace:PrizivaNet"
#       mc:Ignorable="d"
#       d:DesignHeight="550" d:DesignWidth="800"
#       Title="CatalogProducts" Loaded="Page_Loaded">
#
#     <Grid Background="White">
#         <Grid.RowDefinitions>
#             <RowDefinition Height="Auto"></RowDefinition>
#             <RowDefinition Height="Auto"></RowDefinition>
#         </Grid.RowDefinitions>
#         <StackPanel Grid.Row="0" HorizontalAlignment="Center" Height="60" Orientation="Horizontal">
#             <TextBox x:Name="search" Height="30" Width="200" TextChanged="search_TextChanged"/>
#             <ComboBox x:Name="sort" Height="30" Width="200" Margin="10,0,10,0" SelectedIndex="0" SelectionChanged="sort_SelectionChanged">
#                 <TextBlock>Без сортировки</TextBlock>
#                 <TextBlock>Цена (по убыванию)</TextBlock>
#                 <TextBlock>Цена (по возрастанию)</TextBlock>
#             </ComboBox>
#             <ComboBox x:Name="filter" SelectedIndex="0" Height="30" Width="200" Margin="10,0,10,0" SelectionChanged="filter_SelectionChanged">
#                 <TextBlock>Все категории</TextBlock>
#             </ComboBox>
#             <Button Height="30" Width="30" Click="Button_Click">
#                 <Button.Background>
#                     <ImageBrush ImageSource="C:\Users\1\source\repos\PrizivaNet\PrizivaNet\9054404_bx_basket_icon.png"/>
#                 </Button.Background>
#             </Button>
#         </StackPanel>
#         <ListView Grid.Row="1" HorizontalAlignment="Center" x:Name="ListRunners" ScrollViewer.HorizontalScrollBarVisibility="Disabled" MaxHeight="600" SelectionChanged="ListRunners_SelectionChanged" MouseDoubleClick="ListRunners_MouseDoubleClick">
#             <ListView.ItemsPanel>
#                 <ItemsPanelTemplate>
#                     <StackPanel Orientation="Vertical"></StackPanel>
#                 </ItemsPanelTemplate>
#             </ListView.ItemsPanel>
#             <ListView.ItemTemplate>
#                 <DataTemplate>
#                     <Border BorderThickness="1" BorderBrush="Black">
#                         <Grid Width="800" Height="100" Background="White">
#                             <Grid.ColumnDefinitions>
#                                 <ColumnDefinition Width="*"></ColumnDefinition>
#                                 <ColumnDefinition Width="4*"></ColumnDefinition>
#                                 <ColumnDefinition Width="*"></ColumnDefinition>
#                             </Grid.ColumnDefinitions>
#                             <Image x:Name="ImgRunner" HorizontalAlignment="Center" Source="{Binding Image}" VerticalAlignment="Center"/>
#                             <Grid Margin="10,0,0,0" Grid.Column="1" VerticalAlignment="Center">
#                                 <Grid.RowDefinitions>
#                                     <RowDefinition Height="*"></RowDefinition>
#                                     <RowDefinition Height="*"></RowDefinition>
#                                     <RowDefinition Height="2*"></RowDefinition>
#                                 </Grid.RowDefinitions>
#                                 <WrapPanel>
#                                     <TextBlock HorizontalAlignment="Left" x:Name="TBkRunnerFio" Text="{Binding Name}" FontWeight="Bold"></TextBlock>
#                                 </WrapPanel>
#                                 <TextBlock HorizontalAlignment="Left" Grid.Row="1" x:Name="TBkBirthDay" Text="{Binding Price}"></TextBlock>
#                                 <StackPanel Grid.Row="2">
#                                     <TextBlock HorizontalAlignment="Left" Grid.Row="2" x:Name="TBCountry" TextWrapping="Wrap" Text="{Binding Manufacturer}"></TextBlock>
#                                     <TextBlock HorizontalAlignment="Left" Grid.Row="2" x:Name="TBCount" TextWrapping="Wrap" Text="{Binding Count}"></TextBlock>
#                                 </StackPanel>
#                             </Grid>
#                             <TextBlock Grid.Column="2" HorizontalAlignment="Center" x:Name="TBkRole" Text="{Binding Category}"></TextBlock>
#                         </Grid>
#                     </Border>
#                 </DataTemplate>
#             </ListView.ItemTemplate>
#         </ListView>
#     </Grid>
# </Page>

###CatalogProducts.cs###

# using PrizivaNet.Classes;
# using System;
# using System.Collections.Generic;
# using System.IO;
# using System.Linq;
# using System.Text;
# using System.Text.Json;
# using System.Threading.Tasks;
# using System.Windows;
# using System.Windows.Controls;
# using System.Windows.Data;
# using System.Windows.Documents;
# using System.Windows.Input;
# using System.Windows.Media;
# using System.Windows.Media.Imaging;
# using System.Windows.Navigation;
# using System.Windows.Shapes;
#
# namespace PrizivaNet
# {
#     /// <summary>
#     /// Логика взаимодействия для CatalogProducts.xaml
#     /// </summary>
#     public partial class CatalogProducts : Page
#     {
#         public Frame MainFrame { get; set; }
#         public DataClass data = new DataClass();
#         public List<Product> products = new List<Product>();
#         public List<Category> categories = new List<Category>();
#         public TextBlock userFI = (TextBlock)Application.Current.MainWindow.FindName("userFIO");
#
#         public CatalogProducts(Frame mf)
#         {
#             InitializeComponent();
#             MainFrame = mf;
#         }
#
#         private void ListRunners_SelectionChanged(object sender, SelectionChangedEventArgs e)
#         {
#
#         }
#
#         private void Button_Click(object sender, RoutedEventArgs e)
#         {
#             if (userFI.Text != "Гость")
#             {
#                 MainFrame.Navigate(new Basket());
#             }
#         }
#
#         private void ListRunners_MouseDoubleClick(object sender, MouseButtonEventArgs e)
#         {
#             if (ListRunners.SelectedItem != null && userFI.Text != "Гость")
#             {
#                 Product selectedItem = (Product)ListRunners.SelectedItem;
#                 if (selectedItem.Count > 0)
#                 {
#                     selectedItem.CountBasket += 1;
#                     selectedItem.Count -= 1;
#
#                     List<Product> serealizedProducts = new List<Product>();
#                     ListRunners.Items.Refresh();
#                     foreach (Product product in ListRunners.Items)
#                     {
#                         serealizedProducts.Add(product);
#                     }
#
#                     FileStream fs2 = new FileStream("products.json", FileMode.Truncate);
#                     {
#                         JsonSerializer.Serialize(fs2, serealizedProducts);
#                         fs2.Close();
#                     }
#                 }
#                 else
#                 {
#                     MessageBox.Show("Товара нет в наличии");
#                 }
#
#             }
#         }
#
#         private void loadSort()
#         {
#             if (ListRunners != null)
#                 ListRunners.ItemsSource = SortedProduct(products, filter, sort, search);
#         }
#
#         private void search_TextChanged(object sender, TextChangedEventArgs e)
#         {
#             loadSort();
#         }
#
#         private void sort_SelectionChanged(object sender, SelectionChangedEventArgs e)
#         {
#             loadSort();
#         }
#
#         private void filter_SelectionChanged(object sender, SelectionChangedEventArgs e)
#         {
#             loadSort();
#         }
#
#         public void LoadCategoriesIntoComboBox(List<Category> categories, ComboBox filter)
#         {
#             if (System.IO.File.Exists("categories.json"))
#             {
#                 categories = data.LoadCategories(categories, "categories.json");
#                 int i = 1;
#                 foreach (Category сategory in categories)
#                 {
#                     filter.Items.Insert(i, сategory.Name);
#                     i++;
#                 }
#             }
#         }
#
#         public List<Product> SortedProduct(List<Product> products, ComboBox filter, ComboBox sort, TextBox search)
#         {
#             List<Product> sortProducts = new List<Product>();
#             sortProducts = products;
#             if (filter != null && filter.SelectedIndex != 0)
#             {
#                 sortProducts = sortProducts.Where(i => i.Category.Contains(filter.SelectedItem.ToString())).ToList();
#             }
#             if (sort != null && sort.SelectedIndex == 1)
#             {
#                 sortProducts = sortProducts.OrderByDescending(i => i.Price).ToList();
#             }
#             if (sort != null && sort.SelectedIndex == 2)
#             {
#                 sortProducts = sortProducts.OrderBy(i => i.Price).ToList();
#             }
#             if (search.Text != null && sortProducts != null)
#             {
#                 sortProducts = sortProducts.Where(i => i.Name.Contains(search.Text.ToString())).ToList();
#             }
#             return sortProducts;
#         }
#
#         private void Page_Loaded(object sender, RoutedEventArgs e)
#         {
#             products = data.LoadProducts(products, "products.json");
#             categories = data.LoadCategories(categories, "categories.json");
#             LoadCategoriesIntoComboBox(categories, filter);
#             ListRunners.ItemsSource = products;
#         }
#     }
# }

###Basket.cs###

# using PrizivaNet.Classes;
# using System;
# using System.Collections.Generic;
# using System.IO;
# using System.Linq;
# using System.Printing.IndexedProperties;
# using System.Text;
# using System.Text.Json;
# using System.Threading.Tasks;
# using System.Windows;
# using System.Windows.Controls;
# using System.Windows.Data;
# using System.Windows.Documents;
# using System.Windows.Input;
# using System.Windows.Media;
# using System.Windows.Media.Imaging;
# using System.Windows.Navigation;
# using System.Windows.Shapes;
#
# namespace PrizivaNet
# {
#     /// <summary>
#     /// Логика взаимодействия для Basket.xaml
#     /// </summary>
#     public partial class Basket : Page
#     {
#         public List<Product> MyList = new List<Product>();
#         public DataClass data = new DataClass();
#         public Basket()
#         {
#             InitializeComponent();
#             RefreshItems();
#
#         }
#
#         private void btnClear_Click(object sender, RoutedEventArgs e)
#         {
#             List<Product> products = new List<Product>();
#             products = data.LoadProducts(products, "products.json");
#
#
#             foreach(Product product1 in MyList)
#             {
#                 foreach(Product product in products)
#                 {
#                     if (product1.Name == product.Name)
#                     {
#                         product.Count += product.CountBasket;
#                         product.CountBasket = 0;
#                         break;
#                     }
#                 }
#             }
#
#             FileStream fs2 = new FileStream("products.json", FileMode.Truncate);
#             {
#                 JsonSerializer.Serialize(fs2, products);
#                 fs2.Close();
#             }
#             MyList.Clear();
#             List<Product> MyListClear = new List<Product>();
#             ListRunners.ItemsSource = MyListClear;
#             totalPrice.Text = "Корзина пуста  |";
#             totalProduct.Text = "Нет";
#             ListRunners.Visibility = Visibility.Hidden;
#         }
#
#
#
#         private void ListRunners_MouseDoubleClick(object sender, MouseButtonEventArgs e)
#         {
#             if (ListRunners.SelectedItem != null)
#             {
#                 Product selectedItem = (Product)ListRunners.SelectedItem;
#                 List<Product> products = new List<Product>();
#                 products = data.LoadProducts(products, "products.json");
#                 foreach(Product product in products)
#                 {
#                     if (selectedItem.Name == product.Name)
#                     {
#                         if (product.CountBasket > 0)
#                         {
#                             product.CountBasket -= 1;
#                             product.Count += 1;
#                             FileStream fs2 = new FileStream("products.json", FileMode.Truncate);
#                             {
#                                 JsonSerializer.Serialize(fs2, products);
#                                 fs2.Close();
#                             }
#                             RefreshItems();
#                             ListRunners.Items.Refresh();
#                             break;
#                         }
#                         else
#                         {
#                             product.CountBasket = 0;
#                             product.Count += product.CountBasket;
#                             FileStream fs2 = new FileStream("products.json", FileMode.Truncate);
#                             {
#                                 JsonSerializer.Serialize(fs2, products);
#                                 fs2.Close();
#                             }
#                             RefreshItems();
#                             ListRunners.Items.Refresh();
#                             break;
#                         }
#                     }
#                 }
#
#
#             }
#         }
#
#         public void RefreshItems()
#         {
#             MyList = new List<Product>();
#             List<Product> products = new List<Product>();
#             products = data.LoadProducts(products, "products.json");
#             foreach (Product product in products)
#             {
#                 if (product.CountBasket != 0)
#                 {
#                     MyList.Add(product);
#                 }
#             }
#
#             if (MyList.Count == 0)
#             {
#                 ListRunners.Visibility = Visibility.Hidden;
#                 totalPrice.Text = "Корзина пуста  |";
#                 totalProduct.Text = "Нет";
#             }
#             else
#             {
#                 double tot = 0;
#                 int count = 0;
#                 foreach (Product product in MyList)
#                 {
#                     tot += product.CountBasket * product.Price;
#                     count += product.CountBasket;
#                 }
#                 totalPrice.Text = $"{tot.ToString()}  |";
#                 totalProduct.Text = count.ToString();
#                 ListRunners.ItemsSource = MyList;
#             }
#         }
#     }
# }

###DataClass.cs###

# using System;
# using System.Collections.Generic;
# using System.IO;
# using System.Linq;
# using System.Text;
# using System.Text.Json;
# using System.Threading.Tasks;
# using System.Windows;
# using System.Windows.Controls;
# using System.Windows.Data;
# using System.Windows.Documents;
# using System.Windows.Input;
# using System.Windows.Media;
# using System.Windows.Media.Imaging;
# using System.Windows.Navigation;
# using System.Windows.Shapes;
# using System.Windows.Threading;
# using static System.Net.WebRequestMethods;
#
# namespace PrizivaNet.Classes
# {
#     public class DataClass
#     {
#         public DataClass()
#         {
#
#         }
#
#
#         public void AddCategory(string name, string file)
#         {
#             bool inCategory = false;
#             List<Category> categories = new List<Category>();
#             if (!System.IO.File.Exists(file))
#             {
#                 FileStream fs1 = new FileStream(file, FileMode.Create);
#                 {
#                     categories.Add(new Category(name));
#                     JsonSerializer.Serialize(fs1, categories);
#                     MessageBox.Show("Файл создан и категория добавлена!");
#                     fs1.Close();
#                 }
#             }
#             else
#             {
#                 categories = LoadCategories(categories, file);
#                 foreach (Category сategory in categories)
#                 {
#                     if (сategory.Name == name)
#                     {
#                         MessageBox.Show("Категория с таким именем уже уже существует");
#                         inCategory = true;
#                         break;
#                     }
#                 }
#                 if (!inCategory)
#                 {
#                     FileStream fs2 = new FileStream(file, FileMode.Truncate);
#                     categories.Add(new Category(name));
#                     JsonSerializer.Serialize(fs2, categories);
#                     MessageBox.Show("Категория добавлена!");
#                     fs2.Close();
#                 }
#             }
#         }
#
#         public void DeleteProduct(string name, string file)
#         {
#             bool inProduct = false;
#             List<Product> products = new List<Product>();
#             products = LoadProducts(products, file);
#             foreach (Product product in products)
#             {
#                 if (product.Name == name)
#                 {
#                     inProduct = true;
#                     products.Remove(product);
#                     break;
#                 }
#             }
#
#             if (!inProduct)
#             {
#                 MessageBox.Show("Товара с таким именем нет");
#             }
#             else
#             {
#                 MessageBox.Show("Товар удален");
#             }
#
#             FileStream fs2 = new FileStream(file, FileMode.Truncate);
#             {
#                 JsonSerializer.Serialize(fs2, products);
#                 fs2.Close();
#             }
#         }
#
#         public void DeleteCategory(string name, string file)
#         {
#             bool inCategory = false;
#             List<Category> categories = new List<Category>();
#             categories = LoadCategories(categories, file);
#             foreach (Category сategory in categories)
#             {
#                 if (сategory.Name == name)
#                 {
#                     inCategory = true;
#                     categories.Remove(сategory);
#                     break;
#                 }
#             }
#
#             if (!inCategory)
#             {
#                 MessageBox.Show("Категории с таким именем нет");
#             }
#             else
#             {
#                 MessageBox.Show("Категория удалена");
#             }
#             FileStream fs2 = new FileStream(file, FileMode.Truncate);
#             {
#                 JsonSerializer.Serialize(fs2, categories);
#                 fs2.Close();
#             }
#         }
#
#         public void ChangeProduct(string name, string category, string manufacturer, string image, double price, int count, string whatChange, string file)
#         {
#             bool inProduct = false;
#             List<Product> products = new List<Product>();
#             products = LoadProducts(products, file);
#             foreach (Product product in products)
#             {
#                 if (product.Name == whatChange)
#                 {
#                     inProduct = true;
#                     product.Name = name;
#                     product.Category = category;
#                     product.Manufacturer = manufacturer;
#                     product.Image = image;
#                     product.Price = price;
#                     product.Count = count;
#                     break;
#                 }
#             }
#
#             if (!inProduct)
#             {
#                 MessageBox.Show("Товара с таким именем нет");
#             }
#             else
#             {
#                 MessageBox.Show("Товар изменён");
#             }
#             FileStream fs2 = new FileStream(file, FileMode.Truncate);
#             {
#                 JsonSerializer.Serialize(fs2, products);
#                 fs2.Close();
#             }
#         }
#
#         public void AddProduct(string name, string category, string manufacturer, string image, double price, int count, string file)
#         {
#             bool inProducts = false;
#             List<Product> products = new List<Product>();
#             if (!System.IO.File.Exists(file))
#             {
#                 FileStream fs1 = new FileStream(file, FileMode.Create);
#                 {
#                     products.Add(new Product(name, category, manufacturer, image, price, count));
#                     JsonSerializer.Serialize(fs1, products);
#                     MessageBox.Show("Файл создан и товар добавлен!");
#                     fs1.Close();
#                 }
#             }
#             else
#             {
#                 products = LoadProducts(products, file);
#                 foreach (Product product in products)
#                 {
#                     if (product.Name == name)
#                     {
#                         MessageBox.Show("Товар с таким именем уже уже существует");
#                         inProducts = true;
#                         break;
#                     }
#                 }
#
#                 if (!inProducts)
#                 {
#                     FileStream fs2 = new FileStream(file, FileMode.Truncate);
#                     products.Add(new Product(name, category, manufacturer, image, price, count));
#                     JsonSerializer.Serialize(fs2, products);
#                     MessageBox.Show("Товар добавлен!");
#                     fs2.Close();
#                 }
#             }
#         }
#
#         public List<Product> LoadProducts(List<Product> products, string file)
#         {
#             FileStream fs1 = new FileStream(file, FileMode.Open);
#             {
#                 products = (List<Product>)JsonSerializer.Deserialize(fs1, typeof(List<Product>));
#                 fs1.Close();
#             }
#             return products;
#         }
#
#         public List<User> LoadUsers(List<User> users)
#         {
#             FileStream fs1 = new FileStream("users.json", FileMode.Open);
#             {
#                 users = (List<User>)JsonSerializer.Deserialize(fs1, typeof(List<User>));
#                 fs1.Close();
#             }
#             return users;
#         }
#
#         public List<Category> LoadCategories(List<Category> categories, string file)
#         {
#             FileStream fs1 = new FileStream(file, FileMode.Open);
#             {
#                 categories = (List<Category>)JsonSerializer.Deserialize(fs1, typeof(List<Category>));
#                 fs1.Close();
#             }
#             return categories;
#         }
#     }
# }

###Sock.send.cs###

# using System;
# using System.Collections.Generic;
# using System.Linq;
# using System.Net.Sockets;
# using System.Net;
# using System.Text;
# using System.Threading.Tasks;
# using System.Text.Json;
# using System.Windows.Controls;
# using System.Windows;
#
# namespace Rus
# {
#     public class Sock
#     {
#
#         private static List<Socket> clients = new List<Socket>();
#
#         public static async void startServer()
#         {
#             try
#             {
#                 IPEndPoint ipPoint = new IPEndPoint(IPAddress.Any, 8080);
#                 Socket socket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
#                 socket.Bind(ipPoint);
#                 while (true)
#                 {
#                     socket.Listen(10);
#                     // получаем входящее подключение
#                     Socket client = await socket.AcceptAsync();
#                     ProductsInfo info = new ProductsInfo(JsonRepository.findAllProducts(), JsonRepository.findAllCategories());
#
#                     string json = JsonSerializer.Serialize(info);
#
#                     byte[] data = Encoding.ASCII.GetBytes(json);
#
#                     byte[] data1 = new byte[1];
#                     data1[0] = 1;
#                     client.Send(data.Concat(data1).ToArray());
#
#                     clients.Add(client);
#                 }
#             } catch (SocketException ex)
#             {
#
#             }
#         }
#
#         public static void sendData()
#         {
#             try
#             {
#                 ProductsInfo info = new ProductsInfo(JsonRepository.findAllProducts(), JsonRepository.findAllCategories());
#
#                 string json = JsonSerializer.Serialize(info);
#
#                 byte[] data = Encoding.ASCII.GetBytes(json);
#
#                 byte[] data1 = new byte[1];
#                 data1[0] = 1;
#
#                 foreach (var client in clients)
#                 {
#                     client.Send(data.Concat(data1).ToArray());
#                 }
#             }
#             catch (SocketException ex)
#             {
#
#             }
#         }
#     }
# }


###UnitTestC####

# using PrizivaNet;
# using PrizivaNet.Classes;
# using System.Windows.Documents;
# using System;
# using System.Collections.Generic;
# using System.IO;
# using System.Linq;
# using System.Text;
# using System.Text.Json;
# using System.Threading.Tasks;
# using System.Windows;
# using System.Windows.Controls;
# using System.Windows.Data;
# using System.Windows.Input;
# using System.Windows.Media;
# using System.Windows.Media.Imaging;
# using System.Windows.Navigation;
# using System.Windows.Shapes;
# using System.Windows.Threading;
#
# namespace PrizivaNetTest
# {
#     [TestClass]
#     public class DataClassTest
#     {
#         [TestMethod]
#         public void LoadProducts_LoadProductsFromJSONFile_ReturnsListProducts()
#         {
#             // Arrange
#             DataClass data = new DataClass();
#             List<Product> products = new List<Product>();
#
#             // Act
#             products = data.LoadProducts(products, "products.json");
#
#             // Assert
#             Assert.AreNotEqual(0, products.Count);
#         }
#
#         [TestMethod]
#         public void LoadUsers_LoadUsersFromJSONFile_ReturnsListUsers()
#         {
#             // Arrange
#             DataClass data = new DataClass();
#             List<User> users = new List<User>();
#
#             // Act
#             users = data.LoadUsers(users);
#
#             // Assert
#             Assert.AreNotEqual(0, users.Count);
#         }
#
#         [TestMethod]
#         public void LoadCategories_LoadCategoriesFromJSONFile_ReturnsListCategories()
#         {
#             // Arrange
#             DataClass data = new DataClass();
#             string file = "categories.json";
#             List<Category> categories = new List<Category>();
#
#             // Act
#             categories = data.LoadCategories(categories, file);
#
#             // Assert
#             Assert.AreNotEqual(0, categories.Count);
#         }
#
#         [TestMethod]
#         public void AddCategory_CreateNewJSONFileAndAddCategory_CreateJSONFile()
#         {
#             // Arrange
#             DataClass data = new DataClass();
#             List<Category> categories = new List<Category>();
#             string file = "categoriesNEW.json";
#             if (System.IO.File.Exists(file))
#             {
#                 System.IO.File.Delete(file);
#             }
#
#             // Act
#             data.AddCategory("Призыв", file);
#
#             // Assert
#             Assert.IsTrue(System.IO.File.Exists(file));
#         }
#
#         [TestMethod]
#         public void AddCategory_AddCategoryIntoJSONFile_AddCategoryInFile()
#         {
#             // Arrange
#             DataClass data = new DataClass();
#             List<Category> categories = new List<Category>();
#             string file = "categoriesNEW.json";
#
#
#             // Act
#             categories = data.LoadCategories(categories, file);
#             if (categories.Count > 0)
#             {
#                 foreach (Category category in categories)
#                 {
#                     if (category.Name == "Призывок")
#                     {
#                         categories.Remove(category);
#                         break;
#                     }
#                 }
#             }
#             data.AddCategory("Призывок", file);
#             categories = data.LoadCategories(categories, file);
#
#             // Assert
#             Assert.IsTrue(System.IO.File.Exists(file));
#             Assert.AreNotEqual(0, categories.Count);
#         }
#
#         [TestMethod]
#         public void AddCategory_NameCategoryInJSONFile_DontAddCategoryInFile()
#         {
#             // Arrange
#             DataClass data = new DataClass();
#             List<Category> categories = new List<Category>();
#             string file = "categoriesNEW.json";
#
#
#             // Act
#             data.AddCategory("Призывок", file);
#             categories = data.LoadCategories(categories, file);
#
#             // Assert
#             Assert.IsTrue(System.IO.File.Exists(file));
#             Assert.AreNotEqual(0, categories.Count);
#         }
#
#         [TestMethod]
#         public void DeleteProduct_DeleteCategoryFromJSONFile_DeleteCategoryInFile()
#         {
#             // Arrange
#             DataClass data = new DataClass();
#             List<Product> products = new List<Product>();
#             bool inProducts = false;
#             string file = "productsNEW.json";
#             data.AddProduct("Последний шанс", "Призыв", "ПризываНет", "C:\\Users\\10a\\source\\repos\\PrizivaNet\\PrizivaNet\\9054404_bx_basket_icon.png", 1000, file);
#
#
#             // Act
#
#             data.DeleteProduct("Последний шанс", file);
#             products = data.LoadProducts(products, file);
#
#             // Assert
#             Assert.IsTrue(System.IO.File.Exists(file));
#             Assert.AreEqual(1, products.Count);
#         }
#
#         [TestMethod]
#         public void DeleteProduct_DeleteProductFromJSONFileWithIncorrectName_DontDeleteProductInFile()
#         {
#             // Arrange
#             DataClass data = new DataClass();
#             List<Product> products = new List<Product>();
#             string file = "productsNEW.json";
#
#
#             // Act
#
#             data.DeleteProduct("Последний шансfsdfsdfdsfdsfdsfds", file);
#             products = data.LoadProducts(products, file);
#
#             // Assert
#             Assert.IsTrue(System.IO.File.Exists(file));
#             Assert.AreEqual(1, products.Count);
#         }
#
#         [TestMethod]
#         public void DeleteCategory_DeleteCategoryFromJSONFile_DeleteCaregoryInFile()
#         {
#             // Arrange
#             DataClass data = new DataClass();
#             List<Category> categories = new List<Category>();
#             string file = "categoriesNEW.json";
#             data.AddCategory("Последний шанс", file);
#
#             // Act
#
#             data.DeleteCategory("Последний шанс", file);
#             categories = data.LoadCategories(categories, file);
#
#             // Assert
#             Assert.IsTrue(System.IO.File.Exists(file));
#             Assert.AreEqual(2, categories.Count);
#         }
#
#         [TestMethod]
#         public void DeleteCategory_DeleteCategoryFromJSONFileWithIncorrectName_DontDeleteCategoryInFile()
#         {
#             // Arrange
#             DataClass data = new DataClass();
#             List<Category> categories = new List<Category>();
#             string file = "categoriesNEW.json";
#
#
#             // Act
#
#             data.DeleteCategory("Последний ш423423432432432анс", file);
#             categories = data.LoadCategories(categories, file);
#
#
#             // Assert
#             Assert.IsTrue(System.IO.File.Exists(file));
#             Assert.AreEqual(2, categories.Count);
#         }
#
#         [TestMethod]
#         public void ChangeProduct_ChangeProductInJSONFile_ChangeProductInFile()
#         {
#             // Arrange
#             DataClass data = new DataClass();
#             List<Product> products = new List<Product>();
#             string file = "productsNEWNEW.json";
#
#
#             // Act
#
#             data.ChangeProduct("TANK","Мобилизация","ПризываНет", "C:\\Users\\10a\\source\\repos\\PrizivaNet\\PrizivaNet\\9054404_bx_basket_icon.png",5000,"TANK", file);
#             data.ChangeProduct("TANK", "Мобилизация", "ПризываНет", "C:\\Users\\10a\\source\\repos\\PrizivaNet\\PrizivaNet\\9054404_bx_basket_icon.png", 5000, "TANK441421", file);
#             products = data.LoadProducts(products, file);
#
#
#             // Assert
#             Assert.IsTrue(System.IO.File.Exists(file));
#             Assert.AreEqual(1, products.Count);
#         }
#
#         [TestMethod]
#         public void AddProduct_CreateNewJSONFileAndAddProducts_CreateJSONFile()
#         {
#             // Arrange
#             DataClass data = new DataClass();
#             List<Product> products = new List<Product>();
#             string file = "productsNEWNEWNEW.json";
#             if (System.IO.File.Exists(file))
#             {
#                 System.IO.File.Delete(file);
#             }
#
#             // Act
#             data.AddProduct("TANK", "Мобилизация", "ПризываНет", "C:\\Users\\10a\\source\\repos\\PrizivaNet\\PrizivaNet\\9054404_bx_basket_icon.png", 5000, file);
#             data.AddProduct("TANK", "Мобилизация", "ПризываНет", "C:\\Users\\10a\\source\\repos\\PrizivaNet\\PrizivaNet\\9054404_bx_basket_icon.png", 5000, file);
#             products = data.LoadProducts(products, file);
#
#             // Assert
#             Assert.IsTrue(System.IO.File.Exists(file));
#             Assert.AreEqual(1, products.Count);
#         }
#     }
# }

#################Kotlin_Android#######################

###Security###

# package com.example.crud3
#
# class Security {
#
#     companion object {
#         var user: User? = null
#     }
#
# }
#
# data class User(val login: String, var productsId: MutableList<Int>)

###Login###

# package com.example.crud3
#
# import android.content.Intent
# import androidx.appcompat.app.AppCompatActivity
# import android.os.Bundle
# import android.widget.Button
# import android.widget.EditText
# import android.widget.Toast
# import org.json.JSONObject
# import java.io.File
#
# class Login : AppCompatActivity() {
#     override fun onCreate(savedInstanceState: Bundle?) {
#         super.onCreate(savedInstanceState)
#         setContentView(R.layout.activity_main)
#
#         var registration = findViewById<Button>(R.id.reg);
#         registration.setOnClickListener {
#             val intent = Intent(this, Registration::class.java)
#             startActivity(intent)
#             finish()
#         }
#
#         val userLogin: EditText = findViewById(R.id.loginField)
#         val userPass: EditText = findViewById(R.id.passwordField)
#         val authButton: Button = findViewById(R.id.login)
#
#         authButton.setOnClickListener {
#             val login = userLogin.text.toString()
#             val pass = userPass.text.toString()
#
#             if (login.isEmpty() || pass.isEmpty()) {
#                 Toast.makeText(this, "поля пустые", Toast.LENGTH_SHORT).show()
#                 return@setOnClickListener
#             }
#
#             val jsonString = File(applicationContext.filesDir, "users.json").bufferedReader().use { it.readText() }
#             val jsonObject = JSONObject(jsonString)
#             val usersArray = jsonObject.getJSONArray("users")
#
#             var isAuth = false
#             for (i in 0 until usersArray.length()) {
#                 val userObject = usersArray.getJSONObject(i)
#                 val userJSON = userObject.getString("login")
#                 val passJSON = userObject.getString("password")
#
#                 if (userJSON == login && passJSON == pass) {
#                     Toast.makeText(this, "$login вошел успешно", Toast.LENGTH_SHORT).show()
#                     isAuth = true
#                     val intent = Intent(this, Products::class.java)
#                     startActivity(intent)
#                     finish()
#                     Security.user = User(userJSON, mutableListOf())
#                     break
#                 }
#             }
#
#             if (!isAuth) {
#                 Toast.makeText(this, "Скорее всего, данные неверны", Toast.LENGTH_SHORT).show()
#             }
#         }
#     }
# }

###Registration###

# package com.example.crud3
#
# import android.content.Intent
# import android.os.Bundle
# import android.widget.Button
# import android.widget.EditText
# import android.widget.Toast
# import androidx.appcompat.app.AppCompatActivity
# import org.json.JSONArray
# import org.json.JSONObject
# import java.io.File
#
# class Registration : AppCompatActivity() {
#     override fun onCreate(savedInstanceState: Bundle?) {
#         super.onCreate(savedInstanceState)
#         setContentView(R.layout.registration)
#
#         var login = findViewById<Button>(R.id.login);
#         login.setOnClickListener {
#             val intent = Intent(this, Login::class.java)
#             startActivity(intent)
#             finish()
#         }
#
#         val loginField: EditText = findViewById(R.id.loginField)
#         val password: EditText = findViewById(R.id.passwordField)
#         val name: EditText = findViewById(R.id.nameField)
#         val surname: EditText = findViewById(R.id.surnameField)
#         var registration = findViewById<Button>(R.id.reg);
#
#         registration.setOnClickListener {
#             val login = loginField.text.toString()
#             val pass = password.text.toString()
#             val nm = name.text.toString()
#             val snm = surname.text.toString()
#
#             if (login.isEmpty() || pass.isEmpty()) {
#                 Toast.makeText(this, "Заполните поля", Toast.LENGTH_SHORT).show()
#                 return@setOnClickListener
#             }
#
#             if (userExists(login)) {
#                 Toast.makeText(this, "Пользователь уже существует", Toast.LENGTH_SHORT).show()
#             } else {
#                 addUser(login, pass,nm,snm)
#                 Toast.makeText(this, "Пользователь зарегистрирован", Toast.LENGTH_SHORT).show()
#             }
#         }
#     }
#
#     private fun userExists(email: String): Boolean {
#         var jsonString = "{\"users\":[]}";
#         if(File(applicationContext.filesDir, "users.json").exists()) {
#             jsonString =
#                 File(applicationContext.filesDir, "users.json").bufferedReader().use { it.readText() }
#         }
#         val jsonObject = JSONObject(jsonString)
#         val usersArray = jsonObject.getJSONArray("users")
#
#         for (i in 0 until usersArray.length()) {
#             val userObject = usersArray.getJSONObject(i)
#             if (userObject.getString("email") == email) {
#                 return true
#             }
#         }
#         return false
#     }
#
#     private fun addUser(email: String, pass: String,name: String,surname: String) {
#         val usersFile = File(applicationContext.filesDir, "users.json")
#         val jsonString: String
#         val jsonObject: JSONObject
#
#         if (!usersFile.exists()) {
#             jsonObject = JSONObject()
#             jsonObject.put("users", JSONArray())
#         } else {
#             jsonString = usersFile.readText()
#             jsonObject = JSONObject(jsonString)
#         }
#
#         val usersArray = jsonObject.getJSONArray("users")
#         val newUser = JSONObject()
#         newUser.put("login", email)
#         newUser.put("password", pass)
#         newUser.put("name", name)
#         newUser.put("surname", surname)
#         usersArray.put(newUser)
#
#         usersFile.writeText(jsonObject.toString())
#     }
# }

###Products###

# package com.example.crud3
#
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
# import android.widget.LinearLayout
# import android.widget.Spinner
# import android.widget.TextView
# import android.widget.Toast
# import androidx.appcompat.app.AppCompatActivity
# import androidx.recyclerview.widget.RecyclerView.Orientation
# import com.google.gson.Gson
# import org.json.JSONArray
# import org.json.JSONObject
# import java.io.File
# import java.io.IOException
# import java.net.InetSocketAddress
# import java.net.Socket
# import java.net.SocketException
# import java.net.SocketTimeoutException
# import java.nio.charset.Charset
# import java.time.LocalDate
# import java.time.LocalDateTime
# import java.util.Date
# import java.util.UUID
# import java.util.concurrent.Executors
#
#
# class Products : AppCompatActivity() {
#
#     private var products = mutableListOf<Product>()
#     private var views = mutableListOf<MutableList<View>>()
#
#     override fun onCreate(savedInstanceState: Bundle?) {
#         super.onCreate(savedInstanceState)
#         setContentView(R.layout.products)
#
#         Thread() {
#             try {
#                 var socket = Socket()
#                 socket.connect(InetSocketAddress("10.0.2.2", 8080), 500)
#                 var inputStream = socket.getInputStream()
#
#                 val executor = Executors.newSingleThreadExecutor()
#                 var handler = Handler(Looper.getMainLooper())
#
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
#
#                                 handler.post(Runnable {
#                                     kotlin.run {
#                                         try {
#                                             Log.i("client", buffer.toString())
#
#                                             val jsonObject = jsonToJsonObject(buffer)
#                                             Log.i("client", jsonObject.toString())
#
#                                             val usersFile =
#                                                 File(
#                                                     applicationContext.filesDir,
#                                                     "products.json"
#                                                 )
#                                             usersFile.writeText(jsonObject.toString())
#
#                                             val categories = getCategoriesFromJsonObject(jsonObject);
#
#                                             val s = findViewById<Spinner>(R.id.spinner)
#                                             val adapter: ArrayAdapter<String> =
#                                                 ArrayAdapter<String>(
#                                                     this,
#                                                     androidx.appcompat.R.layout.support_simple_spinner_dropdown_item,
#                                                     categories
#                                                 )
#                                             s.adapter = adapter
#
#                                             setProducts("", "")
#
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
#
#
#         val linearLayout = findViewById<LinearLayout>(R.id.list)
#
#         var editText = findViewById<EditText>(R.id.search)
#         var search = ""
#         var sort = ""
#         editText.setOnKeyListener(object : View.OnKeyListener {
#             override fun onKey(v: View?, keyCode: Int, event: KeyEvent): Boolean {
#                 // if the event is a key down event on the enter button
#                 if (event.action == KeyEvent.ACTION_DOWN &&
#                     keyCode == KeyEvent.KEYCODE_ENTER
#                 ) {
#                     editText.clearFocus()
#                     editText.isCursorVisible = false
#
#                     search = editText.text.toString()
#                     linearLayout.removeAllViews()
#
#                     setProducts(search, sort)
#
#                     return true
#                 }
#                 return false
#             }
#         })
#
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
#
#             override fun onNothingSelected(parentView: AdapterView<*>?) {
#
#             }
#         })
#
#         var order = findViewById<Button>(R.id.order)
#         order.setOnClickListener {
#             makeOrder()
#         }
#
#
#     }
#
#     companion object {
#         fun getCategoriesFromJsonObject(jsonObject: JSONObject): MutableList<String> {
#             val categories = mutableListOf<String>()
#             categories.add("Без фильтра")
#             val categoryArray = jsonObject.getJSONArray("category")
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
#
#             return JSONObject(tmpMeassage);
#         }
#         fun createOrder(products: MutableList<Product>): String {
#             var id = UUID.randomUUID().toString();
#             var date = LocalDateTime.now()
#
#             var prods = mutableListOf<Product>()
#
#             for (i in Security.user?.productsId!!) {
#                 var product = products.filter { it.Id == i }[0].copy()
#                 if (prods.filter { it.Id == i }.isEmpty()) {
#                     product.Count = 1
#                     prods.add(product)
#                 } else {
#                     prods.filter { it.Id == i }[0].Count += 1
#                 }
#             }
#
#             var gson = Gson();
#             var json =
#                 gson.toJson(Order(id, prods, date.toString(), UserJson(Security.user!!.login)))
#
#             return json
#         }
#         fun getProducts(search: String,jsonObject1: JSONObject,sort: String): MutableList<Product> {
#             val productsArray1 = jsonObject1.getJSONArray("products")
#
#             var products = mutableListOf<Product>()
#
#             for (i in 0 until productsArray1.length()) {
#                 val userObject = productsArray1.getJSONObject(i)
#                 val id = userObject.getInt("Id")
#                 val url = userObject.getString("Url")
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
#
#             if (sort != "Без фильтра") products = products.filter { it.Category.Name == sort }.toMutableList()
#
#             return products;
#         }
#     }
#
#     fun makeOrder() {
#         if (Security.user?.productsId?.size!! > 0) {
#             var json = createOrder(products)
#
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
#                 } catch (e: SocketException) {
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
#
#     fun setProducts(search: String, sort: String) {
#         val linearLayout = findViewById<LinearLayout>(R.id.list)
#
#         linearLayout.removeAllViews()
#
#         val file1 = File(filesDir, "products.json")
#
#         val jsonString1 = if (file1.exists()) {
#             file1.bufferedReader().use {
#                 it.readText()
#             }
#         } else {
#             "{\"products\":[]}"
#         }
#
#         val jsonObject1 = JSONObject(jsonString1)
#         if (jsonObject1.length() > 0) {
#             products = getProducts(search,jsonObject1,sort)
#
#             for (item in products) {
#                 val linearLayout1 = LinearLayout(this)
#                 linearLayout1.layoutParams = LinearLayout.LayoutParams(
#                     LinearLayout.LayoutParams.MATCH_PARENT,
#                     220
#                 )
#                 linearLayout1.gravity = Gravity.CENTER or Gravity.LEFT
#                 linearLayout1.orientation = LinearLayout.HORIZONTAL
#
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
#
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
#
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
#
#
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
#
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
#
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
#
#                 views.add(mutableListOf(linearLayout3, buy))
#
#                 minus.setOnClickListener {
#                     if (Security.user?.productsId?.contains(item.Id) == true) {
#                         item.Count = (item.Count + 1)
#                         productsCount.text = item.Count.toString()
#                         Security.user?.productsId?.remove(item.Id);
#                         productsUserCount.text =
#                             Security.user?.productsId?.count { it == item.Id }.toString()
#
#                         if (Security.user?.productsId?.count { it == item.Id } == 0) {
#                             linearLayout3.removeAllViews()
#                             linearLayout3.addView(buy)
#                         }
#                     }
#                 }
#
#                 linearLayout.addView(linearLayout1)
#             }
#         }
#     }
#
# }
#
# data class Category(var Name: String)
# data class UserJson(var Name: String)
# data class Order(
#     var id: String,
#     var products: MutableList<Product>,
#     val date: String,
#     val user: UserJson
# )
#
# data class Product(
#     var Id: Int,
#     var Name: String,
#     var Url: String,
#     var Price: Int,
#     var Category: Category,
#     var Count: Int
# )

###UnitTestKotlin####

# package com.example.crud3
#
# import org.json.JSONObject
# import org.junit.Test
# import org.junit.jupiter.api.Assertions.*
# import java.io.File
# import java.time.LocalDateTime
#
# class ProductsTest {
#
#     @Test
#     fun jsonToJsonObjectTest() {
#         val str = "{\"products\":[{\"Id\":4,\"Name\":\"\\u0420\\u041F\\u041E-\\u0410 \\u0027\\u0428\\u043C\\u0435\\u043B\\u044C\\u0027\",\"Description\":\"C\\u043E\\u0432\\u0435\\u0442\\u0441\\u043A\\u0438\\u0439 \\u0438 \\u0440\\u043E\\u0441\\u0441\\u0438\\u0439\\u0441\\u043A\\u0438\\u0439 \\u0440\\u0435\\u0430\\u043A\\u0442\\u0438\\u0432\\u043D\\u044B\\u0439 \\u043F\\u0435\\u0445\\u043E\\u0442\\u043D\\u044B\\u0439 \\u043E\\u0433\\u043D\\u0435\\u043C\\u0451\\u0442 \\u043E\\u0434\\u043D\\u043E\\u0440\\u0430\\u0437\\u043E\\u0432\\u043E\\u0433\\u043E \\u043F\\u0440\\u0438\\u043C\\u0435\\u043D\\u0435\\u043D\\u0438\\u044F. \\u041F\\u0440\\u0435\\u0434\\u0441\\u0442\\u0430\\u0432\\u043B\\u044F\\u0435\\u0442 \\u0441\\u043E\\u0431\\u043E\\u0439 \\u0442\\u0435\\u0440\\u043C\\u043E\\u0431\\u0430\\u0440\\u0438\\u0447\\u0435\\u0441\\u043A\\u0443\\u044E \\u0440\\u0435\\u0430\\u043A\\u0442\\u0438\\u0432\\u043D\\u0443\\u044E \\u0433\\u0440\\u0430\\u043D\\u0430\\u0442\\u0443, \\u043D\\u0430\\u0447\\u0438\\u043D\\u0451\\u043D\\u043D\\u0443\\u044E \\u043E\\u0433\\u043D\\u0435\\u0441\\u043C\\u0435\\u0441\\u044C\\u044E. \\u0412\\u043E \\u0432\\u0440\\u0435\\u043C\\u044F \\u0432\\u043E\\u0439\\u043D\\u044B \\u0432 \\u0410\\u0444\\u0433\\u0430\\u043D\\u0438\\u0441\\u0442\\u0430\\u043D\\u0435 \\u043F\\u043E\\u043B\\u0443\\u0447\\u0438\\u043B \\u043F\\u0440\\u043E\\u0437\\u0432\\u0438\\u0449\\u0435 \\u00AB\\u0428\\u0430\\u0439\\u0442\\u0430\\u0301\\u043D-\\u0442\\u0440\\u0443\\u0431\\u0430\\u0301\\u00BB.\",\"Price\":10000,\"Category\":{\"Id\":2,\"Name\":\"\\u0413\\u0440\\u0430\\u043D\\u0430\\u0442\\u043E\\u043C\\u0451\\u0442\\u044B\"},\"Count\":100,\"Url\":\"C:\\\\Users\\\\10a\\\\Downloads\\\\rpo.png\"},{\"Id\":3,\"Name\":\"\\u0410\\u041A-74M\",\"Description\":\"\\u0410\\u0432\\u0442\\u043E\\u043C\\u0430\\u0442 \\u043A\\u0430\\u043B\\u0438\\u0431\\u0440\\u0430 5,45 \\u043C\\u043C, \\u0440\\u0430\\u0437\\u0440\\u0430\\u0431\\u043E\\u0442\\u0430\\u043D\\u043D\\u044B\\u0439 \\u0432 1970 \\u0433\\u043E\\u0434\\u0443 \\u0441\\u043E\\u0432\\u0435\\u0442\\u0441\\u043A\\u0438\\u043C \\u043A\\u043E\\u043D\\u0441\\u0442\\u0440\\u0443\\u043A\\u0442\\u043E\\u0440\\u043E\\u043C \\u041C. \\u0422. \\u041A\\u0430\\u043B\\u0430\\u0448\\u043D\\u0438\\u043A\\u043E\\u0432\\u044B\\u043C \\u0438 \\u043F\\u0440\\u0438\\u043D\\u044F\\u0442\\u044B\\u0439 \\u043D\\u0430 \\u0432\\u043E\\u043E\\u0440\\u0443\\u0436\\u0435\\u043D\\u0438\\u0435 \\u0432\\u043E\\u043E\\u0440\\u0443\\u0436\\u0451\\u043D\\u043D\\u044B\\u0445 \\u0441\\u0438\\u043B \\u0421\\u0421\\u0421\\u0420 \\u0432 1974 \\u0433\\u043E\\u0434\\u0443. \\u042F\\u0432\\u043B\\u044F\\u0435\\u0442\\u0441\\u044F \\u0434\\u0430\\u043B\\u044C\\u043D\\u0435\\u0439\\u0448\\u0438\\u043C \\u0440\\u0430\\u0437\\u0432\\u0438\\u0442\\u0438\\u0435\\u043C \\u0410\\u041A\\u041C. \\u0420\\u0430\\u0437\\u0440\\u0430\\u0431\\u043E\\u0442\\u043A\\u0430 \\u0410\\u041A-74 \\u0441\\u0432\\u044F\\u0437\\u0430\\u043D\\u0430 \\u0441 \\u043F\\u0435\\u0440\\u0435\\u0445\\u043E\\u0434\\u043E\\u043C \\u043D\\u0430 \\u043D\\u043E\\u0432\\u044B\\u0439 \\u043C\\u0430\\u043B\\u043E\\u0438\\u043C\\u043F\\u0443\\u043B\\u044C\\u0441\\u043D\\u044B\\u0439 \\u043F\\u0430\\u0442\\u0440\\u043E\\u043D 5,45\\u00D739 \\u043C\\u043C.\",\"Price\":1000,\"Category\":{\"Id\":3,\"Name\":\"\\u0410\\u0432\\u0442\\u043E\\u043C\\u0430\\u0442\\u044B\"},\"Count\":100,\"Url\":\"C:\\\\Users\\\\10a\\\\Downloads\\\\ak.jpg\"}],\"category\":[{\"Id\":2,\"Name\":\"\\u0413\\u0440\\u0430\\u043D\\u0430\\u0442\\u043E\\u043C\\u0451\\u0442\\u044B\"},{\"Id\":3,\"Name\":\"\\u0410\\u0432\\u0442\\u043E\\u043C\\u0430\\u0442\\u044B\"},{\"Id\":5,\"Name\":\"\\u0442\\u0430\\u043D\\u043A\\u0438\"},{\"Id\":6,\"Name\":\"\\u0441\\u0430\\u043C\\u043E\\u043B\\u0451\\u0442\\u044B\"}]}"
#         val array = str.toByteArray().toMutableList();
#
#         val productsArray1 = Products.jsonToJsonObject(array).getJSONArray("products")
#
#         assert(productsArray1.length()>0)
#     }
#
#     @Test
#     fun getCategoriesFromJsonObject() {
#         val str = "{\"products\":[{\"Id\":4,\"Name\":\"\\u0420\\u041F\\u041E-\\u0410 \\u0027\\u0428\\u043C\\u0435\\u043B\\u044C\\u0027\",\"Description\":\"C\\u043E\\u0432\\u0435\\u0442\\u0441\\u043A\\u0438\\u0439 \\u0438 \\u0440\\u043E\\u0441\\u0441\\u0438\\u0439\\u0441\\u043A\\u0438\\u0439 \\u0440\\u0435\\u0430\\u043A\\u0442\\u0438\\u0432\\u043D\\u044B\\u0439 \\u043F\\u0435\\u0445\\u043E\\u0442\\u043D\\u044B\\u0439 \\u043E\\u0433\\u043D\\u0435\\u043C\\u0451\\u0442 \\u043E\\u0434\\u043D\\u043E\\u0440\\u0430\\u0437\\u043E\\u0432\\u043E\\u0433\\u043E \\u043F\\u0440\\u0438\\u043C\\u0435\\u043D\\u0435\\u043D\\u0438\\u044F. \\u041F\\u0440\\u0435\\u0434\\u0441\\u0442\\u0430\\u0432\\u043B\\u044F\\u0435\\u0442 \\u0441\\u043E\\u0431\\u043E\\u0439 \\u0442\\u0435\\u0440\\u043C\\u043E\\u0431\\u0430\\u0440\\u0438\\u0447\\u0435\\u0441\\u043A\\u0443\\u044E \\u0440\\u0435\\u0430\\u043A\\u0442\\u0438\\u0432\\u043D\\u0443\\u044E \\u0433\\u0440\\u0430\\u043D\\u0430\\u0442\\u0443, \\u043D\\u0430\\u0447\\u0438\\u043D\\u0451\\u043D\\u043D\\u0443\\u044E \\u043E\\u0433\\u043D\\u0435\\u0441\\u043C\\u0435\\u0441\\u044C\\u044E. \\u0412\\u043E \\u0432\\u0440\\u0435\\u043C\\u044F \\u0432\\u043E\\u0439\\u043D\\u044B \\u0432 \\u0410\\u0444\\u0433\\u0430\\u043D\\u0438\\u0441\\u0442\\u0430\\u043D\\u0435 \\u043F\\u043E\\u043B\\u0443\\u0447\\u0438\\u043B \\u043F\\u0440\\u043E\\u0437\\u0432\\u0438\\u0449\\u0435 \\u00AB\\u0428\\u0430\\u0439\\u0442\\u0430\\u0301\\u043D-\\u0442\\u0440\\u0443\\u0431\\u0430\\u0301\\u00BB.\",\"Price\":10000,\"Category\":{\"Id\":2,\"Name\":\"\\u0413\\u0440\\u0430\\u043D\\u0430\\u0442\\u043E\\u043C\\u0451\\u0442\\u044B\"},\"Count\":100,\"Url\":\"C:\\\\Users\\\\10a\\\\Downloads\\\\rpo.png\"},{\"Id\":3,\"Name\":\"\\u0410\\u041A-74M\",\"Description\":\"\\u0410\\u0432\\u0442\\u043E\\u043C\\u0430\\u0442 \\u043A\\u0430\\u043B\\u0438\\u0431\\u0440\\u0430 5,45 \\u043C\\u043C, \\u0440\\u0430\\u0437\\u0440\\u0430\\u0431\\u043E\\u0442\\u0430\\u043D\\u043D\\u044B\\u0439 \\u0432 1970 \\u0433\\u043E\\u0434\\u0443 \\u0441\\u043E\\u0432\\u0435\\u0442\\u0441\\u043A\\u0438\\u043C \\u043A\\u043E\\u043D\\u0441\\u0442\\u0440\\u0443\\u043A\\u0442\\u043E\\u0440\\u043E\\u043C \\u041C. \\u0422. \\u041A\\u0430\\u043B\\u0430\\u0448\\u043D\\u0438\\u043A\\u043E\\u0432\\u044B\\u043C \\u0438 \\u043F\\u0440\\u0438\\u043D\\u044F\\u0442\\u044B\\u0439 \\u043D\\u0430 \\u0432\\u043E\\u043E\\u0440\\u0443\\u0436\\u0435\\u043D\\u0438\\u0435 \\u0432\\u043E\\u043E\\u0440\\u0443\\u0436\\u0451\\u043D\\u043D\\u044B\\u0445 \\u0441\\u0438\\u043B \\u0421\\u0421\\u0421\\u0420 \\u0432 1974 \\u0433\\u043E\\u0434\\u0443. \\u042F\\u0432\\u043B\\u044F\\u0435\\u0442\\u0441\\u044F \\u0434\\u0430\\u043B\\u044C\\u043D\\u0435\\u0439\\u0448\\u0438\\u043C \\u0440\\u0430\\u0437\\u0432\\u0438\\u0442\\u0438\\u0435\\u043C \\u0410\\u041A\\u041C. \\u0420\\u0430\\u0437\\u0440\\u0430\\u0431\\u043E\\u0442\\u043A\\u0430 \\u0410\\u041A-74 \\u0441\\u0432\\u044F\\u0437\\u0430\\u043D\\u0430 \\u0441 \\u043F\\u0435\\u0440\\u0435\\u0445\\u043E\\u0434\\u043E\\u043C \\u043D\\u0430 \\u043D\\u043E\\u0432\\u044B\\u0439 \\u043C\\u0430\\u043B\\u043E\\u0438\\u043C\\u043F\\u0443\\u043B\\u044C\\u0441\\u043D\\u044B\\u0439 \\u043F\\u0430\\u0442\\u0440\\u043E\\u043D 5,45\\u00D739 \\u043C\\u043C.\",\"Price\":1000,\"Category\":{\"Id\":3,\"Name\":\"\\u0410\\u0432\\u0442\\u043E\\u043C\\u0430\\u0442\\u044B\"},\"Count\":100,\"Url\":\"C:\\\\Users\\\\10a\\\\Downloads\\\\ak.jpg\"}],\"category\":[{\"Id\":2,\"Name\":\"\\u0413\\u0440\\u0430\\u043D\\u0430\\u0442\\u043E\\u043C\\u0451\\u0442\\u044B\"},{\"Id\":3,\"Name\":\"\\u0410\\u0432\\u0442\\u043E\\u043C\\u0430\\u0442\\u044B\"},{\"Id\":5,\"Name\":\"\\u0442\\u0430\\u043D\\u043A\\u0438\"},{\"Id\":6,\"Name\":\"\\u0441\\u0430\\u043C\\u043E\\u043B\\u0451\\u0442\\u044B\"}]}"
#         val array = str.toByteArray().toMutableList();
#
#         val productsArray1 = Products.getCategoriesFromJsonObject(Products.jsonToJsonObject(array))
#
#         assert(productsArray1.size>0)
#     }
#
#     @Test
#     fun getProductsTest() {
#         val str = "{\"products\":[{\"Id\":4,\"Name\":\"\\u0420\\u041F\\u041E-\\u0410 \\u0027\\u0428\\u043C\\u0435\\u043B\\u044C\\u0027\",\"Description\":\"C\\u043E\\u0432\\u0435\\u0442\\u0441\\u043A\\u0438\\u0439 \\u0438 \\u0440\\u043E\\u0441\\u0441\\u0438\\u0439\\u0441\\u043A\\u0438\\u0439 \\u0440\\u0435\\u0430\\u043A\\u0442\\u0438\\u0432\\u043D\\u044B\\u0439 \\u043F\\u0435\\u0445\\u043E\\u0442\\u043D\\u044B\\u0439 \\u043E\\u0433\\u043D\\u0435\\u043C\\u0451\\u0442 \\u043E\\u0434\\u043D\\u043E\\u0440\\u0430\\u0437\\u043E\\u0432\\u043E\\u0433\\u043E \\u043F\\u0440\\u0438\\u043C\\u0435\\u043D\\u0435\\u043D\\u0438\\u044F. \\u041F\\u0440\\u0435\\u0434\\u0441\\u0442\\u0430\\u0432\\u043B\\u044F\\u0435\\u0442 \\u0441\\u043E\\u0431\\u043E\\u0439 \\u0442\\u0435\\u0440\\u043C\\u043E\\u0431\\u0430\\u0440\\u0438\\u0447\\u0435\\u0441\\u043A\\u0443\\u044E \\u0440\\u0435\\u0430\\u043A\\u0442\\u0438\\u0432\\u043D\\u0443\\u044E \\u0433\\u0440\\u0430\\u043D\\u0430\\u0442\\u0443, \\u043D\\u0430\\u0447\\u0438\\u043D\\u0451\\u043D\\u043D\\u0443\\u044E \\u043E\\u0433\\u043D\\u0435\\u0441\\u043C\\u0435\\u0441\\u044C\\u044E. \\u0412\\u043E \\u0432\\u0440\\u0435\\u043C\\u044F \\u0432\\u043E\\u0439\\u043D\\u044B \\u0432 \\u0410\\u0444\\u0433\\u0430\\u043D\\u0438\\u0441\\u0442\\u0430\\u043D\\u0435 \\u043F\\u043E\\u043B\\u0443\\u0447\\u0438\\u043B \\u043F\\u0440\\u043E\\u0437\\u0432\\u0438\\u0449\\u0435 \\u00AB\\u0428\\u0430\\u0439\\u0442\\u0430\\u0301\\u043D-\\u0442\\u0440\\u0443\\u0431\\u0430\\u0301\\u00BB.\",\"Price\":10000,\"Category\":{\"Id\":2,\"Name\":\"\\u0413\\u0440\\u0430\\u043D\\u0430\\u0442\\u043E\\u043C\\u0451\\u0442\\u044B\"},\"Count\":100,\"Url\":\"C:\\\\Users\\\\10a\\\\Downloads\\\\rpo.png\"},{\"Id\":3,\"Name\":\"\\u0410\\u041A-74M\",\"Description\":\"\\u0410\\u0432\\u0442\\u043E\\u043C\\u0430\\u0442 \\u043A\\u0430\\u043B\\u0438\\u0431\\u0440\\u0430 5,45 \\u043C\\u043C, \\u0440\\u0430\\u0437\\u0440\\u0430\\u0431\\u043E\\u0442\\u0430\\u043D\\u043D\\u044B\\u0439 \\u0432 1970 \\u0433\\u043E\\u0434\\u0443 \\u0441\\u043E\\u0432\\u0435\\u0442\\u0441\\u043A\\u0438\\u043C \\u043A\\u043E\\u043D\\u0441\\u0442\\u0440\\u0443\\u043A\\u0442\\u043E\\u0440\\u043E\\u043C \\u041C. \\u0422. \\u041A\\u0430\\u043B\\u0430\\u0448\\u043D\\u0438\\u043A\\u043E\\u0432\\u044B\\u043C \\u0438 \\u043F\\u0440\\u0438\\u043D\\u044F\\u0442\\u044B\\u0439 \\u043D\\u0430 \\u0432\\u043E\\u043E\\u0440\\u0443\\u0436\\u0435\\u043D\\u0438\\u0435 \\u0432\\u043E\\u043E\\u0440\\u0443\\u0436\\u0451\\u043D\\u043D\\u044B\\u0445 \\u0441\\u0438\\u043B \\u0421\\u0421\\u0421\\u0420 \\u0432 1974 \\u0433\\u043E\\u0434\\u0443. \\u042F\\u0432\\u043B\\u044F\\u0435\\u0442\\u0441\\u044F \\u0434\\u0430\\u043B\\u044C\\u043D\\u0435\\u0439\\u0448\\u0438\\u043C \\u0440\\u0430\\u0437\\u0432\\u0438\\u0442\\u0438\\u0435\\u043C \\u0410\\u041A\\u041C. \\u0420\\u0430\\u0437\\u0440\\u0430\\u0431\\u043E\\u0442\\u043A\\u0430 \\u0410\\u041A-74 \\u0441\\u0432\\u044F\\u0437\\u0430\\u043D\\u0430 \\u0441 \\u043F\\u0435\\u0440\\u0435\\u0445\\u043E\\u0434\\u043E\\u043C \\u043D\\u0430 \\u043D\\u043E\\u0432\\u044B\\u0439 \\u043C\\u0430\\u043B\\u043E\\u0438\\u043C\\u043F\\u0443\\u043B\\u044C\\u0441\\u043D\\u044B\\u0439 \\u043F\\u0430\\u0442\\u0440\\u043E\\u043D 5,45\\u00D739 \\u043C\\u043C.\",\"Price\":1000,\"Category\":{\"Id\":3,\"Name\":\"\\u0410\\u0432\\u0442\\u043E\\u043C\\u0430\\u0442\\u044B\"},\"Count\":100,\"Url\":\"C:\\\\Users\\\\10a\\\\Downloads\\\\ak.jpg\"}],\"category\":[{\"Id\":2,\"Name\":\"\\u0413\\u0440\\u0430\\u043D\\u0430\\u0442\\u043E\\u043C\\u0451\\u0442\\u044B\"},{\"Id\":3,\"Name\":\"\\u0410\\u0432\\u0442\\u043E\\u043C\\u0430\\u0442\\u044B\"},{\"Id\":5,\"Name\":\"\\u0442\\u0430\\u043D\\u043A\\u0438\"},{\"Id\":6,\"Name\":\"\\u0441\\u0430\\u043C\\u043E\\u043B\\u0451\\u0442\\u044B\"}]}"
#         val array = str.toByteArray().toMutableList();
#
#         val jo = Products.jsonToJsonObject(array)
#
#         assert(Products.getProducts("",jo,"Без фильтра").size>0)
#     }
#
#     @Test
#     fun getProductsWithFilterest() {
#         val str = "{\"products\":[{\"Id\":4,\"Name\":\"\\u0420\\u041F\\u041E-\\u0410 \\u0027\\u0428\\u043C\\u0435\\u043B\\u044C\\u0027\",\"Description\":\"C\\u043E\\u0432\\u0435\\u0442\\u0441\\u043A\\u0438\\u0439 \\u0438 \\u0440\\u043E\\u0441\\u0441\\u0438\\u0439\\u0441\\u043A\\u0438\\u0439 \\u0440\\u0435\\u0430\\u043A\\u0442\\u0438\\u0432\\u043D\\u044B\\u0439 \\u043F\\u0435\\u0445\\u043E\\u0442\\u043D\\u044B\\u0439 \\u043E\\u0433\\u043D\\u0435\\u043C\\u0451\\u0442 \\u043E\\u0434\\u043D\\u043E\\u0440\\u0430\\u0437\\u043E\\u0432\\u043E\\u0433\\u043E \\u043F\\u0440\\u0438\\u043C\\u0435\\u043D\\u0435\\u043D\\u0438\\u044F. \\u041F\\u0440\\u0435\\u0434\\u0441\\u0442\\u0430\\u0432\\u043B\\u044F\\u0435\\u0442 \\u0441\\u043E\\u0431\\u043E\\u0439 \\u0442\\u0435\\u0440\\u043C\\u043E\\u0431\\u0430\\u0440\\u0438\\u0447\\u0435\\u0441\\u043A\\u0443\\u044E \\u0440\\u0435\\u0430\\u043A\\u0442\\u0438\\u0432\\u043D\\u0443\\u044E \\u0433\\u0440\\u0430\\u043D\\u0430\\u0442\\u0443, \\u043D\\u0430\\u0447\\u0438\\u043D\\u0451\\u043D\\u043D\\u0443\\u044E \\u043E\\u0433\\u043D\\u0435\\u0441\\u043C\\u0435\\u0441\\u044C\\u044E. \\u0412\\u043E \\u0432\\u0440\\u0435\\u043C\\u044F \\u0432\\u043E\\u0439\\u043D\\u044B \\u0432 \\u0410\\u0444\\u0433\\u0430\\u043D\\u0438\\u0441\\u0442\\u0430\\u043D\\u0435 \\u043F\\u043E\\u043B\\u0443\\u0447\\u0438\\u043B \\u043F\\u0440\\u043E\\u0437\\u0432\\u0438\\u0449\\u0435 \\u00AB\\u0428\\u0430\\u0439\\u0442\\u0430\\u0301\\u043D-\\u0442\\u0440\\u0443\\u0431\\u0430\\u0301\\u00BB.\",\"Price\":10000,\"Category\":{\"Id\":2,\"Name\":\"\\u0413\\u0440\\u0430\\u043D\\u0430\\u0442\\u043E\\u043C\\u0451\\u0442\\u044B\"},\"Count\":100,\"Url\":\"C:\\\\Users\\\\10a\\\\Downloads\\\\rpo.png\"},{\"Id\":3,\"Name\":\"\\u0410\\u041A-74M\",\"Description\":\"\\u0410\\u0432\\u0442\\u043E\\u043C\\u0430\\u0442 \\u043A\\u0430\\u043B\\u0438\\u0431\\u0440\\u0430 5,45 \\u043C\\u043C, \\u0440\\u0430\\u0437\\u0440\\u0430\\u0431\\u043E\\u0442\\u0430\\u043D\\u043D\\u044B\\u0439 \\u0432 1970 \\u0433\\u043E\\u0434\\u0443 \\u0441\\u043E\\u0432\\u0435\\u0442\\u0441\\u043A\\u0438\\u043C \\u043A\\u043E\\u043D\\u0441\\u0442\\u0440\\u0443\\u043A\\u0442\\u043E\\u0440\\u043E\\u043C \\u041C. \\u0422. \\u041A\\u0430\\u043B\\u0430\\u0448\\u043D\\u0438\\u043A\\u043E\\u0432\\u044B\\u043C \\u0438 \\u043F\\u0440\\u0438\\u043D\\u044F\\u0442\\u044B\\u0439 \\u043D\\u0430 \\u0432\\u043E\\u043E\\u0440\\u0443\\u0436\\u0435\\u043D\\u0438\\u0435 \\u0432\\u043E\\u043E\\u0440\\u0443\\u0436\\u0451\\u043D\\u043D\\u044B\\u0445 \\u0441\\u0438\\u043B \\u0421\\u0421\\u0421\\u0420 \\u0432 1974 \\u0433\\u043E\\u0434\\u0443. \\u042F\\u0432\\u043B\\u044F\\u0435\\u0442\\u0441\\u044F \\u0434\\u0430\\u043B\\u044C\\u043D\\u0435\\u0439\\u0448\\u0438\\u043C \\u0440\\u0430\\u0437\\u0432\\u0438\\u0442\\u0438\\u0435\\u043C \\u0410\\u041A\\u041C. \\u0420\\u0430\\u0437\\u0440\\u0430\\u0431\\u043E\\u0442\\u043A\\u0430 \\u0410\\u041A-74 \\u0441\\u0432\\u044F\\u0437\\u0430\\u043D\\u0430 \\u0441 \\u043F\\u0435\\u0440\\u0435\\u0445\\u043E\\u0434\\u043E\\u043C \\u043D\\u0430 \\u043D\\u043E\\u0432\\u044B\\u0439 \\u043C\\u0430\\u043B\\u043E\\u0438\\u043C\\u043F\\u0443\\u043B\\u044C\\u0441\\u043D\\u044B\\u0439 \\u043F\\u0430\\u0442\\u0440\\u043E\\u043D 5,45\\u00D739 \\u043C\\u043C.\",\"Price\":1000,\"Category\":{\"Id\":3,\"Name\":\"\\u0410\\u0432\\u0442\\u043E\\u043C\\u0430\\u0442\\u044B\"},\"Count\":100,\"Url\":\"C:\\\\Users\\\\10a\\\\Downloads\\\\ak.jpg\"}],\"category\":[{\"Id\":2,\"Name\":\"\\u0413\\u0440\\u0430\\u043D\\u0430\\u0442\\u043E\\u043C\\u0451\\u0442\\u044B\"},{\"Id\":3,\"Name\":\"\\u0410\\u0432\\u0442\\u043E\\u043C\\u0430\\u0442\\u044B\"},{\"Id\":5,\"Name\":\"\\u0442\\u0430\\u043D\\u043A\\u0438\"},{\"Id\":6,\"Name\":\"\\u0441\\u0430\\u043C\\u043E\\u043B\\u0451\\u0442\\u044B\"}]}"
#         val array = str.toByteArray().toMutableList();
#
#         val jo = Products.jsonToJsonObject(array)
#
#         assert(Products.getProducts("",jo,"Гранатомёты").size==1)
#     }
#
#     @Test
#     fun getProductsWithRightSearchTest() {
#         val str = "{\"products\":[{\"Id\":4,\"Name\":\"\\u0420\\u041F\\u041E-\\u0410 \\u0027\\u0428\\u043C\\u0435\\u043B\\u044C\\u0027\",\"Description\":\"C\\u043E\\u0432\\u0435\\u0442\\u0441\\u043A\\u0438\\u0439 \\u0438 \\u0440\\u043E\\u0441\\u0441\\u0438\\u0439\\u0441\\u043A\\u0438\\u0439 \\u0440\\u0435\\u0430\\u043A\\u0442\\u0438\\u0432\\u043D\\u044B\\u0439 \\u043F\\u0435\\u0445\\u043E\\u0442\\u043D\\u044B\\u0439 \\u043E\\u0433\\u043D\\u0435\\u043C\\u0451\\u0442 \\u043E\\u0434\\u043D\\u043E\\u0440\\u0430\\u0437\\u043E\\u0432\\u043E\\u0433\\u043E \\u043F\\u0440\\u0438\\u043C\\u0435\\u043D\\u0435\\u043D\\u0438\\u044F. \\u041F\\u0440\\u0435\\u0434\\u0441\\u0442\\u0430\\u0432\\u043B\\u044F\\u0435\\u0442 \\u0441\\u043E\\u0431\\u043E\\u0439 \\u0442\\u0435\\u0440\\u043C\\u043E\\u0431\\u0430\\u0440\\u0438\\u0447\\u0435\\u0441\\u043A\\u0443\\u044E \\u0440\\u0435\\u0430\\u043A\\u0442\\u0438\\u0432\\u043D\\u0443\\u044E \\u0433\\u0440\\u0430\\u043D\\u0430\\u0442\\u0443, \\u043D\\u0430\\u0447\\u0438\\u043D\\u0451\\u043D\\u043D\\u0443\\u044E \\u043E\\u0433\\u043D\\u0435\\u0441\\u043C\\u0435\\u0441\\u044C\\u044E. \\u0412\\u043E \\u0432\\u0440\\u0435\\u043C\\u044F \\u0432\\u043E\\u0439\\u043D\\u044B \\u0432 \\u0410\\u0444\\u0433\\u0430\\u043D\\u0438\\u0441\\u0442\\u0430\\u043D\\u0435 \\u043F\\u043E\\u043B\\u0443\\u0447\\u0438\\u043B \\u043F\\u0440\\u043E\\u0437\\u0432\\u0438\\u0449\\u0435 \\u00AB\\u0428\\u0430\\u0439\\u0442\\u0430\\u0301\\u043D-\\u0442\\u0440\\u0443\\u0431\\u0430\\u0301\\u00BB.\",\"Price\":10000,\"Category\":{\"Id\":2,\"Name\":\"\\u0413\\u0440\\u0430\\u043D\\u0430\\u0442\\u043E\\u043C\\u0451\\u0442\\u044B\"},\"Count\":100,\"Url\":\"C:\\\\Users\\\\10a\\\\Downloads\\\\rpo.png\"},{\"Id\":3,\"Name\":\"\\u0410\\u041A-74M\",\"Description\":\"\\u0410\\u0432\\u0442\\u043E\\u043C\\u0430\\u0442 \\u043A\\u0430\\u043B\\u0438\\u0431\\u0440\\u0430 5,45 \\u043C\\u043C, \\u0440\\u0430\\u0437\\u0440\\u0430\\u0431\\u043E\\u0442\\u0430\\u043D\\u043D\\u044B\\u0439 \\u0432 1970 \\u0433\\u043E\\u0434\\u0443 \\u0441\\u043E\\u0432\\u0435\\u0442\\u0441\\u043A\\u0438\\u043C \\u043A\\u043E\\u043D\\u0441\\u0442\\u0440\\u0443\\u043A\\u0442\\u043E\\u0440\\u043E\\u043C \\u041C. \\u0422. \\u041A\\u0430\\u043B\\u0430\\u0448\\u043D\\u0438\\u043A\\u043E\\u0432\\u044B\\u043C \\u0438 \\u043F\\u0440\\u0438\\u043D\\u044F\\u0442\\u044B\\u0439 \\u043D\\u0430 \\u0432\\u043E\\u043E\\u0440\\u0443\\u0436\\u0435\\u043D\\u0438\\u0435 \\u0432\\u043E\\u043E\\u0440\\u0443\\u0436\\u0451\\u043D\\u043D\\u044B\\u0445 \\u0441\\u0438\\u043B \\u0421\\u0421\\u0421\\u0420 \\u0432 1974 \\u0433\\u043E\\u0434\\u0443. \\u042F\\u0432\\u043B\\u044F\\u0435\\u0442\\u0441\\u044F \\u0434\\u0430\\u043B\\u044C\\u043D\\u0435\\u0439\\u0448\\u0438\\u043C \\u0440\\u0430\\u0437\\u0432\\u0438\\u0442\\u0438\\u0435\\u043C \\u0410\\u041A\\u041C. \\u0420\\u0430\\u0437\\u0440\\u0430\\u0431\\u043E\\u0442\\u043A\\u0430 \\u0410\\u041A-74 \\u0441\\u0432\\u044F\\u0437\\u0430\\u043D\\u0430 \\u0441 \\u043F\\u0435\\u0440\\u0435\\u0445\\u043E\\u0434\\u043E\\u043C \\u043D\\u0430 \\u043D\\u043E\\u0432\\u044B\\u0439 \\u043C\\u0430\\u043B\\u043E\\u0438\\u043C\\u043F\\u0443\\u043B\\u044C\\u0441\\u043D\\u044B\\u0439 \\u043F\\u0430\\u0442\\u0440\\u043E\\u043D 5,45\\u00D739 \\u043C\\u043C.\",\"Price\":1000,\"Category\":{\"Id\":3,\"Name\":\"\\u0410\\u0432\\u0442\\u043E\\u043C\\u0430\\u0442\\u044B\"},\"Count\":100,\"Url\":\"C:\\\\Users\\\\10a\\\\Downloads\\\\ak.jpg\"}],\"category\":[{\"Id\":2,\"Name\":\"\\u0413\\u0440\\u0430\\u043D\\u0430\\u0442\\u043E\\u043C\\u0451\\u0442\\u044B\"},{\"Id\":3,\"Name\":\"\\u0410\\u0432\\u0442\\u043E\\u043C\\u0430\\u0442\\u044B\"},{\"Id\":5,\"Name\":\"\\u0442\\u0430\\u043D\\u043A\\u0438\"},{\"Id\":6,\"Name\":\"\\u0441\\u0430\\u043C\\u043E\\u043B\\u0451\\u0442\\u044B\"}]}"
#         val array = str.toByteArray().toMutableList();
#
#         val jo = Products.jsonToJsonObject(array)
#
#         assert(Products.getProducts("РПО",jo,"Без фильтра").size==1)
#     }
#
#     @Test
#     fun getProductsWithWrongSearchTest() {
#         val str = "{\"products\":[{\"Id\":4,\"Name\":\"\\u0420\\u041F\\u041E-\\u0410 \\u0027\\u0428\\u043C\\u0435\\u043B\\u044C\\u0027\",\"Description\":\"C\\u043E\\u0432\\u0435\\u0442\\u0441\\u043A\\u0438\\u0439 \\u0438 \\u0440\\u043E\\u0441\\u0441\\u0438\\u0439\\u0441\\u043A\\u0438\\u0439 \\u0440\\u0435\\u0430\\u043A\\u0442\\u0438\\u0432\\u043D\\u044B\\u0439 \\u043F\\u0435\\u0445\\u043E\\u0442\\u043D\\u044B\\u0439 \\u043E\\u0433\\u043D\\u0435\\u043C\\u0451\\u0442 \\u043E\\u0434\\u043D\\u043E\\u0440\\u0430\\u0437\\u043E\\u0432\\u043E\\u0433\\u043E \\u043F\\u0440\\u0438\\u043C\\u0435\\u043D\\u0435\\u043D\\u0438\\u044F. \\u041F\\u0440\\u0435\\u0434\\u0441\\u0442\\u0430\\u0432\\u043B\\u044F\\u0435\\u0442 \\u0441\\u043E\\u0431\\u043E\\u0439 \\u0442\\u0435\\u0440\\u043C\\u043E\\u0431\\u0430\\u0440\\u0438\\u0447\\u0435\\u0441\\u043A\\u0443\\u044E \\u0440\\u0435\\u0430\\u043A\\u0442\\u0438\\u0432\\u043D\\u0443\\u044E \\u0433\\u0440\\u0430\\u043D\\u0430\\u0442\\u0443, \\u043D\\u0430\\u0447\\u0438\\u043D\\u0451\\u043D\\u043D\\u0443\\u044E \\u043E\\u0433\\u043D\\u0435\\u0441\\u043C\\u0435\\u0441\\u044C\\u044E. \\u0412\\u043E \\u0432\\u0440\\u0435\\u043C\\u044F \\u0432\\u043E\\u0439\\u043D\\u044B \\u0432 \\u0410\\u0444\\u0433\\u0430\\u043D\\u0438\\u0441\\u0442\\u0430\\u043D\\u0435 \\u043F\\u043E\\u043B\\u0443\\u0447\\u0438\\u043B \\u043F\\u0440\\u043E\\u0437\\u0432\\u0438\\u0449\\u0435 \\u00AB\\u0428\\u0430\\u0439\\u0442\\u0430\\u0301\\u043D-\\u0442\\u0440\\u0443\\u0431\\u0430\\u0301\\u00BB.\",\"Price\":10000,\"Category\":{\"Id\":2,\"Name\":\"\\u0413\\u0440\\u0430\\u043D\\u0430\\u0442\\u043E\\u043C\\u0451\\u0442\\u044B\"},\"Count\":100,\"Url\":\"C:\\\\Users\\\\10a\\\\Downloads\\\\rpo.png\"},{\"Id\":3,\"Name\":\"\\u0410\\u041A-74M\",\"Description\":\"\\u0410\\u0432\\u0442\\u043E\\u043C\\u0430\\u0442 \\u043A\\u0430\\u043B\\u0438\\u0431\\u0440\\u0430 5,45 \\u043C\\u043C, \\u0440\\u0430\\u0437\\u0440\\u0430\\u0431\\u043E\\u0442\\u0430\\u043D\\u043D\\u044B\\u0439 \\u0432 1970 \\u0433\\u043E\\u0434\\u0443 \\u0441\\u043E\\u0432\\u0435\\u0442\\u0441\\u043A\\u0438\\u043C \\u043A\\u043E\\u043D\\u0441\\u0442\\u0440\\u0443\\u043A\\u0442\\u043E\\u0440\\u043E\\u043C \\u041C. \\u0422. \\u041A\\u0430\\u043B\\u0430\\u0448\\u043D\\u0438\\u043A\\u043E\\u0432\\u044B\\u043C \\u0438 \\u043F\\u0440\\u0438\\u043D\\u044F\\u0442\\u044B\\u0439 \\u043D\\u0430 \\u0432\\u043E\\u043E\\u0440\\u0443\\u0436\\u0435\\u043D\\u0438\\u0435 \\u0432\\u043E\\u043E\\u0440\\u0443\\u0436\\u0451\\u043D\\u043D\\u044B\\u0445 \\u0441\\u0438\\u043B \\u0421\\u0421\\u0421\\u0420 \\u0432 1974 \\u0433\\u043E\\u0434\\u0443. \\u042F\\u0432\\u043B\\u044F\\u0435\\u0442\\u0441\\u044F \\u0434\\u0430\\u043B\\u044C\\u043D\\u0435\\u0439\\u0448\\u0438\\u043C \\u0440\\u0430\\u0437\\u0432\\u0438\\u0442\\u0438\\u0435\\u043C \\u0410\\u041A\\u041C. \\u0420\\u0430\\u0437\\u0440\\u0430\\u0431\\u043E\\u0442\\u043A\\u0430 \\u0410\\u041A-74 \\u0441\\u0432\\u044F\\u0437\\u0430\\u043D\\u0430 \\u0441 \\u043F\\u0435\\u0440\\u0435\\u0445\\u043E\\u0434\\u043E\\u043C \\u043D\\u0430 \\u043D\\u043E\\u0432\\u044B\\u0439 \\u043C\\u0430\\u043B\\u043E\\u0438\\u043C\\u043F\\u0443\\u043B\\u044C\\u0441\\u043D\\u044B\\u0439 \\u043F\\u0430\\u0442\\u0440\\u043E\\u043D 5,45\\u00D739 \\u043C\\u043C.\",\"Price\":1000,\"Category\":{\"Id\":3,\"Name\":\"\\u0410\\u0432\\u0442\\u043E\\u043C\\u0430\\u0442\\u044B\"},\"Count\":100,\"Url\":\"C:\\\\Users\\\\10a\\\\Downloads\\\\ak.jpg\"}],\"category\":[{\"Id\":2,\"Name\":\"\\u0413\\u0440\\u0430\\u043D\\u0430\\u0442\\u043E\\u043C\\u0451\\u0442\\u044B\"},{\"Id\":3,\"Name\":\"\\u0410\\u0432\\u0442\\u043E\\u043C\\u0430\\u0442\\u044B\"},{\"Id\":5,\"Name\":\"\\u0442\\u0430\\u043D\\u043A\\u0438\"},{\"Id\":6,\"Name\":\"\\u0441\\u0430\\u043C\\u043E\\u043B\\u0451\\u0442\\u044B\"}]}"
#         val array = str.toByteArray().toMutableList();
#
#         val jo = Products.jsonToJsonObject(array)
#
#         assert(Products.getProducts("asdasd",jo,"Без фильтра").size==0)
#     }
#
#     @Test
#     fun createOrderTest() {
#         Security.user = User("test", arrayOf(4,3).toMutableList())
#
#         val str = "{\"products\":[{\"Id\":4,\"Name\":\"\\u0420\\u041F\\u041E-\\u0410 \\u0027\\u0428\\u043C\\u0435\\u043B\\u044C\\u0027\",\"Description\":\"C\\u043E\\u0432\\u0435\\u0442\\u0441\\u043A\\u0438\\u0439 \\u0438 \\u0440\\u043E\\u0441\\u0441\\u0438\\u0439\\u0441\\u043A\\u0438\\u0439 \\u0440\\u0435\\u0430\\u043A\\u0442\\u0438\\u0432\\u043D\\u044B\\u0439 \\u043F\\u0435\\u0445\\u043E\\u0442\\u043D\\u044B\\u0439 \\u043E\\u0433\\u043D\\u0435\\u043C\\u0451\\u0442 \\u043E\\u0434\\u043D\\u043E\\u0440\\u0430\\u0437\\u043E\\u0432\\u043E\\u0433\\u043E \\u043F\\u0440\\u0438\\u043C\\u0435\\u043D\\u0435\\u043D\\u0438\\u044F. \\u041F\\u0440\\u0435\\u0434\\u0441\\u0442\\u0430\\u0432\\u043B\\u044F\\u0435\\u0442 \\u0441\\u043E\\u0431\\u043E\\u0439 \\u0442\\u0435\\u0440\\u043C\\u043E\\u0431\\u0430\\u0440\\u0438\\u0447\\u0435\\u0441\\u043A\\u0443\\u044E \\u0440\\u0435\\u0430\\u043A\\u0442\\u0438\\u0432\\u043D\\u0443\\u044E \\u0433\\u0440\\u0430\\u043D\\u0430\\u0442\\u0443, \\u043D\\u0430\\u0447\\u0438\\u043D\\u0451\\u043D\\u043D\\u0443\\u044E \\u043E\\u0433\\u043D\\u0435\\u0441\\u043C\\u0435\\u0441\\u044C\\u044E. \\u0412\\u043E \\u0432\\u0440\\u0435\\u043C\\u044F \\u0432\\u043E\\u0439\\u043D\\u044B \\u0432 \\u0410\\u0444\\u0433\\u0430\\u043D\\u0438\\u0441\\u0442\\u0430\\u043D\\u0435 \\u043F\\u043E\\u043B\\u0443\\u0447\\u0438\\u043B \\u043F\\u0440\\u043E\\u0437\\u0432\\u0438\\u0449\\u0435 \\u00AB\\u0428\\u0430\\u0439\\u0442\\u0430\\u0301\\u043D-\\u0442\\u0440\\u0443\\u0431\\u0430\\u0301\\u00BB.\",\"Price\":10000,\"Category\":{\"Id\":2,\"Name\":\"\\u0413\\u0440\\u0430\\u043D\\u0430\\u0442\\u043E\\u043C\\u0451\\u0442\\u044B\"},\"Count\":100,\"Url\":\"C:\\\\Users\\\\10a\\\\Downloads\\\\rpo.png\"},{\"Id\":3,\"Name\":\"\\u0410\\u041A-74M\",\"Description\":\"\\u0410\\u0432\\u0442\\u043E\\u043C\\u0430\\u0442 \\u043A\\u0430\\u043B\\u0438\\u0431\\u0440\\u0430 5,45 \\u043C\\u043C, \\u0440\\u0430\\u0437\\u0440\\u0430\\u0431\\u043E\\u0442\\u0430\\u043D\\u043D\\u044B\\u0439 \\u0432 1970 \\u0433\\u043E\\u0434\\u0443 \\u0441\\u043E\\u0432\\u0435\\u0442\\u0441\\u043A\\u0438\\u043C \\u043A\\u043E\\u043D\\u0441\\u0442\\u0440\\u0443\\u043A\\u0442\\u043E\\u0440\\u043E\\u043C \\u041C. \\u0422. \\u041A\\u0430\\u043B\\u0430\\u0448\\u043D\\u0438\\u043A\\u043E\\u0432\\u044B\\u043C \\u0438 \\u043F\\u0440\\u0438\\u043D\\u044F\\u0442\\u044B\\u0439 \\u043D\\u0430 \\u0432\\u043E\\u043E\\u0440\\u0443\\u0436\\u0435\\u043D\\u0438\\u0435 \\u0432\\u043E\\u043E\\u0440\\u0443\\u0436\\u0451\\u043D\\u043D\\u044B\\u0445 \\u0441\\u0438\\u043B \\u0421\\u0421\\u0421\\u0420 \\u0432 1974 \\u0433\\u043E\\u0434\\u0443. \\u042F\\u0432\\u043B\\u044F\\u0435\\u0442\\u0441\\u044F \\u0434\\u0430\\u043B\\u044C\\u043D\\u0435\\u0439\\u0448\\u0438\\u043C \\u0440\\u0430\\u0437\\u0432\\u0438\\u0442\\u0438\\u0435\\u043C \\u0410\\u041A\\u041C. \\u0420\\u0430\\u0437\\u0440\\u0430\\u0431\\u043E\\u0442\\u043A\\u0430 \\u0410\\u041A-74 \\u0441\\u0432\\u044F\\u0437\\u0430\\u043D\\u0430 \\u0441 \\u043F\\u0435\\u0440\\u0435\\u0445\\u043E\\u0434\\u043E\\u043C \\u043D\\u0430 \\u043D\\u043E\\u0432\\u044B\\u0439 \\u043C\\u0430\\u043B\\u043E\\u0438\\u043C\\u043F\\u0443\\u043B\\u044C\\u0441\\u043D\\u044B\\u0439 \\u043F\\u0430\\u0442\\u0440\\u043E\\u043D 5,45\\u00D739 \\u043C\\u043C.\",\"Price\":1000,\"Category\":{\"Id\":3,\"Name\":\"\\u0410\\u0432\\u0442\\u043E\\u043C\\u0430\\u0442\\u044B\"},\"Count\":100,\"Url\":\"C:\\\\Users\\\\10a\\\\Downloads\\\\ak.jpg\"}],\"category\":[{\"Id\":2,\"Name\":\"\\u0413\\u0440\\u0430\\u043D\\u0430\\u0442\\u043E\\u043C\\u0451\\u0442\\u044B\"},{\"Id\":3,\"Name\":\"\\u0410\\u0432\\u0442\\u043E\\u043C\\u0430\\u0442\\u044B\"},{\"Id\":5,\"Name\":\"\\u0442\\u0430\\u043D\\u043A\\u0438\"},{\"Id\":6,\"Name\":\"\\u0441\\u0430\\u043C\\u043E\\u043B\\u0451\\u0442\\u044B\"}]}"
#         val array = str.toByteArray().toMutableList();
#         val jo = Products.jsonToJsonObject(array)
#         var products = Products.getProducts("",jo,"Без фильтра")
#
#         var order = Products.createOrder(products)
#         val orderStr = "{\"date\":\"\",\"id\":\"1d1ef7bc-ccb4-46da-9e8d-cdbf31de795c\",\"products\":[{\"Category\":{\"Name\":\"{\\\"Id\\\":2,\\\"Name\\\":\\\"Гранатомёты\\\"}\"},\"Count\":1,\"Id\":\"4\",\"Name\":\"РПО-А \\u0027Шмель\\u0027\",\"Price\":10000,\"Url\":\"C:\\\\Users\\\\10a\\\\Downloads\\\\rpo.png\"},{\"Category\":{\"Name\":\"{\\\"Id\\\":3,\\\"Name\\\":\\\"Автоматы\\\"}\"},\"Count\":1,\"Id\":\"3\",\"Name\":\"АК-74M\",\"Price\":1000,\"Url\":\"C:\\\\Users\\\\10a\\\\Downloads\\\\ak.jpg\"}],\"user\":{\"Name\":\"123\"}}"
#
#         val orderArray = order.toByteArray().toMutableList();
#         val jo1 = Products.jsonToJsonObject(orderArray)
#         val orderStrArray = orderStr.toByteArray().toMutableList();
#         val jo2 = Products.jsonToJsonObject(orderStrArray)
#
#         assert(jo1.getJSONArray("products").length()==jo2.getJSONArray("products").length())
#     }
#
# }

###DepedensesInBuildGradle###

# dependencies {
#
#     implementation("androidx.core:core-ktx:1.9.0")
#     implementation("androidx.appcompat:appcompat:1.6.1")
#     implementation("com.google.android.material:material:1.8.0")
#     implementation("androidx.constraintlayout:constraintlayout:2.1.4")
#     testImplementation("junit:junit:4.13.2")
#     testImplementation("org.junit.jupiter:junit-jupiter:5.8.1")
#     androidTestImplementation("androidx.test.ext:junit:1.1.5")
#     androidTestImplementation("androidx.test.espresso:espresso-core:3.5.1")
#     implementation("com.google.code.gson:gson:2.8.5")
#     testImplementation("org.json:json:20180813")
# }

###Manifest###

# <?xml version="1.0" encoding="utf-8"?>
# <manifest xmlns:android="http://schemas.android.com/apk/res/android"
#     xmlns:tools="http://schemas.android.com/tools">
#
#     <uses-permission android:name="android.permission.INTERNET" />
#     <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
#
#     <application
#         android:allowBackup="true"
#         android:dataExtractionRules="@xml/data_extraction_rules"
#         android:fullBackupContent="@xml/backup_rules"
#         android:icon="@mipmap/ic_launcher"
#         android:label="@string/app_name"
#         android:roundIcon="@mipmap/ic_launcher_round"
#         android:supportsRtl="true"
#         android:theme="@style/Theme.Crud3"
#         tools:targetApi="31">
#         <activity
#             android:name=".Login"
#             android:exported="true">
#             <intent-filter>
#                 <action android:name="android.intent.action.MAIN" />
#
#                 <category android:name="android.intent.category.LAUNCHER" />
#             </intent-filter>
#         </activity>
#         <activity
#             android:name=".Registration"
#             android:exported="true">
#             <intent-filter>
#                 <action android:name="android.intent.action.MAIN" />
#
#                 <category android:name="android.intent.category.LAUNCHER" />
#             </intent-filter>
#         </activity>
#         <activity
#             android:name=".Products"
#             android:exported="true">
#             <intent-filter>
#                 <action android:name="android.intent.action.MAIN" />
#
#                 <category android:name="android.intent.category.LAUNCHER" />
#             </intent-filter>
#         </activity>
#     </application>
#
# </manifest>



##################Python########################



###DataClass###

# from dataclasses import dataclass
# from datetime import datetime
#
#
# @dataclass
# class Product:
#     Id: str
#     Name: str
#     Price: int
#     Count: int
#     Category: dict
#     Url: str
#
#
#     @staticmethod
#     def deserialize_product(dict):
#         return Product(dict['Id'],dict['Name'],dict['Price'],dict['Count'],dict["Category"],dict["Url"])
#
# @dataclass
# class Order:
#     id: int
#     products: list
#     date: datetime
#     user: dict
#
#     @staticmethod
#     def deserializer(data: dict):
#         if isinstance(data,dict):
#             products = []
#             for value in data['products']:
#                 products.append(Product.deserialize_product(value))
#             return Order(data['id'],products, data['date'],data['user'])


###MainPy####

# import json
# import socket
# import sys
# from datetime import datetime
# from json import JSONDecodeError
#
# from PyQt5 import QtCore
# from PyQt5 import QtWidgets
# from PyQt5.QtWidgets import *
# from PyQt5.QtCore import *
# from PyQt5.QtGui import *
# import threading
# from dataclass import Order
#
#
# class ServerSignals(QObject):
#     new_data = pyqtSignal(object)
#
#
# class ServerThread(threading.Thread):
#     def __init__(self, signals):
#         super().__init__()
#         self.signals = signals
#
#     def run(self):
#         self.start_server(self.signals)
#
#     def start_server(self, signals, host='127.0.0.1', port=12345):
#         server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         server.bind((host, port))
#         server.listen()
#         print(f"Server listening on {host}:{port}")
#
#         try:
#             while True:
#                 conn, addr = server.accept()
#                 client_thread = threading.Thread(target=self.handle_client, args=(conn, addr, signals))
#                 client_thread.start()
#         except KeyboardInterrupt:
#             print("Server is shutting down")
#         finally:
#             server.close()
#
#     def handle_client(self, connection, address, signals):
#         print(f"Connected by {address}")
#         try:
#             while True:
#                 data = connection.recv(10024)
#                 if not data:
#                     break
#
#                 # Обработка данных
#                 received_data = ServerThread.decode(data)
#
#                 # Отправка данных в основной поток через сигнал
#                 signals.new_data.emit(received_data)
#
#         except Exception as e:
#             print(f"Error handling data from {address}: {e}")
#         finally:
#             connection.close()
#
#     @staticmethod
#     def decode(str1):
#         try:
#             received_json = str1.decode('utf-8')
#             received_data = json.loads(received_json)
#             return Order.deserializer(received_data)
#         except JSONDecodeError:
#             return None
#
#
# class MyWindow(QtWidgets.QWidget):
#     products = QtCore.pyqtSignal(object)
#
#     def __init__(self, parent=None):
#         QtWidgets.QWidget.__init__(self, parent)
#         self.setWindowTitle("Calculator")
#
#         self.model = QStandardItemModel()
#         self.model.setColumnCount(1)
#         self.model.setHorizontalHeaderLabels(["Id", "Date", "Time", "User", "Value"])
#         self.table = QTableView()
#         self.table.setModel(self.model)
#         self.table.clicked.connect(self.on_click)
#         # Set column headers
#         self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
#
#         self.clndr = QCalendarWidget(self)
#         self.clndr.selectionChanged.connect(self.changeDate)
#
#         self.grid = QtWidgets.QGridLayout()
#         self.grid.addWidget(self.table, 2, 0, 1, 1)
#         self.grid.addWidget(self.clndr, 1, 0)
#
#         self.start_server()
#
#         self.data = list()
#         self.data1 = list()
#
#         self.setLayout(self.grid)
#
#     @staticmethod
#     def filterData(item,datet2):
#         date1 = item.date
#         datet = datetime.strptime(date1[:date1.index("T")], '%Y-%m-%d').date()
#         return datet>datet2
#
#     @staticmethod
#     def filtered(data,selectedDate):
#         return filter(lambda i: MyWindow.filterData(i,selectedDate), data)
#
#     def changeDate(self):
#         self.model.removeRows(0, self.model.rowCount())
#         newData = MyWindow.filtered(self.data1,self.clndr.selectedDate().toPyDate())
#         for i in newData:
#             self.load_data(i)
#
#     def start_server(self):
#         self.server_signals = ServerSignals()
#
#         self.server_signals.new_data.connect(self.load_data1)
#
#         self.server_thread = ServerThread(self.server_signals)
#         self.server_thread.start()
#
#     def load_data1(self,data):
#         self.data1.append(data)
#         self.load_data(data)
#
#     def load_data(self, data):
#         self.data.append(data.products)
#         sum = 0
#         for i in data.products:
#             sum += i.Price * i.Count
#
#         order_date = data.date
#
#         row = [
#             QStandardItem(str(data.id)),
#             QStandardItem(order_date[:order_date.index("T")]),
#             QStandardItem(order_date[order_date.index("T") + 1:order_date.index(".")]),
#             QStandardItem(data.get("user").get("Name")),
#             QStandardItem(str(sum))
#         ]
#
#         for i in row:
#             i.setEditable(False)
#
#         self.model.appendRow(row)
#
#     @pyqtSlot(QModelIndex)
#     def on_click(self, index):
#         for i in range(len(self.data)):
#             if i == index.row():
#                 self.products.emit(self.data[i])
#         self.parent().setCurrentIndex(1)
#
#
# class MyWindow2(QtWidgets.QWidget):
#     def __init__(self, parent=None):
#         QtWidgets.QWidget.__init__(self, parent)
#         self.layout = QVBoxLayout()
#         self.button = QPushButton("Go back")
#         self.button.clicked.connect(self.go_back)
#
#         self.model = QStandardItemModel()
#         self.model.setColumnCount(1)
#         self.model.setHorizontalHeaderLabels(["Id", "Name", "Count", "Price"])
#         self.table = QTableView()
#         self.table.setModel(self.model)
#         # Set column headers
#         self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
#
#         self.grid = QtWidgets.QGridLayout()
#         self.grid.addWidget(self.table, 2, 0, 1, 1)
#
#         self.search = QLineEdit()
#         self.search.textChanged.connect(self.onSearchChanged)
#
#         self.layout.addWidget(self.button)
#         self.layout.addWidget(self.search)
#         self.layout.addWidget(self.table)
#         self.setLayout(self.layout)
#
#         self.products = None
#
#     def getProducts(self, products):
#         if self.products is None:
#             self.products = products
#
#         for item in products:
#             row = [
#                 QStandardItem(str(item.Id)),
#                 QStandardItem(item.Name),
#                 QStandardItem(str(item.Count)),
#                 QStandardItem(str(item.Price))
#             ]
#             for i in row:
#                 i.setEditable(False)
#             self.model.appendRow(row)
#
#     @pyqtSlot()
#     def go_back(self):
#         self.model.removeRows(0, self.model.rowCount())
#         self.parent().setCurrentIndex(0)
#
#     @staticmethod
#     def search(data,text):
#         searchProducts = data
#         if text != "":
#             searchProducts = filter(lambda p: text in p.Name.lower(), data)
#         return searchProducts
#
#     def onSearchChanged(self,text):
#         self.model.removeRows(0, self.model.rowCount())
#
#         searchProducts = MyWindow2.search(self.products,text)
#
#
#         for item in searchProducts:
#             row = [
#                 QStandardItem(str(item.Id)),
#                 QStandardItem(item.Name),
#                 QStandardItem(str(item.Count)),
#                 QStandardItem(str(item.Price))
#             ]
#             for i in row:
#                 i.setEditable(False)
#             self.model.appendRow(row)
#
#
# if __name__ == '__main__':
#     app = QtWidgets.QApplication(sys.argv)
#     window = QtWidgets.QStackedWidget()
#     widget = MyWindow()
#     widget2 = MyWindow2()
#     widget.products.connect(widget2.getProducts)
#     window.addWidget(widget)
#     window.addWidget(widget2)
#     window.show()
#     sys.exit(app.exec_())


###TestPy###

# import datetime
#
# from main import ServerThread, MyWindow, MyWindow2
# from dataclass import Order
# import json
#
# def test_decode_return_true():
#     json = b'{"user":{"productIds":[],"Role":1,"Email":"egor@egor.com","Password":"123123Z#","Name":"Egor","Surname":"Odinczov","X":0,"Birthdate":"1991-02-24T00:00:00","Country":"\\u0420\\u043E\\u0441\\u0441\\u0438\\u044F","Photo":"C:\\\\Users\\\\Admin\\\\Downloads\\\\flag.jpg"},"products":[{"Id":1,"Name":"AK-74M","Price":1000,"Category":{"Id":1,"Name":null},"Count":1,"Url":"C:\\\\Users\\\\Admin\\\\Downloads\\\\flag.jpg"},{"Id":2,"Name":"test","Price":1000,"Count":1,"Category":{"Id":1,"Name":null},"Url":"C:\\\\Users\\\\Admin\\\\Downloads\\\\flag.jpg"}],"date":"2023-11-24T10:11:39.6450943+05:00","id":"d6deda18-57e1-41df-8560-924f403359d0"}'
#     order = ServerThread.decode(json)
#     assert len(order.products) > 0
#
# def test_decode_return_none():
#     json = b'{"user":{"p":"Egor","Surname":"Odinczov","X":0,"Birthdat"1991-02-24T00:\\\\Users\\\\Admin\\\\Downloads\\\\flag.jpg"},"products":[{"Id":1,"Name":"AK-74M","Price":1000,"Category":{"Id":1,"Name":null},"Count":1,"Url":"C:\\\\Users\\\\Admin\\\\Downloads\\\\flag.jpg"},{"Id":2,"Name":"test","Price":1000,"Count":1}],"date":"2023-11-24T10:11:39.6450943+05:00","id":"d6deda18-57e1-41df-8560-924f403359d0"}'
#     order = ServerThread.decode(json)
#     assert order is None
#
# def test_deserialize_result_true():
#     json1 = b'{"user":{"productIds":[],"Role":1,"Email":"egor@egor.com","Password":"123123Z#","Name":"Egor","Surname":"Odinczov","X":0,"Birthdate":"1991-02-24T00:00:00","Country":"\\u0420\\u043E\\u0441\\u0441\\u0438\\u044F","Photo":"C:\\\\Users\\\\Admin\\\\Downloads\\\\flag.jpg"},"products":[{"Id":1,"Name":"AK-74M","Price":1000,"Category":{"Id":1,"Name":null},"Count":1,"Url":"C:\\\\Users\\\\Admin\\\\Downloads\\\\flag.jpg"},{"Id":2,"Name":"test","Price":1000,"Count":1,"Category":{"Id":1,"Name":null},"Url":"C:\\\\Users\\\\Admin\\\\Downloads\\\\flag.jpg"}],"date":"2023-11-24T10:11:39.6450943+05:00","id":"d6deda18-57e1-41df-8560-924f403359d0"}'
#     received_json = json1.decode('utf-8')
#     received_data = json.loads(received_json)
#     result = Order.deserializer(received_data)
#
#     dict_result = result.__dict__
#     dict_result["products"] = [x.__dict__ for x in dict_result["products"]]
#
#     assert isinstance(result, Order) and result.__dict__ == received_data
#
#
# def test_filter_order_return_true():
#     json = b'{"user":{"productIds":[],"Role":1,"Email":"egor@egor.com","Password":"123123Z#","Name":"Egor","Surname":"Odinczov","X":0,"Birthdate":"1991-02-24T00:00:00","Country":"\\u0420\\u043E\\u0441\\u0441\\u0438\\u044F","Photo":"C:\\\\Users\\\\Admin\\\\Downloads\\\\flag.jpg"},"products":[{"Id":1,"Name":"AK-74M","Price":1000,"Category":{"Id":1,"Name":null},"Count":1,"Url":"C:\\\\Users\\\\Admin\\\\Downloads\\\\flag.jpg"},{"Id":2,"Name":"test","Price":1000,"Count":1,"Category":{"Id":1,"Name":null},"Url":"C:\\\\Users\\\\Admin\\\\Downloads\\\\flag.jpg"}],"date":"2023-11-24T10:11:39.6450943+05:00","id":"d6deda18-57e1-41df-8560-924f403359d0"}'
#     order = ServerThread.decode(json)
#     filtered = list(MyWindow.filtered([order], datetime.date(2020, 1, 1)))
#     assert len(filtered) > 0
#
#
# def test_filter_order_return_0():
#     json = b'{"user":{"productIds":[],"Role":1,"Email":"egor@egor.com","Password":"123123Z#","Name":"Egor","Surname":"Odinczov","X":0,"Birthdate":"1991-02-24T00:00:00","Country":"\\u0420\\u043E\\u0441\\u0441\\u0438\\u044F","Photo":"C:\\\\Users\\\\Admin\\\\Downloads\\\\flag.jpg"},"products":[{"Id":1,"Name":"AK-74M","Price":1000,"Category":{"Id":1,"Name":null},"Count":1,"Url":"C:\\\\Users\\\\Admin\\\\Downloads\\\\flag.jpg"},{"Id":2,"Name":"test","Price":1000,"Count":1,"Category":{"Id":1,"Name":null},"Url":"C:\\\\Users\\\\Admin\\\\Downloads\\\\flag.jpg"}],"date":"2023-11-24T10:11:39.6450943+05:00","id":"d6deda18-57e1-41df-8560-924f403359d0"}'
#     order = ServerThread.decode(json)
#     filtered = list(MyWindow.filtered([order], datetime.date(2025, 1, 1)))
#     assert len(filtered) == 0
#
#
# def test_search_order_return_0():
#     json = b'{"user":{"productIds":[],"Role":1,"Email":"egor@egor.com","Password":"123123Z#","Name":"Egor","Surname":"Odinczov","X":0,"Birthdate":"1991-02-24T00:00:00","Country":"\\u0420\\u043E\\u0441\\u0441\\u0438\\u044F","Photo":"C:\\\\Users\\\\Admin\\\\Downloads\\\\flag.jpg"},"products":[{"Id":1,"Name":"AK-74M","Price":1000,"Category":{"Id":1,"Name":null},"Count":1,"Url":"C:\\\\Users\\\\Admin\\\\Downloads\\\\flag.jpg"},{"Id":2,"Name":"test","Price":1000,"Count":1,"Category":{"Id":1,"Name":null},"Url":"C:\\\\Users\\\\Admin\\\\Downloads\\\\flag.jpg"}],"date":"2023-11-24T10:11:39.6450943+05:00","id":"d6deda18-57e1-41df-8560-924f403359d0"}'
#     order = ServerThread.decode(json)
#     filtered = list(MyWindow2.search(order.products, "p"))
#     assert len(filtered) == 0
#
#
# def test_search_order_return_1():
#     json = b'{"user":{"productIds":[],"Role":1,"Email":"egor@egor.com","Password":"123123Z#","Name":"Egor","Surname":"Odinczov","X":0,"Birthdate":"1991-02-24T00:00:00","Country":"\\u0420\\u043E\\u0441\\u0441\\u0438\\u044F","Photo":"C:\\\\Users\\\\Admin\\\\Downloads\\\\flag.jpg"},"products":[{"Id":1,"Name":"AK-74M","Price":1000,"Category":{"Id":1,"Name":null},"Count":1,"Url":"C:\\\\Users\\\\Admin\\\\Downloads\\\\flag.jpg"},{"Id":2,"Name":"test","Price":1000,"Count":1,"Category":{"Id":1,"Name":null},"Url":"C:\\\\Users\\\\Admin\\\\Downloads\\\\flag.jpg"}],"date":"2023-11-24T10:11:39.6450943+05:00","id":"d6deda18-57e1-41df-8560-924f403359d0"}'
#     order = ServerThread.decode(json)
#     filtered = list(MyWindow2.search(order.products, "test"))
#     assert len(filtered) == 1


