# ======================================
# DeFiChain Intelligence v5
# Daily Image Generator Engine
# ======================================

import os
from PIL import Image, ImageDraw


def generate_daily_image(market=None, intelligence=None, output_path="outputs/daily_update.png"):
    """
    Erzeugt ein einzelnes, ansprechendes Infografik-Bild (1200x675) für X.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    width, height = 1200, 675
    img = Image.new("RGB", (width, height), color=(15, 23, 42))  # Dark Slate Blue
    draw = ImageDraw.Draw(img)

    # Rahmengestaltung
    draw.rectangle([30, 30, width - 30, height - 30], outline=(0, 211, 149), width=4)
    draw.rectangle([30, 30, width - 30, 110], fill=(30, 41, 59))

    # Header
    draw.text((60, 50), "🚀 DeFiChain Intelligence Daily", fill=(255, 255, 255))

    # Daten abfragen
    if not isinstance(market, dict):
        market = {}
    if not isinstance(intelligence, dict):
        intelligence = {}

    dfi_price = market.get("dfi", {}).get("price", market.get("dfi", {}).get("usd", "N/A"))
    dfi_change = market.get("dfi", {}).get("change", "0.0")
    score = intelligence.get("total", "N/A")
    status = intelligence.get("status", "N/A")

    # Block 1: DFI Price
    draw.rectangle([60, 150, 570, 350], fill=(30, 41, 59), outline=(51, 65, 85), width=2)
    draw.text((90, 180), "💎 DFI Price (USD)", fill=(148, 163, 184))
    draw.text((90, 230), f"${dfi_price}", fill=(255, 255, 255))
    
    try:
        change_val = float(dfi_change)
        change_color = (0, 211, 149) if change_val >= 0 else (239, 68, 68)
    except (ValueError, TypeError):
        change_color = (255, 255, 255)
        
    draw.text((90, 280), f"24h: {dfi_change}%", fill=change_color)

    # Block 2: Intelligence Score
    draw.rectangle([630, 150, 1140, 350], fill=(30, 41, 59), outline=(51, 65, 85), width=2)
    draw.text((660, 180), "🧠 Intelligence Score", fill=(148, 163, 184))
    draw.text((660, 230), f"{score} / 100", fill=(255, 255, 255))
    draw.text((660, 280), f"Status: {status}", fill=(255, 255, 255))

    # Footer
    draw.text((60, 600), "Automated Update via DeFiChain Intelligence v5", fill=(100, 116, 139))

    img.save(output_path, "PNG")
    print(f"🖼️ Tägliches Infografik-Bild erstellt: {output_path}", flush=True)
    return output_path


def generate_all_charts(market=None, tokenomics=None, dusd=None, intelligence=None, global_crypto=None):
    """
    Hauptschnittstelle für die Bilderstellung.
    """
    generate_daily_image(market=market, intelligence=intelligence, output_path="outputs/daily_update.png")
