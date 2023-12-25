import multiprocessing


def run_parallel(func, arr_args, num_cores=multiprocessing.cpu_count()):
    pool = multiprocessing.Pool(num_cores)
    data = pool.map(func, arr_args)
    pool.close()
    pool.join()
    return data
