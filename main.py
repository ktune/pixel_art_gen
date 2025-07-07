import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
import glob

class PixelArtApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Retro Pixel Art Generator")
        self.root.geometry("700x600")
        self.root.configure(bg="#f0f0f0")

        self.original_image = None
        self.pixel_art_image = None

        # Upload and Reset buttons
        btn_frame = tk.Frame(root, bg="#f0f0f0")
        btn_frame.pack(pady=10)

        self.upload_btn = tk.Button(btn_frame, text="Upload Image", command=self.upload_image)
        self.upload_btn.grid(row=0, column=0, padx=10)

        self.reset_btn = tk.Button(btn_frame, text="Reset", command=self.reset)
        self.reset_btn.grid(row=0, column=1, padx=10)

        # Sliders
        self.pixel_size_slider = tk.Scale(root, from_=4, to=64, orient=tk.HORIZONTAL, label="Pixel Size", bg="#f0f0f0")
        self.pixel_size_slider.set(16)
        self.pixel_size_slider.pack(fill='x', padx=50)

        self.color_depth_slider = tk.Scale(root, from_=2, to=64, orient=tk.HORIZONTAL, label="Color Depth", bg="#f0f0f0")
        self.color_depth_slider.set(16)
        self.color_depth_slider.pack(fill='x', padx=50)

        # Convert button
        btn2_frame = tk.Frame(root, bg="#f0f0f0")
        btn2_frame.pack(pady=5)

        self.convert_btn = tk.Button(btn2_frame, text="Convert to Pixel Art", command=self.convert_image)
        self.convert_btn.grid(row=0, column=0, padx=10)

        # Image display
        self.image_frame = tk.Frame(root, bg="#f0f0f0")
        self.image_frame.pack(pady=15)

        tk.Label(self.image_frame, text="Original", bg="#f0f0f0").grid(row=0, column=0)
        tk.Label(self.image_frame, text="Pixelated", bg="#f0f0f0").grid(row=0, column=1)

        self.original_canvas = tk.Label(self.image_frame, bg="#e0e0e0", width=256, height=256)
        self.original_canvas.grid(row=1, column=0, padx=20)

        self.pixel_canvas = tk.Label(self.image_frame, bg="#e0e0e0", width=256, height=256)
        self.pixel_canvas.grid(row=1, column=1, padx=20)
        self.pixel_canvas.bind("<Button-1>", self.show_fullscreen_preview)

        # Drag and drop (optional)
        self.root.drop_target_register = getattr(self.root, 'drop_target_register', lambda *args: None)
        self.root.dnd_bind = getattr(self.root, 'dnd_bind', lambda *args: None)
        self.setup_drag_and_drop()

    def setup_drag_and_drop(self):
        try:
            import tkinterdnd2 as dnd
            self.root.drop_target_register(dnd.DND_FILES)
            self.root.dnd_bind('<<Drop>>', self.drop_file)
        except:
            pass

    def drop_file(self, event):
        file_path = event.data.strip().strip('{}')
        if os.path.isfile(file_path):
            self.load_image(file_path)

    def upload_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.load_image(file_path)

    def load_image(self, file_path):
        self.original_image = Image.open(file_path).convert("RGB")
        self.original_image = self.original_image.resize((256, 256))
        self.display_image(self.original_image, self.original_canvas)

    def convert_image(self):
        if not self.original_image:
            return

        pixel_size = self.pixel_size_slider.get()
        color_depth = self.color_depth_slider.get()

        small = self.original_image.resize(
            (self.original_image.width // pixel_size, self.original_image.height // pixel_size),
            resample=Image.NEAREST
        )
        result = small.resize(self.original_image.size, Image.NEAREST)
        result = result.convert("P", palette=Image.ADAPTIVE, colors=color_depth).convert("RGB")

        self.pixel_art_image = result
        self.display_image(result, self.pixel_canvas)

        # Auto-save to output folder with unique name
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)

        existing_files = glob.glob(os.path.join(output_dir, "pixel_art_*.png"))
        next_number = len(existing_files) + 1
        filename = f"pixel_art_{next_number}.png"
        save_path = os.path.join(output_dir, filename)

        self.pixel_art_image.save(save_path)
        messagebox.showinfo("Saved", f"Pixel art saved to:\n{save_path}")

    def show_fullscreen_preview(self, event):
        if not self.pixel_art_image:
            return

        preview_win = tk.Toplevel(self.root)
        preview_win.title("Full-size Pixel Art Preview")
        img = self.pixel_art_image.resize((512, 512), Image.NEAREST)
        tk_img = ImageTk.PhotoImage(img)

        label = tk.Label(preview_win, image=tk_img)
        label.image = tk_img
        label.pack()

    def display_image(self, pil_img, canvas):
        tk_img = ImageTk.PhotoImage(pil_img)
        canvas.config(image=tk_img)
        canvas.image = tk_img

    def reset(self):
        self.original_image = None
        self.pixel_art_image = None
        self.original_canvas.config(image='', text='')
        self.pixel_canvas.config(image='', text='')
        self.pixel_size_slider.set(16)
        self.color_depth_slider.set(16)

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = PixelArtApp(root)
    root.mainloop()
