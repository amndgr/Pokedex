from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)


def buscar_pokemon(identificador):
    url = f"https://pokeapi.co/api/v2/pokemon/{identificador}"

    try: 
        resposta = requests.get(url, timeout=5)
    except requests.RequestException:
        return None

    if resposta.status_code != 200:
        return None

    dados = resposta.json()

    imagem = dados["sprites"]["versions"]["generation-v"]["black-white"]["animated"]["front_default"]
    if imagem is None:
        imagem = dados["sprites"]["front_default"]

    return {
        "id": dados["id"],
        "nome": dados["name"],
        "imagem": imagem,
        "anterior": max(dados["id"] -1, 1),
        "proximo": dados["id"] + 1,
    } 

@app.route("/")
def index():
    busca = request.args.get("busca", "").strip().lower()
    return redirect(url_for("ver_pokemon", identificador=busca or 1))

@app.route("/pokemon/<identificador>")
def ver_pokemon(identificador):
    pokemon = buscar_pokemon(identificador)
    return render_template("index.html", pokemon=pokemon)

if __name__ == "__main__":
    app.run(port=5000)
