"""Manual visual test — run: python tests/ui/test_dial_visual.py"""
if __name__ == "__main__":
    import tkinter as tk
    from app.ui.dial_widget import DialWidget

    root = tk.Tk()
    root.configure(bg="#111111")
    root.title("Dial visual test")
    label = tk.Label(root, text="45 мин", fg="white", bg="#111111", font=("Arial", 14))
    label.pack(pady=4)

    def on_change(v):
        label.config(text=f"{v} мин")

    dial = DialWidget(root, size=240, on_change=on_change, dark=True)
    dial.pack(padx=20, pady=10)
    dial.set_value(45)
    root.mainloop()
