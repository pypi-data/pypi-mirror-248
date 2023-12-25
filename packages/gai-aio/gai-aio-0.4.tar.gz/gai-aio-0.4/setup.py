from setuptools import setup, find_packages
from os.path import abspath
import subprocess, os, sys
from setuptools.command.install import install

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        subprocess.check_call([os.sys.executable, 'post_install.py'])
        install.run(self)
        subprocess.call([os.sys.executable, 'post_install.py'])

setup(
    name='gai-aio',
    version='0.4',
    author="kakkoii1337",
    author_email="kakkoii1337@gmail.com",
    description = """Gai/Gen is the Universal Multi-Modal Wrapper Library for LLM. The library is designed to provide a simplified and unified interface for seamless switching between multi-modal open source language models on a local machine and OpenAI APIs.""",
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    cmdclass={
        'install': PostInstallCommand,
    },
    python_requires='>=3.10',        
    install_requires=[
       "accelerate>=0.24.1", 
       'anthropic==0.3.11',
       "bitsandbytes==0.41.0",
       "einops==0.6.1", 
       "einops-exts==0.0.4", 
       "fastapi",
       "gradio==3.35.2", 
       "gradio_client==0.2.9",
       "httpx==0.24.0", 
       'llama-cpp-python==0.2.11',
       "markdown2[all]", 
       "numpy", 
       'openai==1.6.1',
       "peft>=0.4.0", 
       'protobuf==3.19.6',
       'pydantic==1.10.12',
       'python-dotenv==1.0.0',
       'python-multipart==0.0.6',
       'PyDub==0.25.1',
       'safetensors>=0.3.1',
       "scikit-learn==1.3.0",
       'scipy==1.11.2',
       'sentencepiece==0.1.99',
       "shortuuid",
       'tiktoken==0.4.0',
       "timm>=0.6.13",
       "tokenizers>=0.12.1,<0.15.1", 
       "torch==2.1.2",
       "torchvision>=0.15.2",
       "transformers==4.35.0", 
       'uvicorn==0.23.2'
    ]
)