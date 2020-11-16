#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from cpapi import APIClient, APIClientArgs

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# telegram_token is in an ignored file - don't worry it has already been reset.
from token_file import telegram_token, mgmt_ip, mgmt_username, mgmt_password

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

def install_policy():
    client_args = APIClientArgs(server=mgmt_ip, api_version="1", unsafe=True, context="gaia_api")
    message = ""

    with APIClient(client_args) as client:

        login_res = client.login(mgmt_username, mgmt_password)
        if login_res.success is False:
            message = "Login failed: {}".format(login_res.error_message)

        else:
            api_res = client.api_call("install-policy", {})

            if api_res.success:
                message = "Policy installed successfully!"

            else:
                message = "Policy was UNABLE to be installed :("
                
    return message


def start(update: Update, context: CallbackContext) -> None:
    # Message issues when bot is started.
    update.message.reply_text("Welcome to FirewallBot!\nPlease issue the below commands:\n/install - install standard policy on gateway")

def help(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Please issue the below commands:\n/install - install standard policy on gateway");

def install(update: Update, context: CallbackContext) -> None:
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
