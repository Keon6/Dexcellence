#!bin/sh

for n in 2 5 10
do
  
  for i in 100 500 1000 5000
  do
    echo Number of Assets = "$n" "|" Number of Orders = "$i"
    nohup python3 qp_speed_test.py -n $n -i $i > qp_speed_test_N="$n"_I="$i".log 2>&1 &
    echo $!
    wait $!
  done
done