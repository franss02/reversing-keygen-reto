#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
 keygen.py  --  Generador de claves (keygen) para  reto.exe
--------------------------------------------------------------------------------
 Practica de Ingenieria Inversa
 Autor: Francisco Serrano Sanchez
================================================================================

 Algoritmo de validacion reconstruido a partir del desensamblado del binario:

   1. El nombre de usuario debe tener EXACTAMENTE 10 caracteres (sin espacios,
      ya que el binario lo lee con scanf("%10s", ...)).

   2. El binario calcula un valor entero S:

          S = SUMA( ASCII(usuario[i]) )  +  SUMA( TABLA[i] )      i = 0..9

      donde TABLA es un vector de 10 bytes situado en la VA 0x404088 de la
      seccion .data y cuyo contenido es la cadena "R3V3RS1NG!".
      La suma de esa tabla es constante:  82+51+86+51+82+83+49+78+71+33 = 666.

   3. La clave introducida por el usuario debe ser una cadena puramente
      numerica (el binario la valida con isdigit() caracter a caracter).

   4. La clave es valida si, e interpretada como entero (atoi):

          int(clave)  ==  S XOR 0x6667           (0x6667 = 26215)

 Por tanto, la clave correcta para un usuario dado es simplemente:

          CLAVE = ( SUMA_ASCII_USUARIO + 666 ) XOR 26215
================================================================================
"""

import sys

# --- Constantes extraidas del binario ---------------------------------------
LOOKUP_TABLE = "R3V3RS1NG!"      # 10 bytes en VA 0x404088 (seccion .data)
XOR_CONST    = 0x6667            # constante XOR aplicada en 0x401228 (= 26215)
USER_LEN     = 10                # longitud exacta exigida por el binario

TABLE_SUM = sum(ord(c) for c in LOOKUP_TABLE)   # == 666


def generar_clave(usuario: str) -> int:
    """Devuelve la clave numerica valida para el nombre de usuario indicado.

    Lanza ValueError si el usuario no cumple la restriccion de longitud.
    """
    if len(usuario) != USER_LEN:
        raise ValueError(
            f"El nombre de usuario debe tener EXACTAMENTE {USER_LEN} "
            f"caracteres (recibidos: {len(usuario)})."
        )
    if any(c.isspace() for c in usuario):
        raise ValueError(
            "El nombre de usuario no puede contener espacios "
            "(el binario lo lee con scanf %s)."
        )

    suma_usuario = sum(ord(c) for c in usuario)     # SUMA ASCII de los 10 chars
    s = suma_usuario + TABLE_SUM                    # valor interno S
    return s ^ XOR_CONST                            # clave valida


def verificar(usuario: str, clave: str) -> bool:
    """Emula EXACTAMENTE la comprobacion del binario (autocomprobacion)."""
    if len(usuario) != USER_LEN:
        return False
    if not clave.isdigit():                         # isdigit() del binario
        return False
    s = sum(ord(c) for c in usuario) + TABLE_SUM
    return int(clave) == (s ^ XOR_CONST)


def _banner() -> None:
    print("=" * 64)
    print("  KEYGEN  -  reto.exe   |   Sistema de Registro")
    print("  Francisco Serrano Sanchez  -  Practica de Reversing")
    print("=" * 64)


def main(argv) -> int:
    _banner()

    # El usuario puede pasarse como argumento o introducirse de forma interactiva
    if len(argv) > 1:
        usuario = argv[1]
    else:
        usuario = input("Introduzca el nombre de usuario (10 caracteres): ").strip()

    try:
        clave = generar_clave(usuario)
    except ValueError as err:
        print(f"\n[ERROR] {err}")
        return 1

    print()
    print(f"  Usuario .......... : {usuario}")
    print(f"  Suma ASCII usuario : {sum(ord(c) for c in usuario)}")
    print(f"  Suma tabla (.data) : {TABLE_SUM}   ('{LOOKUP_TABLE}')")
    print(f"  Valor interno S .. : {sum(ord(c) for c in usuario) + TABLE_SUM}")
    print(f"  Constante XOR .... : {XOR_CONST}  (0x{XOR_CONST:04X})")
    print("-" * 64)
    print(f"  >>> CLAVE DE REGISTRO VALIDA : {clave}")
    print("-" * 64)

    # Autocomprobacion: confirma que la clave generada superaria al binario
    ok = verificar(usuario, str(clave))
    print(f"  Autocomprobacion ..: {'CORRECTA (Registro exitoso)' if ok else 'FALLIDA'}")
    print("=" * 64)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
