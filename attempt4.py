from tkinter import *
from tkinter import ttk
from datetime import datetime

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
    update_cart()

def on_entry_click(event):
    if search_entry.get() == " 🔍 Поиск...":
        search_entry.delete(0, END)
        search_entry.config(fg='#e0e0e0')

def on_focus_out(event):
    if search_entry.get() == "":
        search_entry.insert(0, " 🔍 Поиск...")
        search_entry.config(fg='grey')

def update_cart():
    for widget in itemsFrame.winfo_children():
        widget.destroy()

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

        total += cart[name] * price
        cheq.insert(END, f"{name} x{cart[name]} = {cart[name]*price} тг\n")
    if total != 0:
        cheq.insert(END, f"\nИтого: {total} тг")
    else:
        cheq.insert(END, "")
        
    itemsFrame.bind("<Configure>", on_configure)

def download():
    with open("cheque.txt", "w", encoding="utf-8") as f:
        f.write("Чек от: " + datetime.now().strftime("%d.%m.%Y %H:%M:%S") + "\n\n")
        f.write(cheq.get("1.0", END))
    print("Чек сохранён.")

def clear_cart():
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

# ---------- UI ----------
win = Tk()
win.title("Attempt 4")
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

listbox = Listbox(win, height=5, width=20, border=0, bg="#181818", fg="#e0e0e0", highlightthickness=1, highlightbackground="#2a2a2a", highlightcolor="#2a2a2a")
listbox.bind("<<ListboxSelect>>", on_select)

# Поисковая строка
search_var = StringVar()
search_var.trace_add("write", on_search)

search_entry = Entry(win, textvariable=search_var, width=65, bg="#181818", fg="grey", border=0,  highlightthickness=1, highlightbackground="#2a2a2a", highlightcolor="#2a2a2a", insertbackground="#e0e0e0")
search_entry.insert(0, " 🔍 Поиск...")
search_entry.bind('<FocusIn>', on_entry_click)
search_entry.bind('<FocusOut>', on_focus_out)
search_entry.place(x=50, y=50, height=35)

# --- Скроллируемый фрейм для корзины ---
canvas = Canvas(win, width=300, height=250, bg="#181818", highlightthickness=1, highlightbackground="#2a2a2a", highlightcolor="#2a2a2a")
scrollbar = ttk.Scrollbar(win, orient="vertical", style="Vertical.TScrollbar", command=canvas.yview)
scrollable_frame = Frame(canvas, bg="#181818")

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

Label(win, text="Список товаров:", bg="#1E1E1E", fg="#E0E0E0").place(x=60, y=110)
canvas.place(x=50, y=140)

itemsFrame = scrollable_frame  # переопределяем имя для update_cart()

# Чек и кнопки
Label(win, text="Чек:", bg="#1E1E1E", fg="#E0E0E0").place(x=410, y=120)

cheq = Text(win, height=12, width=25, bg="#181818", fg="#e0e0e0", border=0, highlightthickness=1, highlightbackground="#2a2a2a", highlightcolor="#2a2a2a", insertbackground="#e0e0e0")
cheq.place(x=400, y=150)

downloadBtn = Button(win, text="Скачать чек", width=20, bg="#333b4f", fg="#E0E0E0", activebackground="#4a5672", activeforeground="#ffffff", command=download)
downloadBtn.place(relx=1.0, rely=1.0, x=-20, y=-20, anchor="se")

clearBtn = Button(win, text="Очистить", width=20, bg="#333b4f", fg  ="#E0E0E0", activebackground="#4a5672", activeforeground="#ffffff", command=clear_cart)
clearBtn.place(relx=1.0, rely=1.0, x=-220, y=-20, anchor="se")

win.mainloop()
