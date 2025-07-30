from fastapi import APIRouter, HTTPException, status
from ..utils import features_list

router = APIRouter(
    prefix="/api",
    tags=["api"],
)

@router.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    """
    Health check endpoint to verify the API is running.
    """
    return {"status": "ok", "message": "API is running smoothly."}

@router.get("/version", status_code=status.HTTP_200_OK)
def get_version():
    """
    Endpoint to retrieve the API version.
    """
    return {"version": "1.0.0", "description": "Stock Market Analysis API"}

@router.get("/docs", status_code=status.HTTP_200_OK)
def get_docs():
    """
    Endpoint to retrieve API documentation.
    """
    return {"message": "API documentation is available at /docs"}

@router.get("/indicators/all", status_code=status.HTTP_200_OK)
def get_all_indicators():
    """
    Endpoint to retrieve all available indicators.
    """
    return {"indicators": features_list.plot_indicators_list}

@router.get("/indicators/plot", status_code=status.HTTP_200_OK)
def get_plot_indicators():
    """
    Endpoint to retrieve indicators that can be plotted.
    """
    return {"plot_indicators": features_list.plot_indicators_list}