from A_4 import create_index
from A_4 import compress_index
#create_index("animals.txt", "./output/", True)
print("animals, WAH, 8")
compress_index("animals", "./output/", "WAH", 8)
print("animals, WAH, 16")
compress_index("animals", "./output/", "WAH", 16)
print("animals, WAH, 32")
compress_index("animals", "./output/", "WAH", 32)
print("animals, WAH, 64")
compress_index("animals", "./output/", "WAH", 64)
print("animals, BBC")
compress_index("animals", "./output/", "BBC", 8)
print("animals_sorted, WAH, 8")
compress_index("animals_sorted", "./output/", "WAH", 8)
print("animals_sorted, WAH, 16")
compress_index("animals_sorted", "./output/", "WAH", 16)
print("animals_sorted, WAH, 32")
compress_index("animals_sorted", "./output/", "WAH", 32)
print("animals_sorted, WAH, 64")
compress_index("animals_sorted", "./output/", "WAH", 64)
print("animals_sorted, BBC")
compress_index("animals_sorted", "./output/", "BBC", 8)