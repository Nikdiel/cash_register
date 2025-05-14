from tkinter import *
import tkinter.messagebox as box

products = [
    {
        'name': "apple",
        'price': 800
    },
    {
        'name': "banana",
        'price': 1100
    }
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
        box.showerror("Error", message="Вы ничего не выбрали")

win = Tk()
# win.attributes('-fullscreen', True)
# screen_width = win.winfo_screenwidth()
# screen_height = win.winfo_screenheight()
# win.geometry(f"{screen_width}x{screen_height}+0+0") 
win.wm_state('zoomed')
win.geometry("600x400")

fr1 = Frame(win).pack()
lb1 = Label(fr1, text="Выберите товары которые вас интересуют:").pack(side=TOP)
fr2 = Frame(fr1).pack()   

for p in products: 
    var = IntVar()
    check = Checkbutton(fr2, variable=var).pack(side=LEFT, padx=[50, 0])
    lb = Label(fr2, text=f"{p['name']}").pack(side=LEFT)
    numbers.append((var, p['price']))


btn = Button(fr1, text="Вычислить стоимость", command=summa).pack(side=BOTTOM)



# exitBtn = Button(win, text="×", bg="red", fg="white", height=1, width=2, command=exit).place(relx=1.0, y=0, anchor='ne')

win.mainloop()