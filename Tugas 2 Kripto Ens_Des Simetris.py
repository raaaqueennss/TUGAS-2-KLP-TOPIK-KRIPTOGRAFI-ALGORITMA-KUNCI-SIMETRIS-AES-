import os
from tkinter import *
from tkinter import filedialog, messagebox
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64

# Fungsi untuk mengenkripsi data (teks atau file)
def encrypt_data(data, key):
    key = key.encode('utf-8')
    while len(key) < 32:
        key += b' ' 
    key = key[:32]  
    
    cipher = AES.new(key, AES.MODE_CBC)  
    ct_bytes = cipher.encrypt(pad(data, AES.block_size))
    iv = base64.b64encode(cipher.iv).decode('utf-8')
    ct = base64.b64encode(ct_bytes).decode('utf-8')
    return iv, ct

# Fungsi untuk mendekripsi data (teks atau file)
def decrypt_data(iv, ct, key):
    iv = base64.b64decode(iv)
    ct = base64.b64decode(ct)
    key = key.encode('utf-8')
    while len(key) < 32:
        key += b' '
    key = key[:32]
    
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), AES.block_size)
    return pt

# Fungsi untuk memilih file input
def choose_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        file_entry.delete(0, END)
        file_entry.insert(0, file_path)

# Fungsi untuk mengenkripsi data (baik file atau teks yang diketikkan)
def on_encrypt():
    key = key_entry.get()
    file_path = file_entry.get()
    text_data = text_entry.get()
    
    if not key or (not file_path and not text_data):
        messagebox.showerror("Error", "Kunci atau file/teks belum diisi!")
        return

    try:
        if text_data:
            iv, cipher_text = encrypt_data(text_data.encode('utf-8'), key)
            result_entry.delete(0, END)
            result_entry.insert(0, cipher_text)
            iv_entry.delete(0, END)
            iv_entry.insert(0, iv)
        elif file_path:
            with open(file_path, 'rb') as file:
                data = file.read()
            iv, cipher_text = encrypt_data(data, key)
            result_entry.delete(0, END)
            result_entry.insert(0, cipher_text)
            iv_entry.delete(0, END)
            iv_entry.insert(0, iv)

        save_button.config(state=NORMAL)
    except Exception as e:
        messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")

# Fungsi untuk mendekripsi data (baik file atau teks yang diketikkan)
def on_decrypt():
    key = key_entry.get()
    cipher_text = result_entry.get()
    iv = iv_entry.get()
    
    if not key or not cipher_text or not iv:
        messagebox.showerror("Error", "Kunci, IV, atau cipherteks tidak diisi!")
        return
    
    try:
        decrypted_data = decrypt_data(iv, cipher_text, key)
        
        # If binary data, save to file
        try:
            decoded_data = decrypted_data.decode('utf-8')
            messagebox.showinfo("Hasil Dekripsi", f"Plainteks: {decoded_data}")
        except UnicodeDecodeError:
            save_path = filedialog.asksaveasfilename(defaultextension=".bin")
            if save_path:
                with open(save_path, 'wb') as file:
                    file.write(decrypted_data)
                messagebox.showinfo("Berhasil", f"Data biner telah disimpan di {save_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")

# Fungsi untuk menyimpan hasil enkripsi ke file
def save_encrypted():
    cipher_text = result_entry.get()
    iv = iv_entry.get()
    if not cipher_text or not iv:
        messagebox.showerror("Error", "Tidak ada cipherteks untuk disimpan!")
        return
    save_path = filedialog.asksaveasfilename(defaultextension=".txt")
    if save_path:
        try:
            with open(save_path, 'w', encoding='utf-8') as file:
                file.write(f"IV: {iv}\nCiphertext: {cipher_text}")
            messagebox.showinfo("Berhasil", f"Cipherteks telah disimpan di {save_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")

# Membuat GUI dengan Tkinter
root = Tk()
root.title("AES Enkripsi dan Dekripsi")
root.geometry("600x500")

# Layout
Label(root, text="Masukkan Kunci:").pack(pady=5)
key_entry = Entry(root, width=50, show="*")
key_entry.pack(pady=5)

# Input Teks
Label(root, text="Masukkan Teks untuk Enkripsi / Dekripsi:").pack(pady=5)
text_entry = Entry(root, width=50)
text_entry.pack(pady=5)

# Input File
Label(root, text="Pilih File untuk Enkripsi / Dekripsi:").pack(pady=5)
file_entry = Entry(root, width=50)
file_entry.pack(pady=5)
choose_button = Button(root, text="Pilih File", command=choose_file)
choose_button.pack(pady=5)

# Menampilkan Hasil Enkripsi
Label(root, text="Ciphertext (Hasil Enkripsi):").pack(pady=5)
result_entry = Entry(root, width=50)
result_entry.pack(pady=5)

# Menampilkan IV
Label(root, text="IV (Initialization Vector):").pack(pady=5)
iv_entry = Entry(root, width=50)
iv_entry.pack(pady=5)

# Tombol Enkripsi dan Dekripsi
encrypt_button = Button(root, text="Enkripsi", command=on_encrypt)
encrypt_button.pack(pady=10)

decrypt_button = Button(root, text="Dekripsi", command=on_decrypt)
decrypt_button.pack(pady=10)

save_button = Button(root, text="Simpan Hasil Enkripsi", state=DISABLED, command=save_encrypted)
save_button.pack(pady=10)

root.mainloop()
