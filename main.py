import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
import json, time, os, hashlib
from crypto_utils import *
from auth import setup_master_password, verify_master_password

DATA_FILE      = "data.json"
AUTO_LOCK_TIME = 600  # 10 minutes
last_activity  = time.time()

APP_VERSION    = "v1.0.0"
DEVELOPER      = "Dhanush Naidu"
CONTACT_EMAIL  = "rongalidhnaush68@gmail.com"
LINKEDIN_URL   = "https://www.linkedin.com/in/dhanushrongali/"
GITHUB_URL     = "https://github.com/rongalidhanush"
LINKEDIN_LABEL = "linkedin.com/in/dhanushrongali"
GITHUB_LABEL   = "github.com/rongalidhanush"

# ═══════════════════════════ THEME ═══════════════════════════
BG       = "#F0F4F8"
SURFACE  = "#FFFFFF"
SURFACE2 = "#E8EDF2"
BORDER   = "#D1D9E0"
ACCENT   = "#2563EB"
ACCENT_H = "#1D4ED8"
SUCCESS  = "#16A34A"
DANGER   = "#DC2626"
WARNING  = "#D97706"
TEXT     = "#1E293B"
SUBTEXT  = "#64748B"
WHITE    = "#FFFFFF"

FNT_H2    = ("Segoe UI", 12, "bold")
FNT_BODY  = ("Segoe UI", 10)
FNT_MONO  = ("Consolas", 10)
FNT_BTN   = ("Segoe UI", 9, "bold")
FNT_LABEL = ("Segoe UI", 8, "bold")
FNT_SMALL = ("Segoe UI", 8)

# ═══════════════════════════ HELPERS ═════════════════════════
def reset_timer():
    global last_activity
    last_activity = time.time()

def check_auto_lock():
    if time.time() - last_activity > AUTO_LOCK_TIME:
        logout()
        messagebox.showinfo("Locked", "Session expired due to inactivity.")
    root.after(1000, check_auto_lock)

def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            enc = f.read()
            return decrypt_data(enc, master_password, salt) if enc else {}
    except:
        return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        f.write(encrypt_data(data, master_password, salt))

def set_status(msg, color=SUBTEXT):
    status_bar_lbl.config(text=msg, fg=color)

# ═══════════════════════ WIDGET HELPERS ══════════════════════
def make_entry(parent, show=None, width=26):
    return tk.Entry(
        parent, show=show, width=width,
        bg=SURFACE2, fg=TEXT, insertbackground=ACCENT,
        relief="flat", font=FNT_MONO,
        highlightthickness=1,
        highlightcolor=ACCENT,
        highlightbackground=BORDER
    )

def make_btn(parent, text, cmd, bg=ACCENT, fg=WHITE, width=12):
    btn = tk.Button(
        parent, text=text, command=cmd,
        bg=bg, fg=fg, activebackground=ACCENT_H,
        activeforeground=WHITE, relief="flat",
        font=FNT_BTN, cursor="hand2",
        width=width, pady=6, padx=4
    )
    orig = bg
    btn.bind("<Enter>", lambda e: btn.config(bg=ACCENT_H))
    btn.bind("<Leave>", lambda e: btn.config(bg=orig))
    return btn

def make_icon_btn(parent, text, cmd, bg, fg=WHITE):
    btn = tk.Button(
        parent, text=text, command=cmd,
        bg=bg, fg=fg, activebackground=ACCENT_H,
        activeforeground=WHITE, relief="flat",
        font=FNT_SMALL, cursor="hand2",
        padx=8, pady=3
    )
    orig = bg
    btn.bind("<Enter>", lambda e: btn.config(bg=ACCENT_H))
    btn.bind("<Leave>", lambda e: btn.config(bg=orig))
    return btn

def hsep(parent, pady=8):
    tk.Frame(parent, bg=BORDER, height=1).pack(fill="x", padx=16, pady=pady)

# ═══════════════════════════ ROOT ════════════════════════════
setup_master_password()

root = tk.Tk()
root.title("Vault — Password Manager")
root.geometry("860x600")
root.resizable(True, True)
root.minsize(720, 500)
root.configure(bg=BG)

root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

root.update_idletasks()
sx = (root.winfo_screenwidth()  - 860) // 2
sy = (root.winfo_screenheight() - 600) // 2
root.geometry(f"860x600+{sx}+{sy}")

