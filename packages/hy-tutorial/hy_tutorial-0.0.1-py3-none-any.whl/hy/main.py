import sys

def hy(language_code=None):
    greetings = {
        'EN': 'Hey, You!',
        'ES': '¡Hola, tú!',
        'FR': 'Salut, toi!',
        'DE': 'Hallo, du!',
        'IT': 'Ciao, tu!'
    }

    if language_code and language_code in greetings:
        print(greetings[language_code])
    else:
        print("Invalid language code provided.")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        hy(sys.argv[1])
    else:
        hy()
