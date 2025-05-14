from tkinter import *
import tkinter.messagebox as box

# Пример списка товаров
products = [
    {'name': 'Яблоко', 'price': 30},
    {'name': 'Банан', 'price': 25},
    {'name': 'Молоко', 'price': 80},
    {'name': 'Хлеб', 'price': 40},
    {'name': 'Сыр', 'price': 150},
    {'name': 'Сок', 'price': 100}
]

# Корзина
cart = {}

# Добавление товара в корзину
def add_to_cart(product):
    name = product['name']
    price = product['price']
    if name in cart:
        cart[name]['qty'] += 1
    else:
        cart[name] = {'price': price, 'qty': 1}
    update_cart()

# Обновление списка корзины
def update_cart():
    listbox.delete(0, END)
    for name, data in cart.items():
        line = f"{name} x{data['qty']} = {data['qty'] * data['price']}₽"
        listbox.insert(END, line)

# Расчёт суммы
def checkout():
    total = sum(data['qty'] * data['price'] for data in cart.values())
    if total == 0:
        box.showerror("Ошибка", "Корзина пуста")
    else:
        result = box.askyesno("Оплата", f"Итого: {total}₽\nПодтвердить оплату?")
        if result:
            cart.clear()
            update_cart()
            box.showinfo("Успех", "Оплата прошла успешно!")

# Создание окна
win = Tk()
win.title("Касса 1С на Python")
win.geometry("800x600")
win.configure(bg="#f0f0f0")

# Заголовок
Label(win, text="1С КАССА", font=("Arial", 24, "bold"), bg="#f0f0f0").pack(pady=20)

# Фрейм товаров
product_frame = Frame(win)
product_frame.pack()

# Отображение товаров в виде кнопок
for i, product in enumerate(products):
    btn = Button(product_frame, text=f"{product['name']}\n{product['price']}₽",
                 width=15, height=4, font=("Arial", 12),
                 command=lambda p=product: add_to_cart(p))
    btn.grid(row=i//3, column=i%3, padx=10, pady=10)

# Корзина
Label(win, text="Корзина", font=("Arial", 16)).pack(pady=10)
listbox = Listbox(win, font=("Arial", 14), width=50, height=8)
listbox.pack(pady=10)

# Кнопка оплаты
checkout_btn = Button(win, text="Оплатить", font=("Arial", 16), bg="green", fg="white", width=20, command=checkout)
checkout_btn.pack(pady=20)

win.mainloop()

