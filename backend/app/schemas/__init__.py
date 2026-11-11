"""Pydantic schemas package.

Schemas define the shape of data that crosses the API boundary:
request bodies received from clients and response bodies sent back.
They are deliberately kept separate from SQLAlchemy ORM models, which
describe the database structure. A single ORM model can have multiple
schemas (e.g. UserCreate, UserRead, UserUpdate).
"""