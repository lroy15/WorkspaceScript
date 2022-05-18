#!/bin/bash

mxInfo=$(op run --env-file=.env -- python3 1passcreate.py)
mxUserEmail=${mxInfo%:*}
mxUserName=${mxInfo#*:}


op item get "$mxUserName" --fields label=username --vault Private
if [ "$?" -eq 0 ]
then
echo "Account already exists in Onepassword. Continue with Workspace account creation? y/n: "
read wscreate
    if [ $wscreate != y ]
    then echo "Aborting Google Workspace account creation."
    else
    echo -e "WS_PW=op://Private/$mxUserName/password" >> pathtoOPW.env
    op run --env-file=pathtoOPW.env -- python3 googleCreateUser.py
    sed -i '' -e '$ d' pathtoOPW.env
    fi
else

    op item create --category login --title "$mxUserName" --vault Private --generate-password='letters,digits,symbols,12' username="$mxUserEmail@domain.com" 1> /dev/null 

    echo -e "WS_PW=op://Private/$mxUserName/password" >> pathtoOPW.env


    echo "Password created for $mxUserName. Proceed with Google account creation? Y/N: "
    read response

    if [ $response != y ]
    then
        echo "Aborting account creation."
    else
        op run --env-file=pathtoOPW.env -- python3 googleCreateUser.py
    fi

    sed -i '' -e '$ d' pathtoOPW.env

fi