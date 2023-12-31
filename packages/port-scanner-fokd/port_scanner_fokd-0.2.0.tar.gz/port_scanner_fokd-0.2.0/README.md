# Simple port scanner

"Scan" function type signature:

```
def scan(target: str, start=0, stop=1023, threads=500) -> List[int]:
```

By default you only need to enter a target IP address and it will scan the most frequently used ports/system ports, using 500 threads (be patient 🫣).

Installation:

```
>pip install port-scanner-fokd==0.1.0
```

Usage:

```
scanner = port-scanner-fokd.Scanner()
scanner.scan("127.0.0.1")

>> [22, 80, 443]
```
