import os 
import sys

def anakiner(times):
    for i in range(times):
        print(f"I am your father {i+1}")

if __name__ == "__main__":
    times = int(sys.argv[1])
    anakiner(times)