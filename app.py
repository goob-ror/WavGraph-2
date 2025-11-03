import customtkinter as ctk
from tkinter import filedialog, messagebox
from cryptography.fernet import Fernet
from PIL import Image, ImageTk
import numpy as np
import wave
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import darkdetect

from pages.firstPage import BasicStringPage
from pages.secondPage import ImageProcessingPage
from pages.thirdPage import AudioProcessingPage

system_appearance = darkdetect.theme()
ctk.set_appearance_mode(system_appearance)
ctk.set_default_color_theme("blue")

class WaveGraphApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("WaveGraph")
        self.geometry("1000x700")
        self.minsize(900, 600)

        self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)

        self.color_schemes = {
            "light": {
                "bg": "#F0F4F8",
                "card_bg": "#FFFFFF",
                "medium_bg": "#E1E8ED",
                "accent": "#3498DB",
                "accent_hover": "#2980B9",
                "secondary": "#9B59B6",
                "text": "#2C3E50",
                "text_secondary": "#7F8C8D"
            },
            "dark": {
                "bg": "#1A1D21",
                "card_bg": "#252A30",
                "medium_bg": "#2C3E50",
                "accent": "#3498DB",
                "accent_hover": "#2980B9",
                "secondary": "#9B59B6",
                "text": "#ECF0F1",
                "text_secondary": "#BDC3C7"
            }
        }

        self.current_mode = ctk.get_appearance_mode().lower()
        if self.current_mode not in self.color_schemes:
            self.current_mode = "light"
        self.colors = self.color_schemes[self.current_mode]


        self.configure(fg_color=self.colors["bg"])

        self.create_menu_bar()


        self.tabview = ctk.CTkTabview(
            self,
            fg_color=self.colors["card_bg"],
            segmented_button_fg_color=self.colors["medium_bg"],
            segmented_button_selected_color=self.colors["accent"],
            segmented_button_selected_hover_color=self.colors["accent_hover"],
            segmented_button_unselected_color=self.colors["medium_bg"],
            segmented_button_unselected_hover_color=self.colors["medium_bg"],
            text_color=self.colors["text"]
        )
        self.tabview.pack(fill="both", expand=True, padx=20, pady=(10, 20))


        self.tab_basic = self.tabview.add("Text Encoding")
        self.tab_image = self.tabview.add("Image Processing")
        self.tab_audio = self.tabview.add("Audio Analysis")

        self.basic_page = BasicStringPage(self.tab_basic, self.colors)
        self.image_page = ImageProcessingPage(self.tab_image, self.colors)
        self.audio_page = AudioProcessingPage(self.tab_audio, self.colors)

        self.tabview.set("Text Encoding")

    def setup_image_tab(self):
        left_panel = ctk.CTkFrame(self.tab_image, fg_color="transparent")
        left_panel.pack(side="left", fill="y", padx=10, pady=10)

        img_select_frame = ctk.CTkFrame(left_panel, fg_color=self.colors["medium_bg"])
        img_select_frame.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(img_select_frame, text="Image Operations").pack(pady=5)

        self.image_path = None
        self.image_data = None

        select_btn = ctk.CTkButton(
            img_select_frame,
            text="Select Image",
            command=self.select_image,
            fg_color=self.colors["accent"],
            hover_color=self.colors["accent_hover"]
        )
        select_btn.pack(padx=20, pady=5, fill="x")

        steg_frame = ctk.CTkFrame(left_panel, fg_color=self.colors["medium_bg"])
        steg_frame.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(steg_frame, text="Steganography").pack(pady=5)

        ctk.CTkLabel(steg_frame, text="Secret Message:").pack(anchor="w", padx=20, pady=(5, 0))
        self.steg_message = ctk.CTkTextbox(steg_frame, height=60)
        self.steg_message.pack(padx=20, pady=5, fill="x")

        encode_btn = ctk.CTkButton(
            steg_frame,
            text="Encode Message",
            command=self.encode_steganography,
            fg_color=self.colors["accent"],
            hover_color=self.colors["accent_hover"]
        )
        encode_btn.pack(padx=20, pady=5, fill="x")

        decode_btn = ctk.CTkButton(
            steg_frame,
            text="Decode Message",
            command=self.decode_steganography,
            fg_color=self.colors["accent"],
            hover_color=self.colors["accent_hover"]
        )
        decode_btn.pack(padx=20, pady=5, fill="x")

        save_btn = ctk.CTkButton(
            steg_frame,
            text="Save Image",
            command=self.save_image,
            fg_color=self.colors["accent"],
            hover_color=self.colors["accent_hover"]
        )
        save_btn.pack(padx=20, pady=5, fill="x")

        right_panel = ctk.CTkFrame(self.tab_image, fg_color="transparent")
        right_panel.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        preview_frame = ctk.CTkFrame(right_panel, fg_color=self.colors["medium_bg"])
        preview_frame.pack(fill="both", expand=True)

        ctk.CTkLabel(preview_frame, text="Image Preview").pack(pady=5)

        self.image_preview = ctk.CTkLabel(preview_frame, text="No image selected")
        self.image_preview.pack(fill="both", expand=True, padx=10, pady=10)

    def select_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")]
        )

        if file_path:
            try:
                self.image_path = file_path
                self.image_data = Image.open(file_path)
                self.update_image_preview()
                messagebox.showinfo("Success", "Image loaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {str(e)}")

    def update_image_preview(self):
        if self.image_data:
            img_copy = self.image_data.copy()
            img_copy.thumbnail((300, 300))

            photo = ImageTk.PhotoImage(img_copy)

            self.image_preview.configure(image=photo, text="")
            self.image_preview.image = photo

    def encode_steganography(self):
        if not self.image_data:
            messagebox.showwarning("Warning", "Please select an image first.")
            return

        message = self.steg_message.get("1.0", "end-1c")
        if not message:
            messagebox.showwarning("Warning", "Please enter a message to hide.")
            return

        try:
            img_array = np.array(self.image_data)

            binary_message = ''.join(format(ord(char), '08b') for char in message)
            binary_message += '00000000'

            if img_array.size < len(binary_message):
                messagebox.showerror("Error", "Image too small for the message.")
                return

            flat_array = img_array.flatten()

            for i in range(len(binary_message)):
                flat_array[i] = (flat_array[i] & ~1) | int(binary_message[i])

            steg_array = flat_array.reshape(img_array.shape)

            self.image_data = Image.fromarray(steg_array.astype('uint8'))
            self.update_image_preview()

            messagebox.showinfo("Success", "Message hidden successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to encode message: {str(e)}")

    def decode_steganography(self):
        if not self.image_data:
            messagebox.showwarning("Warning", "Please select an image first.")
            return

        try:
            img_array = np.array(self.image_data)

            flat_array = img_array.flatten()

            binary_message = ''.join([str(pixel & 1) for pixel in flat_array])

            message = ""
            for i in range(0, len(binary_message), 8):
                if i + 8 > len(binary_message):
                    break

                byte = binary_message[i:i+8]
                if byte == '00000000':
                    break

                message += chr(int(byte, 2))
            self.steg_message.delete("1.0", "end")
            self.steg_message.insert("1.0", message)

            messagebox.showinfo("Success", "Message extracted successfully!")
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
                self.image_data.save(file_path)
                messagebox.showinfo("Success", "Image saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image: {str(e)}")

    def setup_audio_tab(self):
        left_panel = ctk.CTkFrame(self.tab_audio, fg_color="transparent")
        left_panel.pack(side="left", fill="y", padx=10, pady=10)

        audio_select_frame = ctk.CTkFrame(left_panel, fg_color=self.colors["medium_bg"])
        audio_select_frame.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(audio_select_frame, text="Audio Operations").pack(pady=5)

        self.audio_path = None
        self.audio_data = None
        self.audio_params = None

        select_btn = ctk.CTkButton(
            audio_select_frame,
            text="Select Audio File",
            command=self.select_audio,
            fg_color=self.colors["accent"],
            hover_color=self.colors["accent_hover"]
        )
        select_btn.pack(padx=20, pady=5, fill="x")

        sinusoid_frame = ctk.CTkFrame(left_panel, fg_color=self.colors["medium_bg"])
        sinusoid_frame.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(sinusoid_frame, text="Sinusoid Processing").pack(pady=5)

        freq_frame = ctk.CTkFrame(sinusoid_frame, fg_color="transparent")
        freq_frame.pack(fill="x", padx=20, pady=5)

        ctk.CTkLabel(freq_frame, text="Frequency (Hz):").pack(side="left")
        self.frequency_var = ctk.StringVar(value="440")
        freq_entry = ctk.CTkEntry(freq_frame, textvariable=self.frequency_var, width=80)
        freq_entry.pack(side="right")

        amp_frame = ctk.CTkFrame(sinusoid_frame, fg_color="transparent")
        amp_frame.pack(fill="x", padx=20, pady=5)

        ctk.CTkLabel(amp_frame, text="Amplitude:").pack(side="left")
        self.amplitude_var = ctk.StringVar(value="0.5")
        amp_entry = ctk.CTkEntry(amp_frame, textvariable=self.amplitude_var, width=80)
        amp_entry.pack(side="right")

        op_frame = ctk.CTkFrame(sinusoid_frame, fg_color="transparent")
        op_frame.pack(fill="x", padx=20, pady=5)

        ctk.CTkLabel(op_frame, text="Operation:").pack(side="left")
        self.operation_var = ctk.StringVar(value="add")
        operations = ["add", "subtract", "multiply"]
        op_menu = ctk.CTkOptionMenu(
            op_frame,
            values=operations,
            variable=self.operation_var,
            fg_color=self.colors["accent"],
            button_color=self.colors["accent_hover"]
        )
        op_menu.pack(side="right")

        apply_btn = ctk.CTkButton(
            sinusoid_frame,
            text="Apply Sinusoid",
            command=self.apply_sinusoid,
            fg_color=self.colors["accent"],
            hover_color=self.colors["accent_hover"]
        )
        apply_btn.pack(padx=20, pady=5, fill="x")

        encrypt_frame = ctk.CTkFrame(left_panel, fg_color=self.colors["medium_bg"])
        encrypt_frame.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(encrypt_frame, text="Audio Encryption").pack(pady=5)

        encrypt_audio_btn = ctk.CTkButton(
            encrypt_frame,
            text="Encrypt Audio",
            command=self.encrypt_audio,
            fg_color=self.colors["accent"],
            hover_color=self.colors["accent_hover"]
        )
        encrypt_audio_btn.pack(padx=20, pady=5, fill="x")

        decrypt_audio_btn = ctk.CTkButton(
            encrypt_frame,
            text="Decrypt Audio",
            command=self.decrypt_audio,
            fg_color=self.colors["accent"],
            hover_color=self.colors["accent_hover"]
        )
        decrypt_audio_btn.pack(padx=20, pady=5, fill="x")

        save_btn = ctk.CTkButton(
            left_panel,
            text="Save Audio",
            command=self.save_audio,
            fg_color=self.colors["accent"],
            hover_color=self.colors["accent_hover"]
        )
        save_btn.pack(padx=20, pady=5, fill="x")

        right_panel = ctk.CTkFrame(self.tab_audio, fg_color="transparent")
        right_panel.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        waveform_frame = ctk.CTkFrame(right_panel, fg_color=self.colors["medium_bg"])
        waveform_frame.pack(fill="both", expand=True)

        ctk.CTkLabel(waveform_frame, text="Waveform Display").pack(pady=5)

        self.waveform_container = ctk.CTkFrame(waveform_frame, fg_color="transparent")
        self.waveform_container.pack(fill="both", expand=True, padx=10, pady=10)

        self.waveform_placeholder = ctk.CTkLabel(self.waveform_container, text="No audio loaded")
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

        fig, ax = plt.subplots(figsize=(6, 4), dpi=100)

        time = np.linspace(0, len(self.audio_data) / self.audio_params.framerate, num=len(self.audio_data))
        ax.plot(time, self.audio_data, color=self.colors["accent"])

        text_color = self.colors["text"]

        ax.set_xlabel('Time (s)', color=text_color)
        ax.set_ylabel('Amplitude', color=text_color)
        ax.set_title('Audio Waveform', color=text_color)

        ax.tick_params(axis='x', colors=text_color)
        ax.tick_params(axis='y', colors=text_color)

        for spine in ax.spines.values():
            spine.set_edgecolor(text_color)

        fig.patch.set_facecolor(self.colors["bg"])
        ax.set_facecolor(self.colors["medium_bg"])

        canvas = FigureCanvasTkAgg(fig, master=self.waveform_container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

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

    def encrypt_audio(self):
        if self.audio_data is None:
            messagebox.showwarning("Warning", "Please load an audio file first.")
            return

        try:
            audio_bytes = self.audio_data.tobytes()

            encrypted_bytes = self.cipher.encrypt(audio_bytes)

            self.audio_data = np.frombuffer(encrypted_bytes, dtype=np.uint8)
            self.update_waveform_display()
            messagebox.showinfo("Success", "Audio encrypted successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to encrypt audio: {str(e)}")

    def decrypt_audio(self):
        if self.audio_data is None:
            messagebox.showwarning("Warning", "Please load an audio file first.")
            return

        try:
            audio_bytes = bytes(self.audio_data)

            decrypted_bytes = self.cipher.decrypt(audio_bytes)

            if self.audio_params.sampwidth == 2:
                self.audio_data = np.frombuffer(decrypted_bytes, dtype=np.int16)
            elif self.audio_params.sampwidth == 4:
                self.audio_data = np.frombuffer(decrypted_bytes, dtype=np.int32)
            else:
                self.audio_data = np.frombuffer(decrypted_bytes, dtype=np.uint8)
            self.update_waveform_display()
            messagebox.showinfo("Success", "Audio decrypted successfully!")
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

    def create_menu_bar(self):
        self.menu_frame = ctk.CTkFrame(self, fg_color=self.colors["card_bg"], height=40)
        self.menu_frame.pack(fill="x", padx=20, pady=(20, 0))

        self.title_label = ctk.CTkLabel(
            self.menu_frame,
            text="WaveGraph",
            font=ctk.CTkFont(family="Helvetica", size=18, weight="bold"),
            text_color=self.colors["accent"]
        )
        self.title_label.pack(side="left", padx=10)

        self.subtitle_label = ctk.CTkLabel(
            self.menu_frame,
            text="Signal Processing Studio",
            font=ctk.CTkFont(family="Helvetica", size=12),
            text_color=self.colors["text_secondary"]
        )
        self.subtitle_label.pack(side="left", padx=5)

        self.appearance_mode_menu = ctk.CTkOptionMenu(
            self.menu_frame,
            values=["Light", "Dark"],
            command=self.change_appearance_mode,
            font=ctk.CTkFont(family="Helvetica", size=12),
            fg_color=self.colors["accent"],
            button_color=self.colors["accent_hover"],
            button_hover_color=self.colors["accent_hover"],
            dropdown_fg_color=self.colors["card_bg"],
            dropdown_hover_color=self.colors["medium_bg"],
            dropdown_text_color=self.colors["text"],
            width=90
        )
        self.appearance_mode_menu.pack(side="right", padx=10)

        self.appearance_mode_menu.set("Light" if self.current_mode == "light" else "Dark")

        self.theme_label = ctk.CTkLabel(
            self.menu_frame,
            text="Theme:",
            font=ctk.CTkFont(family="Helvetica", size=12),
            text_color=self.colors["text_secondary"]
        )
        self.theme_label.pack(side="right", padx=5)

    def change_appearance_mode(self, new_mode):
        ctk.set_appearance_mode(new_mode)

        self.current_mode = new_mode.lower()
        self.colors = self.color_schemes[self.current_mode]

        self.configure(fg_color=self.colors["bg"])

        self.menu_frame.configure(fg_color=self.colors["card_bg"])
        self.title_label.configure(text_color=self.colors["accent"])
        self.subtitle_label.configure(text_color=self.colors["text_secondary"])
        self.theme_label.configure(text_color=self.colors["text_secondary"])

        self.appearance_mode_menu.configure(
            fg_color=self.colors["accent"],
            button_color=self.colors["accent_hover"],
            button_hover_color=self.colors["accent_hover"],
            dropdown_fg_color=self.colors["card_bg"],
            dropdown_hover_color=self.colors["medium_bg"],
            dropdown_text_color=self.colors["text"]
        )

        self.tabview.configure(
            fg_color=self.colors["card_bg"],
            segmented_button_fg_color=self.colors["medium_bg"],
            segmented_button_selected_color=self.colors["accent"],
            segmented_button_selected_hover_color=self.colors["accent_hover"],
            segmented_button_unselected_color=self.colors["medium_bg"],
            segmented_button_unselected_hover_color=self.colors["medium_bg"],
            text_color=self.colors["text"]
        )

        for widget in self.tab_basic.winfo_children():
            widget.destroy()
        for widget in self.tab_image.winfo_children():
            widget.destroy()
        for widget in self.tab_audio.winfo_children():
            widget.destroy()

        self.basic_page = BasicStringPage(self.tab_basic, self.colors)
        self.image_page = ImageProcessingPage(self.tab_image, self.colors)
        self.audio_page = AudioProcessingPage(self.tab_audio, self.colors)

if __name__ == "__main__":
    app = WaveGraphApp()
    app.mainloop()