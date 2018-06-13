for obj in *
do
echo "$obj"
convert "$obj"/*.jpg $1"$obj".pdf
done
