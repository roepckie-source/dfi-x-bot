import numpy as np
from PIL import Image
import imageio.v2 as imageio
import os

def create_smooth_fade_gif(image_paths, output_gif_path="daily_update.gif", hold_sec=2.5, fade_sec=0.5, fps=20):
    """
    Erstellt ein GIF mit weichem Überblenden zwischen den Bildern.
    - hold_sec: Wie lange jedes Hauptbild gezeigt wird.
    - fade_sec: Dauer der Überblendung zwischen zwei Bildern.
    """
    frames = []
    hold_frames = int(hold_sec * fps)
    fade_frames = int(fade_sec * fps)
    
    # 1. Bilder laden und auf einheitliche Größe bringen
    loaded_imgs = []
    first_size = None
    for path in image_paths:
        if os.path.exists(path):
            img = Image.open(path).convert('RGB')
            if first_size is None:
                first_size = img.size
            else:
                img = img.resize(first_size, Image.Resampling.LANCZOS)
            loaded_imgs.append(np.array(img, dtype=np.float32))

    if not loaded_imgs:
        raise FileNotFoundError("Keine gültigen Bilder gefunden.")

    # 2. Frames erzeugen (Halten + Überblenden)
    num_imgs = len(loaded_imgs)
    for i in range(num_imgs):
        curr_img = loaded_imgs[i]
        next_img = loaded_imgs[(i + 1) % num_imgs]  # Für Endlos-Schleife zurück zum 1. Bild

        # Hauptbild halten
        for _ in range(hold_frames):
            frames.append(curr_img.astype(np.uint8))

        # Crossfade zum nächsten Bild
        for f in range(fade_frames):
            alpha = (f + 1) / (fade_frames + 1)
            blended = (1 - alpha) * curr_img + alpha * next_img
            frames.append(blended.astype(np.uint8))

    # 3. GIF speichern
    imageio.mimsave(output_gif_path, frames, fps=fps, loop=0)
    print(f"GIF erfolgreich mit Transitions erstellt: {output_gif_path}")
    return output_gif_path

# Beispiel-Aufruf:
# create_smooth_fade_gif(["chart_1.png", "chart_2.png", "summary.png"])
