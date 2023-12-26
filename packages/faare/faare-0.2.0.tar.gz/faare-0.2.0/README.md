# Fully Agnostic Atomic Render Environment

[![pipeline status](https://gitlab.tue.nl/inorganic-materials-chemistry/faare/badges/master/pipeline.svg)](https://gitlab.tue.nl/inorganic-materials-chemistry/faare/-/commits/master)
[![PyPI](https://img.shields.io/pypi/v/faare?color=green)](https://pypi.org/project/faare/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

FAARE is a pure-Python package for automated rendering of VASP structures on headless
servers. Note that FAARE is designed for Linux Debian/Ubuntu and is not intended
to work on other operating systems.

## Installation

### Installing Blender

FAARE is designed to operate with Blender LTS 3.6 and assumes Blender is installed
in the /opt folder. Below, a brief set of instructions are provided to install
Blender.

```bash
sudo apt install -y libxrender-dev libxxf86vm-dev libxfixes-dev libxi-dev libxkbcommon-dev libsm-dev 
sudo mkdir /opt
cd /opt
sudo wget https://ftp.halifax.rwth-aachen.de/blender/release/Blender3.6/blender-3.6.7-linux-x64.tar.xz
sudo tar -xvf blender-3.6.7-linux-x64.tar.xz
sudo rm blender-3.6.7-linux-x64.tar.xz
```

Before proceeding to use Blender, make sure that CUDA support is enabled and that
the correct GPUs are selected. If you use Blender on a remote server, you need
to open the Blender

### PyPi

First, make sure the required dependencies are installed

```bash
sudo apt install python3-venv
```

Next, create a virtual environment (compliant with PEP668) and install FAARE in there

```bash
python3 -m venv ~/.venv
source ~/.venv/bin/activate
```

### Testing your installation



## Manual

See: https://faare-inorganic-materials-chemistry-6980722ff50f253a4f45dd9bd22.pages.tue.nl/