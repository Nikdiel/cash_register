from tkinter import *
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

selectedProducts = []  # (IntVar, name, price)
checkbox_map = {}      # name: IntVar
cart = {}              # name: count

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
                cart[name] = 1
        else:
            if name in cart:
                del cart[name]
            continue

        item_frame = Frame(itemsFrame, bg='white')
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
        listbox.place(x=200, y=70)
    else:
        listbox.place_forget()

def on_select(event):
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

Label(win, text="Введите товар для поиска:").place(x=70, y=50)

# Поисковая строка
search_var = StringVar()
search_var.trace_add("write", on_search)
Entry(win, textvariable=search_var, width=40).place(x=300, y=50)

listbox = Listbox(win, height=5, width=20)
listbox.bind("<<ListboxSelect>>", on_select)

# --- Скроллируемый фрейм для корзины ---
canvas = Canvas(win, bg='white', width=300, height=250)
scrollbar = Scrollbar(win, orient="vertical", command=canvas.yview)
scrollable_frame = Frame(canvas, bg='white')

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

Label(win, text="Список товаров:").place(x=60, y=120)
canvas.place(x=50, y=140)
scrollbar.place(x=350, y=140, height=250)

itemsFrame = scrollable_frame  # переопределяем имя для update_cart()

# Чек и кнопки
Label(win, text="Чек:").place(x=410, y=130)

cheq = Text(win, height=12, width=25)
cheq.place(x=400, y=150)

downloadBtn = Button(win, text="Скачать чек", width=20, command=download)
downloadBtn.place(relx=1.0, rely=1.0, x=-20, y=-20, anchor="se")

clearBtn = Button(win, text="Очистить", width=20, command=clear_cart)
clearBtn.place(relx=1.0, rely=1.0, x=-220, y=-20, anchor="se")

win.mainloop()
