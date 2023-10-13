##Instructions 


1.  Download Edge_Webdriver and extract into folder
2.  Setup json like following example
___
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
___
3. Currently the script exspects that model 2 and 3 are best friends.

python SendGruesseWithJSON.py -c 1 -t 2 (uname1 zu uname2)
python SendGruesseWithJSON.py -c 2 -t 1 (uname2 zu uname1)
python SendGruesseWithJSON.py -c 3 -t 0 (uname3 zu uname0)

