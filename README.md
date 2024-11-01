Deskripsi

Proyek ini adalah aplikasi chatroom berbasis socket UDP, di mana server bertindak sebagai perantara untuk menerima pesan dari klien dan meneruskannya ke klien lainnya. 
Aplikasi ini juga mendukung fitur otentikasi pengguna dengan password dan pengaturan username yang unik.

Kontributor

Sendi Putra Alicia - 18223063
Ni Made Sekar Jelita S. P - 18223101
Fitur

Aplikasi ini memiliki beberapa fitur utama dan opsional:

Fitur Utama
No	Spesifikasi	Nilai
Server mampu menerima pesan yang dikirim client dan mencetaknya ke layar.	
Server mampu meneruskan pesan satu client ke client lain.	
Client mampu mengirimkan pesan ke server dengan IP dan port yang ditentukan pengguna.	
Client mampu menerima pesan dari client lain (yang diteruskan oleh server), dan mencetaknya ke layar.	
Client harus memasukkan password untuk dapat bergabung ke chatroom.	
Client memiliki username yang unik.	

Fitur Opsional
Otentikasi Pengguna - Validasi pengguna menggunakan username dan password.
Cara Menjalankan

Menjalankan Server
Untuk memulai server, gunakan perintah berikut:
python3 server.py --port <nomor_port>

Menjalankan client
untuk memulai client, funakan perintah berikut:
python3 client.py --ip <alamat_ip_server> --port <nomor_port>
