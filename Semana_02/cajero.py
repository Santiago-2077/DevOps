users = []

class Usuario:
    def __init__(self, nombre, NIP):
        self.nombre = nombre
        self.NIP = NIP
        self.saldo = 0.0


    def agregarSaldo(self, saldoNuevo):
        self.saldo += saldoNuevo
        print(f"Saldo actualizado: ${self.saldo:.2f}")

    def retirarSaldo(self, saldoRestado):
        if saldoRestado > self.saldo:
            print("Saldo insuficiente")
        else:
            self.saldo -= saldoRestado
            print(f"Saldo actualizado: ${self.saldo:.2f}")
        

    def ingresar(self, nom, np):
      if nom == self.nombre and np == self.NIP:
        print("Bienvenido", self.nombre)
        return True
      else:
        print("Usuario o NIP incorrecto")
        return False

    def verSaldo(self):
      print(self.saldo)



def menu():
  print(f"- - Selecciona una opción - -")
  print(f" 1. Crear usuario")
  print(f" 2. Ingresar a cuenta existente")
  print(f" 3. Salir")

def menuUser(user):
  while True:
    print(f"- - Selecciona una opción - -")
    print(f" 1. Retirar saldo")
    print(f" 2. Ingresar saldo")
    print(f" 3. Ver saldo")
    print(f" 4. Salir")
    opcion = int(input())
    match opcion:
      case 1:
        saldoRet = float(input("Ingresa el saldo a retirar"))
        user.retirarSaldo(saldoRet)
      case 2:
        saldoSum = float(input("Ingresa el saldo a ingresar"))
        user.agregarSaldo(saldoSum)
      case 3:
        user.verSaldo()
      case 4:
        break


def main():
  while True:
    menu()
    opcion = int(input())
    match opcion:
      case 1:
        n_usuario = input("Ingresa tu nuevo usuario")
        nip = input("Ingresa tu nuevo NIP")

        new_usuario = Usuario(n_usuario, nip)
        users.append(new_usuario)
        menuUser(new_usuario)
      case 2:
        ConsultaUser = input("Ingresa tu nombre: ")
        ConsultaNIP = input("Ingresa tu NIP: ")

        for user in users:
          if user.ingresar(ConsultaUser, ConsultaNIP):
            menuUser(user)
            break
        else:
          print("Usuario o NIP incorrecto.")
      case 3:
        break


if __name__ == "__main__":
  main()