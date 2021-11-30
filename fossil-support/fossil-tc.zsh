prevsha=$(fossil finfo -b -n 2 $1 | awk '{print $1;}' | sed -n '2 p')
nowsha=$(fossil finfo -b -n 2 $1 | awk '{print $1;}' | sed -n '1 p')

prevcnt=$(fossil cat $1 -r $prevsha | wc -m) 
nowcnt=$(fossil cat $1 -r $nowsha | wc -m)

sum=$(($nowcnt - $prevcnt))

echo $sum

