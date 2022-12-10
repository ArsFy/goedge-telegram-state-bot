import requests, json, time, sys, base64

token = {"token": "", "expiresAt": -1}
server = ""

try: token = json.loads(open("./token.json", "r", encoding="utf-8").read())
except: pass

def init(host: str, type: str, accessKeyId: str, accessKey: str):
    global token
    global server

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
    return requests.post(
        url=server+path,
        headers={"X-Edge-Access-Token": token["token"]},
        data=json.dumps(data),
    ).json()

def apiNodeStatus():
    return json.loads(base64.b64decode(requestApi("/APINodeService/findCurrentAPINode", {})["data"]["apiNode"]["statusJSON"]))

def composeServerStatNodeClusterBoard(cid: int):
    return requestApi("/ServerStatBoardService/composeServerStatNodeClusterBoard", {
        "nodeClusterId": cid
    })["data"]