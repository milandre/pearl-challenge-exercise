import heapq
import os
import sys

NEIGHBORHOOD_LINE = "N"
HOME_BUYER_LINE = "H"
PEARL_VALUE_SPLIT_SYMBOL = ":"
PRIORITIES_SPLIT_SYMBOL = ">"


def write_output_file(
    filename: str, assignments: dict[int, list[tuple[int, int]]]
) -> None:
    """
    Write the assignments to an output file in a specific format.

    Parameters:
        filename (str): The name of the output file.
        assignments (dict[int, list[tuple[int, int]]]): A dictionary containing neighborhood assignments for home buyers.

    Returns:
        None
    """
    with open(filename, "w") as f:
        for neighborhood, home_buyers in sorted(assignments.items()):
            home_buyers_assignments: str = " ".join(
                f"{HOME_BUYER_LINE}{home_buyer}({fit_score})"
                for fit_score, home_buyer in sorted(
                    home_buyers, key=lambda elem: -elem[0]
                )
            )
            f.write(f"{NEIGHBORHOOD_LINE}{neighborhood}: {home_buyers_assignments}\n")


def get_valid_priority(
    priorities,
    home_buyers,
    home_buyer_number,
    neighborhoods,
    assignments,
    neighborhood_capacity,
) -> int:
    """
    Return a valid priority based on fit score and neighborhood capacity.

    Args:
        priorities (list): List of priorities to choose from.
        home_buyers (list): List of home buyers.
        home_buyer_number (int): Index of the current home buyer.
        neighborhoods (dict): Dictionary containing neighborhoods information.
        assignments (dict): Dictionary containing assignments for each priority.
        neighborhood_capacity (int): Maximum capacity for a neighborhood.

    Returns:
        int: A valid priority based on the given conditions.
    """
    for priority in priorities:
        if len(assignments[priority]) < neighborhood_capacity:
            return priority
        else:
            (min_fit_score_from_neighborhood, _) = min(
                assignments[priority], key=lambda elem: elem[0]
            )
            fit_score = dot_product(
                home_buyers[home_buyer_number],
                neighborhoods[priority],
            )
            if fit_score > min_fit_score_from_neighborhood:
                return priority

    return priorities[0]


def assign_or_swap_positions(
    home_buyers,
    neighborhoods,
    fit_scores,
    fit_score,
    home_buyer_number,
    neighborhood_number,
    assigned,
    priorities,
    assignments,
    neighborhood_capacity,
) -> tuple:
    """
    Assign or swap positions between home buyers and neighborhoods based on fit scores.

    Args:
        home_buyers (list): List of home buyer vectors.
        neighborhoods (list): List of neighborhood vectors.
        fit_scores (list): List of fit scores for each home buyer.
        fit_score (int): The fit score to compare with.
        home_buyer_number (int): The number representing the home buyer.
        neighborhood_number (int): The number representing the neighborhood.
        assigned (list): List of assigned pairs of neighborhood and home buyer numbers.
        priorities (list): List of priorities for each home buyer.
        assignments (dict): Dictionary containing assignments for each neighborhood.
        neighborhood_capacity (int): Maximum capacity for a neighborhood.

    Returns:
        tuple: Updated fit scores, assignments, and assigned pairs after potential swaps.
    """
    if home_buyer_number not in assigned:
        if len(assignments[neighborhood_number]) < neighborhood_capacity:
            assignments[neighborhood_number].append((-fit_score, home_buyer_number))
            assigned.append(home_buyer_number)
        else:
            # Swapping if current fit_score is better than the minimum in the neighborhood
            (
                min_fit_score_from_neighborhood,
                min_home_buyer_number,
            ) = min(assignments[neighborhood_number], key=lambda elem: elem[0])
            if -fit_score > min_fit_score_from_neighborhood:
                # Swap out the one with the lowest fit score
                assignments[neighborhood_number].remove(
                    (
                        min_fit_score_from_neighborhood,
                        min_home_buyer_number,
                    )
                )
                assigned.remove(min_home_buyer_number)

                assignments[neighborhood_number].append((-fit_score, home_buyer_number))
                assigned.append(home_buyer_number)

                # Reassign the displaced home buyer
                displaced_home_buyer_number = min_home_buyer_number
                valid_priority = get_valid_priority(
                    priorities[displaced_home_buyer_number],
                    home_buyers,
                    displaced_home_buyer_number,
                    neighborhoods,
                    assignments,
                    neighborhood_capacity,
                )
                displaced_fit_score = dot_product(
                    home_buyers[displaced_home_buyer_number],
                    neighborhoods[valid_priority],
                )
                heapq.heappush(
                    fit_scores,
                    (
                        -displaced_fit_score,
                        valid_priority,
                        displaced_home_buyer_number,
                    ),
                )
    return fit_scores, assignments, assigned


