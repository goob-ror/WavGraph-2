import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import base64
import hashlib
from cryptography.fernet import Fernet
import os
from PIL import Image

class BasicStringPage:
    def __init__(self, parent, colors):
        self.parent = parent
        self.colors = colors
        self.cipher = Fernet(Fernet.generate_key())

        self.icons = {
            "encode": self.load_icon("assets/first_tab/encoding.png", (20, 20)),
            "decode": self.load_icon("assets/first_tab/decoding.png", (20, 20)),
            "encrypt": self.load_icon("assets/first_tab/lock.png", (20, 20)),
            "decrypt": self.load_icon("assets/first_tab/unlock.png", (20, 20)),
            "hash": self.load_icon("assets/first_tab/md5.png", (20, 20)),
            "swap": self.load_icon("assets/first_tab/switch.png", (20, 20)) or self.load_icon("assets/switch.png", (20, 20)),
            "input": self.load_icon("assets/txt.png", (24, 24)),
            "output": self.load_icon("assets/txt.png", (24, 24)),
            "encoding": self.load_icon("assets/first_tab/encoding.png", (24, 24)),
            "encryption": self.load_icon("assets/first_tab/lock.png", (24, 24)),
            "actions": self.load_icon("assets/second_tab/program.png", (24, 24)) or self.load_icon("assets/first_tab/encoding.png", (24, 24)),
            "swap_big": self.load_icon("assets/first_tab/switch.png", (36, 36))
        }

        self.setup_ui()

    def load_icon(self, path, size):
        try:
            if os.path.exists(path):
                return ctk.CTkImage(
                    light_image=Image.open(path),
                    dark_image=Image.open(path),
                    size=size
                )
            else:
                print(f"Icon not found: {path}")
        except Exception as e:
            print(f"Error loading icon {path}: {str(e)}")
        return None

    def setup_ui(self):
        main_container = ctk.CTkFrame(self.parent, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        main_container.grid_columnconfigure(0, weight=1)
        main_container.grid_columnconfigure(1, weight=0)
        main_container.grid_columnconfigure(2, weight=1)

        left_column = ctk.CTkFrame(main_container, fg_color="transparent")
        left_column.grid(row=0, column=0, sticky="nsew", padx=(0, 5))

        input_frame = ctk.CTkFrame(left_column, fg_color=self.colors["card_bg"], corner_radius=10)
        input_frame.pack(fill="both", expand=True)

        input_header = ctk.CTkFrame(input_frame, fg_color="transparent", height=40)
        input_header.pack(fill="x", padx=15, pady=(15, 5))

        ctk.CTkLabel(
            input_header,
            text="Input Text",
            image=self.icons["input"],
            compound="left",
            font=ctk.CTkFont(family="Helvetica", size=14, weight="bold"),
            text_color=self.colors["text"],
            padx=5
        ).pack(side="left")

        self.input_text = ctk.CTkTextbox(
            input_frame,
            height=150,
            fg_color=self.colors["medium_bg"],
            text_color=self.colors["text"],
            border_width=0,
            corner_radius=8
        )
        self.input_text.pack(fill="both", expand=True, padx=15, pady=(5, 15))

        center_column = ctk.CTkFrame(main_container, fg_color="transparent", width=60)
        center_column.grid(row=0, column=1, sticky="ns")

        swap_container = ctk.CTkFrame(center_column, fg_color="transparent")
        swap_container.pack(fill="y", expand=True)

        swap_btn = ctk.CTkButton(
            swap_container,
            text="",
            image=self.icons["swap_big"],
            command=self.swap_text,
            fg_color=self.colors["accent"],
            hover_color=self.colors["accent_hover"],
            corner_radius=8,
            width=30,
            height=30
        )
        swap_btn.pack(pady=(100, 0))

        self.create_tooltip(swap_btn, "Swap Input and Output")

        right_column = ctk.CTkFrame(main_container, fg_color="transparent")
        right_column.grid(row=0, column=2, sticky="nsew", padx=(5, 0))

        output_frame = ctk.CTkFrame(right_column, fg_color=self.colors["card_bg"], corner_radius=10)
        output_frame.pack(fill="both", expand=True)

        output_header = ctk.CTkFrame(output_frame, fg_color="transparent", height=40)
        output_header.pack(fill="x", padx=15, pady=(15, 5))

        ctk.CTkLabel(
            output_header,
            text="Results",
            image=self.icons["output"],
            compound="left",
            font=ctk.CTkFont(family="Helvetica", size=14, weight="bold"),
            text_color=self.colors["text"],
            padx=5
        ).pack(side="left")

        self.output_text = ctk.CTkTextbox(
            output_frame,
            height=150,
            fg_color=self.colors["medium_bg"],
            text_color=self.colors["text"],
            border_width=0,
            corner_radius=8,
            state="disabled"
        )
        self.output_text.pack(fill="both", expand=True, padx=15, pady=(5, 15))

        options_container = ctk.CTkFrame(self.parent, fg_color="transparent")
        options_container.pack(fill="x", padx=20, pady=(0, 10))
        options_container.grid_columnconfigure(0, weight=1)
        options_container.grid_columnconfigure(1, weight=1)

        encoding_frame = ctk.CTkFrame(options_container, fg_color=self.colors["card_bg"], corner_radius=10)
        encoding_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        encoding_header = ctk.CTkFrame(encoding_frame, fg_color="transparent", height=40)
        encoding_header.pack(fill="x", padx=15, pady=(15, 5))

        ctk.CTkLabel(
            encoding_header,
            text="Encoding Method",
            image=self.icons["encoding"],
            compound="left",
            font=ctk.CTkFont(family="Helvetica", size=14, weight="bold"),
            text_color=self.colors["text"],
            padx=5
        ).pack(side="left")

        self.encoding_var = tk.StringVar(value="base64")
        encoding_options = ctk.CTkFrame(encoding_frame, fg_color="transparent")
        encoding_options.pack(fill="x", padx=15, pady=(5, 15))

        encoding_methods = ["base64", "hex", "unicode", "ASCII"]
        encoding_display = [method.capitalize() for method in encoding_methods]

        encoding_row = ctk.CTkFrame(encoding_options, fg_color="transparent")
        encoding_row.pack(fill="x", padx=10, pady=8)

        ctk.CTkLabel(
            encoding_row,
            text="Select method:",
            font=ctk.CTkFont(family="Helvetica", size=12),
            text_color=self.colors["text"]
        ).pack(side="left", padx=(0, 10))

        encoding_menu = ctk.CTkOptionMenu(
            encoding_row,
            values=encoding_display,
            command=lambda choice: self.update_encoding_var(choice, encoding_display, encoding_methods),
            fg_color=self.colors["accent"],
            button_color=self.colors["accent_hover"],
            button_hover_color=self.colors["accent_hover"],
            dropdown_fg_color=self.colors["card_bg"],
            dropdown_hover_color=self.colors["medium_bg"],
            dropdown_text_color=self.colors["text"],
            font=ctk.CTkFont(family="Helvetica", size=12)
        )
        encoding_menu.pack(side="left", fill="x", expand=True)
        encoding_menu.set(encoding_display[0])

        encryption_frame = ctk.CTkFrame(options_container, fg_color=self.colors["card_bg"], corner_radius=10)
        encryption_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        encryption_header = ctk.CTkFrame(encryption_frame, fg_color="transparent", height=40)
        encryption_header.pack(fill="x", padx=15, pady=(15, 5))

        ctk.CTkLabel(
            encryption_header,
            text="Encryption Method",
            image=self.icons["encryption"],
            compound="left",
            font=ctk.CTkFont(family="Helvetica", size=14, weight="bold"),
            text_color=self.colors["text"],
            padx=5
        ).pack(side="left")

        self.encryption_var = tk.StringVar(value="fernet")
        encryption_options = ctk.CTkFrame(encryption_frame, fg_color="transparent")
        encryption_options.pack(fill="x", padx=15, pady=(5, 15))

        encryption_methods = [("Fernet (AES)", "fernet"), ("XOR", "xor"), ("Caesar Cipher", "caesar")]
        encryption_display = [name for name, _ in encryption_methods]
        encryption_values = [value for _, value in encryption_methods]

        encryption_row = ctk.CTkFrame(encryption_options, fg_color="transparent")
        encryption_row.pack(fill="x", padx=10, pady=8)

        ctk.CTkLabel(
            encryption_row,
            text="Select method:",
            font=ctk.CTkFont(family="Helvetica", size=12),
            text_color=self.colors["text"]
        ).pack(side="left", padx=(0, 10))

        encryption_menu = ctk.CTkOptionMenu(
            encryption_row,
            values=encryption_display,
            command=lambda choice: self.update_encryption_var(choice, encryption_display, encryption_values),
            fg_color=self.colors["accent"],
            button_color=self.colors["accent_hover"],
            button_hover_color=self.colors["accent_hover"],
            dropdown_fg_color=self.colors["card_bg"],
            dropdown_hover_color=self.colors["medium_bg"],
            dropdown_text_color=self.colors["text"],
            font=ctk.CTkFont(family="Helvetica", size=12)
        )
        encryption_menu.pack(side="left", fill="x", expand=True)
        encryption_menu.set(encryption_display[0])

        key_row = ctk.CTkFrame(encryption_options, fg_color="transparent")
        key_row.pack(fill="x", padx=10, pady=(8, 0))

        ctk.CTkLabel(
            key_row,
            text="Encryption Key:",
            font=ctk.CTkFont(family="Helvetica", size=12),
            text_color=self.colors["text"]
        ).pack(side="left", padx=(0, 10))

        self.encryption_key = ctk.CTkEntry(
            key_row,
            placeholder_text="Enter key (optional)",
            fg_color=self.colors["medium_bg"],
            text_color=self.colors["text"],
            border_width=0,
            corner_radius=8,
            font=ctk.CTkFont(family="Helvetica", size=12)
        )
        self.encryption_key.pack(side="left", fill="x", expand=True)

        buttons_frame = ctk.CTkFrame(self.parent, fg_color=self.colors["card_bg"], corner_radius=10)
        buttons_frame.pack(fill="x", padx=20, pady=(0, 20))

        buttons_header = ctk.CTkFrame(buttons_frame, fg_color="transparent", height=40)
        buttons_header.pack(fill="x", padx=15, pady=(15, 5))

        ctk.CTkLabel(
            buttons_header,
            text="Actions",
            image=self.icons["actions"],
            compound="left",
            font=ctk.CTkFont(family="Helvetica", size=14, weight="bold"),
            text_color=self.colors["text"],
            padx=5
        ).pack(side="left")

        button_grid = ctk.CTkFrame(buttons_frame, fg_color="transparent")
        button_grid.pack(fill="x", padx=15, pady=(5, 15))

        actions = [
            ("encode", "Encode", self.encode_text),
            ("decode", "Decode", self.decode_text),
            ("encrypt", "Encrypt", self.encrypt_text),
            ("decrypt", "Decrypt", self.decrypt_text),
            ("hash", "Hash", self.hash_text)
        ]

        for i, (icon_key, text, command) in enumerate(actions):
            btn = ctk.CTkButton(
                button_grid,
                text=text,
                image=self.icons.get(icon_key),
                compound="left",
                command=command,
                fg_color=self.colors["accent"],
                hover_color=self.colors["accent_hover"],
                text_color="#FFFFFF",
                font=ctk.CTkFont(family="Helvetica", size=13, weight="bold"),
                corner_radius=8,
                height=40,
                width=120,
            )
            btn.grid(row=0, column=i, padx=8, pady=5, sticky="ew")
            button_grid.grid_columnconfigure(i, weight=1)

    def encode_text(self):
        text = self.input_text.get("1.0", "end-1c")
        if text:
            encoding_method = self.encoding_var.get()
            try:
                if encoding_method == "base64":
                    encoded = base64.b64encode(text.encode()).decode()
                elif encoding_method == "hex":
                    encoded = text.encode().hex()
                elif encoding_method == "unicode":
                    encoded = "".join([f"\\u{ord(c):04x}" for c in text])
                elif encoding_method == "ASCII":
                    encoded = "".join([f"\\x{ord(c):02x}" for c in text])
                else:
                    encoded = base64.b64encode(text.encode()).decode()

                self.output_text.configure(state="normal")
                self.output_text.delete("1.0", "end")
                self.output_text.insert("1.0", encoded)
                self.output_text.configure(state="disabled")
            except Exception as e:
                messagebox.showerror("Error", f"Encoding error: {str(e)}")
        else:
            messagebox.showwarning("Warning", "Please enter text to encode.")

    def decode_text(self):
        text = self.input_text.get("1.0", "end-1c")
        if text:
            encoding_method = self.encoding_var.get()
            try:
                if encoding_method == "base64":
                    decoded = base64.b64decode(text).decode()
                elif encoding_method == "hex":
                    decoded = bytes.fromhex(text).decode()
                elif encoding_method == "unicode":
                    decoded = text.encode('utf-8').decode('unicode_escape')
                elif encoding_method == "ASCII":
                    decoded = text.encode('utf-8').decode('unicode_escape')
                else:
                    decoded = base64.b64decode(text).decode()

                self.output_text.configure(state="normal")
                self.output_text.delete("1.0", "end")
                self.output_text.insert("1.0", decoded)
                self.output_text.configure(state="disabled")
            except Exception as e:
                messagebox.showerror("Error", f"Decoding error: {str(e)}")
        else:
            messagebox.showwarning("Warning", "Please enter text to decode.")

    def encrypt_text(self):
        text = self.input_text.get("1.0", "end-1c")
        if text:
            encryption_method = self.encryption_var.get()
            user_key = self.encryption_key.get().strip()
            try:
                if encryption_method == "fernet":
                    cipher = self.get_encryption_cipher(user_key if user_key else None)
                    encrypted = cipher.encrypt(text.encode()).decode()
                elif encryption_method == "xor":
                    key = hash(user_key) % 256 if user_key else 42
                    encrypted = "".join([chr(ord(c) ^ key) for c in text])
                    encrypted = base64.b64encode(encrypted.encode()).decode()
                elif encryption_method == "caesar":
                    shift = len(user_key) % 26 if user_key else 3
                    encrypted = "".join([chr((ord(c) - 32 + shift) % 94 + 32) if 32 <= ord(c) < 126 else c for c in text])
                else:
                    cipher = self.get_encryption_cipher(user_key if user_key else None)
                    encrypted = cipher.encrypt(text.encode()).decode()

                self.output_text.configure(state="normal")
                self.output_text.delete("1.0", "end")
                self.output_text.insert("1.0", encrypted)
                self.output_text.configure(state="disabled")
            except Exception as e:
                messagebox.showerror("Error", f"Encryption error: {str(e)}")
        else:
            messagebox.showwarning("Warning", "Please enter text to encrypt.")

    def decrypt_text(self):
        text = self.input_text.get("1.0", "end-1c")
        if text:
            encryption_method = self.encryption_var.get()
            user_key = self.encryption_key.get().strip()
            try:
                if encryption_method == "fernet":
                    cipher = self.get_encryption_cipher(user_key if user_key else None)
                    decrypted = cipher.decrypt(text.encode()).decode()
                elif encryption_method == "xor":
                    key = hash(user_key) % 256 if user_key else 42
                    decoded = base64.b64decode(text).decode()
                    decrypted = "".join([chr(ord(c) ^ key) for c in decoded])
                elif encryption_method == "caesar":
                    shift = -(len(user_key) % 26) if user_key else -3
                    decrypted = "".join([chr((ord(c) - 32 + shift) % 94 + 32) if 32 <= ord(c) < 126 else c for c in text])
                else:
                    cipher = self.get_encryption_cipher(user_key if user_key else None)
                    decrypted = cipher.decrypt(text.encode()).decode()

                self.output_text.configure(state="normal")
                self.output_text.delete("1.0", "end")
                self.output_text.insert("1.0", decrypted)
                self.output_text.configure(state="disabled")
            except Exception as e:
                messagebox.showerror("Error", f"Decryption error: {str(e)}")
        else:
            messagebox.showwarning("Warning", "Please enter text to decrypt.")

    def hash_text(self):
        text = self.input_text.get("1.0", "end-1c")
        if text:
            hashed = hashlib.sha256(text.encode()).hexdigest()
            self.output_text.configure(state="normal")
            self.output_text.delete("1.0", "end")
            self.output_text.insert("1.0", hashed)
            self.output_text.configure(state="disabled")
        else:
            messagebox.showwarning("Warning", "Please enter text to hash.")

    def update_encryption_var(self, choice, display_list, value_list):
        if choice in display_list:
            index = display_list.index(choice)
            self.encryption_var.set(value_list[index])

    def update_encoding_var(self, choice, display_list, value_list):
        if choice in display_list:
            index = display_list.index(choice)
            self.encoding_var.set(value_list[index])

    def get_encryption_cipher(self, key=None):
        if key:
            key_bytes = key.encode('utf-8')
            # Pad or truncate to 32 bytes for Fernet
            if len(key_bytes) < 32:
                key_bytes = key_bytes.ljust(32, b'0')
            else:
                key_bytes = key_bytes[:32]
            # Encode to base64 for Fernet
            fernet_key = base64.urlsafe_b64encode(key_bytes)
            return Fernet(fernet_key)
        else:
            return self.cipher

    def swap_text(self):
        input_content = self.input_text.get("1.0", "end-1c")
        self.output_text.configure(state="normal")
        output_content = self.output_text.get("1.0", "end-1c")
        self.input_text.delete("1.0", "end")
        self.input_text.insert("1.0", output_content)
        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", input_content)
        self.output_text.configure(state="disabled")
        if not input_content and not output_content:
            messagebox.showinfo("Info", "Both input and output areas are empty.")

    def create_tooltip(self, widget, text):
        """Create a tooltip for a given widget with the specified text."""

        def enter(event):
            tooltip = tk.Toplevel(widget)
            tooltip.wm_overrideredirect(True)

            x, y, _, _ = widget.bbox("insert")
            x += widget.winfo_rootx() + 25
            y += widget.winfo_rooty() + 25

            label = tk.Label(tooltip, text=text, justify="left",
                             background=self.colors["card_bg"],
                             foreground=self.colors["text"],
                             relief="solid", borderwidth=1,
                             font=("Helvetica", 10, "normal"))
            label.pack(padx=5, pady=5)

            tooltip.wm_geometry(f"+{x}+{y}")

            widget.tooltip = tooltip

        def leave(event):
            if hasattr(widget, "tooltip"):
                widget.tooltip.destroy()

        widget.bind("<Enter>", enter)
        widget.bind("<Leave>", leave)
