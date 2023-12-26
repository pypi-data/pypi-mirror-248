from setuptools import setup, find_packages

setup(
    name='daofun',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'matplotlib',
        'astropy',
        'aplpy',
        'IPython',
        'PySimpleGUI',
    ],
    entry_points={
        'console_scripts': [
            'daofun = daofun.DAOfun.daofun:main'  # Puede variar dependiendo de cómo definas tu función principal
        ]
    },
    # Otros metadatos como autor, descripción, etc.
    author='Carlos Quezada',
    description="""
DAOFUN is an interactive adaptation of the DAOPHOT 
astronomical image processing software. It provides 
a user-friendly interface through button-based interactions, 
enabling astronomers to perform various tasks seamlessly. 
The software operates by executing DAOPHOT commands in the 
background, facilitating astronomical data analysis, such 
as finding, photometry, and refining point spread functions (PSFs) 
in images. DAOFUN simplifies the utilization of DAOPHOT's capabilities 
by integrating them into an accessible and intuitive graphical user interface.


Credits: by Carlos Quezada
            inspired in the work of Alvaro Valenzuela
            thanks to DAOPHOT by Peter Stetson""",
    license='Licencia',
    keywords='daophot astronomical python',
    url='https://github.com/ciquezada/daofun'
)
