import os 
import sys

def luker(times):
    for i in range(times):
        print(f"I am Luke {i+1}")

if __name__ == "__main__":
    times = int(sys.argv[1])
    luker(times)
