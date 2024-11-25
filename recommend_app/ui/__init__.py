"""
Jinja Templating - UI
"""

# Builtin imports
from typing import TYPE_CHECKING, Optional, Any, TypeAlias

# Project specific imports
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.templating import _TemplateResponse


if TYPE_CHECKING:
    from fastapi import FastAPI, Request

# -----------------------------------------------------------------------------#
# Globals
# -----------------------------------------------------------------------------#
__TEMPLATES = Jinja2Templates(directory="recommend_app/ui/templates")
JinjaTemplateResponse: TypeAlias = _TemplateResponse


# -----------------------------------------------------------------------------#
# Functions
# -----------------------------------------------------------------------------#
def mount_static_files(app: "FastAPI"):
    """
    Mount the static files to the FastAPI App
    """
    app.mount(
        "/static", StaticFiles(directory="recommend_app/ui/static"), name="static"
    )


def show_page(
    request: "Request", name: str, context: Optional[dict[str, Any]] = None
) -> JinjaTemplateResponse:
    """
    Display the page

    Args:
        request (Request): FastAPI request
        name (str): Name of the html file to load. Eg: health.html
        context (dict): Contextual information for the html page
    """
    context = context or {}
    return __TEMPLATES.TemplateResponse(request=request, name=name, context=context)
