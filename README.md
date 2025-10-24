# Intro Neuromorphic HCI

This Repo contains the code for a project of group 3 for the course Introduction to Neuromorphic Human Computer Interaction at Radboud University.

## Running the code

1. First make sure to install poetry following [the guide on their website](https://python-poetry.org/docs/).
2. Activate a virtual environment by running the line
   `python3 -m venv .venv`
3. Activate the environment by running the command
   - On Linux/MacOS: `source .venv/bin/acticate`
   - On Windows: `.venv\Scripts\activate`
4. Next, run `poetry install` in your terminal, this will install all the required packages you need to run the code
5. Navigate to the `Intro_Neuromorphic_HCI` directory and clone the libpointing library:
   `git clone https://github.com/INRIA/libpointing.git`
6. **[FOR MacOS]**: The original libpointing bindings need two modifications to work properly on macOS:
   - Fix the `__init__.py` file:
      The original `__init__.py` tries to import Windows-specific modules on all platforms. Replace it with the fixed version:

      ```bash
      cp __init__.py libpointing/bindings/Python/cython/libpointing/__init__.py
      ```

      Or manually edit `libpointing/bindings/Python/cython/libpointing/__init__.py` to wrap the Windows import in a platform check:

      ```python
      import platform

      from .libpointing import (
         PointingDevice,
         DisplayDevice,
         TransferFunction,
         PointingDeviceManager,
         PointingDeviceDescriptor,
         )

      # Windows-specific acceleration function
      if platform.system() == 'Windows':
         from .libpointing import winSystemPointerAcceleration
      ```

   - Add the Homebrew build script:
   Copy the `build_homebrew.py` script into the bindings directory:

   ```bash
   cp build_homebrew.py libpointing/bindings/Python/cython/build_homebrew.py
   ```

   This script is configured to use the Homebrew-installed libpointing library.

   - Build the libpointing Python Bindings:

   ```bash
   cd libpointing/bindings/Python/cython
   ./venv/bin/python build_homebrew.py build_ext --inplace
   cd ../../../..
   ```

7. In your terminal, navigate to the `Intro_Neuromorphic_HCI` directory, and run `python3 main.py`
