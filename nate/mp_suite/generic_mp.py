from joblib import Parallel, delayed
# from toolz import partition_all
from itertools import chain
from spacy.util import minibatch
from functools import partial
# from spacy.pipeline import merge_entities


def mp(items, function, cpu, *args):
    batch_size = round(len(items)/cpu)
    partitions = minibatch(items, size=batch_size)
    executor = Parallel(n_jobs=cpu, backend="multiprocessing", prefer="processes")
    do = delayed(partial(function, *args))
    tasks = (do(batch) for batch in partitions)
    temp = executor(tasks)
    if isinstance(temp[0], dict):
        results = {}
        for batch in temp:
            for key, value in batch.items():
                results.setdefault(key, []).extend(value)
    elif isinstance(temp[0], (list, tuple)):
        results = list(chain(*temp))

    return results


#####
#
# Old generic MP:
#
#####

# def mp(items, function, cpu, *args):
#     """
#     This is a docstring.
#     """
#     batch_size = round(len(items)/cpu)
#     partitions = partition_all(batch_size, items)
#     temp = Parallel(n_jobs=cpu, max_nbytes=None)(delayed(function)(v, *args) for v in partitions)
#     if isinstance(temp[0], dict):
#         results = {}
#         for batch in temp:
#             for key, value in batch.items():
#                 results.setdefault(key, []).extend(value)
#     elif isinstance(temp[0], (list, tuple)):
#         results = list(chain(*temp))
#     return results