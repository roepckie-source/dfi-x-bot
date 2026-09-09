# ======================================
# DeFiChain Intelligence v5
# Daily Insight Engine
# ======================================

import os

from modules.language import load_language
from modules.market import get_market_data
from modules.tokenomics import get_tokenomics_data
from modules.dusd import get_dusd_data
from modules.network import get_network_data


def safe_float(value, default=0.0):

    try:
        return float(value)

    except (TypeError, ValueError):

        return default


def generate_daily_insight(lang_code=None):

    if lang_code is None:
        lang_code = os.getenv(
            "APP_LANG",
            "de"
        )

    lang_data = load_language(
        lang_code
    )

    market_data = get_market_data()
    tokenomics_data = get_tokenomics_data()
    dusd_data = get_dusd_data()
    network_data = get_network_data()

    insights = []


    # ======================================
    # MARKET
    # ======================================

    change_24h = safe_float(
        market_data.get(
            "change_24h",
            0.0
        )
    )

    if change_24h < -5.0:

        msg = lang_data.get(
            "market_pressure",
            "Market pressure detected"
        )

        template = lang_data.get(
            "insight_market_loss",
            "DFI lost {change:.2f}% in 24h."
        )

        insights.append(
            f"🔴 {msg}: "
            f"{template.format(
                change=abs(change_24h)
            )}"
        )

    elif change_24h > 5.0:

        msg = lang_data.get(
            "market_recovery",
            "Market recovery detected"
        )

        template = lang_data.get(
            "insight_market_gain",
            "DFI gained {change:.2f}% in 24h."
        )

        insights.append(
            f"🟢 {msg}: "
            f"{template.format(
                change=change_24h
            )}"
        )

    else:

        msg = lang_data.get(
            "market_stable",
            "Market stable, limited volatility."
        )

        insights.append(
            f"⚪ {msg}"
        )


    # ======================================
    # TOKENOMICS
    # ======================================

    # WICHTIG:
    # tokenomics.py liefert "net_change"

    net_change = safe_float(
        tokenomics_data.get(
            "net_change",
            0.0
        )
    )

    if net_change > 0:

        msg = lang_data.get(
            "tokenomics_positive",
            "Tokenomics positive"
        )

        template = lang_data.get(
            "insight_burn_exceeds",
            "Net burn is {amount:.2f} M DFI."
        )

        insights.append(
            f"🔥 {msg}: "
            f"{template.format(
                amount=net_change / 1_000_000
            )}"
        )

    else:

        msg = lang_data.get(
            "emission_high",
            "Current emission exceeds burn."
        )

        insights.append(
            f"⚠️ {msg}"
        )


    # ======================================
    # dUSD
    # ======================================

    # WICHTIG:
    # dusd.py liefert "peg_difference"

    peg_difference = safe_float(
        dusd_data.get(
            "peg_difference",
            0.0
        )
    )

    if peg_difference < -10.0:

        msg = lang_data.get(
            "dusd_critical",
            "dUSD remains critical"
        )

        template = lang_data.get(
            "insight_peg_dev",
            "Peg deviation {peg:.2f}%."
        )

        insights.append(
            f"⚠️ {msg}: "
            f"{template.format(
                peg=peg_difference
            )}"
        )

    elif peg_difference < -2.0:

        msg = lang_data.get(
            "dusd_warning",
            "dUSD health improved but remains under pressure"
        )

        template = lang_data.get(
            "insight_peg_dev",
            "Peg deviation {peg:.2f}%."
        )

        insights.append(
            f"🟡 {msg}: "
            f"{template.format(
                peg=peg_difference
            )}"
        )

    else:

        msg = lang_data.get(
            "dusd_stable",
            "dUSD health stable"
        )

        insights.append(
            f"🟢 {msg}"
        )


    # ======================================
    # NETWORK
    # ======================================

    is_healthy = network_data.get(
        "healthy",
        True
    )

    if is_healthy:

        msg = lang_data.get(
            "network_health",
            "Network operating normally"
        )

        template = lang_data.get(
            "insight_chain_normal",
            "Blockchain operating normally."
        )

        insights.append(
            f"⛓ {msg}: "
            f"{template}"
        )


    return "\n\n".join(
        insights
    )
