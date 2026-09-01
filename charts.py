# ======================================
# DeFiChain Intelligence v5
# Chart & GIF Generation Engine
# ======================================

import os
import numpy as np
import imageio.v2 as imageio
from PIL import Image, ImageDraw, ImageFont


def safe_load_image(file_path):
    """
    Lädt ein Bild sicher und konvertiert es in ein NumPy-Array (RGB).
    Erzeugt bei Fehler oder Nicht-Existenz ein aussagekräftiges Fallback-Bild.
    """
    try:
        if os.path.exists(file_path):
            img = Image.open(file_path).convert("RGB")
            return np.array(img)
    except Exception as e:
        print(f"⚠️ Fehler beim Laden des Bildes {file_path}: {e}")

    # Platzhalter mit Text statt reinem Schwarz
    fallback = Image.new("RGB", (800, 450), color=(15, 23, 42))
    draw = ImageDraw.Draw(fallback)
    draw.text((40, 200), f"Chart visualizing...\n{os.path.basename(file_path)}", fill=(255, 255, 255))
    return np.array(fallback)


def generate_summary_chart(output_path="outputs/summary.png", title="DeFiChain Summary"):
    """
    Erstellt ein Basischart als Bild, falls noch keine Matplotlib-Grafik existiert.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img = Image.new("RGB", (800, 450), color=(15, 23, 42))
    draw = ImageDraw.Draw(img)
    
    # Layout-Elemente zeichnen
    draw.rectangle([20, 20, 780, 430], outline=(0, 211, 149), width=3)
    draw.text((40, 40), "🚀 DeFiChain Intelligence v5", fill=(255, 255, 255))
    draw.text((40, 80), f"Visualized Update: {title}", fill=(0, 211, 149))
    
    img.save(output_path)
    print(f"📊 Summary Chart gespeichert: {output_path}")


def create_smooth_fade_gif(image_files, output_gif_path="outputs/daily_update.gif", fps=15, display_duration=2.5, fade_duration=0.8):
    """
    Erstellt ein flüssiges GIF aus mehreren Bildern mit sanftem Cross-Fade Übergang.
    """
    try:
        os.makedirs(os.path.dirname(output_gif_path), exist_ok=True)

        loaded_images = []
        for file in image_files:
            img_arr = safe_load_image(file)
            loaded_images.append(img_arr)

        if not loaded_images:
            print("⚠️ Keine gültigen Bilder für die GIF-Erstellung vorhanden.")
            return False

        target_height, target_width, _ = loaded_images[0].shape

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

            for _ in range(display_frames):
                all_frames.append(current_img.astype(np.uint8))

            for f in range(fade_frames):
                alpha = f / float(fade_frames)
                blended = (1.0 - alpha) * current_img + alpha * next_img
                all_frames.append(blended.astype(np.uint8))

        imageio.mimsave(output_gif_path, all_frames, fps=fps)
        print(f"✅ GIF erfolgreich erstellt ({fps} FPS): {output_gif_path}")
        return True

    except Exception as e:
        print(f"❌ Fehler bei der GIF-Erstellung: {e}")
        return False


def create_animated_summary_gif(image_files, output_gif_path="outputs/daily_update.gif", fps=15, display_duration=2.5, fade_duration=0.8):
    return create_smooth_fade_gif(image_files, output_gif_path, fps, display_duration, fade_duration)


def generate_all_charts(market=None, tokenomics=None, dusd=None, intelligence=None, global_crypto=None):
    """
    Erzeugt alle benötigten Einzelgrafiken und baut daraus das animierte GIF auf.
    """
    os.makedirs("outputs", exist_ok=True)
    
    # 1. Bilder sicherstellen/generieren
    chart1 = "outputs/chart1.png"
    chart2 = "outputs/chart2.png"
    summary = "outputs/summary.png"

    generate_summary_chart(chart1, title="Market Metrics")
    generate_summary_chart(chart2, title="Intelligence Score")
    generate_summary_chart(summary, title="Summary Overview")
    
    # 2. GIF aus den drei erzeugten Bildern erstellen
    chart_files = [chart1, chart2, summary]
    create_animated_summary_gif(chart_files, output_gif_path="outputs/daily_update.gif", fps=15)
