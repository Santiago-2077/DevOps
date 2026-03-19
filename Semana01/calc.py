import math
def calculadora():

    menuOpciones()
    opcion= int(input())
    a = float(input ("Introduce tu primer valor (a): "))
    if opcion != 6 and opcion != 7:
        b = float(input ("Introduce tu segundo valor (b): "))


    match(opcion):
        case 1: 
           resultado = suma(a, b)
        case 2: 
            resultado = resta(a, b)
        case 3: 
            resultado = multi(a, b)
        case 4: 
            resultado = dividir(a, b)
        case 5: 
            resultado = exponente(a, b)
        case 6: 
            resultado = math.sqrt(a)
        case 7: 
            resultado = a ** 2
        case _:
            print("Error, opción no válida")

    return(resultado)





def menuOpciones():
    print("Bienvenido a tu calculadora, selecciona una opción: ")
    print("1. Suma")
    print("2. Resta")
    print("3. Multiplicación")
    print("4. División")
    print("5. Exponente (a ** b)")
    print("6. Raíz cuadrada")
    print("7. Elevado al cuadrado")


def suma(a, b):
    return (a + b)

def resta(a, b):
    return (a - b)

def multi(a, b):
    return (a * b)

def dividir(a, b):
    return (a / b)

def exponente(a, b):
    return (a ** b)

if __name__ == '__main__':
    while True:
        print(calculadora())
