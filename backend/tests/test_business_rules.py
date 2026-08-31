from app.services.ticket_service import TRANS

def test_closed_has_no_outgoing_transitions(): assert TRANS['closed']==set()
def test_cancelled_cannot_be_resolved(): assert 'resolved' not in TRANS['cancelled']
def test_resolved_only_closes(): assert TRANS['resolved']=={'closed'}
def test_open_can_progress_or_cancel(): assert TRANS['open']=={'in_progress','cancelled'}
