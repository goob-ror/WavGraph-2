import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import numpy as np
import io
import os
import base64
from cryptography.fernet import Fernet

class ImageProcessingPage:
    def __init__(self, parent, colors):
        self.parent = parent
        self.colors = colors
        self.image_path = None
        self.image_data = None
        self.cipher = Fernet(Fernet.generate_key())

        self.icons = {
            "image_ops": self.load_icon("assets/second_tab/gallery.png", (24, 24)),
            "steganography": self.load_icon("assets/second_tab/program.png", (24, 24)),
            "preview": self.load_icon("assets/second_tab/gallery.png", (24, 24)),
            "select": self.load_icon("assets/second_tab/folder.png", (20, 20)),
            "encode": self.load_icon("assets/first_tab/lock.png", (20, 20)),
            "decode": self.load_icon("assets/first_tab/unlock.png", (20, 20)),
            "save": self.load_icon("assets/second_tab/gallery.png", (20, 20))
        }

        self.setup_ui()

    def load_icon(self, path, size):
        if os.path.exists(path):
            return ctk.CTkImage(
                light_image=Image.open(path),
                dark_image=Image.open(path),
                size=size
            )
        return None

    def setup_ui(self):
        main_container = ctk.CTkFrame(self.parent, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)

        main_container.grid_columnconfigure(0, weight=1)
        main_container.grid_columnconfigure(1, weight=2)
        main_container.grid_rowconfigure(0, weight=1)

        left_panel = ctk.CTkScrollableFrame(
            main_container,
            fg_color="transparent",
            scrollbar_button_color=self.colors["accent"],
            scrollbar_button_hover_color=self.colors["accent_hover"],
            width=300,
            height=500
        )
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        img_select_frame = ctk.CTkFrame(left_panel, fg_color=self.colors["card_bg"], corner_radius=10)
        img_select_frame.pack(fill="x", pady=(0, 15))

        img_header = ctk.CTkFrame(img_select_frame, fg_color="transparent", height=40)
        img_header.pack(fill="x", padx=15, pady=(15, 5))

        ctk.CTkLabel(
            img_header,
            text="Image Operations",
            image=self.icons["image_ops"],
            compound="left",
            font=ctk.CTkFont(family="Helvetica", size=14, weight="bold"),
            text_color=self.colors["text"],
            padx=5
        ).pack(side="left")

        select_btn = ctk.CTkButton(
            img_select_frame,
            text="Select Image",
            image=self.icons["select"],
            compound="left",
            command=self.select_image,
            fg_color=self.colors["accent"],
            hover_color=self.colors["accent_hover"],
            text_color="#FFFFFF",
            font=ctk.CTkFont(family="Helvetica", size=12, weight="bold"),
            corner_radius=8,
            height=32,
            border_spacing=10
        )
        select_btn.pack(padx=15, pady=(5, 10), fill="x")

        encoding_label = ctk.CTkLabel(
            img_select_frame,
            text="Encoding Method:",
            font=ctk.CTkFont(family="Helvetica", size=12),
            text_color=self.colors["text"]
        )
        encoding_label.pack(anchor="w", padx=15, pady=(5, 0))

        self.steg_encoding_var = tk.StringVar(value="none")
        encoding_methods = ["None", "Base64", "ASCII", "Reverse Bits"]

        self.encoding_menu = ctk.CTkOptionMenu(
            img_select_frame,
            values=encoding_methods,
            variable=self.steg_encoding_var,
            fg_color=self.colors["medium_bg"],
            button_color=self.colors["accent"],
            button_hover_color=self.colors["accent_hover"],
            dropdown_fg_color=self.colors["card_bg"],
            dropdown_hover_color=self.colors["medium_bg"],
            dropdown_text_color=self.colors["text"],
            font=ctk.CTkFont(family="Helvetica", size=12),
            width=120
        )
        self.encoding_menu.pack(padx=15, pady=(0, 10), fill="x")

        encryption_label = ctk.CTkLabel(
            img_select_frame,
            text="Encryption Method:",
            font=ctk.CTkFont(family="Helvetica", size=12),
            text_color=self.colors["text"]
        )
        encryption_label.pack(anchor="w", padx=15, pady=(5, 0))

        self.steg_encryption_var = tk.StringVar(value="none")
        encryption_methods = ["None", "Fernet (AES)", "XOR", "Caesar Cipher"]

        self.encryption_menu = ctk.CTkOptionMenu(
            img_select_frame,
            values=encryption_methods,
            variable=self.steg_encryption_var,
            fg_color=self.colors["medium_bg"],
            button_color=self.colors["accent"],
            button_hover_color=self.colors["accent_hover"],
            dropdown_fg_color=self.colors["card_bg"],
            dropdown_hover_color=self.colors["medium_bg"],
            dropdown_text_color=self.colors["text"],
            font=ctk.CTkFont(family="Helvetica", size=12),
            width=120
        )
        self.encryption_menu.pack(padx=15, pady=(0, 10), fill="x")

        key_label = ctk.CTkLabel(
            img_select_frame,
            text="Encryption Key:",
            font=ctk.CTkFont(family="Helvetica", size=12),
            text_color=self.colors["text"]
        )
        key_label.pack(anchor="w", padx=15, pady=(5, 0))

        self.encryption_key = ctk.CTkEntry(
            img_select_frame,
            placeholder_text="Enter encryption key (leave empty for auto-generated)",
            fg_color=self.colors["medium_bg"],
            text_color=self.colors["text"],
            border_width=0,
            corner_radius=8,
            font=ctk.CTkFont(family="Helvetica", size=12)
        )
        self.encryption_key.pack(padx=15, pady=(0, 15), fill="x")

        steg_frame = ctk.CTkFrame(left_panel, fg_color=self.colors["card_bg"], corner_radius=10)
        steg_frame.pack(fill="x", pady=(0, 15))

        steg_header = ctk.CTkFrame(steg_frame, fg_color="transparent", height=40)
        steg_header.pack(fill="x", padx=15, pady=(15, 5))

        ctk.CTkLabel(
            steg_header,
            text="Steganography",
            image=self.icons["steganography"],
            compound="left",
            font=ctk.CTkFont(family="Helvetica", size=14, weight="bold"),
            text_color=self.colors["text"],
            padx=5
        ).pack(side="left")

        message_label = ctk.CTkLabel(
            steg_frame,
            text="Secret Message:",
            font=ctk.CTkFont(family="Helvetica", size=12),
            text_color=self.colors["text"]
        )
        message_label.pack(anchor="w", padx=15, pady=(10, 5))

        self.steg_message = ctk.CTkTextbox(
            steg_frame,
            height=80,
            fg_color=self.colors["medium_bg"],
            text_color=self.colors["text"],
            border_width=0,
            corner_radius=8
        )
        self.steg_message.pack(padx=15, pady=(0, 10), fill="x")

        steg_buttons = ctk.CTkFrame(steg_frame, fg_color="transparent")
        steg_buttons.pack(fill="x", padx=15, pady=(0, 15))
        steg_buttons.grid_columnconfigure(0, weight=1)
        steg_buttons.grid_columnconfigure(1, weight=1)

        encode_btn = ctk.CTkButton(
            steg_buttons,
            text="Encode",
            image=self.icons["encode"],
            compound="left",
            command=self.encode_steganography,
            fg_color=self.colors["accent"],
            hover_color=self.colors["accent_hover"],
            text_color="#FFFFFF",
            font=ctk.CTkFont(family="Helvetica", size=12, weight="bold"),
            corner_radius=8,
            height=32,
            border_spacing=10
        )
        encode_btn.grid(row=0, column=0, padx=(0, 5), pady=5, sticky="ew")

        decode_btn = ctk.CTkButton(
            steg_buttons,
            text="Decode",
            image=self.icons["decode"],
            compound="left",
            command=self.decode_steganography,
            fg_color=self.colors["accent"],
            hover_color=self.colors["accent_hover"],
            text_color="#FFFFFF",
            font=ctk.CTkFont(family="Helvetica", size=12, weight="bold"),
            corner_radius=8,
            height=32,
            border_spacing=10
        )
        decode_btn.grid(row=0, column=1, padx=(5, 0), pady=5, sticky="ew")

        action_buttons = ctk.CTkFrame(steg_frame, fg_color="transparent")
        action_buttons.pack(fill="x", padx=15, pady=(0, 15))
        action_buttons.grid_columnconfigure(0, weight=1)
        action_buttons.grid_columnconfigure(1, weight=1)

        view_btn = ctk.CTkButton(
            action_buttons,
            text="View Message",
            image=self.icons["preview"],
            compound="left",
            command=self.view_secret_message,
            fg_color=self.colors["secondary"],
            hover_color=self.colors["accent_hover"],
            text_color="#FFFFFF",
            font=ctk.CTkFont(family="Helvetica", size=12, weight="bold"),
            corner_radius=8,
            height=32,
            border_spacing=10
        )
        view_btn.grid(row=0, column=0, padx=(0, 5), pady=5, sticky="ew")

        save_btn = ctk.CTkButton(
            action_buttons,
            text="Save Image",
            image=self.icons["save"],
            compound="left",
            command=self.save_image,
            fg_color=self.colors["secondary"],
            hover_color=self.colors["accent_hover"],
            text_color="#FFFFFF",
            font=ctk.CTkFont(family="Helvetica", size=12, weight="bold"),
            corner_radius=8,
            height=32,
            border_spacing=10
        )
        save_btn.grid(row=0, column=1, padx=(5, 0), pady=5, sticky="ew")

        right_scroll_container = ctk.CTkScrollableFrame(
            main_container,
            fg_color="transparent",
            orientation="vertical",
            scrollbar_button_color=self.colors["accent"],
            scrollbar_button_hover_color=self.colors["accent_hover"],
            width=500,
            height=500
        )
        right_scroll_container.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        right_panel = ctk.CTkFrame(right_scroll_container, fg_color="transparent")
        right_panel.pack(fill="both", expand=True)

        preview_frame = ctk.CTkFrame(right_panel, fg_color=self.colors["card_bg"], corner_radius=10)
        preview_frame.pack(fill="both", expand=True)

        preview_header = ctk.CTkFrame(preview_frame, fg_color="transparent", height=40)
        preview_header.pack(fill="x", padx=15, pady=(15, 5))

        ctk.CTkLabel(
            preview_header,
            text="Image Preview",
            image=self.icons["preview"],
            compound="left",
            font=ctk.CTkFont(family="Helvetica", size=14, weight="bold"),
            text_color=self.colors["text"],
            padx=5
        ).pack(side="left")

        preview_container = ctk.CTkFrame(preview_frame, fg_color=self.colors["medium_bg"], corner_radius=8)
        preview_container.pack(fill="both", expand=True, padx=15, pady=(5, 15))

        self.image_preview = ctk.CTkLabel(
            preview_container,
            text="No image selected\nSelect an image to preview",
            font=ctk.CTkFont(family="Helvetica", size=14),
            text_color=self.colors["text_secondary"]
        )
        self.image_preview.pack(fill="both", expand=True, padx=10, pady=10)

    def select_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")]
        )

        if file_path:
            try:
                self.image_path = file_path
                img = Image.open(file_path)
                if img.mode not in ['RGB', 'RGBA']:
                    img = img.convert('RGB')
                self.image_data = img
                self.update_image_preview()
                messagebox.showinfo("Success", "Image loaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {str(e)}")

    def update_image_preview(self):
        if self.image_data:
            img_copy = self.image_data.copy()

            max_display_width = 450
            max_display_height = 400

            img_width, img_height = img_copy.size
            scale_width = max_display_width / img_width
            scale_height = max_display_height / img_height
            scale_factor = min(scale_width, scale_height, 1.0)

            new_width = int(img_width * scale_factor)
            new_height = int(img_height * scale_factor)

            img_copy = img_copy.resize((new_width, new_height), Image.Resampling.LANCZOS)

            border_size = 5
            mode = img_copy.mode
            size = (img_copy.width + 2*border_size, img_copy.height + 2*border_size)

            if mode in ('RGBA', 'LA') or (mode == 'P' and 'transparency' in img_copy.info):
                border_color = self.hex_to_rgb(self.colors["accent"])
                bg = Image.new(mode, size, border_color + (255,) if len(border_color) == 3 else border_color)
            else:
                border_color = self.hex_to_rgb(self.colors["accent"])
                bg = Image.new(mode, size, border_color)

            bg.paste(img_copy, (border_size, border_size))

            display_width = min(bg.width, max_display_width)
            display_height = min(bg.height, max_display_height)

            ctk_image = ctk.CTkImage(light_image=bg, dark_image=bg, size=(display_width, display_height))

            self.image_preview.configure(
                image=ctk_image,
                text="",
                fg_color="transparent"
            )

    def hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

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

    def encrypt_message(self, message):
        encryption_method = self.steg_encryption_var.get()
        user_key = self.encryption_key.get().strip()

        if encryption_method == "None":
            return message

        try:
            if encryption_method == "Fernet (AES)":
                cipher = self.get_encryption_cipher(user_key if user_key else None)
                encrypted = cipher.encrypt(message.encode()).decode()
                return encrypted
            elif encryption_method == "XOR":
                key = hash(user_key) % 256 if user_key else 42
                encrypted = "".join([chr(ord(c) ^ key) for c in message])
                return base64.b64encode(encrypted.encode()).decode()
            elif encryption_method == "Caesar Cipher":
                shift = len(user_key) % 26 if user_key else 3
                encrypted = "".join([chr((ord(c) - 32 + shift) % 94 + 32) if 32 <= ord(c) < 126 else c for c in message])
                return encrypted
            else:
                return message
        except Exception as e:
            messagebox.showerror("Encryption Error", f"Failed to encrypt message: {str(e)}")
            return message

    def decrypt_message(self, encrypted_message):
        encryption_method = self.steg_encryption_var.get()
        user_key = self.encryption_key.get().strip()

        if encryption_method == "None":
            return encrypted_message

        try:
            if encryption_method == "Fernet (AES)":
                cipher = self.get_encryption_cipher(user_key if user_key else None)
                decrypted = cipher.decrypt(encrypted_message.encode()).decode()
                return decrypted
            elif encryption_method == "XOR":
                key = hash(user_key) % 256 if user_key else 42
                decoded = base64.b64decode(encrypted_message).decode()
                decrypted = "".join([chr(ord(c) ^ key) for c in decoded])
                return decrypted
            elif encryption_method == "Caesar Cipher":
                shift = -(len(user_key) % 26) if user_key else -3
                decrypted = "".join([chr((ord(c) - 32 + shift) % 94 + 32) if 32 <= ord(c) < 126 else c for c in encrypted_message])
                return decrypted
            else:
                return encrypted_message
        except Exception as e:
            messagebox.showerror("Decryption Error", f"Failed to decrypt message: {str(e)}")
            return encrypted_message

    def encode_steganography(self):
        if not self.image_data:
            messagebox.showwarning("Warning", "Please select an image first.")
            return

        message = self.steg_message.get("1.0", "end-1c")
        if not message:
            messagebox.showwarning("Warning", "Please enter a message to hide.")
            return

        try:
            if self.image_data.mode not in ['RGB', 'RGBA']:
                self.image_data = self.image_data.convert('RGB')

            encrypted_message = self.encrypt_message(message)

            encoding_method = self.steg_encoding_var.get()

            if encoding_method == "Base64":
                encrypted_message = base64.b64encode(encrypted_message.encode()).decode()
            elif encoding_method == "ASCII":
                encrypted_message = "".join([f"\\x{ord(c):02x}" for c in encrypted_message])
            elif encoding_method == "Reverse Bits":
                encrypted_message = "".join([chr(int(format(ord(c), '08b')[::-1], 2)) for c in encrypted_message])

            img_array = np.array(self.image_data, dtype=np.uint8)

            binary_message = ''.join(format(ord(char), '08b') for char in encrypted_message)
            binary_message += '00000000'

            if img_array.size < len(binary_message):
                messagebox.showerror("Error", "Image too small for the message.")
                return

            flat_array = img_array.flatten()

            for i in range(len(binary_message)):
                bit = int(binary_message[i])
                flat_array[i] = (flat_array[i] & 0xFE) | bit

            steg_array = flat_array.reshape(img_array.shape)

            self.image_data = Image.fromarray(steg_array, mode=self.image_data.mode)
            self.update_image_preview()

            encryption_method = self.steg_encryption_var.get()
            messagebox.showinfo("Success", f"Message hidden successfully using {encoding_method if encoding_method != 'None' else 'no'} encoding and {encryption_method if encryption_method != 'None' else 'no'} encryption!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to encode message: {str(e)}")

    def decode_steganography(self):
        if not self.image_data:
            messagebox.showwarning("Warning", "Please select an image first.")
            return

        try:
            if self.image_data.mode not in ['RGB', 'RGBA']:
                self.image_data = self.image_data.convert('RGB')

            img_array = np.array(self.image_data, dtype=np.uint8)

            flat_array = img_array.flatten()

            binary_message = ''.join([str(pixel & 1) for pixel in flat_array])

            message = ""
            for i in range(0, len(binary_message), 8):
                if i + 8 > len(binary_message):
                    break

                byte = binary_message[i:i+8]
                if byte == '00000000':
                    break

                try:
                    message += chr(int(byte, 2))
                except ValueError:
                    continue

            encoding_method = self.steg_encoding_var.get()

            if encoding_method == "Base64":
                try:
                    message = base64.b64decode(message).decode()
                except Exception:
                    messagebox.showwarning("Warning", "Failed to decode Base64. The message may not be Base64 encoded.")
            elif encoding_method == "ASCII":
                try:
                    message = message.encode('utf-8').decode('unicode_escape')
                except Exception:
                    messagebox.showwarning("Warning", "Failed to decode ASCII. The message may not be ASCII encoded.")
            elif encoding_method == "Reverse Bits":
                try:
                    message = "".join([chr(int(format(ord(c), '08b')[::-1], 2)) for c in message])
                except Exception:
                    messagebox.showwarning("Warning", "Failed to decode Reverse Bits. The message may not be encoded with reversed bits.")

            decrypted_message = self.decrypt_message(message)

            self.steg_message.delete("1.0", "end")
            self.steg_message.insert("1.0", decrypted_message)

            encryption_method = self.steg_encryption_var.get()
            messagebox.showinfo("Success", f"Message extracted successfully using {encoding_method if encoding_method != 'None' else 'no'} decoding and {encryption_method if encryption_method != 'None' else 'no'} decryption!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to decode message: {str(e)}")

    def save_image(self):
        if not self.image_data:
            messagebox.showwarning("Warning", "No image to save.")
            return

        file_path = filedialog.asksaveasfilename(
            title="Save Image",
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )

        if file_path:
            try:
                if self.image_data.mode not in ['RGB', 'RGBA']:
                    self.image_data = self.image_data.convert('RGB')

                self.image_data.save(file_path, format='PNG')
                messagebox.showinfo("Success", "Image saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image: {str(e)}")

    def view_secret_message(self):
        if not self.image_data:
            messagebox.showwarning("Warning", "Please select an image first.")
            return

        try:
            if self.image_data.mode not in ['RGB', 'RGBA']:
                self.image_data = self.image_data.convert('RGB')

            img_array = np.array(self.image_data, dtype=np.uint8)

            flat_array = img_array.flatten()

            binary_message = ''.join([str(pixel & 1) for pixel in flat_array])

            message = ""
            for i in range(0, len(binary_message), 8):
                if i + 8 > len(binary_message):
                    break

                byte = binary_message[i:i+8]
                if byte == '00000000':
                    break

                try:
                    message += chr(int(byte, 2))
                except ValueError:
                    continue

            encoding_method = self.steg_encoding_var.get()
            decoded_message = message

            if encoding_method == "Base64":
                try:
                    decoded_message = base64.b64decode(message).decode()
                except Exception:
                    pass
            elif encoding_method == "ASCII":
                try:
                    decoded_message = message.encode('utf-8').decode('unicode_escape')
                except Exception:
                    pass
            elif encoding_method == "Reverse Bits":
                try:
                    decoded_message = "".join([chr(int(format(ord(c), '08b')[::-1], 2)) for c in message])
                except Exception:
                    pass

            decrypted_message = self.decrypt_message(decoded_message)

            if not message:
                messagebox.showinfo("Secret Message", "No hidden message found in this image.")
                return

            popup = ctk.CTkToplevel(self.parent)
            popup.title("Secret Message")
            popup.geometry("400x300")
            popup.resizable(True, True)

            popup.transient(self.parent)
            popup.grab_set()

            frame = ctk.CTkFrame(popup, fg_color=self.colors["card_bg"], corner_radius=10)
            frame.pack(fill="both", expand=True, padx=20, pady=20)

            header = ctk.CTkFrame(frame, fg_color="transparent", height=40)
            header.pack(fill="x", padx=15, pady=(15, 5))

            encryption_method = self.steg_encryption_var.get()
            ctk.CTkLabel(
                header,
                text=f"Secret Message ({encoding_method} + {encryption_method})",
                image=self.icons["preview"],
                compound="left",
                font=ctk.CTkFont(family="Helvetica", size=14, weight="bold"),
                text_color=self.colors["text"],
                padx=5
            ).pack(side="left")

            tab_view = ctk.CTkTabview(
                frame,
                fg_color=self.colors["medium_bg"],
                segmented_button_fg_color=self.colors["card_bg"],
                segmented_button_selected_color=self.colors["accent"],
                segmented_button_selected_hover_color=self.colors["accent_hover"],
                segmented_button_unselected_color=self.colors["card_bg"],
                segmented_button_unselected_hover_color=self.colors["medium_bg"],
                text_color=self.colors["text"]
            )
            tab_view.pack(fill="both", expand=True, padx=15, pady=(5, 15))

            raw_tab = tab_view.add("Raw")
            decoded_tab = tab_view.add("Decoded")
            decrypted_tab = tab_view.add("Decrypted")

            raw_display = ctk.CTkTextbox(
                raw_tab,
                fg_color=self.colors["medium_bg"],
                text_color=self.colors["text"],
                border_width=0,
                corner_radius=8,
                font=ctk.CTkFont(family="Helvetica", size=12)
            )
            raw_display.pack(fill="both", expand=True, padx=10, pady=10)
            raw_display.insert("1.0", message)
            raw_display.configure(state="disabled")

            decoded_display = ctk.CTkTextbox(
                decoded_tab,
                fg_color=self.colors["medium_bg"],
                text_color=self.colors["text"],
                border_width=0,
                corner_radius=8,
                font=ctk.CTkFont(family="Helvetica", size=12)
            )
            decoded_display.pack(fill="both", expand=True, padx=10, pady=10)
            decoded_display.insert("1.0", decoded_message)
            decoded_display.configure(state="disabled")

            decrypted_display = ctk.CTkTextbox(
                decrypted_tab,
                fg_color=self.colors["medium_bg"],
                text_color=self.colors["text"],
                border_width=0,
                corner_radius=8,
                font=ctk.CTkFont(family="Helvetica", size=12)
            )
            decrypted_display.pack(fill="both", expand=True, padx=10, pady=10)
            decrypted_display.insert("1.0", decrypted_message)
            decrypted_display.configure(state="disabled")

            close_btn = ctk.CTkButton(
                frame,
                text="Close",
                command=popup.destroy,
                fg_color=self.colors["accent"],
                hover_color=self.colors["accent_hover"],
                text_color="#FFFFFF",
                font=ctk.CTkFont(family="Helvetica", size=12, weight="bold"),
                corner_radius=8,
                height=32
            )
            close_btn.pack(pady=(0, 15))

            popup.update_idletasks()
            x = self.parent.winfo_rootx() + (self.parent.winfo_width() - popup.winfo_width()) // 2
            y = self.parent.winfo_rooty() + (self.parent.winfo_height() - popup.winfo_height()) // 2
            popup.geometry(f"+{x}+{y}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to extract message: {str(e)}")
