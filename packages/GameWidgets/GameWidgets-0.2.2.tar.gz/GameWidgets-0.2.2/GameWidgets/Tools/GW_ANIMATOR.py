import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class Simple2DAnimator:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple 2D Animator")

        # Initialize variables
        self.frame_images = []
        self.current_frame = 0
        self.frame_rate = tk.DoubleVar(value=1.0)

        # Create widgets
        self.canvas = tk.Canvas(root, width=400, height=400)
        self.canvas.pack(padx=10, pady=10)

        self.frame_label = tk.Label(root, text="Frame: 0")
        self.frame_label.pack(pady=5)

        self.frame_rate_label = tk.Label(root, text="Frame Rate:")
        self.frame_rate_label.pack(pady=5)

        self.frame_rate_entry = tk.Entry(root, textvariable=self.frame_rate)
        self.frame_rate_entry.pack(pady=5)

        self.play_button = tk.Button(root, text="Play", command=self.play_animation)
        self.play_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = tk.Button(root, text="Stop", command=self.stop_animation)
        self.stop_button.pack(side=tk.LEFT, padx=5)

        self.prev_button = tk.Button(root, text="Previous", command=self.prev_frame)
        self.prev_button.pack(side=tk.LEFT, padx=5)

        self.next_button = tk.Button(root, text="Next", command=self.next_frame)
        self.next_button.pack(side=tk.LEFT, padx=5)

        self.add_frame_button = tk.Button(root, text="Add Frame", command=self.add_frame)
        self.add_frame_button.pack(side=tk.LEFT, padx=5)

        # Load initial image frames from user input
        self.load_initial_frames()

        # Display the initial frame
        self.display_frame()

    def display_frame(self):
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.frame_images[self.current_frame])

        # Update frame label
        self.frame_label.config(text=f"Frame: {self.current_frame}")

        # Schedule the next frame display if the animation is playing
        if getattr(self, 'animating', False):
            delay = int(1000 / self.frame_rate.get())
            self.root.after(delay, self.next_frame)

    def play_animation(self):
        if not getattr(self, 'animating', False):
            self.animating = True
            self.play_button.config(text="Pause")
            self.display_frame()

    def stop_animation(self):
        if getattr(self, 'animating', False):
            self.animating = False
            self.play_button.config(text="Play")

    def next_frame(self):
        if self.current_frame < len(self.frame_images) - 1:
            self.current_frame += 1
        else:
            self.current_frame = 0
        self.display_frame()

    def prev_frame(self):
        if self.current_frame > 0:
            self.current_frame -= 1
        else:
            self.current_frame = len(self.frame_images) - 1
        self.display_frame()

    def add_frame(self):
        file_path = filedialog.askopenfilename(title="Select Frame Image", filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])
        if file_path:
            img = Image.open(file_path)
            img.thumbnail((400, 400))
            self.frame_images.append(ImageTk.PhotoImage(img))
            self.display_frame()

    def load_initial_frames(self):
        for _ in range(1):  # Load 5 initial frames (you can adjust this number)
            file_path = filedialog.askopenfilename(title="Select Initial Frame Image", filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])
            if file_path:
                img = Image.open(file_path)
                img.thumbnail((400, 400))
                self.frame_images.append(ImageTk.PhotoImage(img))

root = tk.Tk()
app = Simple2DAnimator(root)
root.mainloop()
