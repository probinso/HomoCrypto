

while true
do
netcat -l 6112 > query.txt
echo "Do Work Time"
echo "Responding" |netcat acm.wwu.edu 6112
done