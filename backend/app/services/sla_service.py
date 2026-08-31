from datetime import timedelta,datetime,timezone
from app.models.sla import SLAPolicy
DEFAULTS={"low":48,"medium":24,"high":8,"critical":2}
def seed_slas(db):
    for p,h in DEFAULTS.items():
        if not db.query(SLAPolicy).filter_by(priority=p).first(): db.add(SLAPolicy(priority=p,response_hours=h,resolution_hours=h))
    db.commit()
def deadline(db,priority):
    p=db.query(SLAPolicy).filter_by(priority=priority.lower(),is_active=True).first(); hours=p.resolution_hours if p else DEFAULTS.get(priority.lower(),24)
    return datetime.now(timezone.utc)+timedelta(hours=hours)
def sla_status(ticket):
    if not ticket.sla_deadline:return "unknown"
    now=datetime.now(timezone.utc); remaining=(ticket.sla_deadline-now).total_seconds()/3600
    if ticket.status in ("resolved","closed"): return "within_sla" if ticket.resolved_at and ticket.resolved_at<=ticket.sla_deadline else "breached"
    if remaining<=0:return "breached"
    if remaining<=max(2, (ticket.sla_deadline-ticket.created_at).total_seconds()/3600*0.25):return "at_risk"
    return "within_sla"
