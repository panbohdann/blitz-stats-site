from flask import Flask, request, jsonify, send_from_directory
import requests

app = Flask(__name__, static_folder=".")

API_KEY = "2d12c7215cccfdef82f3a730d70e0d1e"

@app.route("/")
def index():
    return send_from_directory('.', 'index.html')

@app.route("/stats")
def stats():
    nickname = request.args.get("nickname")
    if not nickname:
        return jsonify({"error": "nickname required"})

    # поиск account_id по нику
    search_url = f"https://api.wotblitz.eu/wotb/account/list/?application_id={API_KEY}&search={nickname}"
    r = requests.get(search_url).json()

    if not r["data"]:
        return jsonify({"error": "player not found"})

    account_id = r["data"][0]["account_id"]

    # статистика по аккаунту
    info_url = f"https://api.wotblitz.eu/wotb/account/info/?application_id={API_KEY}&account_id={account_id}&fields=statistics.all"
    data = requests.get(info_url).json()

    stats = data["data"][str(account_id)]["statistics"]["all"]

    battles = stats.get("battles", 0)
    wins = stats.get("wins", 0)
    avg_dmg = stats.get("damage_dealt",0)//battles if battles else 0
    survival = stats.get("survived_battles",0)
    return jsonify({
        "nickname": nickname,
        "battles": battles,
        "winrate": round(wins/battles*100,2) if battles else 0,
        "avg_damage": avg_dmg,
        "frags": stats.get("frags",0),
        "survival_rate": round(survival/battles*100,2) if battles else 0
    })

if __name__ == "__main__":
    app.run()
