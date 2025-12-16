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


