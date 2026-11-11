"""Business logic services package.

Services orchestrate application workflows: they receive data from
routers, interact with the database via SQLAlchemy, call external
APIs, and return results. Services know nothing about HTTP (no
Request, Response, or status codes).
"""