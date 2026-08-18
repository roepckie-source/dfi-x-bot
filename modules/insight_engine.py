import os
from modules.language import load_language
from modules.market import get_market_data
from modules.tokenomics import get_tokenomics_data
from modules.dusd import get_dusd_data
from modules.network import get_network_data


def generate_daily_insight(lang_code=None):
    """
    Generiert die täglichen Insights in der gewählten Sprache.
    """
    if lang_code is None:
        lang_code = os.getenv("APP_LANG", "de")

    lang_data = load_language(lang_code)

    market_data = get_market_data()
    tokenomics_data = get_tokenomics_data()
    dusd_data = get_dusd_data()
    network_data = get_network_data()

    insights = []

    # 1. Market Insight
    change_24h = market_data.get("change_24h", 0.0) if isinstance(market_data, dict) else 0.0
    if change_24h < -5.0:
        msg = lang_data.get("market_pressure", "Market pressure detected")
        insight_loss_template = lang_data.get("insight_market_loss", "DFI lost {change:.2f}% in 24h.")
        insights.append(f"🔴 {msg}: {insight_loss_template.format(change=abs(change_24h))}")
    elif change_24h > 5.0:
        msg = lang_data.get("market_recovery", "Market recovery detected")
        insight_gain_template = lang_data.get("insight_market_gain", "DFI gained {change:.2f}% in 24h.")
        insights.append(f"🟢 {msg}: {insight_gain_template.format(change=change_24h)}")
    else:
        msg = lang_data.get("market_stable", "Market stable, limited volatility.")
        insights.append(f"⚪ {msg}")

    # 2. Tokenomics Insight
    net_burn = tokenomics_data.get("net_burn", 0.0) if isinstance(tokenomics_data, dict) else 0.0
    if net_burn > 0:
        msg = lang_data.get("tokenomics_positive", "Tokenomics positive")
        insight_burn_template = lang_data.get("insight_burn_exceeds", "Net burn is {amount:.2f} M DFI.")
        insights.append(f"🔥 {msg}: {insight_burn_template.format(amount=net_burn / 1_000_000)}")
    else:
        msg = lang_data.get("emission_high", "Current emission exceeds burn.")
        insights.append(f"⚠️ {msg}")

    # 3. dUSD Insight
    peg_deviation = dusd_data.get("peg_deviation", 0.0) if isinstance(dusd_data, dict) else 0.0
    if peg_deviation < -10.0:
        msg = lang_data.get("dusd_critical", "dUSD remains critical")
        insight_peg_template = lang_data.get("insight_peg_dev", "Peg deviation {peg:.2f}%.")
        insights.append(f"⚠️ {msg}: {insight_peg_template.format(peg=peg_deviation)}")
    elif peg_deviation < -2.0:
        msg = lang_data.get("dusd_warning", "dUSD health improved but under pressure")
        insight_peg_template = lang_data.get("insight_peg_dev", "Peg deviation {peg:.2f}%.")
        insights.append(f"🟡 {msg}: {insight_peg_template.format(peg=peg_deviation)}")
    else:
        msg = lang_data.get("dusd_stable", "dUSD health stable")
        insights.append(f"🟢 {msg}")

    # 4. Network Insight
    is_healthy = network_data.get("healthy", True) if isinstance(network_data, dict) else True
    if is_healthy:
        msg = lang_data.get("network_health", "Network operating normally")
        insight_chain = lang_data.get("insight_chain_normal", "Blockchain operating normally.")
        insights.append(f"⛓ {msg}: {insight_chain}")

    return "\n\n".join(insights)
