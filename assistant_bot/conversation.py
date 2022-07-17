#!/usr/bin/env python
# coding: utf-8

# In[2]:


import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from ExtractSymptoms import  Extract 
from get_icd import GetICD

# In[3]:
Extractor= Extract()
icdfy = GetICD()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
token = '5591282402:AAFyuapuAD3wt7x05N5TZvSlWF5Ea_chHUs'

#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few callback functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging

from telegram import __version__ as TG_VER
import os
import pandas as pd


try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

GENDER, PHOTO, LOCATION, AGE, BIO,DURATION = range(6)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks the user about their gender."""
    reply_keyboard = [["Male", "Female", "Other"]]

    await update.message.reply_text(
        "Hi! I am your medical assistant Bot. I will collect some basic information to help improve your experience. "
        "Send /cancel to stop talking to me.\n\n"
        "Are you a Male or a Female?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Male or Female?"
        ),
    )

    return GENDER


async def gender(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected gender and asks for a photo."""
    user = update.message.from_user
    logger.info("Gender of %s: %s", user.first_name, update.message.text)
    os.makedirs(f'../hackathon/assets/{user.id}',exist_ok=True)
   #os.mkdir(f'../hackathon/assets/{user.first_name}')
    val={'Sex':[update.message.text]}
    print(val)
    df = pd.DataFrame.from_dict(val)
    print(f' value is {update.message.text}')
    print(df)
    df.to_csv(f'../hackathon/assets/{user.id}/bio.csv',index=False)
    
    await update.message.reply_text(
        "I see! Please send me a photo of your report "
        "so I can share with doctor or send /skip if you don't want to.",
        reply_markup=ReplyKeyboardRemove(),
    )

    return PHOTO


async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the photo and asks for a location."""
    user = update.message.from_user
    photo_file = await update.message.photo[-1].get_file()
    await photo_file.download(f"../hackathon/assets/{user.id}/report.jpg")
    logger.info("report of %s: %s", user.first_name, f"../hackathon/assets/{user.id}/report.jpg")
    await update.message.reply_text(
        "Thank you! Now, please share your age, or send /skip if you don't want to."
    )

    return AGE


async def skip_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Skips the photo and asks for a location."""
    user = update.message.from_user
    logger.info("User %s did not send a report.", user.first_name)

    await update.message.reply_text(
        "If you get any report please bring it along at the time of appointment, please share age."
    )

    return AGE


async def age(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the info about the user and ends the conversation."""
    user = update.message.from_user
    logger.info("Age of %s: %s", user.first_name, update.message.text)
    bio = pd.read_csv(f'../hackathon/assets/{user.id}/bio.csv')
    bio['Age']=[update.message.text]
    bio.to_csv(f'../hackathon/assets/{user.id}/bio.csv',index=False)
    await update.message.reply_text("Thank you! Please share your symptoms")

    return BIO

async def location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the location and asks for some info about the user."""
    user = update.message.from_user
    user_location = update.message.location
    logger.info(
        "Location of %s: %f / %f", user.first_name, user_location.latitude, user_location.longitude
    )
    await update.message.reply_text(
        "Maybe I can visit you sometime! At last, tell me something about yourself."
    )

    return BIO


async def skip_location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Skips the location and asks for info about the user."""
    user = update.message.from_user
    logger.info("User %s did not send a location.", user.first_name)
    await update.message.reply_text(
        "You seem a bit paranoid! At last, tell me something about yourself."
    )

    return BIO



async def bio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the info about the user and ends the conversation."""
    user = update.message.from_user
    logger.info("Symptoms of %s: %s", user.first_name, update.message.text)
    bio = pd.read_csv(f'../hackathon/assets/{user.id}/bio.csv')
    bio['Symptoms']=[update.message.text]
    bio.to_csv(f'../hackathon/assets/{user.id}/bio.csv',index=False)
    await update.message.reply_text(f"Thank you! Please share since when you are having {update.message.text}")

    return DURATION

async def duration(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the info about the user and ends the conversation."""
    user = update.message.from_user
    logger.info("Duration of Symptoms %s: %s", user.first_name, update.message.text)
    bio = pd.read_csv(f'../hackathon/assets/{user.id}/bio.csv')
    bio['Duration']=[update.message.text]
    bio['Patient Name']=[user.first_name]
    bio['ABHA ID'] = [user.id]
    logger.info(user)
    bio.to_csv(f'../hackathon/assets/{user.id}/bio.csv',index=False)
    analysis = pd.read_csv('../hackathon/Analysis.csv')
    analysis = pd.concat([analysis,bio])
    analysis.reset_index(inplace=True,drop=True)
    analysis.to_csv('../hackathon/Analysis.csv')
    values = Extractor.get_symptoms(f'../hackathon/assets/{user.id}/report.jpg')
    print(values)
    output = pd.DataFrame(values)

    output['ICD 10'] = output['Symptom'].map(icdfy.get)

    output.to_csv(f'../hackathon/assets/{user.id}/output.csv',index=False)
    await update.message.reply_text("Thank you! This is all the information we need")

    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    
    await update.message.reply_text(
        "Bye! If you need anything please type /start", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(token).build()

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            GENDER: [MessageHandler(filters.Regex("^(Male|Female|Other)$"), gender)],
            PHOTO: [MessageHandler(filters.PHOTO, photo), CommandHandler("skip", skip_photo)],
            LOCATION: [
                MessageHandler(filters.LOCATION, location),
                CommandHandler("skip", skip_location),
            ],
            AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, age)],
            BIO: [MessageHandler(filters.TEXT & ~filters.COMMAND, bio)],
            DURATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, duration)],
            
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()