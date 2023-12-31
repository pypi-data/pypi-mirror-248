from PIL import Image
import pygame
pygame.init()
class Pixelate:
    def __init__(self,image_path:str, pixel_size:int, download_path:str, show_image:bool):
        image = Image.open(image_path)
        self.download_path = download_path
        image_tiny = image.resize((pixel_size,pixel_size))    # resize it to a relatively tiny size
        # pixeliztion is resizing a smaller image into a larger one with some resampling
        self.pixelated = image_tiny.resize(image.size,Image.NEAREST)   # resizing the smaller image to the original size
        # Image.NEARESEST is the resampling function predefined in the Image class
        self.show_image = show_image
        
    def save_image(self):
        if self.show_image:
            self.pixelated.show("image.png")
        self.pixelated.save(self.download_path)