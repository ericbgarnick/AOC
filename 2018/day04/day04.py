import re
from datetime import datetime
from sys import argv
from typing import List, Tuple, Dict


def schedule_finder(observations: List[str], part_num: int):
    guard_schedule = {}     # {<guard_id>: {'sleep_total': <sleep total>,
    #                                       'asleep_minutes': [count of asleeps for each minute in an hour}}
    ordered_events = order_observations(observations)

    sleep_start = -1
    current_guard = -1
    sleepiest_guard = {'guard_id': -1, 'sleep_total': 0}

    for timestamp, event in ordered_events:
        if event.startswith('Guard'):
            current_guard = int(re.search(r'\d+', event).group())
            if current_guard not in guard_schedule:
                add_guard(guard_schedule, current_guard)
        else:
            minute = timestamp.minute
            if event.startswith('falls'):
                sleep_start = minute
            elif event.startswith('wakes'):
                sleep_duration = minute - sleep_start
                # Update sleep total
                sleep_total = (guard_schedule[current_guard]['sleep_total'] +
                               sleep_duration)
                guard_schedule[current_guard]['sleep_total'] = sleep_total
                # Update asleep minutes
                for minute_idx in range(sleep_start, minute):
                    guard_schedule[current_guard]['asleep_minutes'][minute_idx] += 1

                if sleep_total > sleepiest_guard['sleep_total']:
                    sleepiest_guard = {'guard_id': current_guard,
                                       'sleep_total': sleep_total}

    if part_num == 1:
        sleepiest_guard_info = guard_schedule[sleepiest_guard['guard_id']]
        best_minute = sleepiest_minute(sleepiest_guard_info['asleep_minutes'])
        print("Result: {}".format(sleepiest_guard['guard_id'] * best_minute))
    elif part_num == 2:
        best_guard = most_asleep_guard_minute(guard_schedule)
        sleepiest_guard_info = guard_schedule[best_guard]
        best_minute = sleepiest_minute(sleepiest_guard_info['asleep_minutes'])
        print("Result: {}".format(best_guard * best_minute))


def order_observations(observations: List[str]) -> List[Tuple[datetime, str]]:
    events = []
    for entry in observations:
        timestring = re.search(r'\[.+\]', entry).group().strip('[]')
        timestamp = datetime.strptime(timestring, '%Y-%m-%d %H:%M')
        event = entry.split(' ', maxsplit=2)[-1]
        events.append((timestamp, event))
    return sorted(events)


def add_guard(guard_schedule: Dict[int, Dict], current_guard: int):
    minute_list = [0 for _ in range(60)]
    guard_schedule[current_guard] = {'sleep_total': 0,
                                     'asleep_minutes': minute_list}


def sleepiest_minute(asleep_minutes: List[int]) -> int:
    return asleep_minutes.index(max(asleep_minutes))


def most_asleep_guard_minute(guard_schedule: Dict[int, Dict]) -> int:
    best_guard_minute = {'guard_id': -1, 'minutes_asleep': 0}
    for guard_id, guard_info in guard_schedule.items():
        max_sleep = max(guard_info['asleep_minutes'])
        if max_sleep > best_guard_minute['minutes_asleep']:
            best_guard_minute = {'guard_id': guard_id,
                                 'minutes_asleep': max_sleep}
    return best_guard_minute['guard_id']


if __name__ == '__main__':
    data_file = argv[1]
    data_lines = [l.strip() for l in open(data_file, 'r').readlines()]
    part = int(argv[2])

    schedule_finder(data_lines, part)
