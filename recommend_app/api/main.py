"""
Main entrypoint
"""

# Builtin imports
import os

# Project specific imports
import uvicorn


def main():
    """Main function"""
    uvicorn.run(
        "recommend_app.api.app:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8000")),
        reload=True,
    )


if __name__ == "__main__":
    main()
