from datetime import datetime
import sys
import os

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from extensions import db

# This file is deprecated. Please use the JobApplication model from models/job.py instead.
# This file is kept for reference purposes only.

"""
The JobApplication model has been moved to models/job.py to avoid duplication.
Please import JobApplication from models/job.py instead of Application from this file.

Example:
from models.job import JobApplication
"""
