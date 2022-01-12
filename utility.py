from typing import List

# All weights are in lbs

WEIGHT_PLATES = [45, 35, 25, 10, 5]  # We are skipping 2.5 lbs and 55 lbs plates as they are scarce
WEIGHT_PLATES_TO_STR = {
    45: "plate",
    35: "35",
    25: "25",
    10: "10",
    5: "5",
}
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
        ret_list.append(percent(weight, i))  # some jank math, but // 1 to remove decimal number

    return ret_list


def percent(weight, percentage):
    return (weight * (percentage / 100)) // 1


def weight_to_plates(weight) -> str:
    """
    A function that returns a string to how much weight to load on a barbell
    :param weight: int
    :return: str
    """
    if 45 <= weight <= 54:
        return "Just the barbell."

    total_weight = BAR_WEIGHT
    plate_cache = []  # to cache the plates we put on the barbell
    for plate in WEIGHT_PLATES:
        while True:  # keep adding to the barbell til it's over our goal weight
            total_weight += plate * 2  # each side has one plate
            if total_weight > weight:
                # if the weight is over the weight given by 1 or 2 then we can keep it
                if total_weight - weight == 2 or total_weight - weight == 1:
                    plate_cache.append(plate)
                    plate_cache.append(plate)
                    break
                total_weight -= plate * 2  # revert back to original weight since we went over
                break
            plate_cache.append(plate)
            plate_cache.append(plate)
            if total_weight == weight:
                break
            if weight - total_weight < 10:
                break

    # convert our plate_cache into readable text
    plates_used = list(set(plate_cache))
    plates_used.sort(reverse=True)
    readable_weight = ""

    for i, plate in enumerate(plates_used):
        plate_count = int(plate_cache.count(plate) / 2)
        plate_str = plural(WEIGHT_PLATES_TO_STR.get(plate), plate_count)
        if i == len(plates_used) - 1 and len(plates_used) != 1:
            readable_weight += "and "
        readable_weight += f"{plate_count if plate_count > 1 else 'a'} {plate_str}, "

    return readable_weight + f"total weight of barbell: {total_weight} lbs"


def plural(text, num) -> str:
    if num <= 1:
        return text
    return text + "s"
