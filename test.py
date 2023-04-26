import tkinter as tk

root = tk.Tk()

# configure the grid
root.columnconfigure(0, weight=0, minsize=75)
root.columnconfigure(1, weight=0, minsize=150)
root.columnconfigure(2, weight=0, minsize=75)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)

# create widgets and place them in the grid
label1 = tk.Label(root, text="Widget 1")
label1.grid(row=0, column=0, padx=5, pady=5)
label2 = tk.Label(root, text="Widget 2")
label2.grid(row=0, column=1, padx=5, pady=5)
label3 = tk.Label(root, text="Widget 3")
label3.grid(row=0, column=2, padx=5, pady=5)
label4 = tk.Label(root, text="Widget 4")
label4.grid(row=1, column=0, padx=5, pady=5)
label5 = tk.Label(root, text="Widget 5")
label5.grid(row=1, column=1, padx=5, pady=5)
label6 = tk.Label(root, text="Widget 6")
label6.grid(row=1, column=2, padx=5, pady=5)

root.mainloop()