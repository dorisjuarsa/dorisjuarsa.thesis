#!/bin/bash

# ==========================================
# Create Python Virtual Environment (.venv)
# Ubuntu & Linux
# ==========================================

echo "🔧 Membuat virtual environment .venv..."

# Cek python3 terpasang atau tidak
if ! command -v python3 &> /dev/null
then
    echo "❌ Python3 tidak ditemukan."
    echo "Install Python3 dengan:"
    echo "sudo apt install python3 python3-venv"
    exit
fi

# Buat venv
python3 -m venv .venv

echo "✅ Virtual environment (.venv) berhasil dibuat!"

echo ""
echo "🔧 Untuk mengaktifkan venv:"
echo "source .venv/bin/activate"
echo ""
echo "🎉 Selesai!"

