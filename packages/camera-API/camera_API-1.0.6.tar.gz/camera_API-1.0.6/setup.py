from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='camera_API',
    version='1.0.6',
    packages=['camera_API'],
    package_data={
        'camera_API': ['\\cv2\\*',
                       '\\hid.cp310-win_amd64.pyd'],
    },
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        'numpy==1.24.3', 'opencv-python==4.5.5.62', 'hidapi==0.13.1',
    ],
    author='Sivabalan T',
    author_email='sivabalan.t@e-consystems.com',
    description='Used to accessing the camera.',
    classifiers=['Programming Language :: Python :: 3', ],
)
