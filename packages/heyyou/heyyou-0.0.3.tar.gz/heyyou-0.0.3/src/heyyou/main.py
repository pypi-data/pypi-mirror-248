import sys

def heyyou():
    if len(sys.argv) > 1:
        language_code = sys.argv[1]
    else:
        language_code = 'EN'

    greetings = {
        'EN': 'Hey, You!',
        'ES': '¡Hola, tú!',
        'FR': 'Salut, toi!',
        'DE': 'Hallo, du!',
        'IT': 'Ciao, tu!',
        'MS': 'Hai, awak!',
        'ZH': '嘿，你！',
        'JA': 'やあ、君！',
        'KO': '안녕, 너!',
        'RU': 'Привет, ты!',
        'AR': 'مرحبا أنت!',
        'HI': 'नमस्ते, तुम!',
    }

    if language_code and language_code in greetings:
        print(greetings[language_code])

    else:
        print("Language code provided invalid or unsupported.")
