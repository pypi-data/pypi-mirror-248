from setuptools import setup, find_packages


'''
    install_requires=[
        'DataVisualization.exe',
        'glewinfo.exe',
        'visualinfo.exe'
        'DataVisualization.exp',
        'DataVisualization.lib',
        'DataVisualization.pdb',
        'freeglut.dll',
        'glew32.dll',
        'glfw3.dll',
        'imgui.ini',
        'MANIFEST.in',
        'openal32.dll',
        'BackgroundFragment.glsl',
        'SpheresFragment.glsl',
        'SpheresVertex.glsl',
        'UserPrefs.txt'
    ],
'''


setup(
    name='DAV',
    version='1.1',
    include_package_data=True,
    packages=find_packages(),
    
)


