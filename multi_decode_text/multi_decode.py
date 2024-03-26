# Скрипт декодирования строки формата "binary_encoding|hex_encoding|base64_encoding|..."
import base64

# Название файла можно изменить
with open("multi_encoding_text.txt", "r") as f:
    text = f.read()
    
chars = text.split("|")
result = ""

for char in range(0, len(chars)-2, 3):
    result += chr(int(chars[char], 2))
    result += chr(int(chars[char+1], 16))
    result += base64.b64decode(chars[char+2]).decode()
    
print(result)
