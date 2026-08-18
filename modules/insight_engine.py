import os
import requests


def generate_daily_insight() -> str:
    """Generiert strukturierte Daily Insights und korrigiert Formatierungs- sowie Rechenfehler."""

    # 1. Daten von DeFiChain API & Marktdaten beziehen (Beispieldaten / API-Aufruf)
    dfi_price_change_24h = -41.64  # Prozentwert direkt als float (-41.64%)
    dusd_peg_deviation = -99.93    # Prozentwert direkt als float (-99.93%)

    # Tokenomics: Dynamische Berechnung von Net Burn (Burn minus Emission)
    total_burned_dfi = 351.48      # in Millionen DFI
    total_emitted_dfi = 225.15     # in Millionen DFI
    net_burn_dfi = round(total_burned_dfi - total_emitted_dfi, 2)  # 126.33M DFI

    # 2. Formatierung von Prozentwerten (Vermeidet doppeltes Teilen durch 100)
    def format_percentage(value: float) -> str:
        sign = "+" if value > 0 else ""
        icon = "🟢" if value >= 0 else "🔴"
        return f"{icon} {sign}{value:.2f}%"

    dfi_change_str = format_percentage(dfi_price_change_24h)

    # 3. Textbausteine für Berichte erstellen
    insight_text = (
        f"🔴 Market pressure detected: DFI lost {abs(dfi_price_change_24h):.2f}% in 24h.\n\n"
        f"🔥 Tokenomics positive: Net burn is {net_burn_dfi:.2f} M DFI.\n\n"
        f"⚠️ dUSD remains critical: Peg deviation {dusd_peg_deviation:.2f}%.\n\n"
        f"⛓ Network healthy: Blockchain operating normally."
    )

    return insight_text


def calculate_adjusted_score(dfi_change: float, dusd_dev: float, base_score: int = 55) -> dict:
    """
    Berechnet den Intelligence Score unter Berücksichtigung von Extremrisiken
    (z. B. starker DFI-Drop oder extremer dUSD De-Peg).
    """
    score = base_score

    # Abzug bei starkem Preisverlust (> 20%)
    if dfi_change < -20.0:
        score -= 20

    # Abzug bei starker dUSD-Abweichung (> 50%)
    if dusd_dev < -50.0:
        score -= 25

    # Untergrenze auf 0 begrenzen
    score = max(0, score)

    # Status-Einstufung
    if score < 30:
        status = "🔴 High Risk / Critical"
    elif score < 60:
        status = "🟠 Vorsicht"
    else:
        status = "🟢 Neutral / Bullish"

    return {"score": score, "status": status}
