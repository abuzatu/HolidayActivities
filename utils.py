import sys
import numpy as np
import logging
import copy
import functools
import time

VAL_FREE = 0
VAL_ACTIVITY = 1

def timing(f):
    """Print the timing for the function"""
    # create a decorator as a wrapper so that before the function call we get the time
    # after the function call we get the new time, so compute the elapsed time, and print it
    # also print out the result if the permutation is possible or not and the two words
    @functools.wraps(f) # preserves information about the original function
    def wrapper(*args, **kwargs):
        start = time.time()
        result = f(*args, **kwargs)
        end = time.time()
        logging.info(f"Result of {int(result)} for function { f.__name__}() in elapsed time {end - start:.3f} seconds.")
        return result
    # done inner function
    return wrapper
# done functionx

def get_list_tuple_a(list_line):
    counter = 0
    list_tuple_a = []
    for line in list_line:
        # print(line, end="")
        counter += 1
        if counter == 1:
            # first line
            N = int(line)
        else:
            # regular line with 2 elements
            t1, t2 = (int(t) for t in line.rstrip().split(" "))
            if t1 == 24:
                t1 == 0
            if t1 < 0 or t1 > 24:
                continue
                logging.warning(f"t1={t1} is not allowed, will skip this activity")
            if t2 < 0 or t2 > 24:
                continue
                logging.warning(f"t2={t2} is not allowed as negative or > 24, will skip this activity")
            if t2 == t1:
                continue
                logging.warning(f"t1={t2} is not allowed, will skip this activity")
            elif t2 > t1:
                list_tuple_a.append(((t1, t2), ))
            else:
                # means t2 < t1
                logging.warning(f"t2<t1 since {t2}<{t1}. This activity  goes overnight into a second day, split into two events, add extra work for this edge case.")
                list_tuple_a.append(((t1, 24), (0, t2))) # the second tuple to be run the following day
            
    logging.debug(f"list_tuple_a={list_tuple_a}")
    return list_tuple_a

def print_list_day(list_day):
    logging.debug("list_day:")
    for day in list_day:
        logging.debug(f"{day}")

def get_string_from_list_day(list_day):
    s = ""
    for day in list_day:
        for val in day:
            s += f"{val}"
        s += "\n"
    return s

def add_activity_to_schedule(list_day, tuple_a):
    logging.debug(f"Start add_activity_to_schedule tuple_a={tuple_a}")
    if (0 < len(tuple_a) < 3) == False:
        logging.error(f"tuple_a={tuple_a} does not have 1 or 2 elements")
        raise RuntimeError(f"tuple_a={tuple_a} does not have 1 or 2 elements")
    # process the first activity regularly
    a = tuple_a[0] 
    t1, t2 = a
    logging.debug(f"a, t1={t1}, t2={t2}")
    # this activity will need to use the hours of indices range(t1, t2)
    # check where it fits
    # loop over all the days that are currently in the list, from first to last,
    # and see if it fits, if it fits, set it there and break, if not, create a new day and set it there
    added = False
    # available = True
    j_used = -1
    for j in range(len(list_day)):
        available = True
        logging.debug(f"{list_day[j]} for day j={j}, available={available}")
        for h in range(t1, t2):
            logging.debug(f"h={h}")
            available = available and list_day[j][h] == VAL_FREE
        logging.debug(f"available={available}")
        if available:
            j_used = j
            # add to that day
            for h in range(t1, t2):
                list_day[j_used][h] = VAL_ACTIVITY
            added = True
            available = True
            break
    logging.debug(f"tuple_a={tuple_a} found match at day {j_used}, now list_day:")
    # now do the extra step if this event is made of two components, wher ethe second is the following day
    if len(tuple_a) == 1:
        return list_day
    # if here, there are two elements, so let's process the second too
    a = tuple_a[1] 
    t1, t2 = a
    logging.debug(f"a, t1={t1}, t2={t2}")
    added = False
    for j in range(j_used+1, len(list_day), 1):
        available = True
        logging.debug(f"{list_day[j]} for day j={j}, available={available}")
        for h in range(t1, t2):
            logging.debug(f"h={h}")
            available = available and list_day[j][h] == VAL_FREE
        logging.debug(f"available={available}")
        if available:
            j_used = j
            # add to that day
            for h in range(t1, t2):
                list_day[j_used][h] = VAL_ACTIVITY
            added = True
            available = True
            break

def create_schedule(list_tuple_a):
    nb_a = len(list_tuple_a)
    logging.debug(f"nb_a={nb_a}")
    if nb_a == 0:
        nb_d = 0
        list_day = []
        return list_day
    # if here, there is at least one activity
    # create a list of one day fill with all the indices of hours in that day
    # any activity can take only full hours, not dividisons of hours
    list_day = [[VAL_FREE for j in range(24)] for i in range(nb_a+2)]
    for tuple_a in list_tuple_a:
        add_activity_to_schedule(list_day, tuple_a)
        logging.debug(f"After adding tuple_a={tuple_a}:")
        # print_list_day(list_day)
    # keep only days that have at least one hour occupied
    list_day_final =[]
    for day in list_day:
        if VAL_ACTIVITY in day:
            list_day_final.append(day)
    logging.debug(f"After cleaning to keep only days with activities:")
    print_list_day(list_day_final)
    return list_day_final

@timing
def process_list_line(list_line):
    logging.info("")
    logging.info("")
    logging.info(f"**** new use case  ****")
    logging.info(f"list_line={list_line}:")
    list_tuple_a = get_list_tuple_a(list_line)
    list_day = create_schedule(list_tuple_a)
    logging.info(f"The solution, the number of days needed for all the activities, is: {len(list_day)}.")
    #logging.info(f"The schedule is as follows (row = a day; columns = an hour from the day; 1 = activity, 0 = free):\n{get_string_from_list_day(list_day)}")
    return len(list_day)
