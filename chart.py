import goedge
import io
import base64
import json
import time
import matplotlib.pyplot as plt

def d15(cid: int):
    board = goedge.composeServerStatNodeClusterBoard(cid)

    dailyTrafficStats = board["dailyTrafficStats"]

    timeData = []
    bytes = []
    cachedBytes = []
    attackBytes = []

    for i in dailyTrafficStats:
        timeData.append(i["day"][4:6]+"-"+i["day"][6:])
        bytes.append(round(i["bytes"] / 1024 / 1024 / 1024, 2))
        cachedBytes.append(round(i["cachedBytes"] / 1024 / 1024 / 1024, 2))
        if "attackBytes" in i: attackBytes.append(round(i["attackBytes"] / 1024 / 1024 / 1024, 2))
        else: attackBytes.append(0)

    data = []
    titleList = [[
        "Traffic",
        "#BAE0EF"
    ], [
        "Cached",
        "#7CB3BE"
    ], [
        "Attack",
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
                plt.text(ii - 0.25, data[i][ii] + data[i][ii] * 0.05, str(data[i][ii])+ "G", fontdict={'size': 7})

    plt.xticks(rotation=320)
    plt.grid(True)
    plt.ylabel("15-day traffic trend (GB)", fontdict={'size': 16})
    plt.legend()
    plt.tight_layout()
    plt.rcParams['axes.unicode_minus'] = False

    imgBuf = io.BytesIO()
    plt.savefig(imgBuf, format='jpeg')
    return imgBuf.getvalue()

def h24(cid: int):
    board = goedge.composeServerStatNodeClusterBoard(cid)

    hourlyTrafficStats = board["hourlyTrafficStats"]

    timeData = []
    bytes = []
    cachedBytes = []
    attackBytes = []

    for i in hourlyTrafficStats:
        timeData.append(i["hour"][8:])
        bytes.append(round(i["bytes"] / 1024 / 1024 / 1024, 2))
        cachedBytes.append(round(i["cachedBytes"] / 1024 / 1024 / 1024, 2))
        if "attackBytes" in i: attackBytes.append(round(i["attackBytes"] / 1024 / 1024 / 1024, 2))
        else: attackBytes.append(0)

    data = []
    titleList = [[
        "Traffic",
        "#BAE0EF"
    ], [
        "Cached",
        "#7CB3BE"
    ], [
        "Attack",
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
                plt.text(ii - 0.25, data[i][ii] + data[i][ii] * 0.05, str(data[i][ii])+ "G", fontdict={'size': 7})

    plt.xticks(rotation=320)
    plt.grid(True)
    plt.ylabel("24-hour traffic trend (GB)", fontdict={'size': 16})
    plt.legend()
    plt.tight_layout()
    plt.rcParams['axes.unicode_minus'] = False

    imgBuf = io.BytesIO()
    plt.savefig(imgBuf, format='jpeg')
    return imgBuf.getvalue()

def cpuNode(cid: int):
    board = goedge.composeServerStatNodeClusterBoard(cid)

    timeList = []
    cpuNode = []

    for i in board["cpuNodeValues"]:
        cpuNode.append(json.loads(base64.b64decode(i['valueJSON']))['usage'] * 100)
        timeList.append(time.strftime("%H:%M", time.localtime(i['createdAt'])))

    plt.figure(figsize=(14, 6))

    plt.plot(timeList, cpuNode, label="CPU")
    for i in range(0, len(cpuNode)):
        if cpuNode[i] != 0:
            plt.text(i - 0.5, cpuNode[i] + cpuNode[i] * 0.05, "{}%".format(round(cpuNode[i], 1)), fontdict={'size': 7})

    plt.xticks(rotation=320)
    plt.grid(True)
    plt.ylabel("Cluster CPU (%)", fontdict={'size': 16})
    plt.legend()
    plt.tight_layout()
    plt.rcParams['axes.unicode_minus'] = False

    imgBuf = io.BytesIO()
    plt.savefig(imgBuf, format='jpeg')
    return imgBuf.getvalue()

def memoryNode(cid: int):
    board = goedge.composeServerStatNodeClusterBoard(cid)

    timeList = []
    memoryNode = []

    for i in board["memoryNodeValues"]:
        memoryNode.append(json.loads(base64.b64decode(i['valueJSON']))['usage'] * 100)
        timeList.append(time.strftime("%H:%M", time.localtime(i['createdAt'])))

    plt.figure(figsize=(15, 5))

    plt.plot(timeList, memoryNode, label="Memory")
    for i in range(0, len(memoryNode)):
        if memoryNode[i] != 0:
            plt.text(i - 0.5, memoryNode[i] + memoryNode[i] * 0.01, "{}%".format(round(memoryNode[i], 1)), fontdict={'size': 6})

    plt.xticks(rotation=320)
    plt.grid(True)
    plt.ylabel("Cluster Memory (%)", fontdict={'size': 16})
    plt.legend()
    plt.tight_layout()
    plt.rcParams['axes.unicode_minus'] = False

    imgBuf = io.BytesIO()
    plt.savefig(imgBuf, format='jpeg')
    return imgBuf.getvalue()
    
def loadNode(cid: int):
    board = goedge.composeServerStatNodeClusterBoard(cid)

    timeList = []
    loadNode = []

    for i in board["loadNodeValues"]:
        loadNode.append(json.loads(base64.b64decode(i['valueJSON']))['load1m'])
        timeList.append(time.strftime("%H:%M", time.localtime(i['createdAt'])))

    plt.figure(figsize=(18, 10))

    plt.plot(timeList, loadNode, label="Load")
    for i in range(0, len(loadNode)):
        if loadNode[i] != 0:
            plt.text(i - 0.5, loadNode[i] + loadNode[i] * 0.05, round(loadNode[i], 1), fontdict={'size': 7})

    plt.xticks(rotation=320)
    plt.grid(True)
    plt.ylabel("Cluster Load", fontdict={'size': 16})
    plt.legend()
    plt.tight_layout()
    plt.rcParams['axes.unicode_minus'] = False

    imgBuf = io.BytesIO()
    plt.savefig(imgBuf, format='png')
    return imgBuf.getvalue()
