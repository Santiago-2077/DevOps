peso : float = float(input("Ingresa tu peso en (kg)"))
estatura : float  = float(input("Ingresa tu estatura en metros: "))
imc = peso / (estatura * estatura)

print(f"Tu índice de masa corporal es: {round(imc)}")