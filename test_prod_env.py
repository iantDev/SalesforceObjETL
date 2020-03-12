import LoginAuthentication, ExtractByObject, LoadData

try:
    LoginAuthentication.get_access_token()
except BaseException as e:
    print(f"Error in get_access_token: {e}.")
finally:
    print("Executed LoginAuth.get_access_token.")