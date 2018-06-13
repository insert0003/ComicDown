for old in *
do
    for jpg in $old/*
    do
        echo $jpg
        new="$(echo $jpg | sed 's/第//g')"
        new="$(echo $new | sed 's/話//g')"
        new="$(echo $new | sed 's/\//\-/g')"
        echo $new
        mv "$jpg" "$new"
    done
#    new="$(echo $new | sed 's/話//g')"
#    echo $new
done
