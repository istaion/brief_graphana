from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
import datetime

from app.database import get_db
from app.schemas.item import ItemCreate, ItemResponse, ItemUpdate
from app.services.item_service import ItemService
from app.monitoring.metrics import (
    items_created_total,
    items_read_total,
    items_updated_total,
    items_deleted_total,
    DatabaseQueryTimer
)

router = APIRouter(prefix="/items", tags=["items"])

MAX_ITEMS_PER_PAGE = 1000

@router.get("/", response_model=list[ItemResponse])
def get_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Récupère la liste des items avec pagination."""
    # Mesurer la durée de la requête DB
    with DatabaseQueryTimer():
        items = ItemService.get_all(db, skip, limit)

    # Incrémenter le compteur APRÈS succès
    items_read_total.inc()

    return items


@router.get("/{item_id}", response_model=ItemResponse)
def get_item(item_id: int, db: Session = Depends(get_db)):
    # Mesurer la durée de la requête DB
    with DatabaseQueryTimer():
        item = ItemService.get_by_id(db, item_id)

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found",
        )

    # Incrémenter le compteur APRÈS succès
    items_read_total.inc()

    return item


@router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(item_data: ItemCreate, db: Session = Depends(get_db)):
    # Mesurer la durée de la requête DB
    with DatabaseQueryTimer():
        new_item = ItemService.create(db, item_data)

    # Incrémenter le compteur APRÈS succès
    items_created_total.inc()

    return new_item


@router.put("/{item_id}", response_model=ItemResponse)
def update_item(item_id: int, item_data: ItemUpdate, db: Session = Depends(get_db)):
    # Mesurer la durée de la requête DB
    with DatabaseQueryTimer():
        item = ItemService.update(db, item_id, item_data)

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found",
        )

    # Incrémenter le compteur APRÈS succès
    items_updated_total.inc()

    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    # Mesurer la durée de la requête DB
    with DatabaseQueryTimer():
        deleted = ItemService.delete(db, item_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found",
        )

    # Incrémenter le compteur APRÈS succès
    items_deleted_total.inc()

def _old_helper_function(data):
    """Cette fonction n'est plus utilisée mais n'a pas été supprimée."""
    return data.upper()