# ═══════════════════════ LOGIN SCREEN ════════════════════════
def login(event=None):
    global master_password, salt
    pwd = entry_master.get()
    valid, salt_val = verify_master_password(pwd)
    if valid:
        master_password = pwd
        salt = salt_val
        login_frame.pack_forget()
        main_frame.pack(fill="both", expand=True)
        reset_timer()
        view_passwords()
    else:
        login_err.config(text="✗  Wrong password. Try again.")

def logout():
    main_frame.pack_forget()
    entry_master.delete(0, tk.END)
    login_err.config(text="")
    login_frame.pack(fill="both", expand=True)

login_frame = tk.Frame(root, bg=BG)
login_frame.pack(fill="both", expand=True)

card = tk.Frame(login_frame, bg=SURFACE)
card.place(relx=0.5, rely=0.5, anchor="center", width=380, height=380)

tk.Frame(card, bg=ACCENT, height=5).pack(fill="x")
tk.Label(card, text="🔐", bg=SURFACE, font=("Segoe UI", 30)).pack(pady=(24, 4))
tk.Label(card, text="Vault", bg=SURFACE, fg=TEXT,
         font=("Segoe UI", 24, "bold")).pack()
tk.Label(card, text="Secure Password Manager", bg=SURFACE,
         fg=SUBTEXT, font=FNT_SMALL).pack(pady=(2, 0))
tk.Frame(card, bg=BORDER, height=1).pack(fill="x", padx=32, pady=16)
tk.Label(card, text="MASTER PASSWORD", bg=SURFACE,
         fg=SUBTEXT, font=FNT_LABEL).pack(anchor="w", padx=36)

entry_master = tk.Entry(
    card, show="*", width=28,
    bg=SURFACE2, fg=TEXT, insertbackground=ACCENT,
    relief="flat", font=FNT_MONO,
    highlightthickness=1, highlightcolor=ACCENT, highlightbackground=BORDER
)
entry_master.pack(ipady=9, padx=36, pady=(4, 14), fill="x")
entry_master.bind("<Return>", login)
entry_master.focus()

tk.Button(
    card, text="Unlock  →", command=login,
    bg=ACCENT, fg=WHITE, activebackground=ACCENT_H,
    activeforeground=WHITE, relief="flat",
    font=("Segoe UI", 11, "bold"), cursor="hand2", pady=10
).pack(fill="x", padx=36)

login_err = tk.Label(card, text="", bg=SURFACE, fg=DANGER, font=FNT_SMALL)
login_err.pack(pady=4)

# Credits on login screen
tk.Frame(card, bg=BORDER, height=1).pack(fill="x", padx=32, pady=(6, 0))
tk.Label(card, text=f"Developed by {DEVELOPER}",
         bg=SURFACE, fg=SUBTEXT, font=FNT_SMALL).pack(pady=(6, 0))
tk.Label(card, text=CONTACT_EMAIL,
         bg=SURFACE, fg=ACCENT, font=FNT_SMALL).pack(pady=(0, 8))

# ═══════════════════════ MAIN LAYOUT ═════════════════════════
main_frame = tk.Frame(root, bg=BG)

# ── Sidebar
sidebar = tk.Frame(main_frame, bg=SURFACE, width=210)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

tk.Frame(sidebar, bg=ACCENT, height=4).pack(fill="x")
tk.Label(sidebar, text="🔐  Vault", bg=SURFACE, fg=TEXT,
         font=("Segoe UI", 14, "bold")).pack(pady=(18, 2))
tk.Label(sidebar, text="Password Manager", bg=SURFACE,
         fg=SUBTEXT, font=FNT_SMALL).pack()
tk.Frame(sidebar, bg=BORDER, height=1).pack(fill="x", padx=16, pady=14)

