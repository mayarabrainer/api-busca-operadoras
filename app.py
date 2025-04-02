from flask import Flask, request, jsonify
from flask_cors import CORS
import csv
import os  

app = Flask(__name__)
CORS(app)

def formatar_telefone(ddd, numero):
    return f"({ddd}) {numero}"

def carregar_operadoras():
    operadoras = []
    csv_path = os.path.join(os.path.dirname(__file__), 'Relatorio_cadop.csv')
    
    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=';', quotechar='"')
        for row in reader:
            ddd = row["DDD"].split(";")[1] if ";" in row["DDD"] else row["DDD"]
            numero = row["Telefone"].split(";")[1] if ";" in row["Telefone"] else row["Telefone"]
            row["Telefone"] = formatar_telefone(ddd, numero)
            operadoras.append(row)
    return operadoras

@app.route('/')
def health_check():
    return jsonify({"status": "ok", "message": "API operacional"})

@app.route('/buscar_operadoras', methods=['GET'])
def buscar_operadoras():
    termo_busca = request.args.get('q', '').lower()
    operadoras = carregar_operadoras()
    
    resultado = [
        {
            "Razao_Social": op["Razao_Social"],
            "CNPJ": op["CNPJ"],
            "Cidade": op["Cidade"],
            "UF": op["UF"],
            "Telefone": op["Telefone"],
            "Endereco_eletronico": op["Endereco_eletronico"],
        }
        for op in operadoras
        if termo_busca in op["Razao_Social"].lower() or termo_busca in op["CNPJ"].lower()
    ]
    return jsonify(resultado)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=5000)
    args = parser.parse_args()
    
    app.run(host='0.0.0.0', port=args.port)