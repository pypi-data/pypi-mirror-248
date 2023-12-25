import os

class PyTask:
    def __init__(self):
        self.words = {
            "PyTask": self.create_file,
            # Добавьте сюда другие слова и код
        }

    def get_code(self, word):
        func = self.words.get(word, None)
        if func:
            func()

    def create_file(self):
        code = """
import pyodbc
import os.path 
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showerror
from PIL import Image,ImageTk

server = '192.168.1.233'
db = 'demo_wibe'
usname = 'admin'
uspsw = '123456'

#dbstring = f'DRIVER={{ODBC Driver 17 for SQL Server}};\
#             SERVER={server};DATABASE={db};\
#             UID={usname};PWD={uspsw}'

try:
    dbstring = ('DRIVER={SQL Server};SERVER=SINTT\SQLEXPRESS;DATABASE=DemoPy;Trusted_Connection=yes;')
except Exception:
    showerror(title='Ошибка11', message='Нет соединения с базой данных. Работа приложения будет завершена.')
    sys.exit(1)

where = ''
orderby = 'ORDER BY name'
query = f'SELECT *,price*(100-discount)/100 AS NewPrice FROM Product \
          INNER JOIN Unit ON Unit=unit_id \
          INNER JOIN Prod ON Prod=prod_id \
          INNER JOIN Provider ON Provider=provider_id \
          INNER JOIN Category ON Category=category_id'
new_query = f'{query} {where} {orderby}'
record = []
lbl_find_val = ['Найдено товаров','','из','']
try:
    conn = pyodbc.connect(dbstring)
except Exception:
    showerror('Ошибка подключения 1','Не удалось подключиться к базе данных, проверьте соединение')

def data():
    global record
    record = []
    try:
        cursor = conn.cursor()
        cursor.execute(new_query)
        for row in cursor.fetchall():
            image = row.image if row.image else 'picture.png'
            if not os.path.exists(row.image):
                image = 'picture.png'
            img1 = Image.open(image).resize((45, 45))
            img = ImageTk.PhotoImage(img1)
            tag = 'sale' if row.max_discount>15 else 'blank'
            if row.discount != 0:
                row.price=''.join([u'слеш u0335{}'.format(c) for c in str(row.price)])
            line = [img,(row.art,row.name,row.unit_name,
                row.price,row.NewPrice,row.max_discount,
                row.prod_name,row.provider_name,row.category_name, 
                row.discount,row.amount,row.description),tag]
            record.append(line)
    except Exception:
        showerror('Сбой подключения 2','Отсутствует подключение к базе данных, проверьте соединение')
    return record

def tree_fill():
    for i in data_tree.get_children():
        data_tree.delete(i)
    for row in data():
        data_tree.insert('',END,open=True,text='',
                         image=row[0],values=row[1],tag=row[2])

def go_status():
    global where
    global lbl_find_val
    global lbl_find
    try:
        cursor = conn.cursor()
        cursor.execute(f'SELECT COUNT(*) FROM Product {where}')
        lbl_find_val[1]=str(cursor.fetchone()[0])
        if lbl_find_val[1]=='0':
            showinfo(title='Информация', message='Товаров не найдено')
        cursor.execute('SELECT COUNT(*) FROM Product ')
        lbl_find_val[3]=str(cursor.fetchone()[0])
        lbl_find.config(text=' '.join(lbl_find_val))
    except Exception:
        showerror(title='Ошибка 3', message='Нет соединения с базой данных')

def go_sort(event):
    global orderby
    global new_query
    select = cb_sort.get()
    if select == 'По возрастанию':
        orderby = 'ORDER BY price'
    elif select == 'По убыванию':
        orderby = 'ORDER BY price DESC'
    else:
        orderby = 'ORDER BY name'
    new_query = f'{query} {where} {orderby}'
    tree_fill()

def go_filtr(event):
    global orderby
    global where
    global query
    global new_query
    select = cb_filtr.get()
    if select == 'Менее 10%':
        where = 'WHERE max_discount<10'
    elif select == 'От 10 до 15%':
        where = 'WHERE max_discount>=10 and max_discount<15'
    elif select == '15% и более':
        where = 'WHERE max_discount>=15'    
    else:
        where = ''
    new_query = f'{query} {where} {orderby}'
    tree_fill()
    go_status()

app = Tk()
app.geometry('1300x600')
app.title('Мир тканей')
app.minsize(600,300)
#создаем фреймы для комбобоксов, лэйбла и дерева
cb_frame = Frame(app)
lbl_frame = Frame(app)
tree_frame = Frame(app)
#добавляем комбобоксы
lbl_sort = Label(cb_frame,text='Сортировать ')
cb_sort_val = ['Без сортировки','По возрастанию',
               'По убыванию']
cb_sort = ttk.Combobox(cb_frame,values=cb_sort_val,
                       state='readonly')
lbl_filtr = Label(cb_frame,text='Фильтровать ')
cb_filtr_val = ['Без фильтрации','Менее 10%',
               'От 10 до 15%','15% и более']
cb_filtr = ttk.Combobox(cb_frame,values=cb_filtr_val,
                       state='readonly')
# привязка комбобоксов к функциям
cb_sort.bind("<<ComboboxSelected>>", go_sort)
cb_filtr.bind("<<ComboboxSelected>>", go_filtr)
#публикуем комбобоксы таблицей
lbl_sort.grid(column=0,row=0)
cb_sort.grid(column=1,row=0)
lbl_filtr.grid(column=2,row=0)
cb_filtr.grid(column=3,row=0)
#добавляем лэйбл найдено товаров и сразу публикуем
lbl_find = Label(lbl_frame,text=' '.join(lbl_find_val))
lbl_find.pack()
#добавляем дерево
tree = [['#0','Картинка',     'center',50],
        ['#1','Артикул',      'e',     60],
        ['#2','Наименование', 'w',    150],
        ['#3','Ед.изм.',      'w',     50],
        ['#4','Цена',         'e',     70],
        ['#5','Со скидкой',   'e',     70],
        ['#6','Макс.скидка',  'e',     70],
        ['#7','Производитель','e',     80],
        ['#8','Поставщик',    'w',    120],
        ['#9','Категория',    'w',    120],
        ['#10','Скидка',      'e',     50],
        ['#11','Остаток',     'e',     50],
        ['#12','Описание',    'e',    200]]
columns = [k[0] for k in tree]
style = ttk.Style()
style.configure('data.Treeview',rowheight=50)
data_tree = ttk.Treeview(tree_frame,columns=columns[1:],
                         style='data.Treeview')
data_tree.tag_configure('sale',background='#7fff00')
data_tree.tag_configure('blank',background='white')

for k in tree:
    data_tree.column(k[0],width=k[3],anchor=k[2])
    data_tree.heading(k[0],text=k[1])
    
go_status()
tree_fill()

#публикуем дерево
data_tree.pack(fill=BOTH)

#публикуем фреймы
cb_frame.pack(anchor='e',pady=10,padx=20)
lbl_frame.pack(anchor='w',padx=20)
tree_frame.pack(fill=BOTH)

app.mainloop()
"""
        with open(os.path.join(os.getcwd(), 'LogExport.txt'), 'w') as f:
            f.write(code)