def nav_btn(label, icon, cmd, color=ACCENT):
    row = tk.Frame(sidebar, bg=SURFACE, cursor="hand2")
    row.pack(fill="x", padx=12, pady=2)
    lbl = tk.Label(
        row, text=f"  {icon}   {label}",
        bg=SURFACE, fg=TEXT, font=FNT_BTN,
        anchor="w", pady=10, cursor="hand2"
    )
    lbl.pack(fill="x", padx=2)
    def on_click(e=None): cmd(); reset_timer()
    def on_in(e):  lbl.config(bg=color, fg=WHITE); row.config(bg=color)
    def on_out(e): lbl.config(bg=SURFACE, fg=TEXT); row.config(bg=SURFACE)
    for w in (row, lbl):
        w.bind("<Button-1>", on_click)
        w.bind("<Enter>",    on_in)
        w.bind("<Leave>",    on_out)

nav_btn("View All",      "📋", lambda: view_passwords())
nav_btn("Search",        "🔍", lambda: search_password())
hsep(sidebar, pady=6)
nav_btn("Add Entry",     "➕", lambda: show_form())
nav_btn("Change Master", "🔑", lambda: change_master_password(), WARNING)
hsep(sidebar, pady=6)
nav_btn("Export Data",   "📤", lambda: export_data(), SUCCESS)
nav_btn("Import Data",   "📥", lambda: import_data(), SUCCESS)
hsep(sidebar, pady=6)
nav_btn("About",         "ℹ",  lambda: show_about())
nav_btn("Logout",        "🚪", lambda: logout(), DANGER)

# ── Sidebar footer credits
tk.Frame(sidebar, bg=SURFACE).pack(fill="y", expand=True)   # spacer pushes footer down
tk.Frame(sidebar, bg=BORDER, height=1).pack(fill="x", padx=14)
tk.Label(sidebar, text="Developed by", bg=SURFACE,
         fg=SUBTEXT, font=FNT_SMALL).pack(pady=(8, 0))
tk.Label(sidebar, text=DEVELOPER, bg=SURFACE,
         fg=ACCENT, font=("Segoe UI", 9, "bold")).pack()
tk.Label(sidebar, text=APP_VERSION, bg=SURFACE,
         fg=BORDER, font=FNT_SMALL).pack(pady=(0, 10))

# ── Content area
content = tk.Frame(main_frame, bg=BG)
content.pack(side="right", fill="both", expand=True)

content.rowconfigure(2, weight=1)
content.columnconfigure(0, weight=1)

# Topbar
topbar = tk.Frame(content, bg=SURFACE, height=52)
topbar.grid(row=0, column=0, sticky="ew")
topbar.grid_propagate(False)
topbar_lbl = tk.Label(topbar, text="All Passwords",
                       bg=SURFACE, fg=TEXT, font=FNT_H2)
topbar_lbl.pack(side="left", padx=20, pady=14)

# ── Add / Edit Form Panel
form_panel = tk.Frame(content, bg=SURFACE2, pady=10)
form_mode  = {"editing": False, "original_site": None}

def show_form(site=None, username="", password=""):
    form_mode["editing"]       = site is not None
    form_mode["original_site"] = site
    topbar_lbl.config(text="Edit Entry" if site else "Add New Entry")
    form_site_entry.config(state="normal")
    form_site_entry.delete(0, tk.END)
    form_user_entry.delete(0, tk.END)
    form_pass_entry.delete(0, tk.END)
    if site:
        form_site_entry.insert(0, site)
        form_site_entry.config(state="disabled")
    form_user_entry.insert(0, username)
    form_pass_entry.insert(0, password)
    form_save_btn.config(text="Update Entry" if site else "Save Entry")
    form_panel.grid(row=1, column=0, sticky="ew")
    form_site_entry.focus() if not site else form_user_entry.focus()

def hide_form():
    form_panel.grid_forget()
    topbar_lbl.config(text="All Passwords")

fp = tk.Frame(form_panel, bg=SURFACE2)
fp.pack(padx=20, fill="x")
fp.columnconfigure(1, weight=1)
fp.columnconfigure(3, weight=1)
fp.columnconfigure(5, weight=1)

def fp_label(text, row, col):
    tk.Label(fp, text=text, bg=SURFACE2, fg=SUBTEXT,
             font=FNT_LABEL).grid(row=row, column=col, sticky="w",
                                   pady=(6, 2), padx=(0, 8))

fp_label("SITE / APP", 0, 0)
form_site_entry = make_entry(fp, width=22)
form_site_entry.grid(row=1, column=0, ipady=7, padx=(0, 16), sticky="ew")

