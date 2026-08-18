import os
import tweepy

def send_x_thread(insight, tokenomics, dusd, network, intelligence, current_history, global_crypto, market):
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

        # Text in Blöcke von max. 270 Zeichen aufteilen (Thread)
        paragraphs = str(insight).split("\n\n")
        tweets = []
        current_tweet = ""

        for p in paragraphs:
            if len(current_tweet) + len(p) + 2 <= 270:
                current_tweet += p + "\n\n"
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
