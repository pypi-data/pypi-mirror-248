from borders import frame

# Example 3: Using tuple to set different colours for each line
output = [
    "This text's color is Blue (System Color)",
    ("This text's color is Aquamarine", "Aquamarine"),
    ("This text's color is Coral","255;127;80"),
    ("This text's color is Cosmic Latte","#FFF8E7"),
    ("This text is highlighted in Yellow", "", "x226"),
    ("Frame's color is Red (System Color)", 31),
    "This text's color is back to Blue (System Color)"
]

frame(output, colour=34, frame_colour=31)