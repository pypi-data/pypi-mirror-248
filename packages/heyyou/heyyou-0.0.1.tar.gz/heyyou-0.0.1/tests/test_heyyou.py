import pytest
from io import StringIO
import sys
sys.path.append('src')

from heyyou.main import heyyou

def test_heyyou_default_english():
    sys.argv = ['heyyou']  # Simulating no language code argument passed
    captured_output = StringIO()
    sys.stdout = captured_output
    heyyou()
    sys.stdout = sys.__stdout__
    assert captured_output.getvalue().strip() == 'Hey, You!'

def test_heyyou_spanish():
    sys.argv = ['heyyou', 'ES']  # Simulating 'ES' language code argument passed
    captured_output = StringIO()
    sys.stdout = captured_output
    heyyou()
    sys.stdout = sys.__stdout__
    assert captured_output.getvalue().strip() == '¡Hola, tú!'

# Add more test cases for other language codes as needed...
