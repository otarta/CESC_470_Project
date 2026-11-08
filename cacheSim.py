
from collections import OrderedDict


class Cache:
    def __init__(self, cache_size, block_size, associativity, name):
        self.cache_size = cache_size
        self.block_size = block_size
        self.associativity = associativity
        self.name = name

        self.num_lines = cache_size // block_size
        self.num_sets = self.num_lines // associativity

        self.sets = [OrderedDict() for _ in range(self.num_sets)]

        self.hits = 0
        self.misses = 0

    def access(self, address):
        block_number = address // self.block_size

        set_index = block_number % self.num_sets
        tag = block_number // self.num_sets

        cache_set = self.sets[set_index]

        if tag in cache_set:
            self.hits += 1
            cache_set.move_to_end(tag)

        else:
            self.misses += 1

            if len(cache_set) >= self.associativity:
                cache_set.popitem(last=False)

            cache_set[tag] = True

    def get_results(self):
        total = self.hits + self.misses

        hit_rate = (self.hits / total) * 100 if total else 0
        miss_rate = (self.misses / total) * 100 if total else 0

        return {
            "name": self.name,
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": hit_rate,
            "miss_rate": miss_rate
        }


def print_results(results):
    print("\nCACHE PERFORMANCE COMPARISON")
    print("-" * 75)

    print(f"{'Cache Type':<22} {'Hits':<10} "
          f"{'Misses':<10} {'Hit Rate':<12} {'Miss Rate':<12}")

    print("-" * 75)

    for result in results:
        print(
            f"{result['name']:<22}"
            f"{result['hits']:<10}"
            f"{result['misses']:<10}"
            f"{result['hit_rate']:<12.2f}"
            f"{result['miss_rate']:<12.2f}"
        )

    print("-" * 75)


def main():
    CACHE_SIZE = 256
    BLOCK_SIZE = 16

    mem_addr = [
        0x000, 0x100, 0x200, 0x300,
        0x000, 0x100, 0x400, 0x500,
        0x000, 0x100, 0x200, 0x300,
        0x010, 0x020, 0x030, 0x040,
        0x000, 0x100, 0x200, 0x300,
        0x010, 0x020, 0x030, 0x040
    ]

    caches = [
        Cache(CACHE_SIZE, BLOCK_SIZE, 1, "Direct-Mapped"),
        Cache(CACHE_SIZE, BLOCK_SIZE, 4, "4-Way Set-Assoc."),
        Cache(CACHE_SIZE, BLOCK_SIZE,
              CACHE_SIZE // BLOCK_SIZE, "Fully Associative")
    ]

    for address in mem_addr:
        for cache in caches:
            cache.access(address)

    results = [cache.get_results() for cache in caches]

    print(f"Cache Size: {CACHE_SIZE} bytes")
    print(f"Block Size: {BLOCK_SIZE} bytes")
    print(f"Total Memory Accesses: {len(mem_addr)}")

    print_results(results)


if __name__ == "__main__":
    main()
