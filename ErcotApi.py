#Import Packages
import pandas as pd
import requests 

#ERCOT API Calls
def ercot_connection(data_url):
    # USER MUST PROVIDE THIS INFORMATION
    #
    from config_local import USERNAME, PASSWORD

    # Authorization URL for signing into ERCOT Public API account
    #
    AUTH_URL = "https://ercotb2c.b2clogin.com/ercotb2c.onmicrosoft.com/B2C_1_PUBAPI-ROPC-FLOW/oauth2/v2.0/token?username={username}&password={password}&grant_type=password&scope=openid+fec253ea-0d06-4272-a5e6-b478baeecd70+offline_access&client_id=fec253ea-0d06-4272-a5e6-b478baeecd70&response_type=id_token"

    # Sign In/Authenticate
    access_token = ""
    auth_response = requests.post(AUTH_URL.format(username = USERNAME, password=PASSWORD), verify=False)
    if auth_response.status_code != 200:
        auth_msg = "Authentication Failed"
    else:
        auth_msg = "Success"
        ## Retrieve access token
        access_token = auth_response.json().get("access_token")
    
    data_list = list()
    for i in data_url:
        # Your specific API endpoint (could also be passed as a command line argument)
        #
        ARCHIVE_URL = "https://api.ercot.com/api/public-reports/"
        ARCHIVE_TARGET = i
        SUBSCRIPTION_KEY = "2026b555a3de4e52b016e4ea45489ce8"


        # Use Subscription key and bearer token to retrieve all Public API Reports
        #
        headers = {"Authorization": "Bearer " + access_token, "Ocp-Apim-Subscription-Key": SUBSCRIPTION_KEY}
        product_response = requests.get(ARCHIVE_URL + ARCHIVE_TARGET, headers=headers)
        if product_response.status_code != 200:
            return(data_list.append(pd.DataFrame(["Error"])))
        else:

            erc_rsp = product_response.json()
            erc_data = pd.DataFrame(erc_rsp["data"])
            columnsnames  = [x["name"] for  x in erc_rsp["fields"]]
            erc_data.columns = columnsnames
            data_list.append(erc_data)
    return(data_list)




