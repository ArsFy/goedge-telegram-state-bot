import goedge
import json
import sys
import time
import matplotlib.pyplot as plt

try:
    config = json.loads(open("./config.json", "r", encoding="utf-8").read())
except:
    print("Config Error: config.json format error or file does not exist.")
    sys.exit()

# Init
goedge.init(config["host"], config["auth"]["type"], config["auth"]["accessKeyId"], config["auth"]["accessKey"])

def d15():
    board = goedge.composeServerStatNodeClusterBoard()

    dailyTrafficStats = board["dailyTrafficStats"]

    timeData = []
    bytes = []
    cachedBytes = []
    attackBytes = []

    for i in dailyTrafficStats:
        # timeData.append(time.strftime("%H", time.localtime(i[""])))
        timeData.append(i["day"][4:6]+"-"+i["day"][6:])
        bytes.append(round(i["bytes"] / 1024 / 1024 / 1024, 2))
        cachedBytes.append(round(i["cachedBytes"] / 1024 / 1024 / 1024, 2))
        attackBytes.append(round(i["attackBytes"] / 1024 / 1024 / 1024, 2))

        data = []
        titleList = [[
            "Bytes",
            "#BAE0EF"
        ], [
            "Cached Bytes",
            "#7CB3BE"
        ], [
            "Attack Bytes",
            "#F39494"
        ]]

        data.append(bytes)
        data.append(cachedBytes)
        data.append(attackBytes)

        plt.figure(figsize=(10, 5))

        for i in range(0, len(titleList)):
            plt.fill_between(timeData, data[i], label=titleList[i][0], alpha=0.8, color=titleList[i][1])
            for ii in range(0, len(data[i])):
                if data[i][ii] != 0:
                    plt.text(ii - 0.25, data[i][ii] + 5, str(data[i][ii])+ "G", fontdict={'size': 7})

        plt.xticks(rotation=320)
        plt.grid(True)
        plt.ylabel("15-day traffic trend (GB)", fontdict={'size': 16})
        plt.legend()
        plt.tight_layout()
        plt.rcParams['axes.unicode_minus'] = False
        plt.show()