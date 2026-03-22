# Importamos la librería para hacer traducciones usando Google Translate
from deep_translator import GoogleTranslator

# Diccionario de idiomas disponibles: la clave es el número del menú,
# el valor es una tupla con (nombre legible, código de idioma para la API)
IDIOMAS = {
    "1": ("Español",  "es"),
    "2": ("Inglés",   "en"),
    "3": ("Francés",  "fr"),
    "4": ("Alemán",   "de"),
}

# Separador visual para la interfaz de consola
SEPARADOR = "─" * 40


def mostrar_menu(titulo: str) -> tuple[str, str]:
    """Muestra un menú con los idiomas disponibles y retorna el idioma elegido."""
    print(f"\n{SEPARADOR}")
    print(f"  {titulo}")
    print(SEPARADOR)
    # Imprimimos cada opción del menú con su número y nombre
    for clave, (nombre, _) in IDIOMAS.items():
        print(f"  {clave}. {nombre}")
    print(SEPARADOR)

    # Pedimos la opción al usuario hasta que ingrese una válida
    while True:
        opcion = input("  Elige una opción (1-4): ").strip()
        if opcion in IDIOMAS:
            return IDIOMAS[opcion]  # Retornamos la tupla (nombre, código)
        print("  Opción no válida. Intenta de nuevo.")


def traducir(texto: str, origen: str, destino: str) -> str:
    """Traduce un texto del idioma de origen al idioma de destino usando Google Translate."""
    return GoogleTranslator(source=origen, target=destino).translate(texto)


def main():
    # Encabezado del programa
    print("\n" + "=" * 40)
    print("       TRADUCTOR MULTILENGUAJE")
    print("=" * 40)
    print("  Idiomas disponibles: Español, Inglés,")
    print("                       Francés, Alemán")

    # Ciclo principal: el programa sigue traduciendo hasta que el usuario decida salir
    while True:
        # El usuario elige el idioma de origen y el idioma de destino
        nombre_origen, codigo_origen = mostrar_menu("IDIOMA DE ORIGEN")
        nombre_destino, codigo_destino = mostrar_menu("IDIOMA DE DESTINO")

        # Validamos que el origen y destino no sean el mismo idioma
        if codigo_origen == codigo_destino:
            print("\n  ⚠  El idioma de origen y destino son iguales.")
            continue

        print(f"\n{SEPARADOR}")
        print(f"  Traduciendo: {nombre_origen} → {nombre_destino}")
        print(SEPARADOR)
        texto = input("  Escribe el texto: ").strip()

        # Validaciones del texto ingresado
        if not texto:
            print("  No ingresaste ningún texto.")
        elif len(texto) > 25:
            print("  El texto es muy largo (máx. 25 caracteres).")
        else:
            # Intentamos traducir; si ocurre un error lo mostramos
            try:
                resultado = traducir(texto, codigo_origen, codigo_destino)
                print(f"\n  Traducción: {resultado}")
            except Exception as e:
                print(f"\n  Error al traducir: {e}")

        # Preguntamos si el usuario quiere hacer otra traducción
        print(f"\n{SEPARADOR}")
        otra = input("  ¿Traducir otro texto? (s/n): ").strip().lower()
        if otra != "s":
            print("\n  ¡Hasta luego!\n")
            break


# Punto de entrada del programa
if __name__ == "__main__":
    main()
