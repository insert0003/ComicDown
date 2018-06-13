for old in *; do new="$(echo $old | sed 's/ //g')"; echo $new; mv "$old" "$new"; done
