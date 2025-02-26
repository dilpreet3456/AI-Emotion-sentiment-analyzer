from flask import Flask, request, jsonify,render_template
from nltk.sentiment import SentimentIntensityAnalyzer
import random
import nltk
nltk.download('vader_lexicon')


app = Flask(__name__)
sia = SentimentIntensityAnalyzer()

# AI-powered emotion detection
@app.route('/analyze', methods=['POST'])
def analyze_emotion():
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({"error": "Invalid input"}), 400

        text = data['text'].strip().lower()  # Normalize input
        sentiment_score = sia.polarity_scores(text)

        print(f"Text: {text}, Scores: {sentiment_score}")  # Debugging log

        # Emotion categorization
        if sentiment_score['compound'] >= 0.3:
            emotion = "Happy 😊"
            emoji_list = ["😊", "😁", "😃"]
            quote = random.choice([
                "Happiness is a choice. Spread the joy!",
                "Keep smiling, the world is brighter with you!",
                "Joy is contagious, share it!"
            ])
        elif sentiment_score['compound'] <= -0.3:
            emotion = "Sad 😢"
            emoji_list = ["😢", "😭", "😞"]
            quote = random.choice([
                "Sadness is temporary, keep going!",
                "Every storm runs out of rain.",
                "You're stronger than you think!"
            ])
        else:
            emotion = "Neutral 😐"
            emoji_list = ["😐", "🤔", "😑"]
            quote = random.choice([
                "Stay calm and enjoy the moment.",
                "Balance is the key to happiness.",
                "Take a deep breath and relax."
            ])

        return jsonify({"emotion": emotion, "emoji": emoji_list, "quote": quote})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

# AI-based Recommendation
@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data received"}), 400
    # Extract emotion and category safely
    emotion = data.get("emotion", "").strip().lower()
    category = data.get("category", "").strip().lower()

    recommendations = {
        "happy": {
            "music": "https://open.spotify.com/playlist/37i9dQZF1DX3rxVfibe1L0",
            "movies": "https://www.imdb.com/title/tt0114709/",  # Toy Story
            "novels": "https://www.goodreads.com/book/show/41865.Pride_and_Prejudice",
            "vacations": "https://www.tripadvisor.com/Attractions-g187147-Activities-Paris_Ile_de_France.html",
            "games": "https://store.steampowered.com/app/730/CounterStrike_Global_Offensive/"
        },
        "sad": {
            "music": "https://open.spotify.com/playlist/37i9dQZF1DX7qK8ma5wgG1",
            "movies": "https://www.imdb.com/title/tt2582802/",  # Inside Out
            "novels": "https://www.goodreads.com/book/show/2657.To_Kill_a_Mockingbird",
            "vacations": "https://www.tripadvisor.com/Attractions-g60763-Activities-New_York_City_New_York.html",
            "games": "https://store.steampowered.com/app/440/Team_Fortress_2/"
        },
        "neutral": {
            "music": "https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M",
            "movies": "https://www.imdb.com/title/tt1375666/",  # Inception
            "novels": "https://www.goodreads.com/book/show/4671.The_Great_Gatsby",
            "vacations": "https://www.tripadvisor.com/Attractions-g294217-Activities-Hong_Kong.html",
            "games": "https://store.steampowered.com/app/105600/Terraria/"
        }
    }
 # Validate input
    if emotion not in recommendations:
        return jsonify({"suggestion": "No emotion match found"}), 404

    if category not in recommendations[emotion]:
        return jsonify({"suggestion": "No recommendations found"}), 404

    suggestion = recommendations[emotion][category]
    return jsonify({"suggestion": suggestion})


@app.route('/')
def home():
    return render_template('index.html')  # Ensure 'index.html' exists in 'templates' folder


if __name__ == '__main__':
    app.run(debug=True)