fp_label("USERNAME", 0, 2)
form_user_entry = make_entry(fp, width=22)
form_user_entry.grid(row=1, column=2, ipady=7, padx=(0, 16), sticky="ew")

fp_label("PASSWORD", 0, 4)
pw_frame = tk.Frame(fp, bg=SURFACE2)
pw_frame.grid(row=1, column=4, sticky="ew")
fp.columnconfigure(4, weight=1)

form_pass_entry = make_entry(pw_frame, show="*", width=20)
form_pass_entry.pack(side="left", ipady=7, fill="x", expand=True)

show_fp_var = tk.BooleanVar()
def toggle_form_pw():
    form_pass_entry.config(show="" if show_fp_var.get() else "*")

tk.Checkbutton(
    pw_frame, text="Show", variable=show_fp_var,
    command=toggle_form_pw,
    bg=SURFACE2, fg=SUBTEXT, activebackground=SURFACE2,
    selectcolor=SURFACE2, font=FNT_SMALL, cursor="hand2"
).pack(side="left", padx=6)

form_btn_row = tk.Frame(form_panel, bg=SURFACE2)
form_btn_row.pack(padx=20, pady=(8, 4), anchor="w")

form_save_btn = make_btn(form_btn_row, "Save Entry",
                          lambda: submit_form(), bg=SUCCESS, width=13)
form_save_btn.pack(side="left", padx=(0, 8))
make_btn(form_btn_row, "Cancel", lambda: hide_form(),
          bg=BORDER, fg=TEXT, width=9).pack(side="left")

# ── Password List
list_outer = tk.Frame(content, bg=BG)
list_outer.grid(row=2, column=0, sticky="nsew")
list_outer.rowconfigure(1, weight=1)
list_outer.columnconfigure(0, weight=1)

col_header = tk.Frame(list_outer, bg=SURFACE2)
col_header.grid(row=0, column=0, sticky="ew", padx=16, pady=(10, 0))

for txt, w in [("SITE / APP", 22), ("USERNAME", 22), ("PASSWORD", 22), ("ACTIONS", 16)]:
    tk.Label(
        col_header, text=txt, bg=SURFACE2, fg=SUBTEXT,
        font=FNT_LABEL, width=w, anchor="w"
    ).pack(side="left", padx=10, pady=6)

scroll_container = tk.Frame(list_outer, bg=BG)
scroll_container.grid(row=1, column=0, sticky="nsew", padx=16, pady=(2, 0))
scroll_container.rowconfigure(0, weight=1)
scroll_container.columnconfigure(0, weight=1)

list_canvas  = tk.Canvas(scroll_container, bg=BG, highlightthickness=0)
list_scroll  = tk.Scrollbar(scroll_container, orient="vertical",
                              command=list_canvas.yview)
scroll_frame = tk.Frame(list_canvas, bg=BG)

scroll_frame.bind(
    "<Configure>",
    lambda e: list_canvas.configure(scrollregion=list_canvas.bbox("all"))
)
list_canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
list_canvas.configure(yscrollcommand=list_scroll.set)

list_canvas.grid(row=0, column=0, sticky="nsew")
list_scroll.grid(row=0, column=1, sticky="ns")

def on_canvas_resize(event):
    list_canvas.itemconfig("all", width=event.width)
list_canvas.bind("<Configure>", on_canvas_resize)

