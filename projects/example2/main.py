from src.test_class import TestClass
from time import sleep

T = TestClass("LED")
T.blink(5)
sleep(2)
T.blink(10)

