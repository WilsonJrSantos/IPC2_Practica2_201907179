# Sistema de Turnos Médicos 🏥

<p align="center">
  <img src="https://shields.io/badge/Python-3.6+-blue?logo=python&logoColor=white" alt="Python version">
  <img src="https://shields.io/badge/License-MIT-green" alt="License">
  <img src="https://shields.io/badge/Status-Terminado-brightgreen" alt="Project Status">
</p>

Sistema de escritorio para la gestión de turnos en una clínica médica, desarrollado en **Python**. La aplicación utiliza una **cola dinámica** implementada desde cero para manejar el flujo de pacientes, una interfaz gráfica con **Tkinter** y visualización de datos en tiempo real con **Graphviz**.

**Universidad San Carlos de Guatemala | Introducción a la Programación y Computación 2**
* **Estudiante:** Wilson Manuel Santos Ajcot
* **Carné:** 201907179

---

## 📋 Tabla de Contenido
1.  [📖 Sobre el Proyecto](#-sobre-el-proyecto)
    * [✨ Características Principales](#-características-principales)
2.  [🛠️ Tecnologías Utilizadas](#️-tecnologías-utilizadas)
3.  [🚀 Empezando](#-empezando)
    * [Prerrequisitos](#prerrequisitos)
    * [Instalación y Ejecución](#️-instalación-y-ejecución)
4.  [📁 Estructura del Proyecto](#-estructura-del-proyecto)

---

## 📖 Sobre el Proyecto

Este proyecto digitaliza y optimiza el sistema de colas de una clínica, reemplazando el método tradicional de espera física por una aplicación de escritorio intuitiva. La principal restricción del desarrollo fue la **prohibición de usar estructuras de datos nativas de Python** (listas, diccionarios, etc.), forzando la implementación de una cola dinámica con nodos enlazados.

### ✨ Características Principales

* **Implementación Pura de Cola:** Gestión de turnos con una estructura de Cola dinámica (FIFO) construida desde cero.
* **Registro de Pacientes:** Formulario para añadir nuevos pacientes a la cola, capturando nombre, edad y especialidad médica.
* **Atención Secuencial:** Sistema para atender pacientes en el estricto orden de llegada.
* **Cálculo de Tiempos:** El sistema estima el tiempo de espera para los pacientes en cola y calcula el tiempo total de atención.
* **Visualización en Tiempo Real:** Genera representaciones gráficas del estado de la cola y estadísticas del sistema usando **Graphviz**.
* **Interfaz Gráfica Intuitiva:** Desarrollada con **Tkinter** para una interacción de usuario simple y directa.



---

## 🛠️ Tecnologías Utilizadas

* **Lenguaje:** Python 3.6+
* **Interfaz Gráfica:** Tkinter (biblioteca estándar de Python para GUIs nativas).
* **Visualización de Datos:** Graphviz (para generar diagramas a partir de la estructura de datos).
* **Manejo de Imágenes:** Pillow (para integrar los gráficos generados en la interfaz de Tkinter).

---

## 🚀 Empezando

Sigue estos pasos para ejecutar el proyecto en tu máquina local.

### Prerrequisitos

1.  **Python:** Asegúrate de tener Python 3.6 o superior instalado.
2.  **Graphviz:** Debes instalar el software de Graphviz en tu sistema operativo.
    * Puedes descargarlo desde la [página oficial de descargas de Graphviz](https://graphviz.org/download/).
    * **Importante:** Durante la instalación, o después de ella, asegúrate de agregar la carpeta `bin` de Graphviz a la variable de entorno **PATH** de tu sistema. De lo contrario, el programa no podrá generar los gráficos.

### ⚙️ Instalación y Ejecución

1.  **Clona el repositorio:**
    ```sh
    git clone https://github.com/WilsonJrSantos/IPC2_Practica2_201907179.git
    cd IPC2_Practica2_201907179
    ```

2.  **(Opcional pero recomendado) Crea y activa un entorno virtual:**
    ```sh
    # Crear el entorno
    python -m venv venv

    # Activar en Windows
    .\venv\Scripts\activate

    # Activar en macOS/Linux
    source venv/bin/activate
    ```

3.  **Instala las dependencias de Python:**
    ```sh
    pip install -r requirements.txt
    ```

4.  **Ejecuta la aplicación:**
    Navega al directorio `src` y ejecuta el script principal.
    ```sh
    python src/main.py
    ```
---

## 📁 Estructura del Proyecto

El proyecto está organizado en una arquitectura por capas para separar responsabilidades y facilitar el mantenimiento.

```
/
├── .gitignore
├── README.md
├── requirements.txt
└── src/
    ├── main.py             # Punto de entrada de la aplicación
    ├── gui/
    │   └── interfaz.py     # Lógica y construcción de la GUI con Tkinter
    ├── models/
    │   ├── nodo.py         # Clase Nodo para las estructuras enlazadas
    │   ├── cola.py         # Implementación de la Cola dinámica
    │   ├── paciente.py     # Modelo de datos para el Paciente
    │   └── reporte.py      # Modelos para los reportes de estadísticas
    ├── services/
    │   ├── turno_service.py    # Lógica de negocio (manejo de la cola, cálculos)
    │   └── graphviz_service.py # Lógica para generar los gráficos
    └── utils/
        └── constantes.py   # Constantes del sistema (colores, textos, etc.)
```
---
