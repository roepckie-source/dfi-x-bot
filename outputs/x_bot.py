import os
import tweepy

def chunk_text(text, max_len=260):
    """Sucht saubere Umbrüche oder spaltet Text hart ab, wenn ein Block zu lang ist."""
    chunks = []
    while len(text) > max_len:
        # Versuche bei einem Zeilenumbruch oder Leerzeichen zu trennen
        split_at = text.rfind("\n", 0, max_len)
        if split_at == -1:
            split_at = text.rfind(" ", 0, max_len)
        if split_at == -1:
            split_at = max_len

        chunks.append(text[:split_at].strip())
        text = text[split_at:].strip()

    if text:
        chunks.append(text)
    return chunks

def send_x_thread(insight, tokenomics=None, dusd=None, network=None, intelligence=None, current_history=None, global_crypto=None, market=None):
    """Sendet den vollständigen Bericht als zusammenhängenden Thread auf X."""

    api_key = os.getenv("X_API_KEY")
    api_secret = os.getenv("X_API_SECRET")
    access_token = os.getenv("X_ACCESS_TOKEN")
    access_token_secret = os.getenv("X_ACCESS_TOKEN_SECRET")

    if not all([api_key, api_secret, access_token, access_token_secret]):
        print("⚠️ X (Twitter) API Keys fehlen. Überspringe X-Versand.")
        return False

    try:
        client = tweepy.Client(
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_token_secret
        )

        # Falls insight ein Gesamtbericht-String ist, nutze ihn direkt;
        # andernfalls kombiniere alle übergebenen Komponenten:
        if isinstance(insight, str) and len(insight) > 100:
            full_text = insight
        else:
            components = [insight, tokenomics, dusd, network, intelligence, current_history, global_crypto, market]
            full_text = "\n\n".join([str(c) for c in components if c])

        # Vorab-Absätze trennen
        raw_paragraphs = full_text.split("\n\n")
        paragraphs = []
        
        # Stelle sicher, dass kein einzelner Absatz das Limit von ~250 Zeichen überschreitet
        for p in raw_paragraphs:
            if len(p) > 250:
                paragraphs.extend(chunk_text(p, max_len=250))
            else:
                paragraphs.append(p)

        # Blöcke bauen (Sicherheits-Puffer von 250 Zeichen für "(X/Y)\n" Präfixe)
        tweets = []
        current_tweet = ""

        for p in paragraphs:
            if len(current_tweet) + len(p) + 2 <= 250:
                current_tweet += (p + "\n\n")
            else:
                if current_tweet.strip():
                    tweets.append(current_tweet.strip())
                current_tweet = p + "\n\n"

        if current_tweet.strip():
            tweets.append(current_tweet.strip())

        # Thread versenden
        last_tweet_id = None
        for i, tweet_text in enumerate(tweets):
            formatted_text = f"({i+1}/{len(tweets)})\n{tweet_text}" if len(tweets) > 1 else tweet_text
            
            # Sicherheitscheck
            if len(formatted_text) > 280:
                formatted_text = formatted_text[:277] + "..."

            if last_tweet_id is None:
                response = client.create_tweet(text=formatted_text)
            else:
                response = client.create_tweet(text=formatted_text, in_reply_to_tweet_id=last_tweet_id)

            last_tweet_id = response.data['id']

        print("🎉 X Thread erfolgreich gesendet!")
        return True

    except Exception as e:
        print(f"❌ Fehler beim Senden an X: {e}")
        return False
