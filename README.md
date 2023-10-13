## Instructions 


1.  Download Chrome
2.  Setup json like following example
___

```json
            {
                "1": [
                    "uname1",
                    "pw1"
                ],
                "2": [
                    "uname2",
                    "pw2"
                ],
                "3": [
                    "uame3",
                    "pw3"
                ]
            }
```
3. Run SendGruesseWithJSON.py in Terminal/PowerShell/CMD (see Examples below)
___

### Requirements

Build with Python 3.11 + modules in requirements.txt

___

### Examples

python SendGruesseWithJSON.py -c 1 -t 2 (uname1 zu uname2)

python SendGruesseWithJSON.py -c 2 -t 1 (uname2 zu uname1)

python SendGruesseWithJSON.py -c 3 -t 0 (uname3 zu uname0)

