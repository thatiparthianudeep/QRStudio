import customtkinter as ctk
from tkinter import filedialog, messagebox
from generator import generate_qr
from scanner import scan_qr
from PIL import ImageTk, Image

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

PURPLE = "#7C3AED"
PURPLE_HOVER = "#6D28D9"
DARK_BG = "#1a1a2e"
CARD_BG = "#16213e"
TEXT_MUTED = "#a0aec0"

app = ctk.CTk()
app.title("QR Studio")
app.geometry("520x750")
app.resizable(False, False)
app.configure(fg_color=DARK_BG)

logo_path = None
qr_image = None

# --- Header ---
header = ctk.CTkFrame(app, fg_color=CARD_BG, corner_radius=0, height=70)
header.pack(fill="x")
header.pack_propagate(False)

ctk.CTkLabel(
    header,
    text="⬛ QR Studio",
    font=ctk.CTkFont(family="Arial", size=22, weight="bold"),
    text_color=PURPLE
).pack(side="left", padx=20, pady=16)

ctk.CTkLabel(
    header,
    text="Generate & Scan QR Codes",
    font=ctk.CTkFont(size=12),
    text_color=TEXT_MUTED
).pack(side="left", padx=4, pady=16)

# --- Tab View ---
tabs = ctk.CTkTabview(
    app,
    fg_color=CARD_BG,
    segmented_button_fg_color=DARK_BG,
    segmented_button_selected_color=PURPLE,
    segmented_button_selected_hover_color=PURPLE_HOVER,
    segmented_button_unselected_color=DARK_BG,
    border_color=PURPLE,
    border_width=1
)
tabs.pack(fill="both", expand=True, padx=16, pady=16)
tabs.add("Generate")
tabs.add("Scan")

# ── Generate Tab ──
gen = tabs.tab("Generate")

ctk.CTkLabel(gen, text="Text or URL", font=ctk.CTkFont(size=13), text_color=TEXT_MUTED).pack(anchor="w", padx=8, pady=(16, 4))
entry = ctk.CTkEntry(
    gen,
    placeholder_text="https://example.com",
    height=42,
    corner_radius=8,
    border_color=PURPLE,
    fg_color="#0f0f23"
)
entry.pack(fill="x", padx=8)

# Logo row
logo_frame = ctk.CTkFrame(gen, fg_color="transparent")
logo_frame.pack(fill="x", padx=8, pady=10)

logo_label = ctk.CTkLabel(logo_frame, text="No logo selected", text_color=TEXT_MUTED, font=ctk.CTkFont(size=12))
logo_label.pack(side="left")

def browse_logo():
    global logo_path
    path = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg")])
    if path:
        logo_path = path
        logo_label.configure(text=path.split("\\")[-1], text_color=PURPLE)

ctk.CTkButton(
    logo_frame,
    text="Add Logo",
    width=100,
    height=34,
    fg_color=PURPLE,
    hover_color=PURPLE_HOVER,
    corner_radius=8,
    command=browse_logo
).pack(side="right")

# Preview box
preview_frame = ctk.CTkFrame(gen, fg_color="#0f0f23", corner_radius=12, width=260, height=260)
preview_frame.pack(pady=10)
preview_frame.pack_propagate(False)

preview = ctk.CTkLabel(preview_frame, text="QR preview will\nappear here", text_color=TEXT_MUTED)
preview.pack(expand=True)

def generate():
    global qr_image
    text = entry.get()
    if not text:
        messagebox.showwarning("Empty", "Please enter text or URL.")
        return
    qr_image = generate_qr(text, logo_path=logo_path if logo_path else None)
    tk_img = ImageTk.PhotoImage(qr_image.resize((240, 240)))
    preview.configure(image=tk_img, text="")
    preview.image = tk_img

def save():
    if not qr_image:
        messagebox.showwarning("No QR", "Generate a QR first.")
        return
    path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png")])
    if path:
        qr_image.save(path)
        messagebox.showinfo("Saved", f"QR saved successfully!")

# Buttons row
btn_frame = ctk.CTkFrame(gen, fg_color="transparent")
btn_frame.pack(fill="x", padx=8, pady=8)

ctk.CTkButton(
    btn_frame, text="Generate QR",
    height=42, fg_color=PURPLE, hover_color=PURPLE_HOVER,
    corner_radius=8, font=ctk.CTkFont(size=14, weight="bold"),
    command=generate
).pack(side="left", expand=True, fill="x", padx=(0, 6))

ctk.CTkButton(
    btn_frame, text="Save PNG",
    height=42, fg_color="#2d2d4e", hover_color="#3d3d6e",
    corner_radius=8, font=ctk.CTkFont(size=14),
    command=save
).pack(side="left", expand=True, fill="x", padx=(6, 0))

# ── Scan Tab ──
scan_tab = tabs.tab("Scan")

ctk.CTkLabel(
    scan_tab,
    text="Open an image containing a QR code\nto decode its content.",
    text_color=TEXT_MUTED,
    font=ctk.CTkFont(size=13),
    justify="center"
).pack(pady=(30, 20))

scan_icon = ctk.CTkFrame(scan_tab, fg_color="#0f0f23", corner_radius=12, width=120, height=120)
scan_icon.pack()
scan_icon.pack_propagate(False)
ctk.CTkLabel(scan_icon, text="🔍", font=ctk.CTkFont(size=48)).pack(expand=True)

scan_result = ctk.CTkTextbox(
    scan_tab,
    height=100,
    fg_color="#0f0f23",
    border_color=PURPLE,
    border_width=1,
    corner_radius=8,
    text_color="white",
    font=ctk.CTkFont(size=13)
)
scan_result.pack(fill="x", padx=8, pady=16)
scan_result.insert("end", "Scan result will appear here...")
scan_result.configure(state="disabled")

def scan():
    path = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg")])
    if path:
        result = scan_qr(path)
        scan_result.configure(state="normal")
        scan_result.delete("1.0", "end")
        scan_result.insert("end", result)
        scan_result.configure(state="disabled")

ctk.CTkButton(
    scan_tab,
    text="Open Image to Scan",
    height=42,
    fg_color=PURPLE,
    hover_color=PURPLE_HOVER,
    corner_radius=8,
    font=ctk.CTkFont(size=14, weight="bold"),
    command=scan
).pack(padx=8, fill="x")

# --- Footer ---
ctk.CTkLabel(
    app,
    text="QR Studio v1.0  •  Built with Python",
    font=ctk.CTkFont(size=11),
    text_color=TEXT_MUTED
).pack(pady=10)

app.mainloop()
