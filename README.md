# 🔐 Vault — Password Manager

A secure desktop password manager built using Python. It allows users to safely store, manage, and retrieve passwords using encryption and a master password.

## 🚀 Features

* 🔑 Master password authentication
* 🔐 Encrypted password storage
* ➕ Add new credentials (site, username, password)
* ✏ Edit existing entries
* 🗑 Delete entries
* 👁 Show / hide passwords
* 🔍 Search by site or username
* 📤 Export data (JSON format)
* 📥 Import data (merge existing data)
* ⏳ Auto-lock after inactivity (10 minutes)

## 🛠 Tech Stack

* Python
* Tkinter (GUI)
* JSON (data storage)
* Custom encryption (via `crypto_utils.py`)

## ▶️ How to Run

1. Clone repository:

   ```
   git clone https://github.com/rongalidhanush/password-manager.git
   ```

2. Navigate into folder:

   ```
   cd password-manager
   ```

3. Run the application:

   ```
   python main.py
   ```
## ⚠ Important Notes

* First-time run will prompt you to set a **master password**
* All passwords are stored in encrypted format
* Do NOT delete `auth.json` or `data.json`
* Exported files contain **plain-text passwords** → handle carefully

## 🔒 Security Features

* Encryption of stored passwords
* Hash-based master password authentication
* Session auto-lock after inactivity
* No plain-text password storage inside application files

## 👨‍💻 Developer

Dhanush Naidu

* 📧 Email: [rongalidhnaush68@gmail.com](mailto:rongalidhnaush68@gmail.com)
* 💼 LinkedIn: https://www.linkedin.com/in/dhanushrongali/
* 🐙 GitHub: https://github.com/rongalidhanush
