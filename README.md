# 🔓 Reversing & Keygen: reto.exe

<p align="left">
  <img src="https://img.shields.io/badge/Reversing-A78BFA?style=for-the-badge&logo=hackerone&logoColor=white" alt="Reversing" />
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/C-00599C?style=for-the-badge&logo=c&logoColor=white" alt="C" />
  <img src="https://img.shields.io/badge/Grade-10%2F10-FCC624?style=for-the-badge&logo=academiccap&logoColor=black" alt="Grade 10/10" />
</p>

Este repositorio contiene la solución completa (análisis y generador de claves) a un binario `crackme` de tipo "Sistema de Registro" para Windows. Este proyecto fue desarrollado como práctica de **Ingeniería Inversa** mientras realizaba el CUFA.

---

## 🎯 Objetivo del Proyecto

El reto consistía en realizar un **análisis estático** del binario `reto.exe` (PE32, Intel x86) sin ejecutarlo, con el fin de:
1. Reconstruir el algoritmo de validación de la clave de licencia.
2. Desarrollar un *Keygen* (Generador de claves) capaz de producir una licencia válida para cualquier usuario.

---

## 🔬 Análisis Estático y Reconstrucción

A través del desensamblado del código de la sección `.text` y la inspección de cadenas e importaciones, logré inferir la lógica completa del programa.

El algoritmo de validación oculto funciona de la siguiente manera:
1. **Validación inicial:** El nombre de usuario introducido debe tener exactamente 10 caracteres y no contener espacios[cite: 2, 4].
2. **Cálculo del valor base:** El programa calcula un valor `S` sumando el valor ASCII de cada carácter del nombre de usuario y los sumaba a los valores de una tabla oculta en la memoria (VA `0x404088`)[cite: 2, 4].
3. **El secreto:** Dicha tabla contenía los bytes correspondientes a la cadena `"R3V3RS1NG!"`, cuya suma constante es `666`[cite: 2, 4].
4. **Validación final:** La clave introducida por el usuario se considera válida si es puramente numérica y, al convertirse a entero, es idéntica a `S XOR 0x6667` (donde `0x6667` es `26215` en decimal)[cite: 2, 4].

**Fórmula del Keygen:**
`CLAVE = ( Σ ASCII(usuario) + 666 ) XOR 26215`[cite: 2, 4]

---

## 🚀 Uso del Keygen

He implementado el generador de claves en dos lenguajes: **Python** (para portabilidad) y **C** (el lenguaje original del binario analizado). Ambos incluyen autocomprobación y validación de entrada[cite: 4].

### Opción A: Python
```bash
# Modo interactivo
python3 keygen.py

# Modo por argumento
python3 keygen.py NOMBREUSER
