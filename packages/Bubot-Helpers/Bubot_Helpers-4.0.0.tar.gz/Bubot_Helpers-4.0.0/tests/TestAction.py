import unittest
from Bubot.Helpers.Action import Action
import time


class TestAction(unittest.TestCase):
    def test_action(self):
        res = 1
        a1 = Action('a1', group='1')
        b1 = Action('b1', group='1')
        a2 = Action('a2', group='2')
        b2 = Action('b2', group='2')
        time.sleep(0.2)
        res += a2.add_stat(b2.set_end(res))
        time.sleep(0.2)
        res += b1.add_stat(a2.set_end(res))
        time.sleep(0.2)
        res += a1.add_stat(b1.set_end(res))
        time.sleep(0.2)
        a1.set_end(res)
        self.assertEqual(8, a1.result)
        self.assertEqual(2, len(list(a1.stat.keys())))
        self.assertEqual(2, len(list(a1.stat['2'].keys())))
        self.assertEqual(2, len(list(a1.stat['1'].keys())))
        pass

