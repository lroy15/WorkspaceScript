a=`op run --env-file=.env -- python3 1passcreate.py`


b=${a%:*}

c=${a#*:}
echo $b
echo $c
op item create --category login --title "$c" --vault Private --generate-password='letters,digits,symbols,12' username="$b@domain.com"

echo -e "WS_PW=op://Private/$c/password" >> pathtoOPW.env


echo "Password created for $c. Proceed with Google account creation? Y/N: "
read response

if [ $response != y ]
then
    echo "Aborting account creation."
else
    op run --env-file=pathtoOPW.env -- python3 googleCreateUser.py
fi

sed -i '' -e '$ d' pathtoOPW.env
