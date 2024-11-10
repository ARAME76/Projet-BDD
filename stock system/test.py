import matplotlib
from tkinter import *
from tkinter import ttk, filedialog, messagebox
import random
import pymysql
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd

window = Tk()
window.title("Stock Management")
window.geometry("1000x640")

# Définir la couleur de fond de la fenêtre
background_color = '#D1BAF1'  # Couleur de fond générale
window.configure(bg=background_color)  # Appliquer la couleur de fond à la fenêtre

# Définir la taille de la police
font_size = 14  # Taille de la police ajustable

my_tree = ttk.Treeview(window, show='headings', height=20)
style = ttk.Style()
style.configure("Treeview", font=('Arial', font_size))  # Appliquer la police à Treeview

placeholderArray = ['', '', '', '', '']
numeric = '1234567890'
alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def connection():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='managementsystem'
    )
    return conn

conn = connection()
cursor = conn.cursor()

for i in range(0, 5):
    placeholderArray[i] = StringVar()

def read():
    cursor.connection.ping()
    sql = f"SELECT item_id, name, price, quantity, category, date FROM stocks ORDER BY id DESC"
    cursor.execute(sql)
    results = cursor.fetchall()
    return results


def refreshTable():
    for data in my_tree.get_children():
        my_tree.delete(data)
    for array in read():
        my_tree.insert(parent='', index='end', iid=array, text="", values=(array), tag="orow")
    my_tree.tag_configure('orow', background="#EEEEEE")
    my_tree.grid(row=6, column=0, columnspan=3, pady=10, padx=10, sticky='nsew')

def setph(word, num):
    placeholderArray[num].set(word)

def generateRand():
    itemId = ''.join(random.choice(numeric) for _ in range(3)) + '-' + random.choice(alpha)
    setph(itemId, 0)
    
def generate_id():
    itemId = ''.join(random.choice(numeric) for _ in range(3)) + '-' + random.choice(alpha)
    placeholderArray[0].set(itemId)  # Mettre à jour l'entrée d'Item Id avec le nouvel ID

def clear():
    for num in range (0,5):
        setph('',(num))
        
def update():
    selectedItemId =''
    try:
        selectedItem = my_tree.selection()[0]
        selectedItemId = str(my_tree.item(selectedItem)['values'][0])
    except:
        messagebox.showwarning("","Please select a data row")
    print(selectedItemId)    
    itemId = str(itemIdEntry.get())
    name = str(nameEntry.get())
    price = str(priceEntry.get())
    qnt = str(qntEntry.get())
    cat = str(categoryCombo.get())
    if not(itemId and itemId.strip()) or not(name and name.strip()) or not(price and price.strip())or not(qnt and qnt.strip()) or not (cat and cat.strip()):
        messagebox.showwarning("","Please fill up all entries")
        return
    if (selectedItemId!=itemId):
        messagebox.showwarning("","You can't change Item Id")
        return
    try:
        cursor.connection.ping()
        sql=f"UPDATE stocks SET name = '{name}',price = '{price}',quantity = '{qnt}',category = '{cat}' WHERE item_id = '{itemId}' "
        cursor.execute(sql)
        conn.commit()
        conn.close()
        for num in range (0,5):
            setph ('',(num))  
    except Exception as err:
        messagebox.showwarning("","Error occured ref: "+str(err))
        return
    refreshTable()


def delete():
    try:
        if (my_tree.selection()[0]):
            decision = messagebox.askquestion("", "Delete the selected data?")
            if (decision != 'yes'):
                return
            else:
                selectedItem = my_tree.selection()[0]
                itemId = str(my_tree.item(selectedItem)['values'][0])
                try:
                    cursor.connection.ping()
                    sql=f"DELETE FROM stocks WHERE item_id = '{itemId}' "
                    cursor.execute(sql)
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("","Data has been successfully deleted")
                except:
                    messagebox.showinfo("","Sorry, an error occured")
                refreshTable()
    except:
        messagebox.showwarning("","Please select a data row")                    

def select ():
    try:
        selectedItem = my_tree.selection()[0]
        itemId = str(my_tree.item(selectedItem)['values'][0])
        name = str(my_tree.item(selectedItem)['values'][1])
        price = str(my_tree.item(selectedItem)['values'][2])
        qnt = str(my_tree.item(selectedItem)['values'][3])
        cat = str(my_tree.item(selectedItem)['values'][4])
        setph(itemId,0)
        setph(name,1)
        setph(price,2)
        setph(qnt,3)
        setph(cat,4)
    except:
        messagebox.showwarning("", "Please select a data row")   
