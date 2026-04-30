from sqlalchemy import Column, String, Float, Integer, Boolean, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List
from datetime import datetime
from uuid import uuid4, UUID
import enum