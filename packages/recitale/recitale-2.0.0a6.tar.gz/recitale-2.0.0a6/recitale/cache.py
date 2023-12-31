import json
import logging
import os
import signal

from multiprocessing import Manager

from .utils import remove_superficial_options

CACHE_VERSION = 3


logger = logging.getLogger("recitale." + __name__)


class Cache:
    cache_file_path = os.path.join(os.getcwd(), ".recitale_cache")

    def __init__(self):
        if os.path.exists(os.path.join(os.getcwd(), ".recitale_cache")):
            cache = json.load(open(self.cache_file_path, "r"))
        else:
            cache = {"version": CACHE_VERSION}

        if "version" not in cache or cache["version"] != CACHE_VERSION:
            print("info: cache format as changed, prune cache")
            cache = {"version": CACHE_VERSION}

        # Make the Manager server process ignore the SIGINT (Ctrl+, aka KeyboardInterrupt exception)
        # so that it is possible to still dump the cache variable after a KeyboardInterrupt.
        old = signal.signal(signal.SIGINT, signal.SIG_IGN)
        self.cache = Manager().dict(cache)
        # Current process should handle SIGINT as it used to do before starting the Manager process.
        signal.signal(signal.SIGINT, old)

    def needs_to_be_generated(self, source, target, options):
        if not os.path.exists(target):
            logger.debug("%s does not exist. Requesting generation...", target)
            return True

        if target not in self.cache:
            logger.debug("%s not in cache. Requesting generation...", target)
            return True

        cached_picture = self.cache[target]

        if cached_picture["size"] != os.path.getsize(source):
            logger.debug(
                "%s has different size than in cache. Requesting generation...", target
            )
            return True

        options = remove_superficial_options(options)
        # json.dumps() transforms tuples into list, so to be able to compare options
        # same transformation needs to be done on runtime dict.
        options = json.loads(json.dumps(options))

        if cached_picture["options"] != options:
            logger.debug(
                "%s has different options than in cache. Requesting generation...",
                target,
            )
            return True

        logger.debug("(%s) Skipping cached thumbnail %s", source, target)
        return False

    def cache_picture(self, source, target, options):
        self.cache[target] = {
            "size": os.path.getsize(source),
            "options": remove_superficial_options(options),
        }

    def cache_dump(self):
        json.dump(dict(self.cache), open(self.cache_file_path, "w"))
