from tkinter import *

allProducts = [
    {'name': 'Яблоко', 'price': 30},
    {'name': 'Банан', 'price': 25},
    {'name': 'Молоко', 'price': 80},
    {'name': 'Хлеб', 'price': 40},
    {'name': 'Сыр', 'price': 150},
    {'name': 'Сок', 'price': 100}
]

selectedProducts = []  # (IntVar, name, price)
cart = {}  # name: count

def change_qty(name, delta):
    if name in cart:
        cart[name] += delta
        if cart[name] <= 0:
            del cart[name]
    elif delta > 0:
        cart[name] = 1

    update_cart()

def update_cart():
    for widget in itemsFrame.winfo_children():
        widget.destroy()

    cheq.delete('1.0', END)
    total = 0

    for var, name, price in selectedProducts:
        if var.get():
            if name not in cart:
                cart[name] = 1  # по умолчанию 1, если только выбран

            item_frame = Frame(itemsFrame)
            item_frame.pack(anchor="w", pady=2)

            Label(item_frame, text=f"{name} - {price} тг").pack(side="left", padx=5)
            Button(item_frame, text="-", width=2, command=lambda n=name: change_qty(n, -1)).pack(side="left")
            Label(item_frame, text=str(cart[name]), width=2).pack(side="left")
            Button(item_frame, text="+", width=2, command=lambda n=name: change_qty(n, 1)).pack(side="left")

            total += cart[name] * price
            cheq.insert(END, f"{name} x{cart[name]} = {cart[name]*price} тг\n")

    cheq.insert(END, f"\nИтого: {total} тг")

def download():
    with open("cheque.txt", "w", encoding="utf-8") as f:
        f.write(cheq.get("1.0", END))
    print("Чек сохранён.")

# ---------- UI ----------
win = Tk()
win.title("Attempt 3")
win.geometry("650x450")

Label(win, text="Выберите товар:").place(x=70, y=20)

ProductsFrame = Frame(win)
ProductsFrame.place(x=200, y=10)

row1 = Frame(ProductsFrame)
row1.pack()
row2 = Frame(ProductsFrame)
row2.pack()

for i, product in enumerate(allProducts):
    var = IntVar()
    frame = row1 if i < 3 else row2
    Checkbutton(frame, text=product['name'], variable=var, command=update_cart).pack(side='left', padx=10)
    selectedProducts.append((var, product['name'], product['price']))

# Корзина с кнопками
itemsFrame = Frame(win)
itemsFrame.place(x=50, y=100)

# Чек и кнопка
cheq = Text(win, height=10, width=25)
cheq.place(x=400, y=100)

downloadBtn = Button(win, text="Скачать чек", width=20, command=download)
downloadBtn.place(relx=1.0, rely=1.0, x=-20, y=-20, anchor="se")

win.mainloop()
