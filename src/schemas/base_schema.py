import re
from uuid import uuid4, UUID
from pydantic import BaseModel, field_validator, Field, EmailStr
from datetime import datetime
from typing import Optional, List
from enum import Enum