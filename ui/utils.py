from PIL import Image, ImageTk
import tkinter as tk

def load_icon(path, size):
    image = Image.open(path)
    image = image.resize(size, Image.LANCZOS)
    return ImageTk.PhotoImage(image)

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None
        self.id = None
        self.x = self.y = 0
        self.widget.bind("<Enter>", self.show_tip)
        self.widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        self.x = self.widget.winfo_rootx() + 20
        self.y = self.widget.winfo_rooty() + 20
        self.create_tip()

    def create_tip(self):
        if self.tip_window or not self.text:
            return
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry("+%d+%d" % (self.x, self.y))
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                         background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                         font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hide_tip(self, event=None):
        tw = self.tip_window
        self.tip_window = None
        if tw:
            tw.destroy()

def add_button_feedback(button):
    def on_enter(event):
        button['background'] = '#d9d9d9'  # cor quando o mouse está sobre o botão
    def on_leave(event):
        button['background'] = 'SystemButtonFace'  # cor original do botão
    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)
