import os
import tweepy


def send_x_thread(insight, tokenomics, dusd, network, intelligence, current_history, global_crypto, market):
    """Versendet den Report als X/Twitter Thread."""
    
    api_key = os.getenv("X_API_KEY")
    api_secret = os.getenv("X_API_SECRET")
    access_token = os.getenv("X_ACCESS_TOKEN")
    access_token_secret = os.getenv("X_ACCESS_TOKEN_SECRET")

    if not all([api_key, api_secret, access_token, access_token_secret]):
        print("⚠️ X (Twitter) API Keys fehlen. Überspringe X-Versand.")
        return False

    # Typ-Sicherung für 'market'
    if isinstance(market, dict):
        dfi_raw = market.get("dfi", {})
        if not isinstance(dfi_raw, dict):
            dfi_raw = {}
    else:
        dfi_raw = {}

    try:
        client = tweepy.Client(
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_token_secret
        )

        # Erstes Posting
        tweet_text = f"🚀 DeFiChain Daily Intelligence\n\n{insight}"
        if len(tweet_text) > 280:
            tweet_text = tweet_text[:277] + "..."

        response = client.create_tweet(text=tweet_text)
        print("🎉 X Thread erfolgreich gesendet!")
        return True

    except Exception as e:
        print(f"❌ Fehler beim Senden an X: {e}")
        return False
