import logging

from savarin import unreleased

"""
INFO -> 10
DEBUG -> 20
WARNING -> 30
ERROR -> 40
CRITICAL -> 50
"""

logging.basicConfig(level=logging.INFO)

def main():
    logging.info(unreleased())

# Ejecuta todo lo del bloque solo si y solo si, este archivo se ejecuta como principal.
if __name__ == "__main__":
    logging.debug(">>> Estamos comenzando la ejecución del paquete")
    
    main()

    logging.debug(">>> Estamos finalizando la ejecución del paquete")
