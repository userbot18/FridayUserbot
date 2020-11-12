import io

from telethon.utils import pack_bot_file_id

from fridaybot.Configs import Config
from fridaybot.modules.sql_helper.broadcast_sql import (
    add_chnnl_in_db,
    already_added,
    get_all_chnnl,
    rm_channel,
)
from fridaybot.utils import friday_on_cmd


@friday.on(friday_on_cmd(pattern="badd ?(.*)"))
async def _(event):
    input_chnnl = event.pattern_match.group(1)
    if input_chnnl is None:
        if event.is_channel and event.is_group:
            input_chnnl = event.chat_id
        else:
            await event.edit("Please Give Group / Channel ID")
            return
    if already_added(input_chnnl):
        await event.edit("This Channel Already Found in Database.")
        return
    elif not already_added(input_chnnl):
        add_chnnl_in_db(input_chnnl)
        await event.edit(f"Fine. I have Added {input_chnnl} To DataBase.")


@friday.on(friday_on_cmd(pattern="brm ?(.*)"))
async def _(event):
    input_chnnl = event.pattern_match.group(1)
    if input_chnnl is None:
        if event.is_channel and event.is_group:
            input_chnnl = event.chat_id
        else:
            await event.edit("Please Give Group / Channel ID")
            return
    if already_added(input_chnnl):
        rm_channel(input_chnnl)
        await event.edit(f"Fine. I have Removed {input_chnnl} From DataBase.")
    elif not already_added(input_chnnl):
        await event.edit(
            "Are You Sure? , You Haven't Added This Group / Channel To Database"
        )


@friday.on(friday_on_cmd(pattern="broadcast"))
async def _(event):
    sedpath = Config.TMP_DOWNLOAD_DIRECTORY
    all_chnnl = get_all_chnnl()
    if len(all_chnnl) == 0:
        await event.edit("No Channel Or Group Found On Database. Please Check Again")
        return
    total_errors = 0
    total_count = 0
    total_chnnl = len(all_chnnl)
    if event.reply_to_msg_id:
        hmm = await event.get_reply_message()
    else:
        event.edit("Reply To Some Message.")
        return
    if hmm and hmm.media:
        await borg.download_media(hmm.media, sedpath)
        for channelz in all_chnnl:
            bot_api_file_id = pack_bot_file_id(hmm.media)
            await borg.send_file(
                int(channelz.chat_id), file=bot_api_file_id, caption=event.text
            )
    elif hmm and hmm.text:
        for channelz in all_chnnl:
            await borg.send_message(int(channelz.chat_id), hmm.text)
    elif hmm.message.poll or hmm:
        await event.edit("Bruh, This Can't Be Broadcasted.")
        return
    await event.edit(
        f"BroadCast Success In : {total_count} \nFailed In : {total_errors} \nTotal Channel In DB : {total_chnnl}"
    )


@friday.on(friday_on_cmd(pattern="forward"))
async def _(event):
    all_chnnl = get_all_chnnl()
    if len(all_chnnl) == 0:
        await event.edit("No Channel Or Group Found On Database. Please Check Again")
        return
    total_errors = 0
    total_count = 0
    total_chnnl = len(all_chnnl)
    if event.reply_to_msg_id:
        hmm = await event.get_reply_message()
    else:
        event.edit("Reply To Some Message.")
        return
    for forbard in all_chnnl:
        await hmm.forward_to(int(forbard.chat_id))
    await event.edit(
        f"Forward Success in {total_count} And Failed In {total_errors} And Total Channel In Db is {total_chnnl}"
    )


@friday.on(friday_on_cmd(pattern="bstat"))
async def _(event):
    total_chnnl = get_all_chnnl()
    chnnl_list = ""
    for starked in total_chnnl:
        chnnl_list += ("==> {} \n").format(int(starked.chat_id))
    with io.BytesIO(str.encode(chnnl_list)) as tedt_file:
        tedt_file.name = "dbchnnllist.txt"
        await borg.send_file(
            event.chat_id,
            tedt_file,
            force_document=True,
            caption="Total Channel In DB.",
            allow_cache=False,
        )
