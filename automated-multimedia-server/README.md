# Scripts



## Project Structure




## Prerequisites

1. **Python 3.12.3**: Ensure you have Python 3.12.3 installed. You can check your version by running:

   ```bash
   python3 --version
   ```

   para usar la version de python correcta usaremos pyenv

   Si no tienes **pyenv** instalado, puedes hacerlo siguiendo las instrucciones de la [documentación oficial](https://github.com/pyenv/pyenv#installation). Una vez instalado, asegúrate de reiniciar tu terminal y ejecutar:

   ```bash
   pyenv install 3.12.3
   pyenv local 3.12.3
   ```

2. **uv package manager**: We use uv for dependency management. Install it with:

   ```bash
   python -m pip install --user pipx
   python -m pipx ensurepath
   ```

3. **Environment Variables**: Set up environment variables for API tokens:


## Setup Instructions

1. **Clone the Repository**:

   ```bash
   git clone 
   cd 
   ```

2. **Create a Virtual Environment with uv**:

   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install Required Packages**:

   ```bash
   uv pip install -r requirements.txt
   ```

4. **Set Environment Variables**:
   Export the required environment variables in your shell, or add them to your `.bashrc` or `.zshrc` for persistence.
   ```bash
   export 
   export 
   export 
   export 
   ```

## Usage

Each folder contains specific scripts for interacting with their respective platforms. Detailed documentation for individual scripts can be found within each folder.

## Logging

All scripts generate logs to help track operations, errors, and API responses. Logs are saved with timestamps in separate files within each platform directory.

## License

This repository is licensed under the MIT License.