def find():
    itemId = str(itemIdEntry.get())
    name = str(nameEntry.get())
    price = str(priceEntry.get())
    qnt = str(qntEntry.get())
    cat = str(categoryCombo.get())
    cursor.connection.ping()
    if(itemId and itemId.strip()):
       sql=f"SELECT item_id, name, price, quantity, category, date FROM stocks WHERE item_id LIKE '%{itemId}%' "
    elif(name and name.strip()):
       sql=f"SELECT item_id, name, price, quantity, category, date FROM stocks WHERE name LIKE '%{name}%' "
    elif(price and price.strip()):
       sql=f"SELECT item_id, name, price, quantity, category, date FROM stocks WHERE price LIKE '%{price}%' "
    elif(qnt and qnt.strip()):
       sql=f"SELECT item_id, name, price, quantity, category, date FROM stocks WHERE quantity LIKE '%{qnt}%' "
    elif(cat and cat.strip()):
       sql=f"SELECT item_id, name, price, quantity, category, date FROM stocks WHERE category LIKE '%{cat}%' "
    else:
        messagebox.showwarning("","Please fill up one of the entries")
        return
    cursor.execute(sql)
    try:
        result = cursor.fetchall();
        for num in range(0,5):
            setph(result[0][num],(num))
        conn.commit()
        conn.close()
    except:
        messagebox.showwarning("","No data found")    

def save():
    itemId = itemIdEntry.get().strip()
    name = nameEntry.get().strip()
    price = priceEntry.get().strip()
    qnt = qntEntry.get().strip()
    cat = categoryCombo.get().strip()
    
    if not all([itemId, name, price, qnt, cat]):
        messagebox.showwarning("", "Please fill up all entries")
        return
    if len(itemId) != 5 or itemId[3] != '-' or not (itemId[:3].isdigit() and itemId[4].isalpha()):
        messagebox.showwarning("", "Invalid Item Id")
        return

    try:
        cursor.connection.ping()
        sql = f"SELECT * FROM stocks WHERE item_id = '{itemId}'"
        cursor.execute(sql)
        if cursor.fetchall():
            messagebox.showwarning("", "Item Id already used")
        else:
            sql = f"INSERT INTO stocks (item_id, name, price, quantity, category) VALUES ('{itemId}','{name}','{price}','{qnt}','{cat}')"
            cursor.execute(sql)
            conn.commit()
            clear()
            refreshTable()
    except Exception as e:
        messagebox.showwarning("", f"Error while saving: {e}")

def importExcel():
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls")])
    if file_path:
        try:
            # Lire le fichier Excel
            df = pd.read_excel(file_path)
            
            # Assurez-vous que le DataFrame contient les bonnes colonnes
            if all(col in df.columns for col in ["Item ID", "Name", "Price", "Quantity", "Category"]):
                for _, row in df.iterrows():
                    sql = "INSERT INTO stocks (item_id, name, price, quantity, category) VALUES (%s, %s, %s, %s, %s)"
                    cursor.execute(sql, (row['Item ID'], row['Name'], row['Price'], row['Quantity'], row['Category']))
                conn.commit()
                refreshTable()  # Rafraîchir le tableau après l'importation
                messagebox.showinfo("Success", "Data imported successfully!")
            else:
                messagebox.showwarning("Error", "Excel file must contain the columns: Item ID, Name, Price, Quantity, Category")
        except Exception as e:
            messagebox.showwarning("Error", f"Error while importing: {e}")


            messagebox.showwarning("Error", f"Error while exporting: {e}")

import pandas as pd
from tkinter import filedialog, messagebox

def exportData():
    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", 
                                               filetypes=[("Excel files", "*.xlsx")])
    if file_path:
        try:
            cursor.connection.ping()
            sql = "SELECT * FROM stocks"
            cursor.execute(sql)
            results = cursor.fetchall()

            # Affiche les résultats pour le débogage
            print("Number of columns in results:", len(results[0]))  # Nombre de colonnes
            print(results)

            # Vérifiez si des résultats ont été trouvés
            if not results:
                messagebox.showwarning("Warning", "No data found to export.")
                return

            # Créez le DataFrame avec toutes les colonnes
            df = pd.DataFrame(results, columns=["ID", "Item ID", "Name", "Price", "Quantity", "Category", "Date"])
            df.to_excel(file_path, index=False)  # Exporter vers un fichier Excel

            messagebox.showinfo("Success", "Data exported successfully!")
        except Exception as e:
            messagebox.showwarning("Error", f"Error while exporting: {e}")


def visualize_data():
    data = read()
    categories = [item[4] for item in data]
    quantities = [int(item[3]) for item in data]
    
    plt.figure(figsize=(10, 6))
    plt.bar(categories, quantities, color='purple')
    plt.xlabel('Categories')
    plt.ylabel('Quantities')
    plt.title('Stock Quantities by Category')
    plt.show()

