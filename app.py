from flask import Flask, request, jsonify
from flask_cors import CORS
import csv
import os  

app = Flask(__name__)
CORS(app)

def format_phone(area_code, number):
    return f"({area_code}) {number}"

def load_operators():
    operators = []
    csv_path = os.path.join(os.path.dirname(__file__), 'Operator_Report.csv')
    
    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=';', quotechar='"')
        for row in reader:
            area_code = row["DDD"].split(";")[1] if ";" in row["DDD"] else row["DDD"]
            number = row["Telefone"].split(";")[1] if ";" in row["Telefone"] else row["Telefone"]
            row["Telefone"] = format_phone(area_code, number)
            operators.append(row)
    return operators

@app.route('/')
def health_check():
    return jsonify({"status": "ok", "message": "API is operational"})

@app.route('/search_operators', methods=['GET'])
def search_operators():
    search_term = request.args.get('q', '').lower()
    operators = load_operators()
    
    result = [
        {
            "Business_Name": op["Razao_Social"],
            "CNPJ": op["CNPJ"],
            "City": op["Cidade"],
            "State": op["UF"],
            "Phone": op["Telefone"],
            "Email": op["Endereco_eletronico"],
        }
        for op in operators
        if search_term in op["Razao_Social"].lower() or search_term in op["CNPJ"].lower()
    ]
    return jsonify(result)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=5000)
    args = parser.parse_args()
    
    app.run(host='0.0.0.0', port=args.port)
