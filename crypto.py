#função do cálculo da exponenciação
def power(base, expo, m):
    res = 1
    base = base % m
    while expo > 0:
        if expo & 1:
            res = (res * base) % m
        base = (base * base) % m
        expo = expo // 2
    return res

#função do mdc
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

#função do algoritmo extendido de Euclides
def egcd(a, b):
    if a == 0:
        return b, 0, 1
    g, y, x = egcd(b % a, a)
    return g, x - (b // a) * y, y

#função do cálculo inverso modular
def modInverse(e, phi):
    g, x, _ = egcd(e, phi)
    if g != 1:
        return -1  # Inverso modular não existe
    else:
        return x % phi

#gera as chaves
def generate_keys():
    p = 7919
    q = 1009
    n = p * q
    phi = (p - 1) * (q - 1)
    for e in range(2, phi):
        if gcd(e, phi) == 1:
            break
    d = modInverse(e, phi)
    if d == -1:
        raise ValueError("Falha ao gerar chave privada")
    return (e, n), (d, n)  # Retorna (public_key, private_key)

#criptografa e ddescriptografa as mensagens
def encrypt_message(public_key, message):
    e, n = public_key
    return [power(ord(char), e, n) for char in message]

def decrypt_message(private_key, cipher):
    d, n = private_key
    return ''.join([chr(power(c, d, n)) for c in cipher])
