import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import os
import subprocess
class AutoIndentText(tk.Text):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.bind("<Return>", self.auto_indent)
        self.bind("<Tab>", self.insert_small_indent)

    def auto_indent(self, event):
        current_line = self.index(tk.INSERT).split('.')[0]
        current_line_text = self.get(f"{current_line}.0", f"{current_line}.end")

        # Calculate the indentation of the current line
        indentation = len(current_line_text) - len(current_line_text.lstrip())

        # Insert a new line with the same indentation
        self.insert(tk.INSERT, "\n" + " " * indentation)
        return "break"  # Prevent the default behavior of the Enter key

    def insert_small_indent(self, event):
        # Insert a small indent (e.g., 4 spaces) when the Tab key is pressed
        self.insert(tk.INSERT, " " * 4)
        return "break"  # Prevent the default behavior of the Tab key

class SimpleGameEngine:
    def __init__(self, master):
        self.master = master
        self.master.title("Simple Game Engine")

        self.current_project_path = None
        self.current_file_path = None

        self.create_menus()
        self.create_start_screen()
        self.entity_code = '''
import pygame
pygame.init()
class Entity:
    def __init__(self,screen):
        self.screen = screen
        self.x = 100
        self.y = 100
        self.surf = pygame.Surface((20,20))
        self.rect = self.surf.get_rect()
        self.rect.midbottom = (self.x,self.y)
        self.color = (255,255,255)
    
    def draw(self):
        self.surf.fill(self.color)
        self.screen.blit(self.surf,self.rect)
    
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.y-=1
        if keys[pygame.K_DOWN]:
            self.y+=1
        if keys[pygame.K_RIGHT]:
            self.x+=1
        if keys[pygame.K_LEFT]:
            self.x-=1
        self.rect.midbottom = (self.x,self.y)
        self.animate()
    
    def animate(self):
        #Animate Character...
        pass'''

        self.object_code = '''import pygame
pygame.init()
class Object:
    def __init__(self,screen):
        self.screen = screen
        self.x = 100
        self.y = 100
        self.surf = pygame.Surface((20,20))
        self.rect = self.surf.get_rect()
        self.rect.midbottom = (self.x,self.y)
        self.color = (255,255,255)
    
    def draw(self):
        self.surf.fill(self.color)
        self.screen.blit(self.surf,self.rect)
    
    def update(self):
        self.animate()
    
    def animate(self):
        #Animate Character...
        pass'''
        self.image_code = '''import pygame
pygame.init()
class Image:
    def __init__(self,screen):
        self.screen = screen
        self.x = 100
        self.y = 100
        self.surf = pygame.Surface((20,20))
        self.rect = self.surf.get_rect()
        self.rect.midbottom = (self.x,self.y)
        self.color = (255,255,255)
    
    def draw(self):
        self.surf.fill(self.color)
        self.screen.blit(self.surf,self.rect)
    
    def update(self):
        pass'''

    def create_menus(self):
        menubar = tk.Menu(self.master)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New Project", command=self.new_project)
        file_menu.add_command(label="Load Project", command=self.load_project)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.master.destroy)
        menubar.add_cascade(label="File", menu=file_menu)

        template_menu = tk.Menu(menubar, tearoff=0)
        template_menu.add_command(label="Entity", command=lambda: self.create_template("entity.py", self.entity_code))
        template_menu.add_command(label="Object", command=lambda: self.create_template("object.py", self.object_code))
        template_menu.add_command(label="Image", command=lambda: self.create_template("image.py", self.image_code))
        template_menu.add_command(label="Blank", command=lambda: self.create_template("blank.py", "# Blank template"))
        menubar.add_cascade(label="Templates", menu=template_menu)

        run_menu = tk.Menu(menubar, tearoff=0)
        run_menu.add_command(label="Run", command=self.run_game)
        menubar.add_cascade(label="Run", menu=run_menu)

        self.master.config(menu=menubar)

    def create_start_screen(self):
        start_frame = tk.Frame(self.master)
        start_frame.pack(pady=20)

        new_project_btn = tk.Button(start_frame, text="New Project", command=self.new_project)
        new_project_btn.pack(side=tk.LEFT, padx=10)

        load_project_btn = tk.Button(start_frame, text="Load Project", command=self.load_project)
        load_project_btn.pack(side=tk.LEFT, padx=10)

    def new_project(self):
        project_path = filedialog.askdirectory(title="Select Project Directory")
        if project_path:
            project_name = simpledialog.askstring("New Project", "Enter project name:")
            if project_name:
                self.current_project_path = os.path.join(project_path, project_name)
                os.makedirs(self.current_project_path)

                # Create and save main.py with specified code
                main_code = """import pygame
pygame.init()
screen = pygame.display.set_mode((500, 500))
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    screen.fill((0, 0, 0))
    pygame.display.flip()

pygame.quit()
"""
                main_file_path = os.path.join(self.current_project_path, "main.py")
                with open(main_file_path, "w") as main_file:
                    main_file.write(main_code)

                self.create_editor_screen()

    def load_project(self):
        self.current_project_path = filedialog.askdirectory(title="Select Project Folder")
        if self.current_project_path:
            self.create_editor_screen()

    def create_editor_screen(self):
        editor_frame = tk.Frame(self.master)
        editor_frame.pack(pady=20)

        file_tree_frame = tk.Frame(editor_frame)
        file_tree_frame.pack(side=tk.LEFT, padx=10)

        self.file_tree = tk.Listbox(file_tree_frame, selectmode=tk.SINGLE)
        self.file_tree.pack()

        self.refresh_file_tree()

        text_editor_frame = tk.Frame(editor_frame)
        text_editor_frame.pack(side=tk.LEFT, padx=10)

        self.text_editor = AutoIndentText(text_editor_frame, wrap=tk.WORD)
        self.text_editor.pack()

        save_btn = tk.Button(text_editor_frame, text="Save", command=self.save_file)
        save_btn.pack(pady=10)

        rename_entry = tk.Entry(text_editor_frame)
        rename_entry.insert(0, "main.py")  # Default filename
        rename_entry.pack(pady=10)

        rename_btn = tk.Button(text_editor_frame, text="Rename", command=lambda: self.rename_file(rename_entry.get()))
        rename_btn.pack(pady=10)

    def refresh_file_tree(self):
        self.file_tree.delete(0, tk.END)

        if self.current_project_path:
            files = os.listdir(self.current_project_path)
            for file in files:
                self.file_tree.insert(tk.END, file)

        self.file_tree.bind("<ButtonRelease-1>", self.load_selected_file)

    def load_selected_file(self, event):
        selected_file = self.file_tree.get(self.file_tree.curselection())
        if selected_file:
            self.current_file_path = os.path.join(self.current_project_path, selected_file)
            with open(self.current_file_path, "r") as file:
                content = file.read()
                self.text_editor.delete(1.0, tk.END)
                self.text_editor.insert(tk.END, content)

    def save_file(self):
        if self.current_file_path:
            with open(self.current_file_path, "w") as file:
                file.write(self.text_editor.get(1.0, tk.END))
            messagebox.showinfo("Save", "File saved successfully.")
        else:
            messagebox.showwarning("Save", "No file selected. Please select a file first.")

    def rename_file(self, new_name):
        if self.current_file_path:
            new_path = os.path.join(self.current_project_path, new_name)
            os.rename(self.current_file_path, new_path)
            self.current_file_path = new_path
            self.refresh_file_tree()
            messagebox.showinfo("Rename", "File renamed successfully.")
        else:
            messagebox.showwarning("Rename", "No file selected. Please select a file first.")

    def create_template(self, filename, content):
        if self.current_project_path:
            template_path = os.path.join(self.current_project_path, filename)
            with open(template_path, "w") as template_file:
                template_file.write(content)
            self.refresh_file_tree()

    def run_game(self):
        if self.current_project_path:
            main_file_path = os.path.join(self.current_project_path, "main.py")
            if os.path.exists(main_file_path):
                subprocess.Popen(["python", main_file_path])
                print("Running the game...")
            else:
                print("Error: main.py not found in the project.")


root = tk.Tk()
game_engine = SimpleGameEngine(root)
root.mainloop()
