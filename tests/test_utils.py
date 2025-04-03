import pytest
from app import format_phone

def test_format_phone():
    assert format_phone("11", "987654321") == "(11) 987654321"
    assert format_phone("21", "12345678") == "(21) 12345678"
