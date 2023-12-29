set ARF=%PYTHONPATH%\adabas\arf
python %ARF%\inq.py --trace 4 --service IN4 --rnam OUT4 --token EMPLTEL --inam IEMPLAA --dbid 8 --fnr 11  --value 2001100020019999 --broker daey:3800 -u EMPLUSER
