import json
import os
from pathlib import Path
import re
import subprocess
import sys
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from info import Config, Txt


config_path = Path("config.json")


@Client.on_message(filters.private & filters.chat(Config.SUDO) & filters.command('make_config'))
async def make_config(bot: Client, msg: Message):
    try:
        if config_path.exists():
            return await msg.reply_text(text="**Yᴏᴜ ʜᴀᴠᴇ ᴀʟʀᴇᴀᴅʏ ᴍᴀᴅᴇ ᴀ ᴄᴏɴғɪɢ ғɪʀsᴛ ᴅᴇʟᴇᴛᴇ ɪᴛ ᴛʜᴇɴ ʏᴏᴜ'ʟʟ ᴀʙʟᴇ ᴛᴏ ᴍᴀᴋᴇ ɪᴛ ᴄᴏɴғɪɢ**\n\n Usᴇ /del_config", reply_to_message_id=msg.id)
        else:

            while True:

                try:
                    n = await bot.ask(text=Txt.SEND_NUMBERS_MSG, chat_id=msg.chat.id, filters=filters.text, timeout=60)
                except:
                    await bot.send_message(msg.from_user.id, "Eʀʀᴏʀ..!!\n\nRᴇǫᴜᴇsᴛ ᴛɪᴍᴇᴅ ᴏᴜᴛ.\nRᴇsᴛᴀʀᴛ ʙʏ ᴜsɪɴɢ /make_config", reply_to_message_id=n.id)
                    return

                try:
                    target = await bot.ask(text=Txt.SEND_TARGET_CHANNEL, chat_id=msg.chat.id, filters=filters.text, timeout=60)
                except:

                    await bot.send_message(msg.from_user.id, "Eʀʀᴏʀ..!!\n\nRᴇǫᴜᴇsᴛ ᴛɪᴍᴇᴅ ᴏᴜᴛ.\nRᴇsᴛᴀʀᴛ ʙʏ ᴜsɪɴɢ /make_config", reply_to_message_id=msg.id)
                    return

                if str(n.text).isnumeric():

                    if not str(target.text).isnumeric():
                        break
                    else:
                        await msg.reply_text(text="⚠️ **Pʟᴇᴀsᴇ Sᴇɴᴅ Vᴀʟɪᴅ Tᴀʀɢᴇᴛ Cʜᴀɴɴᴇʟ Lɪɴᴋ oʀ Usᴇʀɴᴀᴍᴇ !!**", reply_to_message_id=target.id)
                        continue

                else:
                    await msg.reply_text(text="⚠️ **Pʟᴇᴀsᴇ sᴇɴᴅ Iɴᴛᴇɢᴇʀ Nᴜᴍʙᴇʀ ɴᴏᴛ Sᴛʀɪɴɢ !**", reply_to_message_id=n.id)
                    continue

            group_target_id = target.text
            gi = re.sub("(@)|(https://)|(http://)|(t.me/)",
                        "", group_target_id)

            try:
                await bot.get_chat(gi)
            except Exception as e:
                return await msg.reply_text(text=f"{e} \n\nError !", reply_to_message_id=target.id)

            config = {
                "Target": gi,
                "accounts": []
            }

            for _ in range(int(n.text)):
                try:
                    session = await bot.ask(text=Txt.SEND_SESSION_MSG, chat_id=msg.chat.id, filters=filters.text, timeout=60)
                except:
                    await bot.send_message(msg.from_user.id, "Eʀʀᴏʀ..!!\n\nRᴇǫᴜᴇsᴛ ᴛɪᴍᴇᴅ ᴏᴜᴛ.\nRᴇsᴛᴀʀᴛ ʙʏ ᴜsɪɴɢ /make_config", reply_to_message_id=msg.id)
                    return

                if config_path.exists():

                    for acocunt in config['accounts']:
                        if acocunt['Session_String'] == session.text:
                            return await msg.reply_text(text=f"**{acocunt['OwnerName']}  ᴀᴄᴄᴏᴜɴᴛ ᴀʟʀᴇᴀᴅʏ ᴇxɪsᴛ ɪɴ ᴄᴏɴғɪɢ ʏᴏᴜ ᴄᴀɴ'ᴛ ᴀᴅᴅ sᴀᴍᴇ ᴀᴄᴄᴏᴜɴᴛ ᴍᴜʟᴛɪᴘʟᴇ ᴛɪᴍᴇs 🤡**\n\n Error !")

                # Run a shell command and capture its output
                try:

                    process = subprocess.Popen(
                        ["python", f"login.py",
                            f"{config['Target']}", f"{session.text}"],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                    )
                except Exception as err:
                    await bot.send_message(msg.chat.id, text=f"<b>ERROR :</b>\n<pre>{err}</pre>")

                # Use communicate() to interact with the process
                stdout, stderr = process.communicate()

                # Get the return code
                return_code = process.wait()

                # Check the return code to see if the command was successful
                if return_code == 0:
                    # Print the output of the command
                    print("Command output:")
                    # Assuming output is a bytes object
                    output_bytes = stdout
                    # Decode bytes to string and replace "\r\n" with newlines
                    output_string = output_bytes.decode(
                        'utf-8').replace('\r\n', '\n')
                    print(output_string)
                    AccountHolder = json.loads(output_string)

                else:
                    # Print the error message if the command failed
                    print("Command failed with error:")
                    print(stderr)
                    return await msg.reply_text('**Sᴏᴍᴇᴛʜɪɴɢ Wᴇɴᴛ Wʀᴏɴɢ Kɪɴᴅʟʏ Cʜᴇᴄᴋ ʏᴏᴜʀ Iɴᴘᴜᴛs Wʜᴇᴛʜᴇʀ Yᴏᴜ Hᴀᴠᴇ Fɪʟʟᴇᴅ Cᴏʀʀᴇᴄᴛʟʏ ᴏʀ Nᴏᴛ !!**')

                try:

                    new_account = {
                        "Session_String": session.text,
                        "OwnerUid": AccountHolder['id'],
                        "OwnerName": AccountHolder['first_name']
                    }
                    config["accounts"].append(new_account)

                    with open(config_path, 'w', encoding='utf-8') as file:
                        json.dump(config, file, indent=4)
                except Exception as e:
                    print(e)

            acocunt_btn = [
                [InlineKeyboardButton(
                    text='Accounts You Added', callback_data='account_config')]
            ]
            await msg.reply_text(text=Txt.MAKE_CONFIG_DONE_MSG.format(n.text), reply_to_message_id=n.id, reply_markup=InlineKeyboardMarkup(acocunt_btn))

    except Exception as e:
        print('Error on line {}'.format(
            sys.exc_info()[-1].tb_lineno), type(e).__name__, e)


@Client.on_message(filters.private & filters.chat(Config.SUDO) & filters.command('see_accounts'))
async def see_account(bot: Client, msg: Message):

    try:

        config = (json.load(open("config.json")))['accounts']
        acocunt_btn = [
            [InlineKeyboardButton(text='Aᴄᴄᴏᴜɴᴛs Yᴏᴜ Aᴅᴅᴇᴅ',
                                  callback_data='account_config')]
        ]
        await msg.reply_text(text=Txt.ADDED_ACCOUNT.format(len(config)), reply_to_message_id=msg.id, reply_markup=InlineKeyboardMarkup(acocunt_btn))

    except:
        return await msg.reply_text(text="**Yᴏᴜ Dᴏɴ'ᴛ Hᴀᴠᴇ Aᴅᴅᴇᴅ Aɴʏ Aᴄᴄᴏᴜɴᴛs 0️⃣ **\n\nUsᴇ /make_config ᴛᴏ ᴀᴅᴅ ᴀᴄᴄᴏᴜɴᴛs 👥", reply_to_message_id=msg.id)
