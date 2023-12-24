# Simple port scanner

"Scan" function type signature:

```
def scan(target: str, start=0, stop=1023, threads=500) -> List[int]:
```

By default you only need to enter a target IP address and it will scan the 1000 most frequently used ports/system ports.

Installation:

```
pip install port-scanner-fokd==0.1.0
```
