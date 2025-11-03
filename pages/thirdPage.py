import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np
import wave
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from cryptography.fernet import Fernet
import os
import tempfile
import winsound
from PIL import Image
import base64

class AudioProcessingPage:
    def __init__(self, parent, colors):
        self.parent = parent
        self.colors = colors
        self.audio_path = None
        self.audio_data = None
        self.audio_params = None
        self.cipher = Fernet(Fernet.generate_key())
        self.temp_audio_file = None
        self.is_playing = False

        self.icons = {
            "audio_ops": self.load_icon("assets/third_tab/audio-editing.png", (24, 24)),
            "sinusoid": self.load_icon("assets/third_tab/radio-waves.png", (24, 24)),
            "encryption": self.load_icon("assets/first_tab/lock.png", (24, 24)),
            "visualization": self.load_icon("assets/third_tab/natural-language-processing.png", (24, 24)),
            "select": self.load_icon("assets/second_tab/folder.png", (20, 20)),
            "apply": self.load_icon("assets/third_tab/radio-waves.png", (20, 20)),
            "encrypt": self.load_icon("assets/first_tab/lock.png", (20, 20)),
            "decrypt": self.load_icon("assets/first_tab/unlock.png", (20, 20)),
            "save": self.load_icon("assets/wav.png", (20, 20)),
            "play": self.load_icon("assets/third_tab/radio-waves.png", (20, 20))
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

        left_scroll_container = ctk.CTkScrollableFrame(
            main_container,
            fg_color="transparent",
            orientation="vertical",
            scrollbar_button_color=self.colors["accent"],
            scrollbar_button_hover_color=self.colors["accent_hover"],
            width=250,
            height=500
        )
        left_scroll_container.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        left_panel = ctk.CTkFrame(left_scroll_container, fg_color="transparent")
        left_panel.pack(fill="both", expand=True)

        audio_select_frame = ctk.CTkFrame(left_panel, fg_color=self.colors["card_bg"], corner_radius=10)
        audio_select_frame.pack(fill="x", pady=(0, 15))

        audio_header = ctk.CTkFrame(audio_select_frame, fg_color="transparent", height=40)
        audio_header.pack(fill="x", padx=15, pady=(15, 5))

        ctk.CTkLabel(
            audio_header,
            text="Audio Operations",
            image=self.icons["audio_ops"],
            compound="left",
            font=ctk.CTkFont(family="Helvetica", size=14, weight="bold"),
            text_color=self.colors["text"],
            padx=5
        ).pack(side="left")

        select_btn = ctk.CTkButton(
            audio_select_frame,
            text="Select Audio File",
            image=self.icons["select"],
            compound="left",
            command=self.select_audio,
            fg_color=self.colors["accent"],
            hover_color=self.colors["accent_hover"],
            text_color="#FFFFFF",
            font=ctk.CTkFont(family="Helvetica", size=12, weight="bold"),
            corner_radius=8,
            height=32,
            border_spacing=10
        )
        select_btn.pack(padx=15, pady=(5, 15), fill="x")

        sinusoid_frame = ctk.CTkFrame(left_panel, fg_color=self.colors["card_bg"], corner_radius=10)
        sinusoid_frame.pack(fill="x", pady=(0, 15))

        sinusoid_header = ctk.CTkFrame(sinusoid_frame, fg_color="transparent", height=40)
        sinusoid_header.pack(fill="x", padx=15, pady=(15, 5))

        ctk.CTkLabel(
            sinusoid_header,
            text="Sinusoid Processing",
            image=self.icons["sinusoid"],
            compound="left",
            font=ctk.CTkFont(family="Helvetica", size=14, weight="bold"),
            text_color=self.colors["text"],
            padx=5
        ).pack(side="left")

        params_container = ctk.CTkFrame(sinusoid_frame, fg_color="transparent")
        params_container.pack(fill="x", padx=15, pady=(5, 10))

        freq_label = ctk.CTkLabel(
            params_container,
            text="Frequency (Hz):",
            font=ctk.CTkFont(family="Helvetica", size=12),
            text_color=self.colors["text"]
        )
        freq_label.grid(row=0, column=0, sticky="w", pady=(0, 10))

        self.frequency_var = ctk.StringVar(value="440")
        freq_entry = ctk.CTkEntry(
            params_container,
            textvariable=self.frequency_var,
            width=100,
            fg_color=self.colors["medium_bg"],
            text_color=self.colors["text"],
            border_width=0
        )
        freq_entry.grid(row=0, column=1, sticky="e", pady=(0, 10))

        amp_label = ctk.CTkLabel(
            params_container,
            text="Amplitude:",
            font=ctk.CTkFont(family="Helvetica", size=12),
            text_color=self.colors["text"]
        )
        amp_label.grid(row=1, column=0, sticky="w", pady=(0, 10))

        self.amplitude_var = ctk.StringVar(value="0.5")
        amp_entry = ctk.CTkEntry(
            params_container,
            textvariable=self.amplitude_var,
            width=100,
            fg_color=self.colors["medium_bg"],
            text_color=self.colors["text"],
            border_width=0
        )
        amp_entry.grid(row=1, column=1, sticky="e", pady=(0, 10))

        op_label = ctk.CTkLabel(
            params_container,
            text="Operation:",
            font=ctk.CTkFont(family="Helvetica", size=12),
            text_color=self.colors["text"]
        )
        op_label.grid(row=2, column=0, sticky="w")

        self.operation_var = ctk.StringVar(value="add")
        operations = ["add", "subtract", "multiply"]
        op_menu = ctk.CTkOptionMenu(
            params_container,
            values=operations,
            variable=self.operation_var,
            fg_color=self.colors["accent"],
            button_color=self.colors["accent_hover"],
            button_hover_color=self.colors["accent_hover"],
            dropdown_fg_color=self.colors["card_bg"],
            dropdown_hover_color=self.colors["medium_bg"],
            dropdown_text_color=self.colors["text"],
            width=100,
            font=ctk.CTkFont(family="Helvetica", size=12)
        )
        op_menu.grid(row=2, column=1, sticky="e")

        params_container.grid_columnconfigure(0, weight=1)
        params_container.grid_columnconfigure(1, weight=1)

        apply_btn = ctk.CTkButton(
            sinusoid_frame,
            text="Apply Sinusoid",
            image=self.icons["apply"],
            compound="left",
            command=self.apply_sinusoid,
            fg_color=self.colors["accent"],
            hover_color=self.colors["accent_hover"],
            text_color="#FFFFFF",
            font=ctk.CTkFont(family="Helvetica", size=12, weight="bold"),
            corner_radius=8,
            height=32,
            border_spacing=10
        )
        apply_btn.pack(padx=15, pady=(0, 15), fill="x")

        encrypt_frame = ctk.CTkFrame(left_panel, fg_color=self.colors["card_bg"], corner_radius=10)
        encrypt_frame.pack(fill="x", pady=(0, 15))

        encrypt_header = ctk.CTkFrame(encrypt_frame, fg_color="transparent", height=40)
        encrypt_header.pack(fill="x", padx=15, pady=(15, 5))

        ctk.CTkLabel(
            encrypt_header,
            text="Audio Encryption",
            image=self.icons["encryption"],
            compound="left",
            font=ctk.CTkFont(family="Helvetica", size=14, weight="bold"),
            text_color=self.colors["text"],
            padx=5
        ).pack(side="left")

        encryption_method_label = ctk.CTkLabel(
            encrypt_frame,
            text="Encryption Method:",
            font=ctk.CTkFont(family="Helvetica", size=12),
            text_color=self.colors["text"]
        )
        encryption_method_label.pack(anchor="w", padx=15, pady=(5, 0))

        self.audio_encryption_var = tk.StringVar(value="Fernet (AES)")
        encryption_methods = ["Fernet (AES)", "XOR", "Caesar Cipher", "Delta Algorithm"]

        self.audio_encryption_menu = ctk.CTkOptionMenu(
            encrypt_frame,
            values=encryption_methods,
            variable=self.audio_encryption_var,
            fg_color=self.colors["medium_bg"],
            button_color=self.colors["accent"],
            button_hover_color=self.colors["accent_hover"],
            dropdown_fg_color=self.colors["card_bg"],
            dropdown_hover_color=self.colors["medium_bg"],
            dropdown_text_color=self.colors["text"],
            font=ctk.CTkFont(family="Helvetica", size=12),
            width=120
        )
        self.audio_encryption_menu.pack(padx=15, pady=(0, 10), fill="x")

        key_label = ctk.CTkLabel(
            encrypt_frame,
            text="Encryption Key:",
            font=ctk.CTkFont(family="Helvetica", size=12),
            text_color=self.colors["text"]
        )
        key_label.pack(anchor="w", padx=15, pady=(5, 0))

        self.audio_encryption_key = ctk.CTkEntry(
            encrypt_frame,
            placeholder_text="Enter encryption key (leave empty for auto-generated)",
            fg_color=self.colors["medium_bg"],
            text_color=self.colors["text"],
            border_width=0,
            corner_radius=8,
            font=ctk.CTkFont(family="Helvetica", size=12)
        )
        self.audio_encryption_key.pack(padx=15, pady=(0, 15), fill="x")

        encrypt_audio_btn = ctk.CTkButton(
            encrypt_frame,
            text="Encrypt Audio",
            image=self.icons["encrypt"],
            compound="left",
            command=self.encrypt_audio,
            fg_color=self.colors["accent"],
            hover_color=self.colors["accent_hover"],
            text_color="#FFFFFF",
            font=ctk.CTkFont(family="Helvetica", size=12, weight="bold"),
            corner_radius=8,
            height=32,
            border_spacing=10
        )
        encrypt_audio_btn.pack(padx=15, pady=(5, 10), fill="x")

        decrypt_audio_btn = ctk.CTkButton(
            encrypt_frame,
            text="Decrypt Audio",
            image=self.icons["decrypt"],
            compound="left",
            command=self.decrypt_audio,
            fg_color=self.colors["accent"],
            hover_color=self.colors["accent_hover"],
            text_color="#FFFFFF",
            font=ctk.CTkFont(family="Helvetica", size=12, weight="bold"),
            corner_radius=8,
            height=32,
            border_spacing=10
        )
        decrypt_audio_btn.pack(padx=15, pady=(0, 15), fill="x")

        audio_controls_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        audio_controls_frame.pack(fill="x", pady=(0, 15))

        audio_controls_frame.grid_columnconfigure(0, weight=1)
        audio_controls_frame.grid_columnconfigure(1, weight=1)

        play_btn = ctk.CTkButton(
            audio_controls_frame,
            text="Play Audio",
            image=self.icons["play"],
            compound="left",
            command=self.play_audio,
            fg_color=self.colors["accent"],
            hover_color=self.colors["accent_hover"],
            text_color="#FFFFFF",
            font=ctk.CTkFont(family="Helvetica", size=12, weight="bold"),
            corner_radius=8,
            height=32,
            border_spacing=10
        )
        play_btn.grid(row=0, column=0, padx=(0, 5), pady=0, sticky="ew")

        save_btn = ctk.CTkButton(
            audio_controls_frame,
            text="Save Audio",
            image=self.icons["save"],
            compound="left",
            command=self.save_audio,
            fg_color=self.colors["secondary"],
            hover_color=self.colors["accent_hover"],
            text_color="#FFFFFF",
            font=ctk.CTkFont(family="Helvetica", size=12, weight="bold"),
            corner_radius=8,
            height=32,
            border_spacing=10
        )
        save_btn.grid(row=0, column=1, padx=(5, 0), pady=0, sticky="ew")

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

        waveform_frame = ctk.CTkFrame(right_panel, fg_color=self.colors["card_bg"], corner_radius=10)
        waveform_frame.pack(fill="both", expand=True)

        waveform_header = ctk.CTkFrame(waveform_frame, fg_color="transparent", height=40)
        waveform_header.pack(fill="x", padx=15, pady=(15, 5))

        ctk.CTkLabel(
            waveform_header,
            text="Audio Visualization",
            image=self.icons["visualization"],
            compound="left",
            font=ctk.CTkFont(family="Helvetica", size=14, weight="bold"),
            text_color=self.colors["text"],
            padx=5
        ).pack(side="left")

        self.waveform_container = ctk.CTkFrame(waveform_frame, fg_color=self.colors["medium_bg"], corner_radius=8)
        self.waveform_container.pack(fill="both", expand=True, padx=15, pady=(5, 15))

        self.waveform_placeholder = ctk.CTkLabel(
            self.waveform_container,
            text="No audio loaded\nSelect an audio file to visualize",
            font=ctk.CTkFont(family="Helvetica", size=14),
            text_color=self.colors["text_secondary"]
        )
        self.waveform_placeholder.pack(fill="both", expand=True)

    def select_audio(self):
        file_path = filedialog.askopenfilename(
            title="Select Audio File",
            filetypes=[("WAV files", "*.wav")]
        )

        if file_path:
            try:
                self.audio_path = file_path
                self.load_audio_data()
                self.update_waveform_display()
                messagebox.showinfo("Success", "Audio loaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load audio: {str(e)}")

    def load_audio_data(self):
        with wave.open(self.audio_path, 'rb') as wf:
            self.audio_params = wf.getparams()

            frames = wf.readframes(wf.getnframes())

            if self.audio_params.sampwidth == 2:
                self.audio_data = np.frombuffer(frames, dtype=np.int16)
            elif self.audio_params.sampwidth == 4:
                self.audio_data = np.frombuffer(frames, dtype=np.int32)
            else:
                self.audio_data = np.frombuffer(frames, dtype=np.uint8)

    def update_waveform_display(self):
        if self.audio_data is None:
            return

        for widget in self.waveform_container.winfo_children():
            widget.destroy()

        plt.style.use('dark_background' if self.colors["bg"].startswith("#1") else 'default')
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6), dpi=100, gridspec_kw={'height_ratios': [3, 1]})

        time = np.linspace(0, len(self.audio_data) / self.audio_params.framerate, num=len(self.audio_data))

        ax1.plot(time, self.audio_data, color=self.colors["accent"], linewidth=0.8, alpha=0.9)

        ax1.fill_between(time, self.audio_data, alpha=0.2, color=self.colors["accent"])

        ax1.grid(True, linestyle='--', alpha=0.3)

        ax1.set_xlabel('Time (s)', fontsize=10, color=self.colors["text"])
        ax1.set_ylabel('Amplitude', fontsize=10, color=self.colors["text"])
        ax1.set_title('Audio Waveform', fontsize=12, fontweight='bold', color=self.colors["text"])

        ax1.tick_params(axis='both', colors=self.colors["text_secondary"], labelsize=8)

        if len(self.audio_data) > 0:
            _, _, _, im = ax2.specgram(
                self.audio_data,
                Fs=self.audio_params.framerate,
                NFFT=1024,
                noverlap=512,
                cmap='viridis'
            )

            cbar = fig.colorbar(im, ax=ax2, orientation='vertical', pad=0.01, shrink=0.8)
            cbar.set_label('Intensity (dB)', fontsize=8, color=self.colors["text"])
            cbar.ax.tick_params(labelsize=7, colors=self.colors["text_secondary"])

            ax2.set_xlabel('Time (s)', fontsize=10, color=self.colors["text"])
            ax2.set_ylabel('Frequency (Hz)', fontsize=10, color=self.colors["text"])
            ax2.set_title('Spectrogram', fontsize=12, fontweight='bold', color=self.colors["text"])

            ax2.tick_params(axis='both', colors=self.colors["text_secondary"], labelsize=8)

        fig.patch.set_facecolor(self.colors["card_bg"])
        ax1.set_facecolor(self.colors["medium_bg"])
        ax2.set_facecolor(self.colors["medium_bg"])

        plt.tight_layout()
        fig.subplots_adjust(hspace=0.3)

        canvas_frame = ctk.CTkFrame(self.waveform_container, fg_color="transparent")
        canvas_frame.pack(fill="both", expand=True, padx=5, pady=5)

        canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
        canvas.draw()
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.configure(highlightthickness=0, bd=0)
        canvas_widget.pack(fill="both", expand=True)

    def apply_sinusoid(self):
        if self.audio_data is None:
            messagebox.showwarning("Warning", "Please load an audio file first.")
            return

        try:
            frequency = float(self.frequency_var.get())
            amplitude = float(self.amplitude_var.get())
            operation = self.operation_var.get()

            time = np.linspace(0, len(self.audio_data) / self.audio_params.framerate, num=len(self.audio_data))
            sinusoid = amplitude * np.sin(2 * np.pi * frequency * time)

            if self.audio_params.sampwidth == 2:
                sinusoid = sinusoid * 32767
            elif self.audio_params.sampwidth == 4:
                sinusoid = sinusoid * 2147483647
            else:
                sinusoid = (sinusoid + 1) * 127.5

            sinusoid = sinusoid.astype(self.audio_data.dtype)

            if operation == "add":
                self.audio_data = np.clip(self.audio_data + sinusoid, np.iinfo(self.audio_data.dtype).min, np.iinfo(self.audio_data.dtype).max)
            elif operation == "subtract":
                self.audio_data = np.clip(self.audio_data - sinusoid, np.iinfo(self.audio_data.dtype).min, np.iinfo(self.audio_data.dtype).max)
            elif operation == "multiply":
                normalized_sinusoid = (sinusoid / np.abs(np.max(sinusoid))) * 0.5 + 0.5
                self.audio_data = np.clip(self.audio_data * normalized_sinusoid, np.iinfo(self.audio_data.dtype).min, np.iinfo(self.audio_data.dtype).max)

            self.update_waveform_display()
            messagebox.showinfo("Success", f"Applied {operation} operation with sinusoid.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply sinusoid: {str(e)}")

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

    def encrypt_data(self, data_bytes):
        encryption_method = self.audio_encryption_var.get()
        user_key = self.audio_encryption_key.get().strip()

        try:
            if encryption_method == "Fernet (AES)":
                cipher = self.get_encryption_cipher(user_key if user_key else None)
                encrypted = cipher.encrypt(data_bytes)
                return encrypted
            elif encryption_method == "XOR":
                key = hash(user_key) % 256 if user_key else 42
                encrypted = bytes([b ^ key for b in data_bytes])
                return encrypted
            elif encryption_method == "Caesar Cipher":
                shift = len(user_key) % 256 if user_key else 3
                encrypted = bytes([(b + shift) % 256 for b in data_bytes])
                return encrypted
            elif encryption_method == "Delta Algorithm":
                if len(data_bytes) == 0:
                    return data_bytes
                delta_key = hash(user_key) % 256 if user_key else 127
                encrypted = bytearray([data_bytes[0] ^ delta_key])
                for i in range(1, len(data_bytes)):
                    delta = (data_bytes[i] - data_bytes[i-1] + delta_key) % 256
                    encrypted.append(delta)
                return bytes(encrypted)
            else:
                return data_bytes
        except Exception as e:
            messagebox.showerror("Encryption Error", f"Failed to encrypt audio: {str(e)}")
            return data_bytes

    def decrypt_data(self, encrypted_bytes):
        encryption_method = self.audio_encryption_var.get()
        user_key = self.audio_encryption_key.get().strip()

        try:
            if encryption_method == "Fernet (AES)":
                cipher = self.get_encryption_cipher(user_key if user_key else None)
                decrypted = cipher.decrypt(encrypted_bytes)
                return decrypted
            elif encryption_method == "XOR":
                key = hash(user_key) % 256 if user_key else 42
                decrypted = bytes([b ^ key for b in encrypted_bytes])
                return decrypted
            elif encryption_method == "Caesar Cipher":
                shift = -(len(user_key) % 256) if user_key else -3
                decrypted = bytes([(b + shift) % 256 for b in encrypted_bytes])
                return decrypted
            elif encryption_method == "Delta Algorithm":
                if len(encrypted_bytes) == 0:
                    return encrypted_bytes
                delta_key = hash(user_key) % 256 if user_key else 127
                decrypted = bytearray([encrypted_bytes[0] ^ delta_key])
                for i in range(1, len(encrypted_bytes)):
                    original_byte = (decrypted[i-1] + encrypted_bytes[i] - delta_key) % 256
                    decrypted.append(original_byte)
                return bytes(decrypted)
            else:
                return encrypted_bytes
        except Exception as e:
            messagebox.showerror("Decryption Error", f"Failed to decrypt audio: {str(e)}")
            return encrypted_bytes

    def encrypt_audio(self):
        if self.audio_data is None:
            messagebox.showwarning("Warning", "Please load an audio file first.")
            return

        try:
            audio_bytes = self.audio_data.tobytes()

            encrypted_bytes = self.encrypt_data(audio_bytes)

            self.audio_data = np.frombuffer(encrypted_bytes, dtype=np.uint8)

            self.update_waveform_display()
            encryption_method = self.audio_encryption_var.get()
            messagebox.showinfo("Success", f"Audio encrypted successfully using {encryption_method}!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to encrypt audio: {str(e)}")

    def decrypt_audio(self):
        if self.audio_data is None:
            messagebox.showwarning("Warning", "Please load an audio file first.")
            return

        try:
            audio_bytes = bytes(self.audio_data)

            decrypted_bytes = self.decrypt_data(audio_bytes)

            if self.audio_params.sampwidth == 2:
                self.audio_data = np.frombuffer(decrypted_bytes, dtype=np.int16)
            elif self.audio_params.sampwidth == 4:
                self.audio_data = np.frombuffer(decrypted_bytes, dtype=np.int32)
            else:
                self.audio_data = np.frombuffer(decrypted_bytes, dtype=np.uint8)

            self.update_waveform_display()
            encryption_method = self.audio_encryption_var.get()
            messagebox.showinfo("Success", f"Audio decrypted successfully using {encryption_method}!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to decrypt audio: {str(e)}")

    def save_audio(self):
        if self.audio_data is None:
            messagebox.showwarning("Warning", "No audio to save.")
            return

        file_path = filedialog.asksaveasfilename(
            title="Save Audio",
            defaultextension=".wav",
            filetypes=[("WAV files", "*.wav"), ("All files", "*.*")]
        )

        if file_path:
            try:
                with wave.open(file_path, 'wb') as wf:
                    wf.setparams(self.audio_params)
                    wf.writeframes(self.audio_data.tobytes())
                messagebox.showinfo("Success", "Audio saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save audio: {str(e)}")

    def play_audio(self):
        if self.audio_data is None:
            messagebox.showwarning("Warning", "Please load an audio file first.")
            return

        try:
            if self.temp_audio_file:
                try:
                    os.unlink(self.temp_audio_file)
                except:
                    pass

            fd, self.temp_audio_file = tempfile.mkstemp(suffix='.wav')
            os.close(fd)

            with wave.open(self.temp_audio_file, 'wb') as wf:
                wf.setparams(self.audio_params)
                wf.writeframes(self.audio_data.tobytes())

            winsound.PlaySound(self.temp_audio_file, winsound.SND_ASYNC)
            self.is_playing = True

        except Exception as e:
            messagebox.showerror("Error", f"Failed to play audio: {str(e)}")