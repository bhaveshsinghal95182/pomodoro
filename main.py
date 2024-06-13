from tkinter import *
import os
import sys

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
timer = None

# https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# ---------------------------- TIMER RESET ------------------------------- # 

def reset_timer():
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00")
    timer_label.config(text='Timer', fg=GREEN)
    tick_label.config(text="")
    start_button.config(state=ACTIVE)
    global reps 
    reps = 0

# ---------------------------- TIMER MECHANISM ------------------------------- # 

def start_timer():
    global reps
    global started
    reps += 1
    started = True

    long_break_sec = LONG_BREAK_MIN *60
    short_break_sec = SHORT_BREAK_MIN *60
    work_break_sec = WORK_MIN *60

    if reps % 8 == 0:
        timer_label.config(text='Long break', fg=RED)
        count_down(long_break_sec)
        window.attributes('-topmost', True)
    elif reps % 2 == 0:
        timer_label.config(text='Short break', fg=PINK)
        count_down(short_break_sec)
        window.attributes('-topmost', True)
    else:
        timer_label.config(text='Work time')
        count_down(work_break_sec)

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 

def count_down(count):
    count_min = count // 60
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f'0{count_sec}'
    canvas.itemconfig(timer_text, text=f'{count_min}:{count_sec}')
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
        start_button.config(state=DISABLED)
    else:
        start_timer()
        mark = ""
        work_session = reps // 2
        for _ in range(work_session):
            mark += "✔"
        tick_label.config(text=mark)

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodora technique")
window.config(padx=100,pady=50, bg=YELLOW)

# tomato image and timer
canvas = Canvas(width=200, height=224, bg=YELLOW)
tomato_img = PhotoImage(file=resource_path('tomato.png'))
canvas.create_image(100, 112, image=tomato_img)
canvas['highlightthickness'] = 0
timer_text = canvas.create_text(100,130, text='00:00', font=(FONT_NAME, 35, 'bold'), fill='white')
canvas.grid(row=1, column=1)

# start button
start_button = Button(text='Start', borderwidth=0, bg=YELLOW, font=(FONT_NAME, 15), command=start_timer)
start_button.grid(row=2, column=0)

# reset button
reset_button = Button(text='Reset', borderwidth=0, bg=YELLOW, font=(FONT_NAME, 15), command=reset_timer)
reset_button.grid(row=2, column=2)

# tick mark label
tick_label = Label(fg=GREEN, bg=YELLOW, font=(FONT_NAME, 20))
tick_label.grid(row=3, column=1)

# timer label
timer_label = Label(text='Timer', fg=GREEN, bg=YELLOW, font=(FONT_NAME, 50, 'bold'))
timer_label.grid(row=0, column=1)

window.mainloop()