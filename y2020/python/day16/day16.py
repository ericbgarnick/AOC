import re
from sys import argv
from typing import Dict, List, Any


# == PART 1 == ##
def scanning_error_rate(tickets: List[List[int]], constraints: List[Dict]) -> int:
    invalid = []
    for ticket in tickets:
        invalid += all_invalid_values(ticket, constraints)
    return sum(invalid)


# == PART 2 == #
def decode_ticket(sample_tickets: List[List[int]], constraints: List[Dict]) -> List[Dict]:
    field_position_candidates = [[] for _ in range(len(constraints))]
    for position in range(len(constraints)):
        sample_values = {ticket[position] for ticket in sample_tickets}
        min_val, max_val = min(sample_values), max(sample_values)
        for constraint in constraints:
            if (min_val >= constraint["min_valid"]
                    and max_val <= constraint["max_valid"]
                    and not constraint["invalid"] & sample_values):
                field_position_candidates[position].append(constraint)
    filter_candidates(field_position_candidates)
    return [c[0] for c in field_position_candidates]


def filter_candidates(candidates_groups: List[List[Dict]]):
    """Update candidates so that each position has only 1 field definition"""
    known = set()
    while any([len(c) > 1 for c in candidates_groups]):
        for i in range(len(candidates_groups)):
            candidate_group = candidates_groups[i]
            if len(candidate_group) == 1:
                known.add(candidate_group[0]["name"])
            else:
                candidates_groups[i] = [c for c in candidate_group if c["name"] not in known]


def departure_total(ticket: List[int], ticket_definition: List[Dict[str, Any]]) -> int:
    total = 1
    for i in range(len(ticket_definition)):
        field_definition = ticket_definition[i]
        if field_definition["name"].startswith("departure"):
            total *= ticket[i]
    return total


# == SHARED == #
def parse_input(filename: str) -> Dict[str, List]:
    data_sections = ["constraints", "my_ticket", "nearby_tickets"]
    cur_section = data_sections[0]
    cur_section_num = 0
    cur_section_contents = []
    sections = {}
    for line in open(filename, "r"):
        line = line.strip()
        if not line:
            sections[cur_section] = cur_section_contents
            cur_section_num += 1
            cur_section = data_sections[cur_section_num]
            cur_section_contents = []
        else:
            if "ticket" in line:
                # Skip ticket group header line
                continue
            cur_section_contents.append(line)
    sections[cur_section] = cur_section_contents
    return sections


def parse_constraints(constraints: List[str]) -> List[Dict[str, Any]]:
    parsed_constraints = []
    for cons in constraints:
        name = cons.split(": ")[0]
        range1, range2 = re.findall(r"\d+-\d+", cons)
        range1 = tuple(int(val) for val in range1.split("-"))
        range2 = tuple(int(val) for val in range2.split("-"))
        parsed_constraints.append({
            "name": name,
            "min_valid": range1[0],
            "max_valid": range2[1],
            "invalid": set(val for val in range(range1[1] + 1, range2[0]))
        })
    return parsed_constraints


def parse_ticket(raw_ticket: str) -> List[int]:
    return [int(val) for val in raw_ticket.split(",")]


def all_invalid_values(ticket: List[int], constraints: List[Dict]) -> List[int]:
    """Return a list of values in ticket that are invalid for constraints.
    Return an empty list if all values are valid."""
    invalid_values = []
    for val in ticket:
        invalid = True
        for constraint in constraints:
            if (constraint["min_valid"] <= val <= constraint["max_valid"]
                    and val not in constraint["invalid"]):
                invalid = False
        if invalid:
            invalid_values.append(val)
    return invalid_values


if __name__ == "__main__":
    input_file = argv[1]
    parsed = parse_input(input_file)
    constraints_list = parse_constraints(parsed["constraints"])
    parsed_tickets = [parse_ticket(t) for t in parsed["nearby_tickets"]]
    print("PART 1:", scanning_error_rate(parsed_tickets, constraints_list))

    my_ticket = parse_ticket(parsed["my_ticket"][0])
    valid_tickets = [t for t in parsed_tickets if not all_invalid_values(t, constraints_list)]
    decoded_ticket = decode_ticket(valid_tickets, constraints_list)
    print("PART 2:", departure_total(my_ticket, decoded_ticket))