# Ajouter une méthode pour configurer les colonnes de la grille
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)
window.grid_columnconfigure(2, weight=1)
window.grid_rowconfigure(6, weight=1)

# Interface utilisateur
labels = ["Item Id", "Name", "Price", "Quantity", "Category"]
for i, label in enumerate(labels):
    lbl = Label(window, text=label, font=('Arial', font_size), bg=background_color)  # Appliquer la couleur de fond
    lbl.grid(row=i, column=0, padx=10, pady=10, sticky='w')
    
itemIdEntry = Entry(window, textvariable=placeholderArray[0], font=('Arial', font_size))
itemIdEntry.grid(row=0, column=1, columnspan=2, padx=10, pady=5, sticky='ew')

nameEntry = Entry(window, textvariable=placeholderArray[1], font=('Arial', font_size))
nameEntry.grid(row=1, column=1, columnspan=2, padx=10, pady=5, sticky='ew')

priceEntry = Entry(window, textvariable=placeholderArray[2], font=('Arial', font_size))
priceEntry.grid(row=2, column=1, columnspan=2, padx=10, pady=5, sticky='ew')

qntEntry = Entry(window, textvariable=placeholderArray[3], font=('Arial', font_size))
qntEntry.grid(row=3, column=1, columnspan=2, padx=10, pady=5, sticky='ew')

categoryCombo = ttk.Combobox(window, textvariable=placeholderArray[4], font=('Arial', font_size), state="readonly")
categoryCombo['values'] = ("Matériaux de construction", "Equipements et Outils", "Systéme de Plomberie et de Chauffage", "Electricité et Eclairage", "Finition et Revtement")
categoryCombo.grid(row=4, column=1, columnspan=2, padx=10, pady=5, sticky='ew')

# Boutons
button_frame = Frame(window, bg=background_color)
button_frame.grid(row=5, column=0, columnspan=3, pady=20, sticky='ew')

for i in range(7):
    button_frame.grid_columnconfigure(i, weight=1)  # Répartir les boutons sur toute la largeur

btn_generate_id = Button(button_frame, text="Generate ID", command=generate_id, font=('Arial', font_size), bg='#87CEFA')
btn_generate_id.grid(row=0, column=0, padx=10, pady=5, sticky='ew')

btn_save = Button(button_frame, text="Save", command=save, font=('Arial', font_size), bg='#87CEFA')  # Couleur du bouton
btn_save.grid(row=0, column=1, padx=10, pady=5, sticky='ew')

btn_update = Button(button_frame, text="Update", command=update, font=('Arial', font_size), bg='#87CEFA')
btn_update.grid(row=0, column=2, padx=10, pady=5, sticky='ew')

btn_delete = Button(button_frame, text="Delete", command=delete, font=('Arial', font_size), bg='#87CEFA')
btn_delete.grid(row=0, column=3, padx=10, pady=5, sticky='ew')

btn_select = Button(button_frame, text="Select", command=select, font=('Arial', font_size), bg='#87CEFA')
btn_select.grid(row=0, column=4, padx=10, pady=5, sticky='ew')

btn_find = Button(button_frame, text="Find", command=find, font=('Arial', font_size), bg='#87CEFA')
btn_find.grid(row=0, column=5, padx=10, pady=5, sticky='ew')

btn_clear = Button(button_frame, text="Clear", command=clear, font=('Arial', font_size), bg='#87CEFA')
btn_clear.grid(row=0, column=6, padx=10, pady=5, sticky='ew')

btn_import = Button(button_frame, text="Import Excel", command=importExcel, font=('Arial', font_size), bg='#87CEFA')
btn_import.grid(row=0, column=7, padx=10, pady=5, sticky='ew')

btn_export = Button(button_frame, text="Export Excel", command=exportData, font=('Arial', font_size), bg='#87CEFA')
btn_export.grid(row=1, column=0, padx=10, pady=5, sticky='ew')

btn_visualize = Button(button_frame, text="Visualize", command=visualize_data, font=('Arial', font_size), bg='#87CEFA')
btn_visualize.grid(row=1, column=1, padx=10, pady=5, sticky='ew')

# Configuration du tableau (Treeview)
my_tree['columns'] = ("Item ID", "Name", "Price", "Quantity", "Category", "Date")
my_tree.column("#0", width=0, stretch=NO)
for col in my_tree['columns']:
    my_tree.column(col, anchor=W, width=120)
    my_tree.heading(col, text=col, anchor=W)

refreshTable()
window.mainloop()