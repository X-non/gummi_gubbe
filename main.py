from pprint import pprint
from unittest import result
import demo
from parsing.parser import parse
from parsing.scanner import scanner

# while True:
#     text = input()
#     for a in scanner(text):
#         print(a)
#     try:
#         result = parse(text)
#         pprint(result, sort_dicts=True)

#     except Exception as e:
#         print("Err:", e)
demo.start()
