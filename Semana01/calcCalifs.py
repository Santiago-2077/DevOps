class Alumno():
    def __init__(self, nalumno):
        self.nalumno = nalumno
        self.materias = []
        self.promedio = 0

    def agregarMateria(self, nmateria):
        self.materias.append(nmateria)

    def aprobatoria(self, calif : int):
        if calif > 6: return True
        else: return False
    
    def calcPromedio(self):
        sumcalifs = 0
        for materia in self.materias:
            materia += sumcalifs
        self.promedio = sumcalifs / self.materias.range()
        return self.promedio

    def mensaje(self):
        mensaje = ""
        if self.aprobatoria() == False: mensaje = (f"Lo lamento, tu promedio es reprobatorio, tienes un promedio de {self.calcPromedio()}")
        if self.aprobatoria() == True: 
            
            match (self.promedio):
                case 6:
                    mensaje = (f"Felicidades, cuentas con un promedio aprobatorio de: {self.calcPromedio()}; aprobaste apenas! ")
                case _:
                    mensaje = (f"Felicidades, cuentas con un promedio aprobatorio de: {self.calcPromedio()} ")

        return mensaje
    


class Menu():
    def menuPrincipal():
        print(f" - - Sistema para calcular el promedio de calificiaciones de un alumno - -")
        print(f"Selecciona una opción:  ")
        print(f"1. Agregar nuevo Alumno")
        print(f"2. Ver las calificicaciones de un usuario existente ")
        print(f"3. Salir ")




    def menuUser():
        pass

def main():
    if __name__ == "__main__":
        Menu.menuPrincipal()

    
