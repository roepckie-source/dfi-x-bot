
# ======================================
# DeFiChain Intelligence v5
# Daily Insight Engine
# Multi Language Version
# ======================================

from language_manager import load_language


def generate_daily_insight(
    market, tokenomics, dusd, community, network, language="en"
):
    lang = load_language(language)
    insights = []

    # ==============================
    # Market Analyse
    # ==============================
    try:
        change = float(market.get("dfi", {}).get("change", 0))

        if change >= 5:
            tmpl = lang.get("insight_market_gain", "DFI gained {change:.2f}% in 24h.")
            insights.append(
                f"🟢 {lang.get('market_recovery', 'Market recovery detected')}: "
                + tmpl.format(change=change)
            )

        elif change <= -5:
            tmpl = lang.get("insight_market_loss", "DFI lost {change:.2f}% in 24h.")
            insights.append(
                f"🔴 {lang.get('market_pressure', 'Market pressure detected')}: "
                + tmpl.format(change=abs(change))
            )

        else:
            insights.append(
                f"🟡 {lang.get('market_stable', 'Market stable with limited movement')}."
            )

    except Exception:
        pass

    # ==============================
    # Tokenomics Analyse
    # ==============================
    try:
        burn = float(tokenomics.get("burn", {}).get("total", 0))
        emission = float(tokenomics.get("emission", 0))
        difference = burn - emission

        if difference > 0:
            tmpl = lang.get(
                "insight_burn_exceeds",
                "Burn exceeds emission by {amount:.2f} M DFI.",
            )
            insights.append(
                f"🔥 {lang.get('tokenomics_positive', 'Tokenomics positive')}: "
                + tmpl.format(amount=difference / 1_000_000)
            )

        else:
            insights.append(
                f"⚠️ {lang.get('emission_high', 'Emission currently exceeds burn')}."
            )

    except Exception:
        pass

    # ==============================
    # dUSD Analyse
    # ==============================
    try:
        health = int(dusd.get("health_score", 0))
        peg = float(dusd.get("peg_difference", 0))

        if health < 30:
            tmpl = lang.get("insight_peg_dev", "Peg deviation {peg:.2f}%.")
            insights.append(
                f"⚠️ {lang.get('dusd_critical', 'dUSD remains critical')}: "
                + tmpl.format(peg=peg)
            )

        elif health < 60:
            insights.append(
                f"🟡 {lang.get('dusd_warning', 'dUSD health improving but remains under pressure')}."
            )

        else:
            insights.append(
                f"🟢 {lang.get('dusd_stable', 'dUSD health stable')}."
            )

    except Exception:
        pass

    # ==============================
    # Network Analyse
    # ==============================
    try:
        status = network.get("network_status", "")

        if "Online" in status:
            chain_msg = lang.get(
                "insight_chain_normal", "Blockchain operating normally."
            )
            insights.append(
                f"⛓ {lang.get('network_health', 'Network healthy')}: {chain_msg}"
            )

    except Exception:
        pass

    # ==============================
    # Ausgabe
    # ==============================
    return "\n\n".join(insights)
