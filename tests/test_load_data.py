import pytest
from unittest.mock import mock_open, patch
from app import load_operators

def test_load_operators():
    mock_csv = "DDD;Telefone;Razao_Social;CNPJ;Cidade;UF;Endereco_eletronico\n11;987654321;Empresa X;12345678000190;Sao Paulo;SP;email@empresax.com"
    
    with patch("builtins.open", mock_open(read_data=mock_csv)), patch("os.path.join", return_value="mocked.csv"):
        operators = load_operators()
    
    assert len(operators) == 1
    assert operators[0]["Telefone"] == "(11) 987654321"
    assert operators[0]["Razao_Social"] == "Empresa X"
