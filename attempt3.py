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


def log():
    listbox.delete(0, END)  
    cheq.delete('1.0', END) 
    total = 0
    for var, name, price in selectedProducts:
        if var.get():
            listbox.insert(END, f"{name:<10} {price} тг    [-] 1 [+]")
            cheq.insert(END, f"{name}: {price} тг\n")
            total += price
    cheq.insert(END, f"\nИтого: {total} тг")
    

win = Tk()
win.title("Attempt 3")
win.geometry("600x400")

text = Label(win, text="Выберите товар:")
text.place(x=70, y=70)
ProductsFrame = Frame(win, height=20)
ProductsFrame.place(x=250, y=40)


row1 = Frame(ProductsFrame)
row1.pack()
row2 = Frame(ProductsFrame)
row2.pack(side='left')

productCount = 0
for i, product in enumerate(allProducts):
    var = IntVar()
    frame = row1 if i < 3 else row2
    Checkbutton(frame, text=product['name'], variable=var, command=log).pack(side='left', padx=10)
    selectedProducts.append((var, product['name'], product['price']))
    

frameForWin = Frame(win)
frameForWin.place(x=50, y=150)

listbox = Listbox(frameForWin, height=10, width=50)
listbox.pack(side="left")

def download():
    with open("cheque.txt", "w", encoding="utf-8") as f:
        f.write(cheq.get("1.0", END))
    print("Чек сохранён.")

cheq = Text(frameForWin, height=12, width=20)
cheq.pack(side="right", padx=[30, 0])
downloadBtn = Button(frameForWin, text="Скачать чек", width=10, command=download)
downloadBtn.place(relx=1.0, rely=1.0, anchor="se")

win.mainloop()