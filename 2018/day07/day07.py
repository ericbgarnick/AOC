import re
from collections import deque
from sys import argv
from typing import List, Dict, Set, Tuple, Optional


class Elf:
    def __init__(self, elf_id: int, base_time: int):
        self.elf_id = elf_id
        self.base_time = base_time
        self.current_step = None
        self.finished_steps = []
        self.time_remaining = 0

    def __repr__(self):
        return "{} @ {}/{} -> {}".format(self.current_step,
                                         self.time_remaining,
                                         self.base_time,
                                         ''.join(self.finished_steps))

    def assign_step(self, step: str):
        self.current_step = step
        self.time_remaining = ord(step) - 64 + self.base_time

    def complete_step(self) -> Tuple[str, int]:
        finished = self.current_step
        time_taken = self.time_remaining
        self.finished_steps.append(finished)
        self.current_step = None
        self.time_remaining = 0
        return finished, time_taken

    def elapse(self, duration: int):
        self.time_remaining -= duration


def comprehend_instructions(step_list: List[str], part_num: int,
                            num_elves: int=5, base_time: int=60):
    dependencies = _determine_dependencies(step_list)
    new_ready = {let for let, deps in dependencies.items()
                 if not deps['requires']}
    ready = deque(sorted(new_ready))

    if part_num == 1:

        all_finished = []
        while len(all_finished) < len(dependencies):
            all_finished.append(ready.popleft())

            new_ready = (set(ready) |
                         _find_new_ready(dependencies,
                                         all_finished,
                                         ready))
            ready = deque(sorted(new_ready))

        print("ORDERED STEPS:", ''.join(all_finished))

    elif part_num == 2:
        free_elves = deque([Elf(i, base_time) for i in range(num_elves)])
        busy_elves = deque()
        in_progress = set()
        all_finished = []
        total_time = 0

        while len(all_finished) < len(dependencies):

            while len(free_elves) and len(ready):
                # Assign steps to free elves
                cur_elf = free_elves.popleft()
                next_step = ready.popleft()
                cur_elf.assign_step(next_step)
                in_progress.add(next_step)
                busy_elves.append(cur_elf)

            # Find next elf closest to finishing and finish its work
            busy_elves = deque(sorted(busy_elves, key=lambda elf: elf.time_remaining))
            finished_elf = busy_elves.popleft()  # type: Elf
            finished_step, time_elapsed = finished_elf.complete_step()

            # Update finished steps and elves still working
            all_finished.append(finished_step)
            total_time += time_elapsed
            for busy_elf in busy_elves:
                busy_elf.elapse(time_elapsed)

            # Move finished elf back to free and order by elf id
            free_elves.append(finished_elf)
            free_elves = deque(sorted(free_elves, key=lambda elf: elf.elf_id))

            new_ready = (set(ready) |
                         _find_new_ready(dependencies,
                                         all_finished,
                                         ready, in_progress))
            ready = deque(sorted(new_ready))

        print("TOTAL TIME:", total_time)


def _find_new_ready(dependencies: Dict, all_finished: List[str], ready: deque,
                    in_progress: Optional[Set[str]]=None) -> Set[str]:
    finished_set = set(all_finished)
    in_progress = in_progress or set()
    seen = set(ready) | finished_set | in_progress
    return {let for let, deps in dependencies.items()
            if (not deps['requires'] - finished_set)
            and (let not in seen)}


def _determine_dependencies(steps: List[str]) -> Dict:
    dependencies = {}
    for step in steps:
        required, dependent = re.findall(r' ([A-Z]) ', step)
        # Set permittance relationship
        try:
            dependencies[required]['permits'].add(dependent)
        except KeyError:
            dependencies[required] = {'permits': {dependent},
                                      'requires': set()}
        # Set requirement relationship
        try:
            dependencies[dependent]['requires'].add(required)
        except KeyError:
            dependencies[dependent] = {'requires': {required},
                                       'permits': set()}
    return dependencies


if __name__ == '__main__':
    data_file = argv[1]
    data_lines = [l.strip() for l in open(data_file, 'r').readlines()]
    part = int(argv[2])
    kwargs = {'step_list': data_lines, 'part_num': part}
    if len(argv) > 3:
        kwargs['num_elves'] = int(argv[3])
    if len(argv) > 4:
        kwargs['base_time'] = int(argv[4])

    comprehend_instructions(**kwargs)
