from tkinter import *
from tkinter import ttk
from datetime import datetime
import tkinter.messagebox as box

allProducts = [
    {'name': 'Яблоко', 'price': 30},
    {'name': 'Банан', 'price': 25},
    {'name': 'Молоко', 'price': 80},
    {'name': 'Хлеб', 'price': 40},
    {'name': 'Сыр', 'price': 150},
    {'name': 'Сок', 'price': 100},
    {'name': 'Масло', 'price': 120},    
    {'name': 'Кофе', 'price': 200},
    {'name': 'Чай', 'price': 160}
]

selectedProducts = []  
checkbox_map = {}     
cart = {}         
payment = 'cart'

def update_scroll_visibility():
    needs_scroll = canvas.bbox("all")[3] > canvas.winfo_height()
    if needs_scroll:
        scrollbar.place(x=332, y=143, height=245)
    else:
        scrollbar.place_forget()

def on_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))
    update_scroll_visibility()

def change_qty(name, delta):
    if name in cart:
        cart[name] += delta
        if cart[name] <= 0:
            del cart[name]
    elif delta > 0:
        cart[name] = 1
    cheq.config(state=NORMAL)
    update_cart()

def on_entry_click(event):
    if search_entry.get() == " 🔍 Поиск...":
        search_entry.delete(0, END)
        search_entry.config(fg='#e0e0e0')

def on_focus_out(event):
    if search_entry.get() == "":
        search_entry.insert(0, " 🔍 Поиск...")
        search_entry.config(fg='grey')

def delete(n):
    for var, name, price in selectedProducts:
        if name == n:
            var.set(0)  # Сбрасываем количество товара
            break
    update_cart()

def update_cart():
    for widget in itemsFrame.winfo_children():
        widget.destroy()

    cheq.config(state=NORMAL)
    cheq.delete('1.0', END)
    total = 0

    for var, name, price in selectedProducts:
        if var.get():
            if name not in cart:
                cart[name] = 1
        else:
            if name in cart:
                del cart[name]
            continue

        item_frame = Frame(itemsFrame, bg="#181818")
        item_frame.pack(anchor="w", pady=2)

        Label(item_frame, bg="#181818", fg="#e0e0e0", text=f"{name} - {price} тг").pack(side="left", padx=5)
        Button(item_frame, text="-", command=lambda n=name: change_qty(n, -1), relief="flat", width=3, height=1, bg="#2a2a2a", fg="#e0e0e0").pack(side="left", padx=5)
        Label(item_frame, bg="#181818", fg="#e0e0e0", text=str(cart[name]), width=2).pack(side="left", padx=5)
        Button(item_frame, text="+", command=lambda n=name: change_qty(n, 1), relief="flat", width=3, height=1, bg="#2a2a2a", fg="#e0e0e0").pack(side="left", padx=5)
        Button(item_frame, text="отмена", command=lambda: delete(name), relief="flat", width=5, height=1, bg="#2a2a2a", fg="#e0e0e0").pack(side="left", padx=5)

        total += cart[name] * price
        cheq.config(state=NORMAL)
        cheq.insert(END, f"{name} x{cart[name]} = {cart[name]*price} тг\n")
        cheq.config(state=DISABLED)
        
    if total != 0:
        global totality
        totality = 0
        totality += total
        cheq.config(state=NORMAL)
        cheq.insert(END, f"\nИтого: {total} тг")
        cheq.config(state=DISABLED)
    else:
        cheq.config(state=NORMAL)
        cheq.insert(END, "")
        cheq.config(state=DISABLED)

    itemsFrame.bind("<Configure>", on_configure)

def download():
    if payment == 'cash':
        cheq.config(state=NORMAL)
        cheq.insert(END, "\n\nСпособ оплаты: наличные")
        cheq.insert(END, f"\n\nВнесенная сумма: {num.get()}")
        cheq.insert(END, f"\n\nСдача: {num_change}")
    elif payment == 'cart':
        cheq.config(state=NORMAL)
        cheq.insert(END, "\n\nСпособ оплаты: карта")
    
    cheque = cheq.get("1.0", END)
    box.showinfo("Оплата", message="Оплата прошла успешно")
    with open("cheque.txt", "w", encoding="utf-8") as f:
        f.write("Чек от: " + datetime.now().strftime("%d.%m.%Y %H:%M:%S") + "\n\n")
        f.write(cheque)
        
    print("Чек сохранён.")
    
    clear_cart()
    MainWindow()

