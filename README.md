# PPMS_dat_scraber
It finds dependencies and saves their to .csv and .png

Для работы с проектом необходимо выполнить следующие действия:

Клонировать репозиторий.

Активировать виртуальное окружение venv/bin/activate

Установить зависимости pip install -r requirements.txt

В папку /data вставить все .dat файлы от PPMS
Открыть .dat файл любым текстовым редактором и внести изменения согласто шаблону (формулу вещества или массы и диамагнитную поправку) в следующие поля header:

    [Header]
    ; ACMS Data File (default extension .dat)
    ; Copyright 1999, Quantum Design, Inc. All rights reserved.
    TITLE,filename ms = 0.0780 mb = 0.0166 moil = 0.0443
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
    INFO,,
    INFO,,
    DATATYPE,COMMENT,1
    DATATYPE,TIME,2
    FIELDGROUP,AC Mag,2,3,4,5,6,8,9,10,11,12
    FIELDGROUP,DC Mag,2,3,4,7,8
    STARTUPGROUP,All
    STARTUPAXIS,X,2,LINEAR,AUTO
    TIMEMODE,MINUTES,RELATIVE
    PLOT_APPEARANCE,ALL,HORZ_GRID_ON,VERT_GRID_ON,MARKERS_AND_LINES
    RECORDS,ALL_RECORDS
    DATATYPE,TIME,2
    DATATYPE,COMMENT,1
    [Data]



Запустить скрипт .main.py
