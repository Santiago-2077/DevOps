alumnos = []

class Alumno():
    def __init__(self, nalumno):
        self.nalumno = nalumno
        self.materias = []
        self.promedio = 0
        self.califs = []

    def agregarMateria(self, nmateria, calif):
        self.materias.append(nmateria)
        self.califs.append(calif)

    def aprobatoria(self):
        if self.promedio >= 6: return True
        else: return False
    
    def calcPromedio(self):
        sumcalifs = 0
        for materia in self.califs:
            sumcalifs += materia
        self.promedio = sumcalifs / len(self.califs)
        return self.promedio

    def mensaje(self):
        mensaje = ""
        if self.aprobatoria() == False: mensaje = (f"Lo lamento, tu promedio es reprobatorio, tienes un promedio de {self.calcPromedio()}")
        if self.aprobatoria() == True: 
            
            match (self.promedio):
                case 6:
                    mensaje = (f"Felicidades, cuentas con un promedio aprobatorio de: {self.calcPromedio()}; aprobaste apenas!")
                case _:
                    mensaje = (f"Felicidades, cuentas con un promedio aprobatorio de: {self.calcPromedio()}.")

        return mensaje
    
    def __str__(self):
        return (f"Nombre del alumno: {self.nalumno}, Materias: {self.materias}, Calificaciones: {self.califs}, Promedio: {self.promedio}")
    


class Menu():
    @staticmethod
    def printPrincipal():
        print(f" - - Sistema para calcular el promedio de calificiaciones de un alumno - -")
        print(f"Selecciona una opción:  ")
        print(f"1. Agregar nuevo Alumno")
        print(f"2. Ver las calificicaciones de un usuario existente ")
        print(f"3. Salir ")

    @staticmethod
    def printAlumno():
        print(f" - - INTERFAZ DE ALUMNO - -")
        print(f"    Selecciona una opción:  ")
        print(f"1.  Agregar materia y calificación")
        print(f"2.  Ver promedio")
        print(f"3.  Salir ")
    
    @staticmethod
    def menuAlumno():
        nalumno = input("Ingresa tu nombre")
        alumno = Alumno(nalumno)
        alumnos.append(alumno)
        while True:
            Menu.printAlumno()
            opcion = int(input())
            match opcion:
                case 1:
                    nmateria = input("Nombre de la materia: ")
                    calif = int(input("Calificacion: "))
                    alumno.agregarMateria(nmateria, calif)
                case 2:
                    print(alumno.mensaje())
                case 3:
                    break
                case _:
                    print("Opción inválida")

    
    @staticmethod
    def verAlumno(alumnos : list):
        while True:
            nalumno = input("Ingresa el nombre del alumno que buscas.")
            encontrado = next((a for a in alumnos if a.nalumno == nalumno), None)

            if encontrado is None: print("No se encontró ese alumno.")
            else : print(encontrado) ; break
        


def main():
    while True:
        Menu.printPrincipal()
        opcion = int(input())
        match(opcion):
            case 1:
                Menu.menuAlumno()
            case 2:
                Menu.verAlumno(alumnos)
            case 3:
                break
            case _:
                pass

if __name__ == "__main__":
    main()

    
