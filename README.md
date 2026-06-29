# PPMS_dat_scraber
## It finds dependencies from PPMS files and saves theirs to .csv and .png

### Need to begin:

- Clone the repository.

- Activate enviroment: *python -m venv venv* and *.venv/bin/activate* (windows -  *.venv\Scripts\activate.bat*)

- Meet requirements: *pip install -r requirements.txt*

- Put in the folder */data* all *.dat* files from PPMS

- Make changes in *.dat* file by any txt editor, put in INFO line formula, molecular mass and the diamagnetic coefficient in header part in according to sample: 

        [Header]
        ; ACMS Data File (default extension .dat)
        ; Copyright 1999, Quantum Design, Inc. All rights reserved.
        TITLE,YFeTaO-0,1 ms = 0.0780 mb = 0.0166 moil = 0.0443
        FILEOPENTIME,32559857.59,04/24/2026,11:56 am
        BYAPP,ACMS,1.0,1.1
        INFO,PPMS ACMS Option Version: 1.0.9 Build 14,APPNAME
        INFO,HARMONICS,1
        INFO,m_s,0.0780
        INFO,m_b,0.0166
        INFO,moil,0.0443
        INFO,formula,Y1.9Fe+3 1.05Ta0.95Hf0.1O7
        INFO,molm,529.30577
        INFO,dia,132.2
        INFO,,
        INFO,,
        ...
        [Data]
        ...
- Parsing of needed values will be performed only in following lines:

        TITLE,YFeTaO-0,1 ms = 0.0780 mb = 0.0166 moil = 0.0443
        ...
        INFO,m_s,0.0780
        INFO,m_b,0.0166
        INFO,moil,0.0443
        INFO,formula,Y1.9Fe+3 1.05Ta0.95Hf0.1O7
        INFO,molm,529.30577
        INFO,dia,132.2
        ...

- Launch it: *.\main.py* or double click on *launch.bat*
- Have fun
