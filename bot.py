#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from cpapi import APIClient, APIClientArgs

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# token_file parameters
# these variables are imported from another file - this is for demo purposes
from token_file import telegram_token, mgmt_ip, mgmt_user, mgmt_password, mgmt_target_gateway, mgmt_policy

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# install_policy function that calls check point mgmt api
def install_policy():

    client_args = APIClientArgs(server=mgmt_ip, port=4434, api_version=1.5)
    message = ""

    with APIClient(client_args) as client:

        login_res = client.login(username=mgmt_user,password=mgmt_password)
        if login_res.success is False:
            message = "Login failed: {}".format(login_res.error_message)
            print(login_res)

        else:
            api_res = client.api_call("install-policy", {"policy-package":mgmt_policy, "targets":mgmt_target_gateway, "access":0, "threat-prevention":1})

            if api_res.success:
                message = "Policy installed successfully!"

            else:
                message = "Policy was UNABLE to be installed :("

    return message


def start(update: Update, context: CallbackContext) -> None:
    # Message issues when bot is started.
    update.message.reply_text("Welcome to FirewallBot!\nPlease issue the below commands:\n/install - install standard policy on gateway")

def help(update: Update, context: CallbackContext) -> None:
    # Help message for users to enter.
    update.message.reply_text("Please issue the below commands:\n/install - install standard policy on gateway");

def install(update: Update, context: CallbackContext) -> None:
    # Install command for users to enter
    success_message = install_policy();
    update.message.reply_text(success_message);

def main():

    # Prepare credentials for mgmt_api
    # Should be done via secure entry, not hard coded text file.

    # Start Bot.
    updater = Updater(telegram_token, use_context=True)

    # dispatcher to register handlers
    dispatcher = updater.dispatcher

    # commands in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("install", install))
    dispatcher.add_handler(CommandHandler("help", help))

    # Start Bot
    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
