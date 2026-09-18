# Tanyain: Multi-Tenant AI Customer Service & Automated Ordering System 🚀

**Tanyain** adalah platform SaaS (Software as a Service) berbasis AI yang dirancang khusus untuk membantu UMKM/SME dan sekolah dalam mengotomatisasi layanan pelanggan (*Customer Service*). Sistem ini mengintegrasikan pencarian jawaban otomatis menggunakan kecerdasan buatan berbasis **TF-IDF (Term Frequency-Inverse Document Frequency)** dengan fitur otomasi pemesanan (*Automated Ordering System*).

Platform ini mengadopsi arsitektur **Multi-Tenant**, memungkinkan banyak bisnis/klien mendaftar, mengelola FAQ mereka sendiri, dan memiliki halaman *public chat widget* khusus menggunakan keunikan URL slug masing-masing.

---

## 📺 Demo Aplikasi (Video)

Lihat bagaimana **Tanyain** bekerja secara langsung melalui video demonstrasi berikut:

1. **[Demo Utama: AI Chatbot Otomatis untuk Bisnis & UMKM](https://youtu.be/n5JUtc0aTcA)**
   *Menampilkan alur lengkap manajemen multi-tenant, upload massal FAQ via CSV, serta visualisasi dashboard analitik performa chat secara real-time.*

2. **[Demo Fitur CS 24/7: Admin Mudik? Toko Tetap Jalan!](https://youtu.be/iGgr0OmKriQ)**
   *Menampilkan simulasi bagaimana AI chatbot merespons pertanyaan pelanggan secara instan dan akurat demi menjaga operasional bisnis tanpa henti.*

---

## 🌟 Fitur Utama

* **Multi-Tenant Architecture:** Manajemen multi-klien berbasis *slug* dinamis dan sistem persetujuan superadmin (*Super Admin Approval*).
* **AI FAQ Assistant (TF-IDF):** Pencarian jawaban cerdas dan kontekstual menggunakan modul `scikit-learn` dengan mekanisme ambang batas (*threshold*) untuk akurasi optimal.
* **Automated Ordering System:** Alur penangkapan pesanan otomatis langsung dari ruang obrolan (*chat*) yang divalidasi oleh sistem backend.
* **SSOT Integration Ready (Fase II):** Menyediakan rute webhook `/submit_order` yang siap dihubungkan ke platform otomatisasi seperti **Make.com** untuk diteruskan ke Single Source of Truth (SSOT) seperti **Airtable**.
* **Secure Config & Environment Variables:** Menggunakan modul `os` untuk memisahkan konfigurasi sensitif (API/Webhook) dari kode utama demi keamanan tingkat tinggi.
* **Dashboard & Analytics:** Dilengkapi dengan visualisasi data grafik total chat, statistik pertanyaan yang paling sering ditanyakan (*most asked*), serta rasio chat terjawab dan tidak terjawab.
* **Bulk Data Management & QR Code:** Fitur unggah masal data FAQ via CSV, ekspor data, serta generator QR Code otomatis untuk setiap *slug* toko klien.

---

## 🛠️ Tech Stack

* **Backend Framework:** Python (Flask)
* **Database & ORM:** SQLite & Flask-SQLAlchemy (dengan skema `SQLAlchemy Enum` untuk *Role Management*)
* **AI/Machine Learning:** Scikit-learn (`TfidfVectorizer`, `cosine_similarity`)
* **Frontend UI:** HTML5, Tailwind CSS (Responsive Layout), JavaScript (Fetch API)
* **Security:** Werkzeug (`generate_password_hash`, `check_password_hash`)
* **Integrations:** Requests (HTTP Client), Qrcode (Python Library)

---

## 📐 Arsitektur Sistem & Alur Kerja

Aplikasi ini memisahkan logika pencarian informasi produk (FAQ) dengan alur pemesanan barang untuk efisiensi performa:

1.  **Mekanisme FAQ:** Pesan pengguna -> Ekstraksi Vektor TF-IDF -> Perhitungan Cosine Similarity -> *Fallback Check* -> Respons Bot.
2.  **Mekanisme Order (SSOT):** Pemicu Tombol Order -> Pengisian Data di Frontend -> Validasi Sesi Backend (`/submit_order`) -> Secure `os.environ` Check -> Webhook HTTP POST -> Make.com -> Airtable Database.

---

## 🚀 Panduan Instalasi & Penggunaan Lokal

### 1. Prasyarat (Prerequisites)
Pastikan Anda sudah menginstal Python versi 3.8 atau yang lebih baru di komputer Anda.

### 2. Clone Repositori
```bash
git clone [https://github.com/Gayoyo/Tanyain-Customer-Service.git](https://github.com/Gayoyo/Tanyain-Customer-Service.git)
cd Tanyain-Customer-Service

3. Install Dependencies
Instal seluruh library Python yang dibutuhkan melalui terminal:
pip install flask flask_sqlalchemy flask_cors scikit-learn requests qrcode werkzeug

4. Konfigurasi Environment Variables (Secrets)
Sistem ini menggunakan pengondisian variabel lingkungan demi keamanan. Buatlah konfigurasi lingkungan pada platform hosting Anda (seperti Replit Secrets) dengan kunci berikut:

-MAKE_WEBHOOK_URL : URL Webhook resmi dari skenario Make.com Anda.

-SECRET_KEY : String acak untuk mengamankan sesi Flask.

5. Jalankan Aplikasi
python app.py

Aplikasi akan berjalan secara lokal di alamat http://127.0.0.1:5000/.

🔐 Manajemen Hak Akses (Role Management)
-Super Admin: Mengakses halaman /superadmin untuk melakukan peninjauan dan aktivasi/persetujuan (approval) terhadap akun klien baru yang mendaftar.

-Client (Merchant/SME): Mengakses dashboard utama untuk mengelola basis data FAQ (tambah, edit, hapus, unggah CSV), melihat analitik, serta mendapatkan QR Code toko.

-End User (Customer): Mengakses halaman publik /chat/<slug_klien> untuk berinteraksi dengan AI Assistant toko dan melakukan order.

📝 Catatan Keamanan
Kodingan ini telah memenuhi standar 12-Factor App dalam pemisahan konfigurasi dan fungsionalitas kode.
Seluruh URL integrasi pihak ketiga eksternal tidak ditulis secara mentah (hardcoded),
melainkan dimuat secara dinamis melalui objek os.environ guna mencegah kebocoran kredensial di repositori publik



```bash
git clone [https://github.com/Gayoyo/Tanyain-Customer-Service.git](https://github.com/Gayoyo/Tanyain-Customer-Service.git)
cd Tanyain-Customer-Service
