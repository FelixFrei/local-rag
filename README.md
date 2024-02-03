# local-rag
Retrieval-Augmented Generation (RAG) based on LlamaIndex for running on local LLMs.


## RAG with Llamaindex und Llama2

Using Llamaindex and Llama2 to build a RAG setup.
Based on Llamaindex example: https://docs.llamaindex.ai/en/latest/index.html

## Prerequisites
Running AI models local brings a lot of dependencies and requirements with it depending on the operating system, GPU, CPU and the model itself.
The text-generation-webui project from the oobabooga project has a well maintained setup script to install all the requirements and dependencies.
Therefore, we use this project to ensure all the requirements are correctly installed. Since drivers and packages are changing fast, we not copy the installation script to this project.
Instead we use the the oobabooga setup itself. So, you need to have a proper setup of oobabooga text-generation-webui.
local-rag v1.0 runs with the text-generation-webui v1.7.

### Install text-generation-webui
``` 
git clone https://github.com/oobabooga/text-generation-webui.git
git checkout v1.7

``` 
Follow the instructions here:
https://github.com/oobabooga/text-generation-webui


### LLama2
For the use of LLama2 model you need register on https://ai.meta.com/.
When you have an account you can download  models from https://ai.meta.com/download/llama2. What in our case is not neeeded since we use the huggingface platform.

### Huggingface
You need a huggingface account. Since we want to use the llama2 model we need to setup the hugingface account with the same e-address as the meta-ai account.
In addition you need to install the huggingface-cli and login to the huggingface platform.
``` 
pip install --upgrade huggingface_hub
``` 
The destination directory where huggingface-cli is installed must be in the PATH variable.
/home/user/.local/bin


``` 
huggingface-cli login
``` 
On the huggingface platform you need to create a new token for the login


## Install local-rag


Ensure both project are in the same folder.
``` 
git clone https://github.com/FelixFrei/local-rag.git
git clone https://github.com/oobabooga/text-generation-webui.git


ubuntu@host:~$ ls -la
drwxrwxr-x  7 ubuntu ubuntu      4096 Jan 20 05:19 local-rag
drwxrwxr-x 23 ubuntu ubuntu      4096 Jan 20 05:19 text-generation-webui

``` 

Setup the data example.
``` 
./get_bitcoinbook_data.sh

``` 


## run the script
When running the first time, you need to use the argument --update to install or update the requirements and driver.
As default the script will run the localRag.py script. You can change this by using the argument --script <scriptname>.

```

huggingface-cli login


./run_linux.sh --update

```

