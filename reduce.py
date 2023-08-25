def remove_beginning_end(start_time, end_time, n=3):
    return start_time + n, end_time - n


def get_median_n_seconds(start_time, end_time, n=5):
    return start_time + (end_time - start_time) / 2 - n / 2, start_time + (end_time - start_time) / 2 + n / 2


def complex_processing(start_time, end_time):
    # start_time, end_time = remove_beginning_end(start_time, end_time)
    # start_time, end_time = get_median_five_seconds(start_time, end_time)
    # return start_time, end_time
    return start_time, end_time