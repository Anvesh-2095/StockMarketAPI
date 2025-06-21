from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import pytz

from app.database import conn, cursor


def remove_old_entries():
    """
    Removes entries from the stocks and shareholding tables that are older than 30 days.
    This function is intended to be run once a day at market close.
    """
    with conn:
        thirty_days_ago = datetime.now(pytz.timezone("Asia/Kolkata")) - timedelta(days=30)
        cursor.execute("DELETE FROM stocks WHERE recorded_at < %s", (thirty_days_ago,))
        cursor.execute("DELETE FROM shareholding_promoter WHERE recorded_at < %s", (thirty_days_ago,))
        cursor.execute("DELETE FROM shareholding_fii WHERE recorded_at < %s", (thirty_days_ago,))
        cursor.execute("DELETE FROM shareholding_mf WHERE recorded_at < %s", (thirty_days_ago,))
        cursor.execute("DELETE FROM shareholding_others WHERE recorded_at < %s", (thirty_days_ago,))

        conn.commit()

def remove_all_entries():
    """
    Removes all entries from the stocks and shareholding tables.
    This function is intended to be run once a day at market close.
    """
    with conn:
        cursor.execute("DELETE FROM stocks")
        cursor.execute("DELETE FROM shareholding_promoter")
        cursor.execute("DELETE FROM shareholding_fii")
        cursor.execute("DELETE FROM shareholding_mf")
        cursor.execute("DELETE FROM shareholding_others")

        conn.commit()



scheduler = BackgroundScheduler(timezone="Asia/Kolkata")
scheduler.add_job(
    remove_old_entries,
    trigger='cron',
    # run every day at 3:30 PM IST (market close time)
)

if __name__ == "__main__":
    remove_all_entries()