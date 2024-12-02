import re


def handle_1st_node_for_ir_levels(ir_levels):
    """
    Handle the special case for '1st Node', replacing it with an empty string
    and adjusting the order.

    Args:
        ir_levels (list): The original list of levels.

    Returns:
        list: The modified list of levels.
    """
    if "1st Node" in ir_levels:
        return [""] + [level for level in ir_levels if level != "1st Node"]
    return ir_levels


def reorder_and_place_status_levels(ir_levels):
    """
    Reorder StatusLevel items by their numeric order and place them back in their original indices.
    Runs the reordering logic only if more than one StatusLevel is present.

    Args:
        levels (list): The original list of levels.

    Returns:
        list: The list with StatusLevel items reordered numerically and placed back in their initial positions.
    """
    # Preprocess levels to handle '1st Node'
    ir_levels = handle_1st_node_for_ir_levels(ir_levels)

    # Extract StatusLevel items and their indices
    status_levels = [
        (index, level)
        for index, level in enumerate(ir_levels)
        if "StatusLevel" in level
    ]

    # Only reorder if more than one StatusLevel is found
    if len(status_levels) > 1:
        # Sort StatusLevel items by the numeric value extracted from their names
        sorted_status_levels = sorted(
            status_levels, key=lambda x: int(re.search(r"(\d+)", x[1]).group(1))
        )

        # Replace the sorted StatusLevel items back into the original list
        ir_levels_copy = ir_levels.copy()
        for (original_index, _), (_, sorted_level) in zip(
            status_levels, sorted_status_levels
        ):
            ir_levels_copy[original_index] = sorted_level

        return ir_levels_copy

    return ir_levels
