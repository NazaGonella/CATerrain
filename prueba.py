def clear_bits(a, b):
    return a & ~b

a = 0b1101  # Representación binaria de 13
b = 0b1010  # Representación binaria de 10

resultado = clear_bits(a, b)
print(bin(resultado))  # Output: 0b1001
