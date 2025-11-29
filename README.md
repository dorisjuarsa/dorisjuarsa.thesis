# Belajar Git & GitHub – Doris Juarsa

Dokumentasi ini berisi langkah-demi-langkah setup Git, SSH, GitHub, dan inisialisasi project di Ubuntu.  
README ini dibuat sebagai panduan pribadi untuk memulai project thesis menggunakan Python dan GitHub.

---

## 📌 1. Instalasi & Pengecekan Git

Cek apakah Git sudah terpasang:

```bash
git --version
```

Jika muncul versi (misal `git version 2.43.0`), berarti Git sudah terinstall.

---

## 📌 2. Konfigurasi Identitas Git (khusus akun GitHub tesis)

Set identitas Git untuk repo ini:

```bash
git config user.name "Doris Juarsa"
git config user.email "doris_juarsa@teknokrat.ac.id"
```

Cek:

```bash
git config user.name
git config user.email
```

---

## 📌 3. Membuat SSH Key (untuk koneksi aman ke GitHub)

Buat SSH key baru:

```bash
ssh-keygen -t ed25519 -C "doris_juarsa@teknokrat.ac.id" -f ~/.ssh/id_ed25519_tesis
```

Tekan ENTER jika diminta passphrase (bisa kosong).

Tambahkan ke ssh-agent:

```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519_tesis
```

Tampilkan public key:

```bash
cat ~/.ssh/id_ed25519_tesis.pub
```

---

## 📌 4. Tambahkan SSH Key ke GitHub

Masuk ke GitHub:
- Settings  
- SSH and GPG Keys  
- New SSH Key  
- Paste public key  

Test koneksi:

```bash
ssh -T git@github.com
```

Jika sukses:
```
Hi dorisjuarsateknokrat! You've successfully authenticated...
```

---

## 📌 5. Inisialisasi Git di Folder Project

Masuk ke folder project:

```bash
cd ~/DorisJuarsa/Mkom/Thesis/Praktikum/CodeDorisjuarsa
git init
```

---

## 📌 6. Membuat .gitignore (Python Profesional)

Buat file `.gitignore`:

```
# Virtual Environments
venv/
.venv/
env/
ENV/
env.bak/
venv.bak/

# Python Bytecode / Cache
__pycache__/
*.py[cod]
*$py.class

# Jupyter Notebook Checkpoints
.ipynb_checkpoints/

# Distribution / Packaging
build/
dist/
.eggs/
*.egg-info/

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
.tox/
.coverage
.cache

# Django
*.log
db.sqlite3
media/

# Flask
instance/
.webassets-cache

# Environment Variables / Secrets
.env
.env.*
!.env.example

# IDE / Editor
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db
```

---

## 📌 7. Membuat README awal

Contoh isi awal README (dokumen yang sedang kamu baca ini).

---

## 📌 8. Menambahkan & Commit File

```bash
git add .
git commit -m "docs: inisialisasi README dan .gitignore"
```

---

## 📌 9. Membuat Repository di GitHub

Di GitHub:
1. Klik **New repository**
2. Nama misal: `belajar-github`
3. Jangan centang “Initialize with README”
4. Create repository

Hubungkan repo:

```bash
git remote add origin git@github.com:dorisjuarsateknokrat/belajar-github.git
git branch -M main
git push -u origin main
```

---

## 📌 10. Workflow Git Sederhana

Cek status:

```bash
git status
```

Menambahkan file:

```bash
git add <namafile>
```

Commit perubahan:

```bash
git commit -m "pesan commit"
```

Push ke GitHub:

```bash
git push
```

Pull dari GitHub (jika bekerja di komputer lain):

```bash
git pull
```

---

## 📌 11. Penutup

Dokumentasi ini membantu saya:
- memahami alur setup Git dari awal  
- mengatur SSH key  
- mengelola project Python  
- memulai push ke GitHub untuk thesis  

Dengan workflow ini, saya bisa bekerja dari beberapa komputer, aman, rapi, dan profesional.



## ⚙️ Cara Membuat Virtual Environment (venv)

Project ini menggunakan virtual environment agar semua library Python tetap rapi dan terkontrol.

### 🔧 Ubuntu / Linux

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 🔧 Windows (CMD)

```cmd
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 🔧 Windows (PowerShell)

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 🔄 Setelah install library baru
Jika kamu menambah library (misalnya numpy):

```bash
pip install numpy
pip freeze > requirements.txt
```

### ❗ Penting
Folder `venv/` **tidak diupload ke GitHub**.  
Setiap komputer harus membuat venv-nya sendiri.