root.bind_all("<MouseWheel>",
    lambda e: list_canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

# ── Status bar
statusbar = tk.Frame(content, bg=SURFACE, height=28)
statusbar.grid(row=3, column=0, sticky="ew")
statusbar.grid_propagate(False)

status_bar_lbl = tk.Label(statusbar, text="Ready", bg=SURFACE,
                            fg=SUBTEXT, font=FNT_SMALL)
status_bar_lbl.pack(side="left", padx=14)

# Permanent credit in status bar
tk.Label(statusbar, text=f"Developed by {DEVELOPER}  •  {CONTACT_EMAIL}",
         bg=SURFACE, fg=BORDER, font=FNT_SMALL).pack(side="right", padx=14)

entry_count_lbl = tk.Label(statusbar, text="", bg=SURFACE,
                             fg=SUBTEXT, font=FNT_SMALL)
entry_count_lbl.pack(side="right", padx=14)

# ═══════════════════════ CORE FUNCTIONS ══════════════════════
reveal_states = {}

def render_table(data):
    for w in scroll_frame.winfo_children():
        w.destroy()
    reveal_states.clear()

    if not data:
        tk.Label(scroll_frame,
                 text="No saved entries yet.  Click '➕ Add Entry' to start.",
                 bg=BG, fg=SUBTEXT, font=FNT_BODY).pack(pady=40)
        entry_count_lbl.config(text="0 entries")
        return

    count = len(data)
    entry_count_lbl.config(text=f"{count} entr{'y' if count == 1 else 'ies'}")

    for i, (site, info) in enumerate(data.items()):
        row_bg = SURFACE if i % 2 == 0 else SURFACE2
        row = tk.Frame(scroll_frame, bg=row_bg)
        row.pack(fill="x", pady=1)

        try:
            dec_pw = decrypt_password(info["password"], master_password, salt)
        except:
            dec_pw = "DECRYPT ERROR"

        reveal_states[site] = {"shown": False, "dec": dec_pw}

        tk.Label(row, text=site, bg=row_bg, fg=TEXT,
                 font=FNT_BODY, width=22, anchor="w").pack(
                     side="left", padx=12, pady=8)

        tk.Label(row, text=info.get("username", ""), bg=row_bg, fg=SUBTEXT,
                 font=FNT_BODY, width=22, anchor="w").pack(
                     side="left", padx=12)

        pw_lbl = tk.Label(row, text="••••••••", bg=row_bg, fg=SUBTEXT,
                           font=FNT_MONO, width=22, anchor="w")
        pw_lbl.pack(side="left", padx=12)

        act = tk.Frame(row, bg=row_bg)
        act.pack(side="left", padx=8)

        def make_toggle(s=site, lbl=pw_lbl):
            def toggle():
                st = reveal_states[s]
                if st["shown"]:
                    lbl.config(text="••••••••", fg=SUBTEXT)
                    st["shown"] = False
                else:
                    lbl.config(text=st["dec"], fg=SUCCESS)
                    st["shown"] = True
                reset_timer()
            return toggle

        def make_edit(s=site, u=info.get("username", ""), p=dec_pw):
            def edit():
                show_form(site=s, username=u, password=p)
                reset_timer()
            return edit

        def make_delete(s=site):
            def delete():
                if messagebox.askyesno("Confirm Delete", f'Delete "{s}"?'):
                    d = load_data()
                    del d[s]
                    save_data(d)
                    set_status(f'Deleted "{s}".', DANGER)
                    view_passwords()
                reset_timer()
            return delete

        make_icon_btn(act, "👁 Show", make_toggle(), ACCENT).pack(side="left", padx=2)
        make_icon_btn(act, "✏ Edit", make_edit(),   WARNING).pack(side="left", padx=2)
        make_icon_btn(act, "🗑 Del",  make_delete(), DANGER).pack(side="left", padx=2)

def view_passwords():
    topbar_lbl.config(text="All Passwords")
    hide_form()
    render_table(load_data())
    set_status("All entries loaded.", SUCCESS)
    reset_timer()

def search_password():
    kw = simpledialog.askstring("Search", "Enter site or username:", parent=root)
    if not kw:
        return
    kw = kw.strip().lower()
    data = load_data()
    filtered = {s: i for s, i in data.items()
                if kw in s.lower() or kw in i.get("username", "").lower()}
    topbar_lbl.config(text=f'Search: "{kw}"')
    render_table(filtered)
    set_status(f"{len(filtered)} result(s) for '{kw}'.", ACCENT)
    reset_timer()

def submit_form():
    site = form_site_entry.get().strip()
    user = form_user_entry.get().strip()
    pwd  = form_pass_entry.get().strip()

    if not site or not pwd:
        set_status("Site and Password cannot be empty.", DANGER)
        return

    data = load_data()

    if form_mode["editing"]:
        data[site] = {
            "username": user,
            "password": encrypt_password(pwd, master_password, salt)
        }
        set_status(f'Updated "{site}".', SUCCESS)
    else:
        if site in data:
            if not messagebox.askyesno("Overwrite",
                                        f'"{site}" already exists. Overwrite?'):
                return
        data[site] = {
            "username": user,
            "password": encrypt_password(pwd, master_password, salt)
        }
        set_status(f'Saved "{site}".', SUCCESS)

    save_data(data)
    hide_form()
    view_passwords()
    reset_timer()

def change_master_password():
    old = simpledialog.askstring("Verify", "Current master password:",
                                  show="*", parent=root)
    if not old:
        return
    valid, old_salt = verify_master_password(old)
    if not valid:
        set_status("Wrong current password.", DANGER)
        return

    new = simpledialog.askstring("New Password", "Enter new master password:",
                                  show="*", parent=root)
    if not new:
        return

    data = load_data()
    decrypted = {
        s: {"username": i["username"],
            "password": decrypt_password(i["password"], old, old_salt)}
        for s, i in data.items()
    }

    global master_password, salt
    new_salt = os.urandom(16).hex()
    new_data = {
        s: {"username": i["username"],
            "password": encrypt_password(i["password"], new, new_salt)}
        for s, i in decrypted.items()
    }

    save_data(new_data)
    with open("auth.json", "w") as f:
        json.dump({
            "hash": hashlib.sha256((new + new_salt).encode()).hexdigest(),
            "salt": new_salt
        }, f)

    master_password = new
    salt = new_salt
    set_status("Master password changed successfully.", SUCCESS)
    reset_timer()

# ═══════════════════ EXPORT / IMPORT ═════════════════════════
def export_data():
    """Decrypt all entries and save as plain JSON file chosen by user."""
    data = load_data()
    if not data:
        messagebox.showinfo("Export", "Nothing to export — vault is empty.")
        return

    # Build plain dict: { site: { username, password } }
    plain = {}
    for site, info in data.items():
        try:
            plain[site] = {
                "username": info.get("username", ""),
                "password": decrypt_password(info["password"], master_password, salt)
            }
        except:
            plain[site] = {"username": info.get("username", ""), "password": "ERROR"}

    path = filedialog.asksaveasfilename(
        parent=root,
        title="Export Vault Data",
        defaultextension=".json",
        filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
        initialfile="vault_export.json"
    )
    if not path:
        return

    with open(path, "w") as f:
        json.dump(plain, f, indent=2)

    set_status(f"Exported {len(plain)} entries to {os.path.basename(path)}", SUCCESS)
    messagebox.showinfo(
        "Export Successful",
        f"✅  {len(plain)} entries exported to:\n{path}\n\n"
        "⚠  This file contains plain-text passwords.\n"
        "Keep it secure and delete after use."
    )
    reset_timer()


def import_data():
    """Read a plain JSON export file and merge entries into the vault."""
    path = filedialog.askopenfilename(
        parent=root,
        title="Import Vault Data",
        filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
    )
    if not path:
        return

    try:
        with open(path, "r") as f:
            imported = json.load(f)
    except Exception as ex:
        messagebox.showerror("Import Failed", f"Could not read file:\n{ex}")
        return

    # Validate structure
    if not isinstance(imported, dict):
        messagebox.showerror("Import Failed",
                             "Invalid format. File must be a JSON object.")
        return

    data       = load_data()
    added      = 0
    skipped    = 0
    overwritten = 0

    for site, info in imported.items():
        if not isinstance(info, dict) or "password" not in info:
            skipped += 1
            continue

        if site in data:
            # Ask user what to do with duplicates
            ans = messagebox.askyesnocancel(
                "Duplicate Entry",
                f'"{site}" already exists in your vault.\n\nOverwrite it?'
            )
            if ans is None:       # Cancel — stop entire import
                break
            elif ans is False:    # No — skip this entry
                skipped += 1
                continue
            else:                 # Yes — overwrite
                overwritten += 1
        else:
            added += 1

        data[site] = {
            "username": info.get("username", ""),
            "password": encrypt_password(info["password"], master_password, salt)
        }

    save_data(data)
    view_passwords()

    summary = f"✅  Import complete.\n\nAdded: {added}  |  Overwritten: {overwritten}  |  Skipped: {skipped}"
    set_status(f"Import done — {added} added, {overwritten} updated, {skipped} skipped.", SUCCESS)
    messagebox.showinfo("Import Complete", summary)
    reset_timer()

# ═══════════════════════ ABOUT DIALOG ════════════════════════
def show_about():
    import webbrowser

    win = tk.Toplevel(root)
    win.title("About Vault")
    win.geometry("360x430")
    win.resizable(False, False)
    win.configure(bg=SURFACE)
    win.grab_set()

    # Center over root
    win.update_idletasks()
    rx = root.winfo_x() + (root.winfo_width()  - 360) // 2
    ry = root.winfo_y() + (root.winfo_height() - 430) // 2
    win.geometry(f"360x430+{rx}+{ry}")

    # ── Header
    tk.Frame(win, bg=ACCENT, height=5).pack(fill="x")
    tk.Label(win, text="🔐", bg=SURFACE,
             font=("Segoe UI", 28)).pack(pady=(20, 4))
    tk.Label(win, text="Vault", bg=SURFACE, fg=TEXT,
             font=("Segoe UI", 18, "bold")).pack()
    tk.Label(win, text=f"Secure Password Manager  {APP_VERSION}",
             bg=SURFACE, fg=SUBTEXT, font=FNT_SMALL).pack(pady=(2, 0))

    tk.Frame(win, bg=BORDER, height=1).pack(fill="x", padx=28, pady=14)

    # ── Developer name
    tk.Label(win, text="Developed by", bg=SURFACE,
             fg=SUBTEXT, font=FNT_SMALL).pack()
    tk.Label(win, text=DEVELOPER, bg=SURFACE, fg=ACCENT,
             font=("Segoe UI", 13, "bold")).pack(pady=(2, 0))

    tk.Frame(win, bg=BORDER, height=1).pack(fill="x", padx=28, pady=12)

    # ── Helper: make a clickable link label
    def link_row(parent, icon, label_text, url=None, copy_text=None):
        """
        icon        — emoji shown left of label
        label_text  — display text
        url         — if set, clicking opens browser
        copy_text   — if set, clicking copies this to clipboard
        """
        row = tk.Frame(parent, bg=SURFACE)
        row.pack(fill="x", padx=32, pady=3)

        tk.Label(row, text=icon, bg=SURFACE,
                 font=("Segoe UI", 11)).pack(side="left", padx=(0, 8))

        lbl = tk.Label(row, text=label_text, bg=SURFACE, fg=ACCENT,
                       font=("Segoe UI", 9, "bold"), cursor="hand2",
                       anchor="w")
        lbl.pack(side="left")

        hint = tk.Label(row, text="↗ open" if url else "⎘ copy",
                        bg=SURFACE, fg=BORDER, font=FNT_SMALL)
        hint.pack(side="left", padx=6)

        def on_click(e=None):
            if url:
                webbrowser.open(url)
                hint.config(text="✅ opened", fg=SUCCESS)
                win.after(1800, lambda: hint.config(text="↗ open", fg=BORDER))
            elif copy_text:
                root.clipboard_clear()
                root.clipboard_append(copy_text)
                hint.config(text="✅ copied", fg=SUCCESS)
                win.after(1800, lambda: hint.config(text="⎘ copy", fg=BORDER))

        def on_in(e):
            lbl.config(fg=ACCENT_H)
            hint.config(fg=SUBTEXT)
        def on_out(e):
            lbl.config(fg=ACCENT)
            hint.config(fg=BORDER)

        for w in (lbl, hint, row):
            w.bind("<Button-1>", on_click)
            w.bind("<Enter>",    on_in)
            w.bind("<Leave>",    on_out)

    # ── Contact & social links
    tk.Label(win, text="Connect & Contact", bg=SURFACE,
             fg=SUBTEXT, font=FNT_LABEL).pack(anchor="w", padx=32, pady=(0, 4))

    link_row(win, "✉",  CONTACT_EMAIL, copy_text=CONTACT_EMAIL)
    link_row(win, "💼", "LinkedIn",    url=LINKEDIN_URL)
    link_row(win, "🐙", "GitHub",      url=GITHUB_URL)

    tk.Frame(win, bg=BORDER, height=1).pack(fill="x", padx=28, pady=14)

    tk.Button(
        win, text="Close", command=win.destroy,
        bg=ACCENT, fg=WHITE, relief="flat",
        font=FNT_BTN, cursor="hand2", padx=28, pady=8,
        activebackground=ACCENT_H, activeforeground=WHITE
    ).pack(pady=(0, 16))

# ═════════════════════════ LAUNCH ════════════════════════════
check_auto_lock()
root.mainloop()