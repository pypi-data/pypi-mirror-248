import os 
import sys

def leiar(times):
    for i in range(times):
        print(f"I am a Princess {i+1}")

if __name__ == "__main__":
    times = int(sys.argv[1])
    leiar(times)