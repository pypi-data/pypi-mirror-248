from dataclasses import dataclass
from inspect import ismethod, isbuiltin
from typing import Iterable, Any, Optional

import cloudpickle
from returns.result import safe, Failure, Result
from tabulate import tabulate

from pinjected.di.proxiable import DelegatedVar


def rec_valmap(f, tgt: dict):
    res = dict()
    for k, v in tgt.items():
        if isinstance(v, dict):
            res[k] = rec_valmap(f, v)
        else:
            res[k] = f(v)
    return res


def rec_val_filter(f, tgt: dict):
    res = dict()
    for k, v in tgt.items():
        if isinstance(v, dict):
            res[k] = rec_val_filter(f, v)
        elif f(v):
            res[k] = v
    return res


def rec_as_dict(tgt, trace="root"):
    print(f"converting item to dict. {trace}")
    res = dict()
    for k in dir(tgt):
        if not k.startswith("__"):
            attr = getattr(tgt, k)
            if not ismethod(attr):
                res[k] = rec_as_dict(attr, trace + f".{k}")
    return res


@dataclass
class PicklingFailure:
    trace: str
    pkl: Result
    value: Any

    def truncated_tuple(self, n: int = 100):
        return self.trace, self.pkl, str(self.value)[:n]


def dfs_picklability(tgt, trace="root", dumps=cloudpickle.dumps) -> Iterable[PicklingFailure]:
    visited = set()
    safe_pickle = safe(dumps)

    def dfs(tgt, trace):
        if len(trace) >= 1000:
            yield PicklingFailure(trace, Failure("trace too long"), tgt)
            return
        pkl = safe_pickle(tgt)
        if isinstance(pkl, Failure):
            yield PicklingFailure(trace, pkl, tgt)
            visited.add(id(tgt))

            if isinstance(tgt, dict):
                for k, v in tgt.items():
                    if id(v) not in visited:
                        visited.add(id(v))
                        yield from dfs(v, trace + f"['{k}']")
            if isinstance(tgt, DelegatedVar):
                yield from dfs(tgt.value, trace + f".value")
            elif isinstance(tgt, Iterable):
                for i, item in enumerate(tgt):
                    if id(i) not in visited:
                        visited.add(id(i))
                        yield from dfs(item, trace + f"[{i}]")
            else:
                for k in dir(tgt):
                    if not k.startswith("__") and not k == "_abc_impl":
                        attr = getattr(tgt, k)
                        if not ismethod(attr) and not isbuiltin(attr) and id(attr) not in visited:
                            new_trace = trace + f".{k}"
                            yield from dfs(attr, new_trace)
            if hasattr(tgt, "__closure__") and tgt.__closure__ is not None:
                for i, cell in enumerate(tgt.__closure__):
                    if id(cell) not in visited:
                        visited.add(id(cell))
                        yield from dfs(cell, trace + f".__closure__[{i}]")

    return dfs(tgt, trace)


def assert_picklable(tgt, message: Optional[str] = None, trace="root", dumps=cloudpickle.dumps):
    from loguru import logger
    failures = [r.truncated_tuple() for r in dfs_picklability(tgt, trace, dumps)]
    if failures:
        logger.info(f"failed to pickle target, traces:\n{tabulate(failures)}")
        raise AssertionError(f"failed to pickle target, {message} traces:\n{tabulate(failures)}")


def dig_picklability(tgt, trace="root", dumps=cloudpickle.dumps):
    from loguru import logger
    failures = [r.truncated_tuple() for r in dfs_picklability(tgt, trace, dumps)]
    if failures:
        logger.info(f"failed to pickle target, traces:\n{tabulate(failures)}")
