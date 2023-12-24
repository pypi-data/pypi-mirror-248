import os
import sys

# Get the directory of the script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Append the parent directory to sys.path
sys.path.append(os.path.join(script_dir, '..'))

from qrraj.qr import method
