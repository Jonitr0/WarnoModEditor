# cache that is emptied when a file is changed

cache_dict = {}


def clear_caches_for_file(file_name: str):
    try:
        for cache in cache_dict[file_name]:
            cache.clear()
    except KeyError:
        return


class SmartCache:
    def __init__(self, file_name: str):
        self.file_name = file_name
        self._data = {}

        try:
            cache_dict[file_name].append(self)
        except KeyError:
            cache_dict[file_name] = [self]

    def set(self, key, val):
        self._data[key] = val

    def get(self, key, default = None):
        try:
            return self._data[key]
        except KeyError:
            return default
    
    def contains(self, key):
        return self._data.__contains__(key)

    def clear(self):
        self._data = {}

    def __del__(self):
        cache_dict[self.file_name].remove(self)