def clear_cart():
    cheq.config(state=NORMAL)
    cart.clear()
    for var, _, _ in selectedProducts:
        var.set(0)
    update_cart()

# Поиск по товарам
def on_search(*args):
    query = search_var.get().lower()
    listbox.delete(0, END)
    if not query.strip():
        listbox.place_forget()
        return
    matches = [p['name'] for p in allProducts if query in p['name'].lower()]
    if matches:
        for name in matches:
            listbox.insert(END, name)
        listbox.place(x=50, y=85)
        listbox.lift()
    else:
        listbox.place_forget()

def on_select(event):
    global listbox
    selection = listbox.get(ACTIVE)
    if selection not in checkbox_map:
        # Добавляем только если не было ранее
        product = next((p for p in allProducts if p['name'] == selection), None)
        if product:
            var = IntVar(value=1)  # сразу добавляем
            selectedProducts.append((var, product['name'], product['price']))
            checkbox_map[product['name']] = var
    else:
        checkbox_map[selection].set(1)
    update_cart()
    listbox.place_forget()
    search_var.set("")


def update_change(*args):
    if num.get() == "":
        n = ""
    else:
        n =  int(num.get())
    
    if n == "":
        change.config(text="Сдача: 0")
    else:
        global num_change
        num_change = n - totality
        change.config(text=f"Сдача: {num_change}")
        
def MainWindow():
    mainFrame.place(relwidth=1, relheight=1)
    PaymentWinFrame.pack_forget()
    buyWinFrame.pack_forget()

def BuyWindow():
    mainFrame.place_forget()
    PaymentWinFrame.pack_forget()
    buyWinFrame.pack()
    
def PaymentWindow():
    global payment
    payment = 'cash'
    mainFrame.place_forget()
    PaymentWinFrame.pack()
    buyWinFrame.pack_forget()

# ---------- UI ----------
win = Tk()
win.title("Simulator Cash Register")
win.geometry("700x500")
win.config(bg="#1E1E1E")

style = ttk.Style()
style.theme_use("clam")  # Обязательно, чтобы стиль применился

style.configure("Vertical.TScrollbar",
                gripcount=0,
                background="#3A3A3A",     # Цвет ползунка
                darkcolor="#3A3A3A",
                lightcolor="#3A3A3A",
                troughcolor="#181818",    # Цвет фона дорожки
                bordercolor="#181818",
                arrowcolor="#E0E0E0")     # Цвет стрелок

style.configure("TButton",
                font=("Segoe UI", 9),  # Мелкий шрифт
                padding=6,             # Уменьшаем внутренние отступы
                relief="flat",         # Плоская кнопка (без рамки)
                background="#2a2a2a",  # Темный фон
                foreground="#e0e0e0",  # Светлый текст
                borderwidth=0)        # Убираем рамку

mainFrame = Frame(win, bg="#1E1E1E")

listbox = Listbox(mainFrame, height=5, width=20, border=0, bg="#181818", fg="#e0e0e0", highlightthickness=1, highlightbackground="#2a2a2a", highlightcolor="#2a2a2a")
listbox.bind("<<ListboxSelect>>", on_select)

# Поисковая строка
search_var = StringVar()
search_var.trace_add("write", on_search)

search_entry = Entry(mainFrame, textvariable=search_var, width=65, bg="#181818", fg="grey", border=0,  highlightthickness=1, highlightbackground="#2a2a2a", highlightcolor="#2a2a2a", insertbackground="#e0e0e0")
search_entry.insert(0, " 🔍 Поиск...")
search_entry.bind('<FocusIn>', on_entry_click)
search_entry.bind('<FocusOut>', on_focus_out)
search_entry.place(x=50, y=50, height=35)

# --- Скроллируемый фрейм для корзины ---
canvas = Canvas(mainFrame, width=300, height=250, bg="#181818", highlightthickness=1, highlightbackground="#2a2a2a", highlightcolor="#2a2a2a")
scrollbar = ttk.Scrollbar(mainFrame, orient="vertical", style="Vertical.TScrollbar", command=canvas.yview)
scrollable_frame = Frame(canvas, bg="#181818")

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

