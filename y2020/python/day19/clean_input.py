from sys import argv


def order_rules(filename: str):
    raw_rules, raw_messages = open(filename, "r").read().split("\n\n")
    ordered_rules = sorted(raw_rules.split("\n"), key=lambda m: int(m.split(":")[0]))
    with open(filename, "w") as f_out:
        written = f_out.write("\n".join(ordered_rules) + "\n\n" + raw_messages)


if __name__ == "__main__":
    order_rules(argv[1])
