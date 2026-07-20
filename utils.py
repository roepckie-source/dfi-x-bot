# ==============================
# UTILS - Hilfsfunktionen
# ==============================


def format_number(value):

    try:
        return f"{float(value):,.2f}"

    except:
        return "N/A"



def format_price(value):

    try:
        return f"${float(value):.8f}"

    except:
        return "N/A"



def format_percent(value):

    try:

        value = float(value)

        if value >= 0:
            return f"🟢 +{value:.2f}%"

        else:
            return f"🔴 {value:.2f}%"

    except:

        return "N/A"



def format_large_number(value):

    try:

        value = float(value)

        if value >= 1_000_000_000:
            return f"{value/1_000_000_000:.2f}B"

        if value >= 1_000_000:
            return f"{value/1_000_000:.2f}M"

        if value >= 1_000:
            return f"{value/1_000:.2f}K"

        return f"{value:.0f}"

    except:

        return "N/A"
