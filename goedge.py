import requests, json, time, sys, base64

token = {"token": "", "expiresAt": -1}
server = ""
reCount = 0

initInfo = {
    "type": "",
    "accessKeyId": "", 
    "accessKey": ""
}

try: token = json.loads(open("./token.json", "r", encoding="utf-8").read())
except: pass

def init(host: str, type: str, accessKeyId: str, accessKey: str):
    global token
    global server
    global initInfo

    initInfo = {
        "type": type,
        "accessKeyId": accessKeyId, 
        "accessKey": accessKey
    }
    server = host

    if token["expiresAt"] < time.time() + 60 * 60:
        rjson = requests.post(
            url=host+'/APIAccessTokenService/GetAPIAccessToken',
            data=json.dumps({
                "type": type,
                "accessKeyId": accessKeyId,
                "accessKey": accessKey
            }),
        ).json()

        if rjson["message"] == "ok":
            token = rjson["data"]
            open("./token.json", "w", encoding="utf-8").write(json.dumps(token))
        else:
            print("Config Error: AccessKeyID or AccessKey incorrect.")
            sys.exit()

def requestApi(path: str, data: any):
    rj = requests.post(
        url=server+path,
        headers={"X-Edge-Access-Token": token["token"]},
        data=json.dumps(data),
    ).json()

    if rj["message"] == "ok":
        reCount = 0
        return rj
    elif reCount < 4:
        reCount+=1
        init(server, initInfo['type'], initInfo["accessKeyId"], initInfo["accessKey"])
        return requestApi(path, data)

def apiNodeStatus():
    return json.loads(base64.b64decode(requestApi("/APINodeService/findCurrentAPINode", {})["data"]["apiNode"]["statusJSON"]))

def composeServerStatNodeClusterBoard(cid: int):
    return requestApi("/ServerStatBoardService/composeServerStatNodeClusterBoard", {
        "nodeClusterId": cid
    })["data"]

def findAllEnabledNodesWithNodeClusterId(cid: int):
    return requestApi("/NodeService/findAllEnabledNodesWithNodeClusterId", {
        "nodeClusterId": cid
    })["data"]["nodes"]