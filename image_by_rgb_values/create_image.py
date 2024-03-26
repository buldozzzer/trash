# Скрипт создания изображения по заданным значениям RGB для пискселей формата:
# (0, 0): 38, 22, 16
# (1, 0): 25, 9, 3
# (2, 0): 20, 4, 0
# (3, 0): 24, 8, 2
# ...

from PIL import Image  
import re

# Ширина*высота, можно изменить
width = 1280
height = 853

img  = Image.new( mode = "RGB", size = (width, height))

# Название файла со значениями пикселей можно изменить
with open("1280-853.txt", "r") as f:
    for line in f:
        values = re.findall(r'\d+', line)
        values = [int(value) for value in values]
        img.putpixel((values[0],values[1]), (values[2], values[3], values[4]))
        
img.save("result.png")        
img.show()