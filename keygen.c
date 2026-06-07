/*
 * ============================================================================
 *  keygen.c  --  Generador de claves (keygen) para  reto.exe
 * ----------------------------------------------------------------------------
 *  Practica de Ingenieria Inversa
 *  Autor: Francisco Serrano Sanchez
 *
 *  Version en C del keygen (equivalente a keygen.py). El binario original
 *  estaba compilado en C/C++ con MSVC, por lo que se incluye tambien esta
 *  variante en el mismo lenguaje.
 *
 *  Compilacion:
 *      gcc -O2 -o keygen keygen.c           (Linux / MinGW)
 *      cl  keygen.c                         (MSVC en Windows)
 *
 *  Uso:
 *      ./keygen NOMBREUSER     (usuario de 10 caracteres, sin espacios)
 *      ./keygen                (modo interactivo)
 *
 *  Algoritmo:  CLAVE = ( SUMA_ASCII(usuario) + 666 ) XOR 0x6667
 *              666   = suma de los 10 bytes de la tabla "R3V3RS1NG!" (0x404088)
 *              0x6667 = constante XOR aplicada por el binario en 0x401228
 * ============================================================================
 */

#include <stdio.h>
#include <string.h>

#define USER_LEN   10            /* longitud exacta exigida por el binario   */
#define XOR_CONST  0x6667        /* constante XOR (= 26215)                  */

/* Tabla de 10 bytes situada en la VA 0x404088 de la seccion .data           */
static const char LOOKUP_TABLE[] = "R3V3RS1NG!";

/* Suma de los bytes de la tabla -> constante 666                            */
static int table_sum(void)
{
    int s = 0, i;
    for (i = 0; LOOKUP_TABLE[i] != '\0'; i++)
        s += (unsigned char)LOOKUP_TABLE[i];
    return s;                                  /* == 666 */
}

/* Suma de los valores ASCII de los caracteres del nombre de usuario         */
static int user_sum(const char *user)
{
    int s = 0, i;
    for (i = 0; user[i] != '\0'; i++)
        s += (unsigned char)user[i];
    return s;
}

/* Genera la clave valida. Devuelve -1 si el usuario no tiene 10 caracteres. */
static long generar_clave(const char *user)
{
    if (strlen(user) != USER_LEN)
        return -1;
    return (long)((user_sum(user) + table_sum()) ^ XOR_CONST);
}

int main(int argc, char *argv[])
{
    char  buffer[64];
    const char *user;
    long  clave;

    printf("================================================================\n");
    printf("  KEYGEN - reto.exe  |  Francisco Serrano Sanchez\n");
    printf("================================================================\n");

    if (argc > 1) {
        user = argv[1];
    } else {
        printf("Introduzca el nombre de usuario (10 caracteres): ");
        if (scanf("%63s", buffer) != 1)
            return 1;
        user = buffer;
    }

    clave = generar_clave(user);
    if (clave < 0) {
        printf("\n[ERROR] El usuario debe tener EXACTAMENTE %d caracteres "
               "(recibidos: %d).\n", USER_LEN, (int)strlen(user));
        return 1;
    }

    printf("\n  Usuario ............ : %s\n", user);
    printf("  Suma ASCII usuario . : %d\n", user_sum(user));
    printf("  Suma tabla (.data) . : %d   (\"%s\")\n", table_sum(), LOOKUP_TABLE);
    printf("  Valor interno S .... : %d\n", user_sum(user) + table_sum());
    printf("  Constante XOR ...... : %d (0x%04X)\n", XOR_CONST, XOR_CONST);
    printf("  ------------------------------------------------------------\n");
    printf("  >>> CLAVE DE REGISTRO VALIDA : %ld\n", clave);
    printf("================================================================\n");
    return 0;
}