def get_best_fit_score(
    fit_score, best_fit_scores, home_buyer_number
) -> tuple[int, list[tuple[int, int]]]:
    """
    Return the best fit score and updated list of best fit scores after removing
    the score corresponding to a specific home buyer number if it exists.

    Parameters:
    fit_score (int): The fit score to be returned.
    best_fit_scores (list[tuple[int, int]]): A list of tuples containing fit scores and home buyer numbers.
    home_buyer_number (int): The home buyer number to check and remove from the list if present.

    Returns:
    tuple[int, list[tuple[int, int]]]: A tuple containing the best fit score and the updated list of best fit scores.
    """
    if len(best_fit_scores) > 0 and home_buyer_number in [
        elem[1] for elem in best_fit_scores
    ]:
        fit_score, _ = [
            elem for elem in best_fit_scores if home_buyer_number == elem[1]
        ][0]
        best_fit_scores.remove((fit_score, home_buyer_number))
    return fit_score, best_fit_scores


def dot_product(home_buyer_vector: list, neighborhood_vector: list) -> int:
    """
    Calculate the dot product of two vectors.

    Args:
        home_buyer_vector (list): A list representing the vector of the home buyer.
        neighborhood_vector (list): A list representing the vector of the neighborhood.

    Returns:
        int: The dot product of the two input vectors.
    """
    return sum([i * j for (i, j) in zip(home_buyer_vector, neighborhood_vector)])


def home_buyers_to_neighborhoods(home_buyers, neighborhoods, priorities) -> dict:
    """
    Assign home buyers to neighborhoods based on fit scores and priorities.

    Args:
        home_buyers (list): List of home buyer vectors.
        neighborhoods (list): List of neighborhood vectors.
        priorities (list): List of priorities for each home buyer.

    Returns:
        dict: A dictionary containing the assignments of home buyers to neighborhoods.
    """
    assignments = {neighborhood_id: [] for neighborhood_id in range(len(neighborhoods))}
    # Assumption: Neighborhood capacity will be always even as described in the PDF
    neighborhood_capacity: int = len(home_buyers) // len(neighborhoods)

    # Calculate fit scores
    fit_scores = []
    for h_num, home_buyer_vector in enumerate(home_buyers):
        for n_num, neighborhood_vector in enumerate(neighborhoods):
            fit_score: int = dot_product(home_buyer_vector, neighborhood_vector)
            # The heapq module's priority heap implementation operates as a Min-Heap.
            # The fit_score is negated to ensure the proper ordering of elements as expected.
            fit_scores.append((-fit_score, n_num, h_num))

    # Convert to a priority heap
    heapq.heapify(fit_scores)

    # Assign home buyers

    # The best_fit_scores array will keep the information updated
    # about the fit_score calculation of a homeowner when trying
    # to add it to their preferred neighborhood, taking into account
    # the priorities of the homeowner and their neighbors.
    best_fit_scores: list = []
    # The assigned list will contain the information of the home buyers
    # already assigned to a neighborhood to avoid assigning them to the
    # same neighborhood or another one at the same time.
    assigned = []
    while len(fit_scores) > 0:
        # Get the smallest element of the heap
        fit_score, neighborhood_number, home_buyer_number = heapq.heappop(fit_scores)
        # Get the home buyers priorities
        home_buyer_priorities = priorities[home_buyer_number]

        # Get the best fit score for the home buyer and
        # update the best_fit_scores list
        fit_score, best_fit_scores = get_best_fit_score(
            fit_score, best_fit_scores, home_buyer_number
        )

        # If everything is fine with the neighborhood according
        # to the homeowner's priority, it evaluates whether
        # it needs to be swapped with another or just assigned to their
        # best neighborhood of preference.
        if home_buyer_priorities[0] == neighborhood_number:
            fit_scores, assignments, assigned = assign_or_swap_positions(
                home_buyers,
                neighborhoods,
                fit_scores,
                fit_score,
                home_buyer_number,
                neighborhood_number,
                assigned,
                priorities,
                assignments,
                neighborhood_capacity,
            )
        # If not, calculate the best neighborhood for the home buyer,
        # with the respective fit_score and save the result
        # to best_fit_scores.
        else:
            valid_priority = get_valid_priority(
                priorities[home_buyer_number],
                home_buyers,
                home_buyer_number,
                neighborhoods,
                assignments,
                neighborhood_capacity,
            )
            displaced_fit_score = dot_product(
                home_buyers[home_buyer_number],
                neighborhoods[valid_priority],
            )

            # If the new calculated neighborhood (valid_priority)
            # is distinct to the previous one and the home owner
            # is not assigned yet to a neighborhood, update the
            # best_fit_scores with the new fit_score calculated
            # for the home buyer and add the information to
            # to the heap.
            if (
                neighborhood_number != valid_priority
                and home_buyer_number not in assigned
            ):
                best_fit_scores.append((-displaced_fit_score, home_buyer_number))
                heapq.heappush(
                    fit_scores,
                    (
                        (
                            fit_score
                            if fit_score <= -displaced_fit_score
                            else -displaced_fit_score
                        ),
                        valid_priority,
                        home_buyer_number,
                    ),
                )
            else:
                # If the new calculated neighborhood is the same as the previous one or
                # the home buyer is already assigned, check if the home owner needs to
                # be swap with another one or just assigned to their best neighborhood option.
                fit_scores, assignments, assigned = assign_or_swap_positions(
                    home_buyers,
                    neighborhoods,
                    fit_scores,
                    -displaced_fit_score,
                    home_buyer_number,
                    neighborhood_number,
                    assigned,
                    priorities,
                    assignments,
                    neighborhood_capacity,
                )

    return assignments


