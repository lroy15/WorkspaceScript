from mxApiCall import mxGetUser

mxUserInfo = mxGetUser()

print(mxUserInfo.email+":"+mxUserInfo.name)