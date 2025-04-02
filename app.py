from flask import Flask, request, jsonify
from flask_cors import CORS
import csv

app = Flask(__name__)
CORS(app)

def formatar_telefone(ddd, numero):
    """Função para formatar o telefone com o DDD."""
    return f"({ddd}) {numero}"

def carregar_operadoras():
    operadoras = []
    with open('Relatorio_cadop.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=';', quotechar='"')
        for row in reader:
            ddd = row["DDD"].split(";")[1] if ";" in row["DDD"] else row["DDD"]
            numero = row["Telefone"].split(";")[1] if ";" in row["Telefone"] else row["Telefone"]
            
            telefone_formatado = formatar_telefone(ddd, numero)
            
            row["Telefone"] = telefone_formatado  
            operadoras.append(row)
    return operadoras


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
    app.run(debug=True)
