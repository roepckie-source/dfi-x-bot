# ======================================
# DeFiChain Intelligence v5
# Chart & GIF Generation Engine
# ======================================

import os
import numpy as np
import imageio.v2 as imageio
from PIL import Image


def safe_load_image(file_path):
    """
    Lädt ein Bild sicher und konvertiert es in ein NumPy-Array (RGB).
    Erzeugt bei Fehlern oder Nicht-Existenz ein leeres Fallback-Bild.
    """
    try:
        if os.path.exists(file_path):
            img = Image.open(file_path).convert("RGB")
            return np.array(img)
    except Exception as e:
        print(f"⚠️ Fehler beim Laden des Bildes {file_path}: {e}")

    # Fallback-Bild (Dunkles Canvas 800x450), falls Bild nicht geladen werden konnte
    fallback = Image.new("RGB", (800, 450), color=(15, 23, 42))
    return np.array(fallback)


def create_smooth_fade_gif(image_files, output_gif_path="outputs/daily_update.gif", fps=15, display_duration=2.5, fade_duration=0.8):
    """
    Erstellt ein flüssiges GIF aus mehreren Bildern mit sanftem Cross-Fade Übergang.
    
    :param image_files: Liste von Pfaden zu den PNG/JPG-Dateien
    :param output_gif_path: Ausgabepfad für das GIF
    :param fps: Bilder pro Sekunde (Frames Per Second) - optimiert auf 15 fps
    :param display_duration: Wie lange jedes Hauptbild stehen bleibt (in Sekunden)
    :param fade_duration: Dauer der Überblendung zwischen zwei Bildern (in Sekunden)
    """
    try:
        # Ordner erstellen, falls nicht vorhanden
        os.makedirs(os.path.dirname(output_gif_path), exist_ok=True)

        loaded_images = []
        for file in image_files:
            img_arr = safe_load_image(file)
            loaded_images.append(img_arr)

        if not loaded_images:
            print("⚠️ Keine gültigen Bilder für die GIF-Erstellung vorhanden.")
            return False

        # Zielgröße vom ersten Bild übernehmen
        target_height, target_width, _ = loaded_images[0].shape

        # Alle Bilder an die einheitliche Zielgröße anpassen
        standardized_images = []
        for img_arr in loaded_images:
            if img_arr.shape[:2] != (target_height, target_width):
                pil_img = Image.fromarray(img_arr)
                pil_img = pil_img.resize((target_width, target_height), Image.Resampling.LANCZOS)
                standardized_images.append(np.array(pil_img))
            else:
                standardized_images.append(img_arr)

        display_frames = int(display_duration * fps)
        fade_frames = int(fade_duration * fps)

        all_frames = []
        num_images = len(standardized_images)

        for i in range(num_images):
            current_img = standardized_images[i].astype(np.float32)
            next_img = standardized_images[(i + 1) % num_images].astype(np.float32)

            # Standzeit des aktuellen Bildes
            for _ in range(display_frames):
                all_frames.append(current_img.astype(np.uint8))

            # Cross-Fade Übergang zum nächsten Bild
            for f in range(fade_frames):
                alpha = f / float(fade_frames)
                blended = (1.0 - alpha) * current_img + alpha * next_img
                all_frames.append(blended.astype(np.uint8))

        # Als GIF speichern
        imageio.mimsave(output_gif_path, all_frames, fps=fps)
        print(f"✅ GIF erfolgreich erstellt ({fps} FPS): {output_gif_path}")
        return True

    except Exception as e:
        print(f"❌ Fehler bei der GIF-Erstellung: {e}")
        return False


# Alias-Funktion bereitstellen
def create_animated_summary_gif(image_files, output_gif_path="outputs/daily_update.gif", fps=15, display_duration=2.5, fade_duration=0.8):
    return create_smooth_fade_gif(image_files, output_gif_path, fps, display_duration, fade_duration)
def generate_all_charts(market=None, tokenomics=None, dusd=None, intelligence=None, global_crypto=None):
    """Fallback-Wrapper zum Generieren aller Grafiken."""
    os.makedirs("outputs", exist_ok=True)
    
    # Standard Einzelbilder erzeugen
    generate_summary_chart()
    
    # GIF direkt vorab erstellen
    chart_files = ["outputs/summary.png"]
    create_animated_summary_gif(chart_files, output_gif_path="outputs/daily_update.gif", fps=15)
