import os
import pygame
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Music Player")
        self.root.geometry("600x300")
        self.root.resizable(False, False)

        self.current_song = None
        self.is_playing = False

        pygame.mixer.init()

        self.create_widgets()

    def create_widgets(self):
        # Frames for layout
        self.left_frame = tk.Frame(self.root, width=240, height=300, bg='#20232a')
        self.right_frame = tk.Frame(self.root, width=360, height=300, bg='#61dafb')

        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.left_frame.pack_propagate(False)
        self.right_frame.pack_propagate(False)

        # Load folder button
        self.load_button = ttk.Button(self.left_frame, text="Load Folder", command=self.load_folder)
        self.load_button.pack(pady=10)

        # Song list
        self.song_list = tk.Listbox(self.left_frame, bg="black", fg="white", width=30, height=20, selectbackground='#61dafb', selectforeground='#20232a')
        self.song_list.pack(pady=10)
        self.song_list.bind('<Double-1>', self.play_selected_song)

        # Playback controls
        control_frame = tk.Frame(self.right_frame, bg='#61dafb')
        control_frame.pack(pady=20)

        self.play_button = ttk.Button(control_frame, text="Play", command=self.play_song)
        self.play_button.grid(row=0, column=0, padx=10)

        self.stop_button = ttk.Button(control_frame, text="Stop", command=self.stop_song)
        self.stop_button.grid(row=0, column=1, padx=10)

        # Status Label
        self.status_label = tk.Label(self.right_frame, text="Status: Stopped", bg='#61dafb', fg='#20232a')
        self.status_label.pack(pady=10)

        # Volume control
        volume_frame = tk.Frame(self.right_frame, bg='#61dafb')
        volume_frame.pack(pady=10)

        tk.Label(volume_frame, text="Volume", bg='#61dafb', fg='#20232a').pack(side=tk.LEFT)
        self.volume_slider = ttk.Scale(volume_frame, from_=0, to=1, orient=tk.HORIZONTAL, command=self.set_volume)
        self.volume_slider.set(1)  # Set to full volume by default
        self.volume_slider.pack(side=tk.LEFT, padx=10)

    def load_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            os.chdir(folder_path)
            songs = [f for f in os.listdir(folder_path) if f.endswith(".mp3")]
            self.song_list.delete(0, tk.END)
            for song in songs:
                self.song_list.insert(tk.END, song)

    def play_selected_song(self, event):
        self.play_song()

    def play_song(self):
        try:
            selected_song = self.song_list.get(tk.ACTIVE)
            self.current_song = selected_song
            pygame.mixer.music.load(selected_song)  # Load the song using pygame.mixer.music
            pygame.mixer.music.play()
            self.is_playing = True
            self.update_status_label()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def stop_song(self):
        pygame.mixer.music.stop()
        self.is_playing = False
        self.update_status_label()

    def set_volume(self, volume):
        pygame.mixer.music.set_volume(float(volume))

    def update_status_label(self):
        if self.is_playing:
            self.status_label.config(text="Status: Playing")
        else:
            self.status_label.config(text="Status: Stopped")

if __name__ == "__main__":
    root = tk.Tk()
    app = MusicPlayer(root)
    root.mainloop()
