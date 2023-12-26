# DAOFUN - Proyecto de Procesamiento de Imágenes Astronómicas

## Descripción
DAOFUN es una interfaz gráfica para DAOPHOT, una herramienta de procesamiento de imágenes astronómicas. Esta interfaz proporciona una forma intuitiva de interactuar con DAOPHOT, permitiendo a los astrónomos realizar tareas como encontrar, realizar fotometría y refinar funciones de dispersión de puntos (PSFs) en imágenes.

## Características principales
- Interfaz gráfica intuitiva basada en botones para ejecutar comandos DAOPHOT.
- Facilita tareas comunes de análisis de datos astronómicos.
- Realiza funciones como encontrar objetos, realizar fotometría y refinar PSFs.

## Créditos
- **Desarrollador:** Carlos Quezada
- Inspirado en el trabajo de Alvaro Valenzuela
- Utiliza la funcionalidad de DAOPHOT desarrollada por Peter Stetson

## Uso
El programa se ejecuta mediante el script principal `daofun.py`. Proporciona una interfaz gráfica intuitiva para realizar diversas tareas de procesamiento de imágenes astronómicas.

### Dependencias
El proyecto depende de las siguientes bibliotecas y herramientas:
- `pandas`
- `matplotlib`
- `astropy`
- `aplpy`
- `IPython`
- `PySimpleGUI`

Las siguientes librerias fueron desarrolladas/acondicionadas durante el proyecto
- `daophot_wraps`
- `daofun_gui_selection`
- `daofun_backend`
- `fits_handler`

### Instalación
1. Clona este repositorio.
2. Asegúrate de tener todas las dependencias instaladas, puedes ejecutar `setup.py`.
4. Ejecuta `daofun.py` para iniciar la interfaz gráfica.

## Instrucciones de Uso
1. Ejecuta el programa con `python daofun.py`.
2. Selecciona un archivo `.fits` para comenzar el procesamiento de imágenes astronómicas.
3. Utiliza los botones proporcionados para realizar acciones como encontrar objetos, realizar fotometría, refinar PSFs, entre otros.

## Contribuciones
¡Las contribuciones son bienvenidas! Si deseas contribuir, sigue estos pasos:
1. Haz un `fork` del repositorio.
2. Crea una nueva rama (`branch`): `git checkout -b feature/nueva-caracteristica`.
3. Realiza tus cambios y haz `commit`: `git commit -am 'Agrega nueva característica'`.
4. Haz un `push` a la rama: `git push origin feature/nueva-caracteristica`.
5. Abre un `pull request` en GitHub.

## Licencia
Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para obtener más detalles.
