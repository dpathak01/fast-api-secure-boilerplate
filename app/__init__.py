"""FastAPI Secure Boilerplate - Production-grade API."""

__version__ = "1.0.0"
__all__ = ["app"]


def __getattr__(name: str):
    if name == "app":
        from app.main import app

        return app
    raise AttributeError(name)
