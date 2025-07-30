import base64
import io
from typing import List
import matplotlib.pyplot as plt
from ..database import conn, cursor
from datetime import datetime, timedelta

def get_plot(name: str, indicator: str, start_date: datetime, end_date: datetime) -> str:
    """
    Generate a plot for the given name and indicator within the specified date range.

    Args:
        name (str): The name of the entity to plot.
        indicator (str): The indicator to plot.
        start_date (str): The start date in 'YYYY-MM-DD' format.
        end_date (str): The end date in 'YYYY-MM-DD' format.

    Returns:
        StreamingResponse: A response containing the generated plot image.
    """

    days = (end_date - start_date).days

    x: List[datetime] = []
    y: List[float] = []

    for day in range(days):
        x.append(start_date + timedelta(days=day))
        yVal = None
        sql = f"""SELECT {indicator} FROM stocks WHERE (name = '{name}' OR short_code = '{name}') AND DATE(recorded_at) = '{(start_date + timedelta(days=day)).date()}' ORDER BY recorded_at DESC LIMIT 1;"""
        cursor.execute(sql)
        yVal = cursor.fetchone()

        if yVal is not None:
            y.append(yVal[0])
        else:
            y.append(y[-1] if y else 0)  # Use the last value or 0 if no previous value exists

    plt.plot(x, y)
    plt.xlabel("Date")
    plt.ylabel(indicator)
    plt.title(f"{name} - {indicator} from {start_date} to {end_date}")

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf-8')