[[ $1 == "" ]] && echo "[ERROR] Please enter a run ID" && exit 1

sdRoot=/Volumes/NO\ NAME
root=runs
runDir="$sdRoot/$1"

echo "Moving $1 to runs/..."

cp -r "$runDir" "$root"
([[ -d "$root/$1" ]] && rm -rf "$runDir") || (echo "Not found" && exit 1)

echo "Done."

