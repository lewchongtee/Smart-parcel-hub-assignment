PRIORITY_LEVELS = ["Express", "Standard", "Economy"]
STATUS_LEVELS = ["In Hub", "Dispatched", "Returned"]


class ParcelValidationError(ValueError):
    pass


def validate_parcel_input(tracking_id, sender, receiver, zone, weight, value, priority):
    if not tracking_id or not isinstance(tracking_id, str):
        raise ParcelValidationError("Tracking ID must be a non-empty string.")
    if not sender or not isinstance(sender, str):
        raise ParcelValidationError("Sender name must be a non-empty string.")
    if not receiver or not isinstance(receiver, str):
        raise ParcelValidationError("Receiver name must be a non-empty string.")
    if not zone or not isinstance(zone, str):
        raise ParcelValidationError("Zone must be a non-empty string.")
    try:
        weight = float(weight)
    except (TypeError, ValueError):
        raise ParcelValidationError("Weight must be a number.")
    if weight <= 0:
        raise ParcelValidationError("Weight must be greater than 0.")
    try:
        value = float(value)
    except (TypeError, ValueError):
        raise ParcelValidationError("Declared value must be a number.")
    if value <= 0:
        raise ParcelValidationError("Declared value must be greater than 0.")
    if priority not in PRIORITY_LEVELS:
        raise ParcelValidationError(f"Priority must be one of {PRIORITY_LEVELS}.")
    return tracking_id, sender, receiver, zone, weight, value, priority
