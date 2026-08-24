# ======================================
# DeFiChain Intelligence v5
# Report Formatter
# ======================================

from modules.language import load_language


def safe_float(value, default=0.0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def format_price(value, decimals=2):
    try:
        value = float(value)

        if value < 0.01:
            return f"{value:.8f}"

        if value < 1:
            return f"{value:.6f}"

        if value < 100:
            return f"{value:.4f}"

        return f"{value:,.2f}"

    except (TypeError, ValueError):
        return "N/A"


def create_report(
    market,
    tokenomics,
    dusd,
    community,
    network,
    intelligence,
    daily_insight,
    current_history,
    global_crypto,
    comparison,
    news=None,
    language="de",
    lang_data=None,
):

    # ==================================
    # Sprache
    # ==================================

    if not lang_data:
        lang_data = load_language(language)

    # ==================================
    # Header
    # ==================================

    h_title = lang_data.get(
        "header_title",
        "🚀 DeFiChain Intelligence"
    )

    h_line1 = lang_data.get(
        "header_line1",
        "Decentralized. Independent."
    )

    h_line2 = lang_data.get(
        "header_line2",
        "Beyond Centralized Control."
    )

    # ==================================
    # DFI
    # ==================================

    dfi = {}

    if isinstance(market, dict):
        dfi = market.get("dfi", {})

    dfi_price = dfi.get("price", dfi.get("usd", "N/A"))
    dfi_change = safe_float(
        dfi.get("change", 0)
    )

    dfi_emoji = (
        "🟢"
        if dfi_change >= 0
        else "🔴"
    )

    # ==================================
    # BTC / ETH
    # ==================================

    if not isinstance(global_crypto, dict):
        global_crypto = {}

    btc = global_crypto.get(
        "bitcoin",
        {}
    )

    eth = global_crypto.get(
        "ethereum",
        {}
    )

    btc_price = btc.get(
        "price",
        "N/A"
    )

    btc_change = safe_float(
        btc.get("change", 0)
    )

    eth_price = eth.get(
        "price",
        "N/A"
    )

    eth_change = safe_float(
        eth.get("change", 0)
    )

    btc_emoji = (
        "🟢"
        if btc_change >= 0
        else "🔴"
    )

    eth_emoji = (
        "🟢"
        if eth_change >= 0
        else "🔴"
    )

    # ==================================
    # Intelligence Score
    # ==================================

    if not isinstance(intelligence, dict):
        intelligence = {}

    score = intelligence.get(
        "total",
        0
    )

    status = intelligence.get(
        "status",
        "N/A"
    )

    # ==================================
    # History
    # ==================================

    hist_title = "N/A"
    hist_content = ""

    if (
        current_history
        and isinstance(current_history, dict)
    ):

        hist_title = current_history.get(
            "title",
            "N/A"
        )

        # Unterstützt "content" und "text"
        hist_content = current_history.get(
            "content",
            current_history.get(
                "text",
                ""
            )
        )

    # ==================================
    # REPORT
    # ==================================

    report = ""

    report += (
        f"{h_title} ({language.upper()})\n"
    )

    report += (
        f"{h_line1}\n"
    )

    report += (
        f"{h_line2}\n\n"
    )

    # ==================================
    # GLOBAL CRYPTO
    # ==================================

    report += "🌍 Global Crypto\n\n"

    report += (
        f"₿ Bitcoin: "
        f"${format_price(btc_price)} "
        f"({btc_emoji} {btc_change:.2f}%)\n"
    )

    report += (
        f"Ξ Ethereum: "
        f"${format_price(eth_price)} "
        f"({eth_emoji} {eth_change:.2f}%)\n\n"
    )

    # ==================================
    # DEFIChain
    # ==================================

    report += "💎 DeFiChain DFI\n\n"

    report += (
        f"Price: "
        f"${format_price(dfi_price, 8)}\n"
    )

    report += (
        f"24h: "
        f"{dfi_emoji} {dfi_change:.2f}%\n\n"
    )

    # ==================================
    # INTELLIGENCE
    # ==================================

    report += (
        f"🧠 Intelligence Score: "
        f"{score}/100\n"
    )

    report += (
        f"{status}\n\n"
    )

    # ==================================
    # DAILY INSIGHT
    # ==================================

    if daily_insight:

        report += (
            f"💡 Insight:\n"
            f"{daily_insight}\n\n"
        )

    # ==================================
    # NEWS
    # ==================================

    if news:

        if isinstance(news, dict):

            news_title = news.get(
                "title",
                "DeFiChain News"
            )

            news_text = news.get(
                "text",
                news.get(
                    "content",
                    ""
                )
            )

            report += (
                f"📰 News: "
                f"{news_title}\n"
            )

            if news_text:

                report += (
                    f"{news_text}\n"
                )

        else:

            report += (
                f"📰 News:\n"
                f"{news}\n"
            )

        report += "\n"

    # ==================================
    # HISTORY
    # ==================================

    if hist_title != "N/A":

        report += (
            f"📚 History: "
            f"{hist_title}\n"
        )

        if hist_content:

            report += (
                f"{hist_content}\n"
            )

    return report