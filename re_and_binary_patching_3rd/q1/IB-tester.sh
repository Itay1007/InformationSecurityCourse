#/usr/bin/bash

for i in {1..9}
do
python3 q1b.py 0$i.msg
./msgcheck 0$i.msg.fixed
done


python3 q1b.py 10.msg
./msgcheck 10.msg.fixed


echo "[+] Finished test for 1b"

rm 0?.msg.fixed

for i in {1..9}
do
python3 q1c.py 0$i.msg
./msgcheck 0$i.msg.fixed
done


python3 q1c.py 10.msg
./msgcheck 10.msg.fixed

echo "[+] Finished test for 1c"


rm 0?.msg.fixed

for i in {1..9}
do
./msgcheck.patched 0$i.msg
echo $?
done


./msgcheck.patched 10.msg
echo $?
echo "[+] Finished test for 1d"


for i in {1..9}
do
./msgcheck.patched 0$i.msg
echo $?
done

./msgcheck.patched 10.msg
echo $?

echo "[+] Finished test for 1e"

