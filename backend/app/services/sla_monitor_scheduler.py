
import asyncio
import logging

from app.db.session import SessionLocal
from app.services.sla_monitor_service import SLAMonitorService


logger = logging.getLogger(__name__)


SLA_CHECK_INTERVAL_SECONDS = 60


async def run_sla_monitor():
    """
    Run the SLA monitor continuously in the background.

    The SLA status is checked every 60 seconds.
    """

    while True:
        db = SessionLocal()

        try:
            service = SLAMonitorService(db)

            result = service.check_sla()

            logger.info(
                "SLA Monitor | breached=%s | pending=%s",
                result["breached_count"],
                result["pending_count"],
            )

        except Exception:
            logger.exception(
                "SLA monitor failed"
            )

        finally:
            db.close()

        await asyncio.sleep(
            SLA_CHECK_INTERVAL_SECONDS
        )
