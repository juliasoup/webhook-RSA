import socket
import threading
from datetime import datetime
import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox
from crypto import generate_keys, encrypt_message, decrypt_message
import hashlib
import base64

class ChatApp:
    def __init__(self, master, is_server):
        self.master = master
        self.master.title("Chat Seguro RSA com Hashing e Base64")
        self.is_server = is_server

        self.public_key, self.private_key = None, None
        self.remote_public_key = None

        self.text_area = scrolledtext.ScrolledText(master, state='disabled', width=60, height=20)
        self.text_area.pack(padx=10, pady=10)

        self.entry_field = tk.Entry(master, width=50)
        self.entry_field.pack(side=tk.LEFT, padx=(10, 5), pady=(0, 10))

        self.send_button = tk.Button(master, text="Enviar", command=self.send_message)
        self.send_button.pack(side=tk.LEFT, padx=(5, 10), pady=(0, 10))

        self.setup_connection()

    def setup_connection(self):
        self.public_key, self.private_key = generate_keys()

        if self.is_server:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            host = "0.0.0.0"
            port = 5000
            server.bind((host, port))
            server.listen(1)
            self.conn, _ = server.accept()
        else:
            self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            host = simpledialog.askstring("Host", "Digite o host do servidor (ex: 127.0.0.1):")
            port = simpledialog.askinteger("Porta", "Digite a porta (ex: 5000):")
            self.conn.connect((host, port))

        # Troca de chaves públicas
        # Envia minha chave pública
        self.conn.sendall(f"{self.public_key[0]}|{self.public_key[1]}".encode())
        # Recebe a chave pública remota
        key_data = self.conn.recv(1024).decode()
        e_str, n_str = key_data.split("|")
        self.remote_public_key = (int(e_str), int(n_str))

        threading.Thread(target=self.receive_messages, daemon=True).start()

    def generate_hash(self, message):
        sha256 = hashlib.sha256(message.encode()).digest()
        return base64.b64encode(sha256).decode()

    def secure_package(self, message):
        hash_b64 = self.generate_hash(message)
        return f"{message}||{hash_b64}"

    def validate_package(self, package):
        try:
            message, received_hash = package.split("||")
            calculated_hash = self.generate_hash(message)
            is_valid = calculated_hash == received_hash
            return message, is_valid
        except:
            return package, False

    def receive_messages(self):
        while True:
            try:
                data = self.conn.recv(8192).decode()
                if not data:
                    break
                cipher = list(map(int, data.split(',')))
                decrypted = decrypt_message(self.private_key, cipher)
                message, valid = self.validate_package(decrypted)
                timestamp = datetime.now().strftime("%H:%M:%S")
                tag = "[VÁLIDA]" if valid else "[INVÁLIDA]"
                self.display_message(f"[Remetente - {timestamp}] {tag}: {message}")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao receber mensagem: {str(e)}")
                break

    def send_message(self):
        msg = self.entry_field.get()
        if msg:
            try:
                full_package = self.secure_package(msg)
                encrypted = encrypt_message(self.remote_public_key, full_package)
                encrypted_str = ','.join(map(str, encrypted))
                self.conn.sendall(encrypted_str.encode())
                timestamp = datetime.now().strftime("%H:%M:%S")
                self.display_message(f"[Você - {timestamp}] [ENVIADA]: {msg}")
                self.entry_field.delete(0, tk.END)
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao enviar mensagem: {str(e)}")

    def display_message(self, message):
        self.text_area.configure(state='normal')
        self.text_area.insert(tk.END, message + '\n')
        self.text_area.configure(state='disabled')
        self.text_area.see(tk.END)
