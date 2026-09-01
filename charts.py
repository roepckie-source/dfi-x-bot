# ======================================
# DeFiChain Intelligence v5
# Chart & GIF Generation Engine
# ======================================

import os
import numpy as np
from PIL import Image, ImageDraw


def safe_load_image(file_path):
    """
    Lädt ein Bild sicher und konvertiert es in ein RGB PIL Image.
    Erzeugt bei Fehler oder Nicht-Existenz ein aussagekräftiges Fallback-Bild.
    """
    try:
        if os.path.exists(file_path):
            return Image.open(file_path).convert("RGB")
    except Exception as e:
        print(f"⚠️ Fehler beim Laden des Bildes {file_path}: {e}")

    # Fallback-Bild mit Text
    fallback = Image.new("RGB", (800, 450), color=(15, 23, 42))
    draw = ImageDraw.Draw(fallback)
    draw.text((40, 200), f"Chart visualizing...\n{os.path.basename(file_path)}", fill=(255, 255, 255))
    return fallback


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


def create_smooth_fade_gif(image_files, output_gif_path="outputs/daily_update.gif", fps=10, display_duration=2.0, fade_duration=0.5):
    """
    Erstellt ein X-kompatibles animiertes GIF mit Pillow (löst das Schwarzbild-Problem).
    """
    try:
        os.makedirs(os.path.dirname(output_gif_path), exist_ok=True)

        loaded_images = [safe_load_image(f) for f in image_files]

        if not loaded_images:
            print("⚠️ Keine gültigen Bilder für die GIF-Erstellung vorhanden.")
            return False

        target_size = loaded_images[0].size  # (width, height)

        # Standardisieren der Größen
        standardized_images = []
        for img in loaded_images:
            if img.size != target_size:
                standardized_images.append(img.resize(target_size, Image.Resampling.LANCZOS))
            else:
                standardized_images.append(img)

        display_frames = int(display_duration * fps)
        fade_frames = int(fade_duration * fps)

        frames = []
        num_images = len(standardized_images)

        for i in range(num_images):
            current_img = np.array(standardized_images[i], dtype=np.float32)
            next_img = np.array(standardized_images[(i + 1) % num_images], dtype=np.float32)

            # Standzeit des Bildes
            for _ in range(display_frames):
                frames.append(Image.fromarray(current_img.astype(np.uint8)))

            # Overlap/Fade
            for f in range(fade_frames):
                alpha = f / float(fade_frames)
                blended = (1.0 - alpha) * current_img + alpha * next_img
                frames.append(Image.fromarray(blended.astype(np.uint8)))

        # WICHTIG FOR X: Konvertieren zu 'P' Palette mit ordnungsgemäßem Save
        frame_duration_ms = int(1000 / fps)
        
        # Konvertieren aller Frames in Paletten-Modus für GIF
        palette_frames = [f.convert("P", palette=Image.Palette.ADAPTIVE, colors=256) for f in frames]

        palette_frames[0].save(
            output_gif_path,
            save_all=True,
            append_images=palette_frames[1:],
            optimize=True,
            duration=frame_duration_ms,
            loop=0
        )

        print(f"✅ X-Kompatibles GIF erfolgreich erstellt ({fps} FPS): {output_gif_path}")
        return True

    except Exception as e:
        print(f"❌ Fehler bei der GIF-Erstellung: {e}")
        return False


def create_animated_summary_gif(image_files, output_gif_path="outputs/daily_update.gif", fps=10, display_duration=2.0, fade_duration=0.5):
    return create_smooth_fade_gif(image_files, output_gif_path, fps, display_duration, fade_duration)


def generate_all_charts(market=None, tokenomics=None, dusd=None, intelligence=None, global_crypto=None):
    """
    Erzeugt alle benötigten Einzelgrafiken und baut daraus das animierte GIF auf.
    """
    os.makedirs("outputs", exist_ok=True)
    
    chart1 = "outputs/chart1.png"
    chart2 = "outputs/chart2.png"
    summary = "outputs/summary.png"

    generate_summary_chart(chart1, title="Market Metrics")
    generate_summary_chart(chart2, title="Intelligence Score")
    generate_summary_chart(summary, title="Summary Overview")
    
    chart_files = [chart1, chart2, summary]
    create_animated_summary_gif(chart_files, output_gif_path="outputs/daily_update.gif")
