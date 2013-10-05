#!/bin/bash

#why am I scripting to my script?  nonetheless in bash...
#if [[ -z $1 ]]
#then
#    echo "You need to supply the sample directory as the first argument"
#    exit
#fi

debug=true
package=org.kivy.netcheck
name="Netcheck Testing"
dir=~/projects/netcheck/
version=0.1
orientation='landscape'
jars=()
perms=('INTERNET' 'ACCESS_NETWORK_STATE')



jar_options=()
for j in "${jars[@]}"
do
    jar_options+=(--add-jar "$j")
done

perm_options=()
for p in "${perms[@]}"
do
    perm_options+=(--permission "$p")
done

if $debug
then
    mode=('debug' 'installd')
else
    mode=('release')
fi

command=(./build.py --package "$package" --version $version --orientation "$orientation" --name "$name" --dir "$dir")
#command+=("${jar_options[@]}" "${perm_options[@]}" "${mode[@]}")
command+=("${perm_options[@]}" "${mode[@]}")

#echo "${command[@]}"
"${command[@]}"
