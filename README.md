# Práctica 2: Sistema de Turnos Médicos 🏥

Sistema de gestión de turnos para una clínica médica desarrollado en **Python**, utilizando una implementación de **colas dinámicas**, una interfaz gráfica con **Tkinter** y visualización de datos con **Graphviz**.

**Universidad San Carlos de Guatemala | Introducción a la Programación y Computación 2**
* **Estudiante:** Wilson Manuel Santos Ajcot
* **Carné:** 201907179

---

### ✨ Características Principales

* **Registro de Pacientes:** Permite agregar nuevos pacientes a la cola de espera, capturando nombre, edad y especialidad.
* **Gestión de Turnos FIFO:** Los pacientes son atendidos en el estricto orden en que llegaron (First-In, First-Out).
* **Cálculo de Tiempos:** Estima el tiempo de espera total para cada paciente basándose en los turnos previos.
* **Interfaz Gráfica Intuitiva:** Desarrollada con **Tkinter** para una fácil interacción.
* **Visualización de la Cola:** Genera una representación gráfica del estado de la cola en tiempo real usando **Graphviz**.



---

### 🔧 Tecnologías Utilizadas

* **Lenguaje:** Python 3.10+
* **Interfaz Gráfica:** Tkinter (biblioteca estándar de Python)
* **Visualización:** Graphviz

---

### 🚀 Cómo Empezar

Sigue estos pasos para ejecutar el proyecto en tu máquina local.

#### **Pre-requisitos**

1.  **Python:** Asegúrate de tener Python 3.10 o superior instalado.
2.  **Graphviz:** Debes instalar el software de Graphviz en tu sistema operativo. Puedes descargarlo desde [graphviz.org/download/](https://graphviz.org/download/).
    * **Importante:** Asegúrate de agregar la carpeta `bin` de Graphviz a la variable de entorno PATH de tu sistema para que el programa pueda encontrarlo.

#### **Instalación**

1.  **Clona el repositorio:**

    ```sh

    git clone https://github.com/WilsonJrSantos/IPC2_Practica2_201907179.git

    cd IPC2_Practica2_201907179

#### **Ejecución**

Para iniciar la aplicación, ejecuta el siguiente comando desde la raíz del proyecto:

```sh
python src/main.py