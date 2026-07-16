import random

INSIGHTS = [

    "📚 DeFiChain History\n\nDeFiChain was launched in 2020 with the goal of building a blockchain focused on decentralized finance.",

    "📚 Did you know?\n\nDFI is the native token of the DeFiChain ecosystem and is used for fees, governance and network participation.",

    "📚 DeFiChain Insight\n\nUnlike many DeFi projects, DeFiChain was designed specifically for decentralized financial applications.",

    "📚 dTokens\n\ndTokens provide blockchain-based exposure to different asset classes within the DeFiChain ecosystem.",

    "📚 DUSD\n\nDUSD is DeFiChain's decentralized stable asset. Its value and ecosystem role have evolved through community governance.",

    "📚 Governance\n\nThe DeFiChain community can propose and vote on protocol changes through governance proposals."

]


def get_daily_insight():
    return random.choice(INSIGHTS)
