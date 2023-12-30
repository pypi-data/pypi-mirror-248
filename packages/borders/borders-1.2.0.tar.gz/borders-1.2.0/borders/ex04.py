from borders import frame

# Example 4: Setting a different styles for the frame
styles = ["single", "double", "double horizontal", "double vertical", "dots", None]

for s in styles:
    # Print out the name of the style in a frame of that style.
    frame(f"{s}", frame_colour="Red", frame_background="Gainsboro", alignment="centre", frame_style=s)