def read_input_file(path: str) -> tuple[list, list, list]:
    """
    Reads an input file with a specific structure to extract information
    about neighborhoods and home owners.

    Returns lists of home buyers, neighborhoods, and priorities extracted from the file.
    """
    home_buyers: list[list[int]] = []
    neighborhoods: list[list[int]] = []
    priorities: list[list[int]] = []

    with open(path, "r") as file:
        # Assumption: Each input file is valid and has the structure described in the PDF.
        for line in file:
            parts: list[str] = line.strip().split()
            if len(parts) > 0:
                # If the line is neighborhood information, then add the vector values to the neighborhood array.
                if parts[0] == NEIGHBORHOOD_LINE:
                    neighborhood_vector_values: list[int] = [
                        int(pearl_value.split(PEARL_VALUE_SPLIT_SYMBOL)[1])
                        for pearl_value in parts[2:]
                    ]
                    neighborhoods.append(neighborhood_vector_values)
                # If the line is a home buyer information, add goals vector values to the homeowner's array and extract priorities too.
                elif parts[0] == HOME_BUYER_LINE:
                    goals_vector_values: list[int] = [
                        int(pearl_value.split(PEARL_VALUE_SPLIT_SYMBOL)[1])
                        for pearl_value in parts[2:-1]
                    ]
                    priorities_values: list[int] = list(
                        map(
                            lambda elem: int(elem[1]),
                            parts[-1].split(PRIORITIES_SPLIT_SYMBOL),
                        )
                    )
                    home_buyers.append(goals_vector_values)
                    priorities.append(priorities_values)

    return home_buyers, neighborhoods, priorities


def main(input_file_path: str, output_file_path: str) -> None:
    """
    Executes the main process by reading input data from the specified file,
    assigning home buyers to neighborhoods based on fit scores and priorities,
    and writing the assignments to an output file.

    Parameters:
        input_file_path (str): The path to the input file containing information about neighborhoods and home owners.
        output_file_path (str): The path to the output file where the assignments will be written.

    Returns:
        None
    """
    home_buyers, neighborhoods, priorities = read_input_file(input_file_path)
    assignments: dict[int, list[tuple[int, int]]] = home_buyers_to_neighborhoods(
        home_buyers, neighborhoods, priorities
    )
    write_output_file(output_file_path, assignments)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 app/main.py <input_file_path> <output_file_path>")
        sys.exit(1)

    # If the file path are directories, exit the program
    if os.path.isdir(sys.argv[1]) or os.path.isdir(sys.argv[2]):
        print("The inputs should be file path. Please verify and try again")
        sys.exit(1)

    # Verify if input file exists. If not, exit the program
    if not os.path.exists(sys.argv[1]):
        print(
            "Input file not found. Please verify that already exists in the specific path"
        )
        sys.exit(1)

    main(sys.argv[1], sys.argv[2])
