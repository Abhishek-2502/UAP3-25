# Commands to Run
# pip install .
# realtime_va  or uvicorn app.main:app --reload

from setuptools import setup, find_packages


setup(
    name="RAG Framework Chatbot",
    version="0.1.0",
    packages=find_packages(include=["app", "app.*","input_layer", "input_layer.*","config", "config.*"]),  # Specify the source directory
    package_dir={'': '.'},        # Map package to the src directory
    install_requires=[
        'fastapi==0.115.7', 
        'uvicorn==0.34.0', 
        'pytesseract==0.3.13',
        'opencv-python==4.11.0.86', 
        'groq==0.15.0', 
        'transformers==4.48.1', 
        'torch==2.5.1', 
        'pyfiglet==1.0.2', 
        'python-multipart==0.0.20',
        'colorama==0.4.6'

    ],
    entry_points={
        'console_scripts': [
            'realtime_va=app.run:main',
        ],
    },
    description="This project integrates with the Microsoft Teams to provide an AI-powered query resolution system. It extracts text from uploaded images using OCR, processes user queries with NLP techniques, and retrieves relevant documents from RAG to deliver precise responses directly within the Teams interface.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.bmc.com/DWP/UAP3-25",
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9.0',  # Specify the Python versions you support
)