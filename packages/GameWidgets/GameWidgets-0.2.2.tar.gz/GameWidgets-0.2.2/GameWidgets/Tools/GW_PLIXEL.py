import tkinter as tk
from tkinter import ttk, colorchooser, filedialog, messagebox
from PIL import Image, ImageDraw, ImageTk

class PixelArtEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("GW Plixel ALPHA v0.0.1 ~Manomay Tyagi ")

        # Display warning popup on startup
        self.show_startup_warning()

        # Create a frame to hold the UI elements
        ui_frame = ttk.Frame(root, padding=(10, 10, 10, 10))
        ui_frame.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))

        # Create a frame to hold the Canvas
        canvas_frame = ttk.Frame(root, padding=(10, 10, 10, 10))
        canvas_frame.grid(column=1, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))

        # Canvas settings
        self.canvas_width = tk.IntVar(value=400)
        self.canvas_height = tk.IntVar(value=400)
        self.pixel_size = 10
        self.current_color = "black"
        self.tool = "draw"

        # Canvas
        self.canvas = tk.Canvas(canvas_frame, width=self.canvas_width.get(), height=self.canvas_height.get(), bg="white")
        self.canvas.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))

        self.canvas.bind("<B1-Motion>", self.handle_tool)

        # Save button
        self.save_button = ttk.Button(ui_frame, text="Save", command=self.save_pixel_art)
        self.save_button.grid(column=0, row=0, pady=5, sticky=tk.W)

        # Load button
        self.load_button = ttk.Button(ui_frame, text="Load", command=self.load_pixel_art)
        self.load_button.grid(column=0, row=1, pady=5, sticky=tk.W)

        # Pick Color button
        self.pick_color_button = ttk.Button(ui_frame, text="Pick Color", command=self.pick_color)
        self.pick_color_button.grid(column=0, row=2, pady=5, sticky=tk.W)

        # Color Palette
        self.color_palette_label = ttk.Label(ui_frame, text="Color Palette:")
        self.color_palette_label.grid(column=0, row=3, pady=(5, 2), sticky=tk.W)

        self.color_palette = {"#000000": "Black", "#FFFFFF": "White", "#FF0000": "Red", "#00FF00": "Green",
                      "#0000FF": "Blue", "#FFFF00": "Yellow", "#FF00FF": "Magenta", "#00FFFF": "Cyan"}
        self.palette_buttons = []

        for i, (color, name) in enumerate(self.color_palette.items()):
            button = ttk.Button(ui_frame, text=name, width=8, command=lambda c=color: self.set_palette_color(c))
            button.grid(column=i % 4, row=4 + i // 4, pady=2, padx=2, sticky=tk.W)
            button.configure(style="PaletteButton.TButton", compound=tk.CENTER)
            self.palette_buttons.append(button)



        # Tools
        #tool_label = ttk.Label(ui_frame, text="Current Tool:")
        #tool_label.grid(column=0, row=8, pady=(5, 2), sticky=tk.W)
        
        self.current_tool_label = ttk.Label(ui_frame, text=self.tool.capitalize())
        self.current_tool_label.grid(column=0, row=9, pady=5, sticky=tk.W)

        self.tools = {
            "draw": self.draw_pixel,
            "erase": self.erase_pixel
        }

        self.tool_buttons = {}
        for i, tool in enumerate(self.tools, start=10):
            button = ttk.Button(ui_frame, text=tool.capitalize(), command=lambda t=tool: self.set_tool(t))
            button.grid(column=0, row=i, pady=5, sticky=tk.W)
            self.tool_buttons[tool] = button

        # Clear button
        self.clear_button = ttk.Button(ui_frame, text="Clear", command=self.clear_canvas)
        self.clear_button.grid(column=0, row=i+1, pady=(10, 5), sticky=tk.W)

        # Help button for popup
        self.help_button = ttk.Button(ui_frame, text="Help", command=self.show_help_popup)
        self.help_button.grid(column=0, row=i+2, pady=10, sticky=tk.W)

        # Canvas width slider
        width_label = ttk.Label(ui_frame, text="Canvas Width:")
        width_label.grid(column=0, row=i+3, pady=5, sticky=tk.W)

        self.width_slider = tk.Scale(ui_frame, from_=100, to=1000, orient=tk.HORIZONTAL, label="",
                                     variable=self.canvas_width, command=self.update_canvas_size, resolution=10,
                                     sliderlength=15, length=200)
        self.width_slider.grid(column=0, row=i+4, pady=5, sticky=tk.W)

        # Canvas height slider
        height_label = ttk.Label(ui_frame, text="Canvas Height:")
        height_label.grid(column=0, row=i+5, pady=5, sticky=tk.W)

        self.height_slider = tk.Scale(ui_frame, from_=100, to=800, orient=tk.HORIZONTAL, label="",
                                      variable=self.canvas_height, command=self.update_canvas_size, resolution=10,
                                      sliderlength=15, length=200)
        self.height_slider.grid(column=0, row=i+6, pady=5, sticky=tk.W)

        # Ensure initial canvas size is correct
        self.update_canvas_size()

        # Track the last pixel drawn
        self.last_pixel = None

    def update_canvas_size(self, event=None):
        new_canvas_width = self.canvas_width.get() - 2
        new_canvas_height = self.canvas_height.get() - 2
        self.canvas.config(width=new_canvas_width, height=new_canvas_height)

        # Redraw the pixels on the canvas after resizing
        items = self.canvas.find_all()
        for item in items:
            x, y, _, _ = self.canvas.coords(item)
            pixel_color = self.canvas.itemcget(item, "fill")
            self.canvas.create_rectangle(x, y, x + self.pixel_size, y + self.pixel_size, fill=pixel_color, outline="")

    def handle_tool(self, event):
        x = event.x
        y = event.y

        pixel_x = int(x // self.pixel_size)
        pixel_y = int(y // self.pixel_size)

        if (pixel_x, pixel_y) != self.last_pixel:
            self.last_pixel = (pixel_x, pixel_y)
            pixel_x_start = pixel_x * self.pixel_size
            pixel_y_start = pixel_y * self.pixel_size

            tool_function = self.tools[self.tool]
            tool_function(pixel_x_start, pixel_y_start)

    def draw_pixel(self, x, y):
        self.canvas.create_rectangle(
            x, y, x + self.pixel_size, y + self.pixel_size, fill=self.current_color, outline=""
        )

    def erase_pixel(self, x, y):
        items = self.canvas.find_overlapping(x, y, x + self.pixel_size, y + self.pixel_size)
        for item in items:
            self.canvas.delete(item)

    def save_pixel_art(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])

        if file_path:
            try:
                canvas_image = self.get_canvas_image()
                canvas_image.save(file_path)
            except Exception as e:
                print(f"Error saving pixel art: {e}")

    def load_pixel_art(self):
        file_path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")])

        if file_path:
            try:
                image = Image.open(file_path)
                self.display_image_on_canvas(image)
            except Exception as e:
                print(f"Error loading pixel art: {e}")

    def display_image_on_canvas(self, image):
        tk_image = ImageTk.PhotoImage(image)
        self.canvas.config(width=image.width, height=image.height)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)
        self.canvas.tk_image = tk_image

    def get_canvas_image(self):
        canvas_image = Image.new("RGB", (self.canvas_width.get(), self.canvas_height.get()), "white")
        draw = ImageDraw.Draw(canvas_image)

        for item in self.canvas.find_all():
            x, y, _, _ = self.canvas.coords(item)
            pixel_color = self.canvas.itemcget(item, "fill")
            draw.rectangle([x, y, x + self.pixel_size, y + self.pixel_size], fill=pixel_color)

        return canvas_image.resize((self.canvas_width.get(), self.canvas_height.get()), Image.NEAREST)

    def pick_color(self):
        color = colorchooser.askcolor(initialcolor=self.current_color)[1]
        if color:
            self.current_color = color

    def set_tool(self, tool):
        self.tool = tool
        self.current_tool_label.config(text=f"Current Tool: {tool.capitalize()}")
        self.line_start = None

    def set_palette_color(self, color):
        self.current_color = color

    def clear_canvas(self):
        self.canvas.delete("all")
        self.last_pixel = None

    def show_startup_warning(self):
        warning_message = "Welcome to GW Plixel v0.0.1!\n\nPlease note that this is a simple editor and might lack advanced features.\n\nThis is still in ALPHA development phase. Check the 'Help' button for more intruction."
        messagebox.showinfo("Welcome", warning_message)

    def show_help_popup(self):
        help_message = "Pixel Art Editor Help:\n\n- Use the 'Draw' tool to paint pixels.\n- Use the 'Erase' tool to remove pixels.\n- Click 'Pick Color' to choose a new color.\n- Save and Load your pixel art using the respective buttons.\n- Use the sliders to adjust canvas size.\n\nThere are many glitches to this paint editor, advised that you resize before you draw anything to reduce lag. As well as that, make sure not to use erase after loading in a png."
        messagebox.showinfo("Help", help_message)



root = tk.Tk()
style = ttk.Style(root)
style.configure("TButton", padding=(5, 5, 5, 5), font='Helvetica 10')
editor = PixelArtEditor(root)
root.mainloop()