listText = Label(mainFrame, text="Список товаров:", bg="#1E1E1E", fg="#E0E0E0")
listText.place(x=60, y=110)
canvas.place(x=50, y=140)

itemsFrame = scrollable_frame  # переопределяем имя для update_cart()

# Чек и кнопки
cheqText = Label(mainFrame, text="Чек:", bg="#1E1E1E", fg="#E0E0E0")
cheqText.place(x=410, y=120)

cheq = Text(mainFrame, height=12, width=25, bg="#181818", fg="#e0e0e0", border=0, highlightthickness=1, highlightbackground="#2a2a2a", highlightcolor="#2a2a2a", insertbackground="#e0e0e0")
cheq.config(state=DISABLED)
cheq.place(x=400, y=150)

def buy():
    if not cart:
        box.showerror("Корзина пуста", "Вы не выбрали товары для покупки.")
        return
    cheque_text.config(state=NORMAL)
    cheque_text.delete(1.0, END)
    cheque_text.insert(END, cheq.get("1.0", END))
    cheque_text.config(state=DISABLED)  # Make it read-only

    BuyWindow()
    
    # downloadBtn = Button(win, text="Оплатить", width=20, bg="#333b4f", fg="#E0E0E0", activebackground="#4a5672", activeforeground="#ffffff", command=download)
    # downloadBtn.place(relx=1.0, rely=1.0, x=-20, y=-20, anchor="se")

buyBtn = Button(mainFrame, text="Оплатить", width=20, bg="#333b4f", fg="#E0E0E0", activebackground="#4a5672", activeforeground="#ffffff", command=buy)
buyBtn.place(relx=1.0, rely=1.0, x=-20, y=-20, anchor="se")

clearBtn = Button(mainFrame, text="Очистить", width=20, bg="#333b4f", fg  ="#E0E0E0", activebackground="#4a5672", activeforeground="#ffffff", command=clear_cart)
clearBtn.place(relx=1.0, rely=1.0, x=-220, y=-20, anchor="se")

# ---------- Buy window ----------

buyWinFrame = Frame(win, bg="#1E1E1E")

Label(buyWinFrame, text="Способ оплаты", bg="#1E1E1E", fg="#E0E0E0", font=("Segoe UI", 12)).pack(pady=20)

cheque_text = Text(buyWinFrame, height=10, width=40, bg="#181818", fg="#e0e0e0", border=0, highlightthickness=1, highlightbackground="#2a2a2a", insertbackground="#e0e0e0")
cheque_text.pack(pady=10)


Button(buyWinFrame, text="Оплата картой", width=20, command=download, bg="#333b4f", fg="#E0E0E0", activebackground="#4a5672").pack(pady=5)

Button(buyWinFrame, text="Оплата наличными", width=20, command=PaymentWindow, bg="#333b4f", fg="#E0E0E0", activebackground="#4a5672").pack(pady=5)

Button(buyWinFrame, text="Закрыть", width=20, command=MainWindow, bg="#333b4f", fg="#E0E0E0", activebackground="#4a5672").pack()


# ---------- Cash payment ----------

PaymentWinFrame = Frame(win, bg="#1E1E1E")

Label(PaymentWinFrame, text="Введите купюру/копейку данную вам:", bg="#1E1E1E", fg="#E0E0E0").pack(pady=50)
        
num = StringVar()
num.trace_add("write", update_change)

cashEntry = Entry(PaymentWinFrame, textvariable=num, bg="#181818", fg="#fff", border=0,  highlightthickness=1, highlightbackground="#2a2a2a", highlightcolor="#2a2a2a", insertbackground="#fff")
cashEntry.pack(pady=10)

change = Label(PaymentWinFrame, text="Сдача: 0", bg="#1E1E1E", fg="#E0E0E0")
change.pack(pady=10)

Button(PaymentWinFrame, text="Зафиксировать", width=20, command=download, bg="#333b4f", fg="#E0E0E0", activebackground="#4a5672", activeforeground="#ffffff").pack(pady=10)

Button(PaymentWinFrame, text="Вернуться", width=20, command=BuyWindow, bg="#333b4f", fg="#E0E0E0", activebackground="#4a5672", activeforeground="#ffffff").pack(pady=10)


MainWindow()
win.mainloop()
