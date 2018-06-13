for old in $1/*; do new="$(echo $old | sed 's/\//\_/g')"; echo $new; cp "$old" "$new"; done
