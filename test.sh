ARRAY=(1)

for num in ${ARRAY[@]}; do
    /test_sakura.py
    echo $num"回目のループです"
done