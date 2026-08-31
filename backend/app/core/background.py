import asyncio
from datetime import datetime,timezone
from app.db.session import SessionLocal
from app.models.ticket import Ticket
from app.models.notification import Notification
from app.services.sla_service import sla_status
async def sla_monitor():
    while True:
        try:
            db=SessionLocal()
            for t in db.query(Ticket).filter(Ticket.status.notin_(["closed","cancelled"])).all():
                state=sla_status(t)
                if state in ("at_risk","breached") and t.assigned_agent_id:
                    exists=db.query(Notification).filter(Notification.user_id==t.assigned_agent_id,Notification.message.like(f"SLA {state}%ticket #{t.id}%"),Notification.created_at>=datetime.now(timezone.utc).replace(hour=0,minute=0,second=0,microsecond=0)).first()
                    if not exists:db.add(Notification(user_id=t.assigned_agent_id,title="SLA alert",message=f"SLA {state}: ticket #{t.id} is approaching/exceeding its deadline.",type="sla"))
            db.commit();db.close()
        except Exception: pass
        await asyncio.sleep(60)
