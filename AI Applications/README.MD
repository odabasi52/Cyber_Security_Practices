### Installations and Setup
    - Install miniconda
        
        ```bash
        wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
        chmod +x Miniconda3-latest-Linux-x86_64.sh
        ./Miniconda3-latest-Linux-x86_64.sh -b -u
        eval "$(/home/$USER/miniconda3/bin/conda shell.$(ps -p $$ -o comm=) hook)"
        ```
        
    - To initialize `conda` for your shell, run the following command after installing `Miniconda`:
        
        ```bash
        conda init
        ```
        
    - Finally, run these two commands to complete the `init` process
        
        ```bash
        conda config --add channels defaults
        conda config --add channels conda-forge
        conda config --add channels nvidia # only needed if you are on a PC that has a nvidia gpu
        conda config --add channels pytorch
        conda config --set channel_priority strict
        ```
        
    - To prevent the `base` environment from activating automatically, you can use the following command:
        
        ```bash
        conda config --set auto_activate_base false
        ```
        
    - `conda` provides a simple way to create virtual environments. For example, to create a new environment named `ai` with Python 3.11, use the following command:
        
        ```bash
        conda create -n ai python=3.11
        
        # Activating the Environment
        conda activate ai
        
        # To deactivate the environment, use:
        conda deactivate
        ```
        
    
    ---
    
    - Necessary libraries:
        
        ```bash
        conda install -y numpy scipy pandas scikit-learn matplotlib seaborn transformers datasets tokenizers accelerate evaluate optimum huggingface_hub nltk category_encoders
        conda install -y pytorch torchvision torchaudio pytorch-cuda=12.4 -c pytorch -c nvidia
        pip install requests requests_toolbelt
        ```
        
    - `conda` provides a method to keep conda-managed packages up to date. Running the following command updates all conda-installed packages within the `(ai)` environment, but it does not update packages installed with `pip`. Any pip-installed packages must be managed separately, and mixing `pip` and `conda` installations may increase the risk of dependency conflicts.
        
        ```bash
        conda update --all
        ```
        
    
    ---
    
    - Install jupyter lab
        
        ```bash
        conda install -y jupyter jupyterlab notebook ipykernel 
        ```
        
        Make sure you are running the command from within your ai environment. To start `JupyterLab`, simply run:
        
        ```bash
        jupyter lab
        ```
        
    
    ---
    
    Restarting the `kernel` clears all variables, functions, and imported modules from memory, allowing you to start fresh without shutting down `JupyterLab` entirely.
