import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageFilter, ImageEnhance, ImageOps

BG = "#f6f7f8"
ACCENT = "#faf6f9"
TEXT = "black"

# ---------------- MAIN APP ----------------
root = tk.Tk()
root.title("PixelForge")
root.geometry("900x550")
root.config(bg=BG)

original_img = None
current_img = None
photo = None

# ---------------- IMAGE DISPLAY ----------------
canvas = tk.Label(root, bg=BG)
canvas.pack(side="right", expand=True)

# ---------------- SIDEBAR ----------------
sidebar = tk.Frame(root, width=220, bg="black")
sidebar.pack(side="left", fill="y")

def show_image(img):
    global photo
    img_resized = img.copy()
    img_resized.thumbnail((600, 500))
    photo = ImageTk.PhotoImage(img_resized)
    canvas.config(image=photo)

# ---------------- FILE OPS ----------------
def open_image():
    global original_img, current_img
    path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.png *.jpg *.jpeg")]
    )
    if not path:
        return
    original_img = Image.open(path)
    current_img = original_img.copy()
    show_image(current_img)

def save_image():
    if not current_img:
        return
    path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG", "*.png"), ("JPG", "*.jpg")]
    )
    if path:
        current_img.save(path)
        messagebox.showinfo("Saved", "Image saved successfully")

# ---------------- FILTERS ----------------
def apply_filter(filter_name):
    global current_img
    if not current_img:
        return

    if filter_name == "grayscale":
        current_img = ImageOps.grayscale(current_img)
    elif filter_name == "blur":
        current_img = current_img.filter(ImageFilter.BLUR)
    elif filter_name == "edge":
        current_img = current_img.filter(ImageFilter.FIND_EDGES)
    elif filter_name == "invert":
        current_img = ImageOps.invert(current_img.convert("RGB"))

    show_image(current_img)

# ---------------- BRIGHTNESS ----------------
def adjust_brightness(val):
    global current_img
    if not original_img:
        return
    enhancer = ImageEnhance.Brightness(original_img)
    current_img = enhancer.enhance(float(val))
    show_image(current_img)

# ---------------- RESET ----------------
def reset_image():
    global current_img
    if original_img:
        current_img = original_img.copy()
        show_image(current_img)

# ---------------- UI ----------------
tk.Label(
    sidebar,
    text="PixelForge",
    fg=ACCENT,
    bg="black",
    font=("Arial", 20, "bold")
).pack(pady=20)

btn = lambda t, c: tk.Button(
    sidebar,
    text=t,
    command=c,
    bg="black",
    fg=ACCENT,
    width=20,
    pady=6
).pack(pady=4)

btn("Open Image", open_image)
btn("Save Image", save_image)

tk.Label(sidebar, text="Filters", fg=TEXT, bg="black").pack(pady=8)
btn("Grayscale", lambda: apply_filter("grayscale"))
btn("Blur", lambda: apply_filter("blur"))
btn("Edge Detect", lambda: apply_filter("edge"))
btn("Invert", lambda: apply_filter("invert"))

tk.Label(sidebar, text="Brightness", fg=TEXT, bg="black").pack(pady=8)
tk.Scale(
    sidebar,
    from_=0.5,
    to=2.0,
    resolution=0.1,
    orient="horizontal",
    command=adjust_brightness,
    bg="black",
    fg=ACCENT
).pack()

btn("Reset Image", reset_image)

root.mainloop()