from tkinter import *
import tkinter.messagebox as box

allProducts = [
    {'name': 'Яблоко', 'price': 30},
    {'name': 'Банан', 'price': 25},
    {'name': 'Молоко', 'price': 80},
    {'name': 'Хлеб', 'price': 40},
    {'name': 'Сыр', 'price': 150},
    {'name': 'Сок', 'price': 100}
]

selectedProducts = []

win = Tk()
win.title("Attempt 3")
win.geometry("600x400")

text = Label(win, text="Выберите товар:").place(x=50, y=50)
ProductsFrame = Frame(win, height=20).place(x=100, y=50)

for product in allProducts:
    var = IntVar()
    checkBtn = Checkbutton(ProductsFrame, variable=var).pack()
    labelProduct = Label(ProductsFrame, text=f"{product['name']}").pack(padx=20)
    

listbox = Listbox(win, height=10, width=50)
listbox.insert(1, "Элемент 1")
listbox.pack(side="left", padx=[30, 0])

win.mainloop()