import os
import tweepy


def main():
    print("=" * 60)
    print("X REPLY TEST")
    print("=" * 60)

    api_key = os.getenv("X_API_KEY")
    api_secret = os.getenv("X_API_SECRET")
    access_token = os.getenv("X_ACCESS_TOKEN")
    access_token_secret = os.getenv("X_ACCESS_TOKEN_SECRET")

    if not all([
        api_key,
        api_secret,
        access_token,
        access_token_secret
    ]):
        print("❌ X Zugangsdaten fehlen.")
        return

    print("✅ X Zugangsdaten vorhanden")

    client = tweepy.Client(
        consumer_key=api_key,
        consumer_secret=api_secret,
        access_token=access_token,
        access_token_secret=access_token_secret
    )

    try:
        # 1. Normalen Test-Tweet erstellen
        print("\n1️⃣ Erstelle Test-Tweet...")

        tweet = client.create_tweet(
            text="DeFiChain X API Reply Test"
        )

        tweet_id = tweet.data["id"]

        print(f"✅ Test-Tweet erstellt")
        print(f"Tweet-ID: {tweet_id}")

        # 2. Direkt darauf antworten
        print("\n2️⃣ Teste Reply auf diesen Tweet...")

        reply = client.create_tweet(
            text="Reply-Test erfolgreich.",
            in_reply_to_tweet_id=tweet_id
        )

        print("✅ REPLY FUNKTIONIERT")
        print(f"Reply-ID: {reply.data['id']}")

    except Exception as e:
        print("\n❌ X FEHLER")
        print("-" * 60)
        print(type(e).__name__)
        print(str(e))
        print("-" * 60)


if __name__ == "__main__":
    main()
