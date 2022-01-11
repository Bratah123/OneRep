from typing import List

# All weights are in lbs

WEIGHT_PLATES = [45, 35, 25, 10, 5]  # We are skipping 2.5 lbs and 55 lbs plates as they are scarce
BAR_WEIGHT = 45


def lbs_to_kg(weight_in_lbs):
    return weight_in_lbs / 2.2


def kg_to_lbs(weight_in_kg):
    return weight_in_kg * 2.2


def one_rep_max_percentages(weight) -> List[int]:
    """
    return a list containing of all the percentages of a given weight with decimals removed
    """
    ret_list = []
    for i in range(10, 105, 5):
        # starting at 10% and then incrementing by 5 all til 100%
        ret_list.append((weight * (i / 100)) // 1)  # some jank math, but // 1 to remove decimal number

    return ret_list


def weight_to_plates(weight) -> str:
    """
    A function that returns a string to how much weight to load on a barbell
    :param weight: int
    :return: str
    """
    if weight == 45:
        return "Just the barbell."

    total_weight = BAR_WEIGHT
    plate_cache = []  # to cache the plates we put on the barbell
    for plate in WEIGHT_PLATES:
        while True:  # keep adding to the barbell til it's over
            total_weight += plate * 2  # each side has one plate
            if total_weight > weight:
                total_weight -= plate * 2  # revert back to original weight since we went over
                break
            plate_cache.append(plate)
            plate_cache.append(plate)
            if total_weight == weight:
                break
            if total_weight < weight:
                print(f"total weight: f{total_weight} vs. weight: {weight}")
                continue

    # convert our plate_cache into readable text
    return ""
