from app.models import Invoice


def invoice_payload(invoice: Invoice) -> dict:
    return {
        "id": invoice.id,
        "number": invoice.number,
        "status": invoice.status,
        "total_cents": invoice.total_cents,
        "due_date": invoice.due_date.isoformat(),
    }
