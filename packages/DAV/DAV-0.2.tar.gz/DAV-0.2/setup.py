from setuptools import setup

setup(
    name='DAV',
    version='0.2',
    #packages=['DataAnaliticVisor'],
    install_requires=[
        'DataVisualization.exe',
        'DataVisualization.exp',
        'DataVisualization.lib',
        'DataVisualization.pdb',
        'freeglut.dll',
        'glew32.dll',
        'glewinfo.exe',
        'glfw3.dll',
        'imgui.ini',
        'MANIFEST.in',
        'openal32.dll',
        'visualinfo.exe',
        "BackgroundFragment.glsl",
        "SpheresFragment.glsl",
        "SpheresVertex.glsl",
        "UserPrefs.txt"
        
    ],
)


