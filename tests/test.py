import logging
from math import ceil
import os
from time import sleep
import unittest

from devrandomclone import DevRandom
from devrandomclone.errors import EAGAIN


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(filename)s:%(funcName)s:%(levelname)s:%(message)s')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


class TestRandom(unittest.TestCase):

    def setUp(self) -> None:
        """
        Instantiate a new environment to test the /dev/random clone
        :return: Nothing.
        """
        logger.info("Setting up environment.")
        self.files = ('entropy_avail', 'poolsize', 'random',)
        self.hash_func = 'sha1'
        self.hash_bits = 160
        for file in self.files:
            if os.path.isfile(file):
                logger.debug("Removing {}.".format(file))
                os.remove(file)
        self.random = DevRandom(os.path.join('..', 'reddit_creds.json'))

    def test_files(self) -> None:
        """
        Ensure all files (entropy_avail, poolsize, and random) have been instantiated.
        :return: Nothing.
        """
        for file in self.files:
            self.assertTrue(os.path.isfile(file), msg="File {} was not created by DevRandom's constructor".format(file))
        logger.info("All random files exist.")

    def test_fill_entropy(self) -> None:
        """
        Build up the entropy pool by making calls to reddit's API.
        :return: Nothing.
        """
        logger.info("Filling entropy pool.")
        err = 'Expected %s bits, got %s. Are you using %s hashing?'
        self.assertEqual(0, self.random.entropy_avail)
        self.assertEqual([], self.random.dev_random)
        limits = [5, 15, 3]
        expected_bits = 0
        for limit in limits:
            logger.debug("Fetching {} posts.".format(limit))
            self.random.fill_entropy_pool(reddit_limit=limit)
            expected_bits += self.hash_bits * (ceil(limit / 5))
            self.assertEqual(expected_bits, self.random.entropy_avail,
                             msg=err % (expected_bits, self.random.entropy_avail, self.hash_func,))
            sleep(2)  # To not overload Reddit API

    def test_read_random(self) -> None:
        """
        Generate entropy and empty it out by making specific reads.
        :return: Nothing.
        """
        logging.info("Filling entropy pool.")
        self.random.fill_entropy_pool(reddit_limit=25)
        sleep(2)
        logger.info("Reading from entropy pool.")
        entropy_avail = self.random.entropy_avail
        params = [(0, False,), (10, False,), (512, False,), (1, True,), (512, True,), (512, True)]
        expected_outcomes = [0, 10, None, 1, -1, -1]
        for i, args in enumerate(params):
            logger.debug("Testing entropy {} with params (bytes_request = {}, force = {})".format(entropy_avail, *args))
            try:
                output = self.random.read_random(*args)
                if self.random.entropy_avail < args[0] * 8 and not args[1]:  # Expected to not pull from entropy pool
                    self.assertEqual(None, None,
                                     msg="Reading from random should block and return None if not force and too many "
                                         "bytes are requested.")
                    continue
                elif args == (512, True,):  # Expected to remove all that remains from entropy pool.
                    self.assertGreater(len(output), 0,
                                       msg="Entropy pool should be completely empty if forced.")
                    self.assertEqual(self.random.dev_random, [],
                                     msg="Entropy pool should be completely empty if forced.")
                else:  # All other operations
                    self.assertEqual(len(output), expected_outcomes[i],
                                     msg="Proper amount of entropy was not popped from the pool.")
            except EAGAIN:
                self.assertEqual(args, (512, True,),
                                 msg="EAGAIN should only be raised when force is true and nothing can be popped from "
                                     "entropy pool.")
                self.assertEqual(self.random.entropy_avail, 0,
                                 msg="Entropy pool should be empty.")
                self.assertEqual(self.random.dev_random, [],
                                 msg="Entropy pool should be empty.")
            new_entropy = entropy_avail - args[0] * 8
            new_entropy = new_entropy if new_entropy > 0 else 0
            self.assertEqual(new_entropy, self.random.entropy_avail,
                             msg="Entropy available is wrong (remember, it tracks bits, not bytes)")
            entropy_avail = new_entropy


if __name__ == '__main__':
    TestRandom()
