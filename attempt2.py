from tkinter import *
import tkinter.messagebox as box

products = [
    {'name': "apple", 'price': 800},
    {'name': "banana", 'price': 1100},
    {'name': "orange", 'price': 900},
    {'name': "pineapple", 'price': 1300},
    {'name': "kiwi", 'price': 750},
    {'name': "grape", 'price': 1200},
    {'name': "mango", 'price': 1500},
]
numbers = []

def summa():
    summ = 0
    for var, price in numbers:
        if var.get():
            summ += price
    if summ != 0:
        box.askquestion("Сумма", message=f"Ваша сумма составляет: {summ}")
    else:
        box.showerror("Ошибка", message="Вы ничего не выбрали")

win = Tk()
win.wm_state('zoomed')  # окно на весь экран

main_frame = Frame(win)
main_frame.pack(expand=True)  # центрируем основной фрейм по вертикали

title = Label(main_frame, text="Выберите товары, которые вас интересуют:", font=("Arial", 18))
title.pack(pady=20)

products_frame = Frame(main_frame)
products_frame.pack()

for p in products:
    row = Frame(products_frame)
    row.pack(pady=10)

    var = IntVar()
    check = Checkbutton(row, variable=var)
    check.pack(side=LEFT)

    lb = Label(row, text=f"{p['name'].capitalize()} - {p['price']} тг", font=("Arial", 14))
    lb.pack(side=LEFT, padx=10)

    numbers.append((var, p['price']))

btn = Button(main_frame, text="Вычислить стоимость", command=summa, font=("Arial", 14), bg="#4CAF50", fg="white")
btn.pack(pady=30)

win.mainloop()
