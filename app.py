from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Fungsi untuk menghubungkan ke database SQLite
def get_db_connection():
    conn = sqlite3.connect('database_jasuke.db')
    conn.row_factory = sqlite3.Row
    return conn

# Fungsi otomatis bikin tabel database kalau belum ada
def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS pesanan (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ukuran TEXT NOT NULL,
            rasa TEXT NOT NULL,
            harga INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Panggil fungsi inisialisasi database saat aplikasi nyala
init_db()

@app.route('/')
def halaman_login():
    return render_template('login.html')

@app.route('/kasir')
def halaman_kasir():
    return render_template('kasir.html')

@app.route('/proses_pesanan', methods=['POST'])
def proses():
    ukuran = request.form.get('ukuran')
    rasa = request.form.get('rasa')
    
    # Nentuin harga otomatis
    harga = 15000 if ukuran == "Cup Besar" else 10000
    
    # Simpan permanen ke database SQL
    conn = get_db_connection()
    conn.execute('INSERT INTO pesanan (ukuran, rasa, harga) VALUES (?, ?, ?)', (ukuran, rasa, harga))
    conn.commit()
    conn.close()
    
    return f"<h3>Berhasil! Pesanan masuk: 1 {ukuran}, Rasa {rasa} (Tersimpan Permanen)</h3> <br> <a href='/kasir'>Kembali Input Lagi</a> | <a href='/dashboard'>Lihat Rekap Omzet</a>"

@app.route('/dashboard')
def halaman_dashboard():
    # Ambil semua data dari database
    conn = get_db_connection()
    pesanan = conn.execute('SELECT * FROM pesanan').fetchall()
    
    # Hitung total omzet dari database
    total_omzet = conn.execute('SELECT SUM(harga) FROM pesanan').fetchone()[0]
    if total_omzet is None:
        total_omzet = 0
        
    conn.close()
    
    return render_template('dashboard.html', pesanan=pesanan, total=total_omzet)

if __name__ == '__main__':
    app.run(debug=True)
