from uuid import UUID

from fastapi import status
from fastapi.responses import JSONResponse

from database import Session


def get_or_404(item_class,
               item_id: UUID,
               session: Session):
    """Get an item with uniq id from the database or return http code 404."""
    item = session.query(item_class).filter(item_class.id == item_id).first()
    if item is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": f"{item_class.__name__.lower()} not found"}
        )
    return item
