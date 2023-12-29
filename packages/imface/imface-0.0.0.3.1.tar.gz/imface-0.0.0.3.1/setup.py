from setuptools import setup, find_packages
from setuptools.command.install import install
from pathlib import Path
import gdown
import os


def get_deepface_home():
    """Get the home directory for storing weights and models.

    Returns:
        str: the home directory.
    """
    os.environ.setdefault("DEEPFACE_HOME", "/app")
    return str(os.getenv("DEEPFACE_HOME", default=str(Path.home())))

def initialize_folder():
    """Initialize the folder for storing weights and models.

    Raises:
        OSError: if the folder cannot be created.
    """
    home = get_deepface_home()
    deepFaceHomePath = home + "/.deepface"
    weightsPath = deepFaceHomePath + "/weights"

    if not os.path.exists(deepFaceHomePath):
        os.makedirs(deepFaceHomePath, exist_ok=True)
        print("Directory ", home, "/.deepface created")

    if not os.path.exists(weightsPath):
        os.makedirs(weightsPath, exist_ok=True)
        print("Directory ", home, "/.deepface/weights created")



home_dir = get_deepface_home()
def downloadWeights():
    print(home_dir, "home")
    # facenet512_url = "https://github.com/serengil/deepface_models/releases/download/v1.0/facenet512_weights.h5"
    retinaface_url = "https://github.com/serengil/deepface_models/releases/download/v1.0/retinaface.h5"
    facenet_url = "https://github.com/achmadAt/imface-weight/releases/download/facenet/facenet_weights.h5"
    # dlib_shape_url = "https://github.com/achmadAt/imface-weight/releases/download/shape_predictor_5_face_landmarks.dat/shape_predictor_5_face_landmarks.dat"
    # if os.path.isfile(str(home_dir) + "/.deepface/weights/facenet512_weights.h5") != True:
    #     print("facenet512_weights.h5 will be downloaded...")

    #     output = str(home_dir) + "/.deepface/weights/facenet512_weights.h5"
    #     gdown.download(facenet512_url, output, quiet=False)
    if os.path.isfile(str(home_dir) + "/.deepface/weights/facenet_weights.h5") != True:
        print("facenet_weights.h5 will be downloaded...")

        output = str(home_dir) + "/.deepface/weights/facenet_weights.h5"
        gdown.download(retinaface_url, output, quiet=False)
    if os.path.isfile(str(home_dir) + "/.deepface/weights/retinaface.h5") != True:
        print("retinaface.h5 will be downloaded...")

        output = str(home_dir) + "/.deepface/weights/retinaface.h5"
        gdown.download(retinaface_url, output, quiet=False)
    # if os.path.isfile(str(home_dir) + "/.deepface/weights/shape_predictor_5_face_landmarks.dat") != True:
    #     print("shape_predictor_5_face_landmarks.dat will be downloaded...")

    #     output = str(home_dir) + "/.deepface/weights/shape_predictor_5_face_landmarks.dat"
    #     gdown.download(dlib_shape_url, output, quiet=False)

class CustomInstallCommand(install):
    def run(self):
        install.run(self)
        initialize_folder()
        downloadWeights()

with open("README.md", "r") as file:
    description = file.read()

requirements = ["deepface"]

setup(
    name='imface',
    version='0.0.0.3.1',
    install_requires=requirements,
    packages=find_packages(),
    include_package_data=True,
    entry_points={"console_scripts": ["imface=imface.main:main"]},
    author="Achmad Alfazari",
    license="License :: OSI Approved :: MIT License",
    classifiers=[
        "Programming Language :: Python",
    ],
    long_description=description,
    long_description_content_type="text/markdown",
    python_requires=">=3.5.5",
    cmdclass={
        'install': CustomInstallCommand,
    },
)