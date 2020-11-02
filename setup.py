import pathlib
import setuptools

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")
    
with open("requirements.txt") as f:
    requireds = f.read().splitlines()

setuptools.setup(
    name="yolo_labeler",
    version="0.0.3",
    author="Abhi Panchal",
    author_email="abpanchal95@gmail.com",
    description="Remove image background and label object in yolo format",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/abpanchal95/yolo-labeler",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
    keywords="remove, background, u2net, yolo, labelling, automatic, text, format",
    packages=['yolo_labeler', 'yolo_labeler.utils'],
    python_requires='>=3.6',
    install_requires=requireds,
)
