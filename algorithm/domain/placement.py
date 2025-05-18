from algorithm.domain.models import Item, Placement, StorageSystem


def place_item(
    storage_system: StorageSystem, selected_placement: Placement, item: Item
) -> StorageSystem:
    storage_system.items[selected_placement].append(item)
    return storage_system
