import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
import goedge
import chart
import json
import sys
import time

try:
    config = json.loads(open("./config.json", "r", encoding="utf-8").read())
except:
    print("Config Error: config.json format error or file does not exist.")
    sys.exit()

# Init
goedge.init(config["host"], config["auth"]["type"], config["auth"]["accessKeyId"], config["auth"]["accessKey"])

# Log
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="这是一个适用于 GoEdge CDN 的 Telegram Bot，它可以用于简单管理/查询状态\n\n/start 关于这个 Bot\n/goedge GoEdge 的简要资讯\n/d15 15 天流量统计图\n/h24 24 小时流量统计图\n/node_cpu 集群节点 CPU 占用统计图\n/node_memory 集群节点记忆体占用统计图\n/node_load 集群节点负载统计图\n\nGitHub: https://github.com/ArsFy/goedge-telegram-state-bot"
    )

async def goedge_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    board = goedge.composeServerStatNodeClusterBoard(config['cluster_id'])
    status = goedge.apiNodeStatus()

    todayTraffic = 0
    if len(board['dailyTrafficStats']) > 1:
        todayTraffic = round(board['dailyTrafficStats'][0]["bytes"] / 1024 / 1024 / 1024, 2)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        reply_to_message_id=update.message.message_id,
        text="#GoEdge {} ({})\nNodes: {} ({} Active)\nToday traffic: {}G\nAPI Load: {}\nAPI CPU: {}%\nAPI Memory: {}%\nAPI Disk: {}%".format(
            status["buildVersion"],
            time.strftime("%Y-%m-%d %H:%M", time.localtime(time.time())),
            board['countServers'],
            board['countActiveNodes'],
            todayTraffic,
            "{} {} {}".format(status["load1m"], status["load5m"], status["load15m"]),
            round(status["cpuUsage"], 2), 
            round(status["memoryUsage"], 2), 
            round(status["diskUsage"], 2),
        ),
    )

async def d15(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        reply_to_message_id=update.message.message_id,
        photo=chart.d15(config['cluster_id'])
    )

async def h24(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        reply_to_message_id=update.message.message_id,
        photo=chart.h24(config['cluster_id'])
    )

async def node_cpu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        reply_to_message_id=update.message.message_id,
        photo=chart.cpuNode(config['cluster_id'])
    )

async def node_memory(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        reply_to_message_id=update.message.message_id,
        photo=chart.memoryNode(config['cluster_id'])
    )

async def node_load(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        reply_to_message_id=update.message.message_id,
        photo=chart.loadNode(config['cluster_id'])
    )

if __name__ == '__main__':
    application = ApplicationBuilder().token(config["bot_token"]).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('goedge', goedge_info))
    application.add_handler(CommandHandler('d15', d15))
    application.add_handler(CommandHandler('h24', h24))
    application.add_handler(CommandHandler('node_cpu', node_cpu))
    application.add_handler(CommandHandler('node_memory', node_memory))
    application.add_handler(CommandHandler('node_load', node_load))


    application.run_polling()