import tkinter as tk
from tkinter import filedialog, messagebox
import wave
import pygame
import sqlite3
import hashlib
import numpy as np
from PIL import Image, ImageTk
from cryptography.fernet import Fernet

# Initialize pygame mixer for audio playback
pygame.mixer.init()

class AudioSteganographyApp:
    def init_db(self):
        self.conn = sqlite3.connect("users.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
                   CREATE TABLE IF NOT EXISTS users (
                       username TEXT PRIMARY KEY,
                       password TEXT
                   )
               """)
        self.conn.commit()

    def __init__(self, root):
        self.root = root
        self.init_db()
        self.root.title("Audio Steganography")
        self.root.geometry("1000x600+250+50")
        self.key = None
        self.num_audio_frames = 1037000  # Placeholder, adjust based on audio length
        self.current_user = None

        # Create frames (pages)
        self.main_frame = tk.Frame(root)
        self.login_frame = tk.Frame(root)
        self.signup_frame = tk.Frame(root)
        self.encode_frame = tk.Frame(root)
        self.decode_frame = tk.Frame(root)
        self.audio_playback_frame = tk.Frame(root)

        self.setup_login_page()
        self.setup_signup_page()
        self.setup_main_page()
        self.setup_encode_page()
        self.setup_decode_page()
        self.setup_audio_playback_page()

        # Start with login page
        self.login_frame.pack()

    def setup_login_page(self):
        # Load and set the background image
        self.bg_image = Image.open("bgimage1.jpg")  # Replace with your image path
        self.bg_image = self.bg_image.resize((1000, 600), Image.Resampling.LANCZOS)  # Use LANCZOS instead of ANTIALIAS
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        # Create a Canvas and set the background image
        self.login_canvas = tk.Canvas(self.login_frame, width=1000, height=600)
        self.login_canvas.pack(fill="both", expand=True)
        self.login_canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        # Adding "Hello, Guyss!" text
        self.hello_label = tk.Label(self.login_frame, text="Hello,", font=("Helvetica", 20, "bold"), bg="white", fg="#8F9D8E")
        self.hello_label.pack(pady=20)
        self.hello1_label = tk.Label(self.login_frame, text="Guyss!", font=("Helvetica", 20), bg="white", fg="#8F9D8E")
        self.hello1_label.pack(pady=20)

        # Login and SignUp tabs (Only Login enabled for now)
        self.login_label = tk.Label(self.login_frame, text="Login", font=("Helvetica", 12, "bold"), bg="white", fg="#8F9D8E", cursor="hand2")
        self.login_label.pack()

        # SignUp Label (Click to switch to sign-up page)
        self.signup_label = tk.Label(self.login_frame, text="SignUp", font=("Helvetica", 12, "bold"), bg="white", fg="#8F9D8E", cursor="hand2")
        self.signup_label.pack()
        self.signup_label.bind("<Button-1>", lambda e: self.show_signup_page())
        login_line = tk.Frame(self.login_frame, bg="#8F9D8E", height=1.5)
        login_line.place(x=605, y=177, width=50)


        # username Entry
        default_username_text = "Enter Your Username"
        self.username_entry = tk.Entry(self.login_frame, bd=0, font=("Helvetica", 12), fg="#4a536b")
        self.username_entry.pack(pady=10)
        self.username_entry.insert(0, default_username_text)
        username_line = tk.Frame(self.login_frame, bg="#8F9D8E", height=1)
        username_line.place(x=506, y=240, width=270)
        self.username_entry.bind("<FocusIn>", lambda event: self.clear_entry(event, self.username_entry, default_username_text))
        self.username_entry.bind("<FocusOut>", lambda event: self.restore_entry(event, self.username_entry, default_username_text))

        # Password Entry
        default_password_text = "Enter Your Password"
        self.password_entry = tk.Entry(self.login_frame, bd=0, font=("Helvetica", 12), fg="#4a536b")
        self.password_entry.pack(pady=10)
        self.password_entry.insert(0, default_password_text)
        password_line = tk.Frame(self.login_frame, bg="#8F9D8E", height=1)
        password_line.place(x=506, y=308, width=270)
        self.password_entry.bind("<FocusIn>", lambda event: self.clear_entry(event, self.password_entry, default_password_text))
        self.password_entry.bind("<FocusOut>", lambda event: self.restore_entry(event, self.password_entry, default_password_text))

        # Login Button
        self.login_button = tk.Button(self.login_frame, text="Login", font=("Helvetica", 14), bg="#4a536b", fg="white", width=24, command=self.login)
        self.login_button.pack(pady=10)

        # Use the canvas to place the widgets at specific coordinates (approximate values based on the uploaded image)
        self.login_canvas.create_window(530, 100, window=self.hello_label)
        self.login_canvas.create_window(620, 100, window=self.hello1_label)
        self.login_canvas.create_window(630, 165, window=self.login_label)
        self.login_canvas.create_window(700, 165, window=self.signup_label)
        self.login_canvas.create_window(600, 225, window=self.username_entry)
        self.login_canvas.create_window(600, 295, window=self.password_entry)
        self.login_canvas.create_window(640, 400, window=self.login_button)

    def setup_signup_page(self):
        self.bg_image2 = Image.open("bgimage1.jpg")  # Replace with your image path
        self.bg_image2 = self.bg_image2.resize((1000, 600), Image.Resampling.LANCZOS)  # Use LANCZOS instead of ANTIALIAS
        self.bg_photo2 = ImageTk.PhotoImage(self.bg_image2)

        # Create a Canvas and set the background image
        self.signup_canvas = tk.Canvas(self.signup_frame, width=1000, height=600)
        self.signup_canvas.pack(fill="both", expand=True)
        self.signup_canvas.create_image(0, 0, image=self.bg_photo2, anchor="nw")

        self.create_label = tk.Label(self.signup_frame, text="Create an account", font=("Helvetica", 20, "bold"), bg="white", fg="#8F9D8E")
        self.create_label.pack(pady=20)

        # Login and SignUp tabs (Only Login enabled for now)
        self.login_label = tk.Label(self.signup_frame, text="Login", font=("Helvetica", 12, "bold"), bg="white", fg="#8F9D8E", cursor="hand2")
        self.login_label.pack()
        self.login_label.bind("<Button-1>", lambda e: self.show_login_page())
        signup_line = tk.Frame(self.signup_frame, bg="#8F9D8E", height=1.5)
        signup_line.place(x=674, y=173, width=55)

        # SignUp Label (Click to switch to sign-up page)
        self.signup_label = tk.Label(self.signup_frame, text="SignUp", font=("Helvetica", 12, "bold"), bg="white", fg="#8F9D8E", cursor="hand2")
        self.signup_label.pack()

        self.username_label = tk.Label(self.signup_frame, text="Username :", font=("Helvetica", 12), bg="white", fg="#4a536b")
        self.username_label.pack(pady=20)
        self.signup_username_entry = tk.Entry(self.signup_frame, bd=0, font=("Helvetica", 15), highlightthickness=2, width=30)
        self.signup_username_entry.pack(pady=10)

        self.password_label = tk.Label(self.signup_frame, text="Password :", font=("Helvetica", 12), bg="white", fg="#4a536b")
        self.password_label.pack(pady=20)
        self.signup_password_entry = tk.Entry(self.signup_frame, bd=0, font=("Helvetica", 15), highlightthickness=2, width=30, show="*")
        self.signup_password_entry.pack(pady=10)

        self.email_label = tk.Label(self.signup_frame, text="Email :", font=("Helvetica", 12), bg="white", fg="#4a536b")
        self.email_label.pack(pady=20)
        self.signup_email_entry = tk.Entry(self.signup_frame, bd=0, font=("Helvetica", 15), highlightthickness=2, width=30)
        self.signup_email_entry.pack(pady=10)

        self.phone_label = tk.Label(self.signup_frame, text="Phone Number :", font=("Helvetica", 12), bg="white", fg="#4a536b")
        self.phone_label.pack(pady=20)
        self.signup_phone_entry = tk.Entry(self.signup_frame, bd=0, font=("Helvetica", 15), highlightthickness=2, width=30)
        self.signup_phone_entry.pack(pady=10)

        self.signup_button = tk.Button(self.signup_frame, text="Signup", font=("Helvetica", 14), bg="#4a536b", fg="white", width=24, command=self.signup)
        self.signup_button.pack(pady=10)

        self.signup_canvas.create_window(600, 100, window=self.create_label)
        self.signup_canvas.create_window(630, 160, window=self.login_label)
        self.signup_canvas.create_window(700, 160, window=self.signup_label)
        self.signup_canvas.create_window(520, 185, window=self.username_label)
        self.signup_canvas.create_window(640, 220, window=self.signup_username_entry)
        self.signup_canvas.create_window(520, 260, window=self.password_label)
        self.signup_canvas.create_window(640, 295, window=self.signup_password_entry)
        self.signup_canvas.create_window(500, 335, window=self.email_label)
        self.signup_canvas.create_window(640, 370, window=self.signup_email_entry)
        self.signup_canvas.create_window(534, 410, window=self.phone_label)
        self.signup_canvas.create_window(640, 445, window=self.signup_phone_entry)
        self.signup_canvas.create_window(640, 500, window=self.signup_button)

    def setup_main_page(self):
        self.bg_image3 = Image.open("bgimage2.jpg")  # Replace with your image path
        self.bg_image3 = self.bg_image3.resize((1000, 600), Image.Resampling.LANCZOS)  # Use LANCZOS instead of ANTIALIAS
        self.bg_photo3 = ImageTk.PhotoImage(self.bg_image3)

        # Create a Canvas and set the background image
        self.main_canvas = tk.Canvas(self.main_frame, width=1000, height=600)
        self.main_canvas.pack(fill="both", expand=True)
        self.main_canvas.create_image(0, 0, image=self.bg_photo3, anchor="nw")

        main_frame = tk.Frame(self.main_frame, bg="white", bd=5)
        main_frame.place(relx=0.90, rely=0.54, anchor="e", width=500, height=350)
        # Create a label and match its background to the frame background
        self.hide_label = tk.Label(self.main_frame, text="Hidden Audio Tracker", font=('Bell MT', 23, 'bold'), bg='#fedc55', fg='#97704f')
        self.hide_label.pack(pady=20)

        self.text_label = tk.Label(self.main_frame, text="To encode your audio file into an image for secure transfer,\n\nClick here", font=('Baskerville Old Face', 15), bg='white', fg='black')
        self.text_label.pack(pady=20)

        self.encode_button = tk.Button(self.main_frame, text="Encode Audio", command=self.show_encode_page)
        self.encode_button.pack(pady=10)

        self.text2_label = tk.Label(self.main_frame, text="To decode an image to extract the hidden audio file,\n\n\tClick here", font=('Baskerville Old Face', 15), bg='white', fg='black')
        self.text2_label.pack(pady=20)

        self.decode_button = tk.Button(self.main_frame, text="Decode Audio", command=self.show_decode_page)
        self.decode_button.pack(pady=5)
        self.logout_button = tk.Button(self.main_frame, text="Back", command=self.logout)
        self.logout_button.pack(pady=5)

        self.main_canvas.create_window(500, 50, window=self.hide_label)
        self.main_canvas.create_window(650, 200, window=self.text_label)
        self.main_canvas.create_window(735, 223, window=self.encode_button)
        self.main_canvas.create_window(620, 300, window=self.text2_label)
        self.main_canvas.create_window(748, 323, window=self.decode_button)
        self.main_canvas.create_window(880, 50, window=self.logout_button)

    def setup_encode_page(self):
        self.bg_image5 = Image.open("bgimage4.jpg")  # Replace with your image path
        self.bg_image5 = self.bg_image5.resize((1000, 600), Image.Resampling.LANCZOS)  # Use LANCZOS instead of ANTIALIAS
        self.bg_photo5 = ImageTk.PhotoImage(self.bg_image5)

        # Create a Canvas and set the background image
        self.encode_canvas = tk.Canvas(self.encode_frame, width=1000, height=600)
        self.encode_canvas.pack(fill="both", expand=True)
        self.encode_canvas.create_image(0, 0, image=self.bg_photo5, anchor="nw")

        encode_frame = tk.Frame(self.encode_frame, bg="white", bd=5)
        encode_frame.place(relx=0.50, rely=0.50, anchor="center", width=400, height=600)

        self.label1 = tk.Label(self.encode_frame, text="Encode Audio into Image", font=('Helvetica', 16), bg='white')
        self.label1.pack(pady=20)

        self.label2 = tk.Label(self.encode_frame, text="Select Image File", font=('Arial', 12), bg='white')
        self.label2.pack()
        self.image_file_label = tk.Label(self.encode_frame, text="No file selected", font=('Arial', 12), width=40, bg='white')
        self.image_file_label.pack(pady=5)
        self.button1 = tk.Button(self.encode_frame, text="Browse", command=self.browse_image_file)
        self.button1.pack(pady=5)

        self.label3 = tk.Label(self.encode_frame, text="Select Audio File", font=('Arial', 12), bg='white')
        self.label3.pack()
        default_audio_path_text = "\tNo file selected"
        self.audio_path_entry = tk.Entry(self.encode_frame, bd=0, width=30, font=('Arial', 12))
        self.audio_path_entry.pack(pady=5)
        self.audio_path_entry.insert(0, default_audio_path_text)
        self.button2 = tk.Button(self.encode_frame, text="Browse", command=self.browse_audio_file)
        self.button2.pack(pady=5)

        self.label4 = tk.Label(self.encode_frame, text="Output Image Filename", font=('Arial', 12), bg='white')
        self.label4.pack()
        self.output_image_entry = tk.Entry(self.encode_frame, width=30, bg='white')
        self.output_image_entry.pack(pady=5)

        self.button3 = tk.Button(self.encode_frame, text="Generate Key", command=self.generate_key)
        self.button3.pack(pady=20)
        self.button4 = tk.Button(self.encode_frame, text="Save Key", command=self.save_key)
        self.button4.pack(pady=20)
        self.button5 = tk.Button(self.encode_frame, text="Encode Audio", command=self.encode_audio)
        self.button5.pack(pady=20)
        self.button6 = tk.Button(self.encode_frame, text="Home", command=self.show_main_page)
        self.button6.pack(pady=10)

        self.encode_canvas.create_window(500, 50, window=self.label1)
        self.encode_canvas.create_window(500, 100, window=self.label2)
        self.encode_canvas.create_window(500, 140, window=self.image_file_label)
        self.encode_canvas.create_window(500, 180, window=self.button1)
        self.encode_canvas.create_window(500, 220, window=self.label3)
        self.encode_canvas.create_window(500, 260, window=self.audio_path_entry)
        self.encode_canvas.create_window(500, 300, window=self.button2)
        self.encode_canvas.create_window(500, 340, window=self.label4)
        self.encode_canvas.create_window(500, 380, window=self.output_image_entry)
        self.encode_canvas.create_window(500, 420, window=self.button3)
        self.encode_canvas.create_window(500, 470, window=self.button4)
        self.encode_canvas.create_window(500, 520, window=self.button5)
        self.encode_canvas.create_window(500, 570, window=self.button6)


    def setup_decode_page(self):
        self.bg_image6 = Image.open("bgimage4.jpg")  # Replace with your image path
        self.bg_image6 = self.bg_image6.resize((1000, 600), Image.Resampling.LANCZOS)  # Use LANCZOS instead of ANTIALIAS
        self.bg_photo6 = ImageTk.PhotoImage(self.bg_image6)

        # Create a Canvas and set the background image
        self.decode_canvas = tk.Canvas(self.decode_frame, width=1000, height=600)
        self.decode_canvas.pack(fill="both", expand=True)
        self.decode_canvas.create_image(0, 0, image=self.bg_photo6, anchor="nw")

        decode_frame = tk.Frame(self.decode_frame, bg="white", bd=5)
        decode_frame.place(relx=0.50, rely=0.50, anchor="center", width=400, height=600)

        self.dlabel1 = tk.Label(self.decode_frame, text="Decode Audio from Image", font=('Helvetica', 16), bg='white')
        self.dlabel1.pack(pady=20)

        self.dlabel2 = tk.Label(self.decode_frame, text="Select Encoded Image File", font=('Arial', 12), bg='white')
        self.dlabel2.pack()
        self.encoded_image_file_label = tk.Label(self.decode_frame, text="No file selected", font=('Arial', 12), width=40, bg='white')
        self.encoded_image_file_label.pack(pady=5)
        self.dbutton1 = tk.Button(self.decode_frame, text="Browse", command=self.browse_encoded_image_file)
        self.dbutton1.pack(pady=5)

        self.dlabel3 = tk.Label(self.decode_frame, text="Output Audio Filename", font=('Arial', 12), bg='white')
        self.dlabel3.pack()
        self.output_audio_entry = tk.Entry(self.decode_frame, width=30)
        self.output_audio_entry.pack(pady=5)

        self.dbutton2 = tk.Button(self.decode_frame, text="Load Key", command=self.load_key)
        self.dbutton2.pack(pady=25)
        self.dbutton3 = tk.Button(self.decode_frame, text="Decode Audio", command=self.decode_audio)
        self.dbutton3.pack(pady=20)
        self.dbutton4 = tk.Button(self.decode_frame, text="Play Audio", command=self.show_audioplay_page)
        self.dbutton4.pack(pady=20)
        self.dbutton5 = tk.Button(self.decode_frame, text="Home", command=self.show_main_page)
        self.dbutton5.pack(pady=10)

        self.decode_canvas.create_window(500, 80, window=self.dlabel1)
        self.decode_canvas.create_window(500, 150, window=self.dlabel2)
        self.decode_canvas.create_window(500, 200, window=self.encoded_image_file_label)
        self.decode_canvas.create_window(500, 250, window=self.dbutton1)
        self.decode_canvas.create_window(500, 300, window=self.dlabel3)
        self.decode_canvas.create_window(500, 350, window=self.output_audio_entry)
        self.decode_canvas.create_window(500, 400, window=self.dbutton2)
        self.decode_canvas.create_window(500, 450, window=self.dbutton3)
        self.decode_canvas.create_window(500, 500, window=self.dbutton4)
        self.decode_canvas.create_window(500, 550, window=self.dbutton5)

    def setup_audio_playback_page(self):
        self.bg_image4 = Image.open("bgimage3.jpg")  # Replace with your image path
        self.bg_image4 = self.bg_image4.resize((1000, 600), Image.Resampling.LANCZOS)  # Use LANCZOS instead of ANTIALIAS
        self.bg_photo4 = ImageTk.PhotoImage(self.bg_image4)

        # Create a Canvas and set the background image
        self.audio_playback_canvas = tk.Canvas(self.audio_playback_frame, width=1000, height=600)
        self.audio_playback_canvas.pack(fill="both", expand=True)
        self.audio_playback_canvas.create_image(0, 0, image=self.bg_photo4, anchor="nw")

        self.audio_label = tk.Label(self.audio_playback_frame, text="Audio Player", font=('Bell MT', 20))
        self.audio_label.pack(pady=20)

        # Browse for audio file button
        self.audio_file_label = tk.Label(self.audio_playback_frame, text="No File Selected", width=40, fg='#c51e3a')
        self.audio_file_label.pack(pady=5)

        # Playback buttons (Play, Pause, Resume, Stop)
        self.play_button = tk.Button(self.audio_playback_frame, text="Play ▶", font=("Helvetica", 15), command=self.play_audio, bg='white', fg='#960018')
        self.play_button.pack(pady=10)
        self.pause_button = tk.Button(self.audio_playback_frame, text="⏸", font=("Helvetica", 15), command=self.pause_audio, bg='white', fg='#960018')
        self.pause_button.pack(pady=10)
        self.resume_button = tk.Button(self.audio_playback_frame, text="⏪", font=("Helvetica", 15), command=self.resume_audio, bg='white', fg='#960018')
        self.resume_button.pack(pady=10)
        self.stop_button = tk.Button(self.audio_playback_frame, text="Stop ⏹", font=("Helvetica", 15), command=self.stop_audio, bg='white', fg='#960018')
        self.stop_button.pack(pady=10)
        self.back_button = tk.Button(self.audio_playback_frame, text="Back", command=self.show_decode_page)
        self.back_button.pack(pady=5)

        self.audio_playback_canvas.create_window(500, 80, window=self.audio_label)
        self.audio_playback_canvas.create_window(500, 330, window=self.audio_file_label)
        self.audio_playback_canvas.create_window(300, 405, window=self.play_button)
        self.audio_playback_canvas.create_window(430, 405, window=self.pause_button)
        self.audio_playback_canvas.create_window(550, 405, window=self.resume_button)
        self.audio_playback_canvas.create_window(670, 405, window=self.stop_button)
        self.audio_playback_canvas.create_window(870, 80, window=self.back_button)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        self.cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, hashed_password)
        )
        result = self.cursor.fetchone()

        if result:
            self.current_user = username
            self.show_main_page()
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def clear_entry(self, event, entry_widget, default_text):
        if entry_widget.get() == default_text:
            entry_widget.delete(0, tk.END)
            if entry_widget == self.password_entry:
                entry_widget.config(show="*")  # Show * for password entry

    def restore_entry(self, event, entry_widget, default_text):
        if entry_widget.get() == "":
            entry_widget.insert(0, default_text)
            if entry_widget == self.password_entry:
                entry_widget.config(show="")  # Show text if it's the default message

    def signup(self):
        username = self.signup_username_entry.get()
        password = self.signup_password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Please provide all fields")
            return

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        try:
            self.cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, hashed_password)
            )
            self.conn.commit()
            messagebox.showinfo("Signup Successful", "You can now log in.")
            self.show_login_page()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists")

    def logout(self):
        self.current_user = None
        self.show_login_page()

    def play_audio(self):
        try:
            # Play the selected audio file
            audio_file = self.audio_file_label.cget("text")
            if audio_file != "No file selected":
                pygame.mixer.music.load(audio_file)
                pygame.mixer.music.play()
            else:
                messagebox.showerror("Error", "Please select an audio file first.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to play audio: {str(e)}")

    def pause_audio(self):
        pygame.mixer.music.pause()

    def resume_audio(self):
        pygame.mixer.music.unpause()

    def stop_audio(self):
        pygame.mixer.music.stop()

    def generate_key(self):
        self.key = Fernet.generate_key()
        messagebox.showinfo("Key Generated", "A new encryption key has been generated.")

    def save_key(self):
        if not self.key:
            messagebox.showerror("Error", "No key to save.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".key", filetypes=[("Key files", "*.key")])
        if file_path:
            with open(file_path, 'wb') as key_file:
                key_file.write(self.key)
            messagebox.showinfo("Success", f"Key saved to {file_path}")

    def load_key(self):
        file_path = filedialog.askopenfilename(title="Select Key File", filetypes=[("Key files", "*.key")])
        if file_path:
            with open(file_path, 'rb') as key_file:
                self.key = key_file.read()
            messagebox.showinfo("Success", "Key loaded successfully.")
            print(f"Loaded key: {self.key}")  # Debugging line to verify the key

    def browse_image_file(self):
        file_path = filedialog.askopenfilename(title="Select Image File", filetypes=[("Image files", "*.png")])
        if file_path:
            self.image_file_label.config(text=file_path)

    def browse_audio_file(self):
        file_path = filedialog.askopenfilename(
            title="Select Audio File",
            filetypes=[("Audio files", "*.wav *.mp3")]
        )

        if file_path:
            # For encode page
            self.audio_path_entry.delete(0, tk.END)
            self.audio_path_entry.insert(0, file_path)

            # For playback
            self.audio_file_label.config(text=file_path)
            self.audio_file_path = file_path

    def browse_encoded_image_file(self):
        file_path = filedialog.askopenfilename(title="Select Encoded Image File", filetypes=[("Image files", "*.png")])
        if file_path:
            self.encoded_image_file_label.config(text=file_path)

    def encode_audio(self):
        image_path = self.image_file_label.cget("text")
        audio_path = self.audio_file_label.cget("text")
        output_image_path = self.output_image_entry.get()

        if not self.key:
            messagebox.showerror("Error", "Please generate a key first.")
            return

        if not image_path or not audio_path or not output_image_path:
            messagebox.showerror("Error", "Please provide all input files and output filename.")
            return

        try:
            # Perform audio encoding
            self.encode_audio_in_image(image_path, audio_path, output_image_path, self.key)
            messagebox.showinfo("Success", f"Audio encoded into {output_image_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def decode_audio(self):
        image_path = self.encoded_image_file_label.cget("text")
        output_audio_path = self.output_audio_entry.get()

        if not self.key:
            messagebox.showerror("Error", "Please generate a key first.")
            return

        if not image_path or not output_audio_path:
            messagebox.showerror("Error", "Please provide input image and output audio filename.")
            return

        try:
            # Perform audio decoding
            self.decode_audio_from_image(image_path, self.key, output_audio_path, self.num_audio_frames)
            messagebox.showinfo("Success", f"Audio decoded into {output_audio_path}")
            # After decoding, set the path to the decoded file for playback
            self.audio_file_path = output_audio_path  # Save path for audio playback
            self.audio_file_label.config(text=self.audio_file_path)  # Update the label on audio playback page

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def encode_audio_in_image(self, image_path, audio_path, output_image_path, key):
        image = Image.open(image_path)
        pixels = np.array(image)

        with wave.open(audio_path, 'rb') as audio_file:
            audio_frames = audio_file.readframes(audio_file.getnframes())

        encrypted_audio = Fernet(key).encrypt(audio_frames)
        flat_pixels = pixels.flatten()
        if len(flat_pixels) < len(encrypted_audio):
            raise ValueError("Image is too small to hold the audio data")

        for i in range(len(encrypted_audio)):
            flat_pixels[i] = encrypted_audio[i]

        encoded_pixels = flat_pixels.reshape(pixels.shape)
        encoded_image = Image.fromarray(encoded_pixels.astype('uint8'))
        encoded_image.save(output_image_path)

    def decode_audio_from_image(self, image_path, key, output_audio_path, num_audio_frames):
        image = Image.open(image_path)
        pixels = np.array(image).flatten()

        # Adjust how many pixels you need to read to match the audio size
        num_audio_bytes = num_audio_frames * 2  # Assuming 16-bit audio (2 bytes per frame)
        if len(pixels) < num_audio_bytes:
            raise ValueError("The image does not contain enough data to extract the audio")

        # Extract the audio data from the pixels
        encrypted_audio = bytes(pixels[:num_audio_bytes])

        # Decrypt the audio data
        try:
            decrypted_audio = Fernet(key).decrypt(encrypted_audio)
        except Exception as e:
            raise ValueError(f"Decryption failed: {str(e)}")

        # Write the decrypted audio to a WAV file
        with wave.open(output_audio_path, 'wb') as output_audio_file:
            output_audio_file.setnchannels(1)  # Mono audio
            output_audio_file.setsampwidth(2)  # 16-bit audio (2 bytes)
            output_audio_file.setframerate(44100)  # Standard audio sample rate
            output_audio_file.writeframes(decrypted_audio)

    def show_login_page(self):
        self.login_frame.tkraise()
        self.encode_frame.pack_forget()
        self.decode_frame.pack_forget()
        self.signup_frame.pack_forget()
        self.main_frame.pack_forget()
        self.login_frame.pack()

    def show_signup_page(self):
        self.signup_frame.tkraise()
        self.login_frame.pack_forget()
        self.signup_frame.pack()

    def show_main_page(self):
        self.main_frame.tkraise()
        self.login_frame.pack_forget()
        self.signup_frame.pack_forget()
        self.encode_frame.pack_forget()
        self.decode_frame.pack_forget()
        self.main_frame.pack()

    def show_encode_page(self):
        self.main_frame.pack_forget()
        self.encode_frame.pack()

    def show_decode_page(self):
        self.decode_frame.tkraise()
        self.main_frame.pack_forget()
        self.audio_playback_frame.pack_forget()
        self.decode_frame.pack()

    def show_audioplay_page(self):
        self.audio_playback_frame.tkraise()
        self.decode_frame.pack_forget()
        self.audio_playback_frame.pack()

        # If a decoded audio file exists, update the label to display it
        if hasattr(self, 'audio_file_path') and self.audio_file_path:
            self.audio_file_label.config(text=self.audio_file_path)
        else:
            self.audio_file_label.config(text="No file selected")


# Main application loop
root = tk.Tk()
app = AudioSteganographyApp(root)
root.mainloop()