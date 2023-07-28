from pyrogram import Client, filters, idle
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

API_ID = None #mettere api id
API_HASH = "" # metti il tuo api hash
TOKEN = "" #metti il tuo bot token

client = Client("bot_session", API_ID, API_HASH, bot_token=TOKEN)

client.start()
print("STATUS BOT [ONLINE]")

check = [] 

UserId = None
text_find = "" #metti le parole che deve mettere per forza l'utente. 
admin = [] # id admin nel quale riceve le feed... 
canale_feed = [] # id canale delle feed 

@client.on_message(filters.private & filters.command("start"))
async def avvio(_, message):
    if not message.from_user.id in admin:
        await message.reply(f"""Benvenuto {message.from_user.mention} nel mio FeedBot, se vuoi inviarmi una feed usa il bottone sottostante!. 
        Bot Creato da @paperego68""", reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Mandami una Feed", "inviafeed"), [InlineKeyboardButton("Developer 💻", url="t.me/paperego68")]]
    ]))
    else:
        await message.reply_text("Sei risultato Admin del bot, aspetta che il bot ti invia Le feed!\n developed by @paperego68")

@client.on_callback_query() #Query messaggi 
async def btn(_, query):
    if query.data == "inviafeed":
        if not query.from_user.id in check:
            check.append(query.from_user.id)
            await query.message.edit("""
<b><i><u>Hai acquistato e vuoi lasciare una recensione</u></i></b>❓
<b>Scrivila qui sotto⬇️ seguendo uno di questo format:
[1️⃣]  </b><code> +rep @paperego68 carring, voto, tempo</code>
""", reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✖️ Annulla", "stop")]
            ]))
        else:
            await query.answer("Stai gia provando ad inviare una feed", show_alert=False)
    elif query.data == "stop":
        if query.from_user.id in check:
            check.remove(query.from_user.id)
            await query.message.edit(f"Benvenuto {query.message.from_user.mention} nel mio FeedBot, se vuoi inviarmi una feed usa il bottone sottostante!.\nBot Creato da @paperego68", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ Mandami una Feed", "inviafeed"), [InlineKeyboardButton("Developer 💻", url="t.me/paperego68")]]
    ]))
        else:
            await query.answer("Avvia di nuovo il feed Bot", show_alert=False)
    elif query.data == "startcb":
        await query.message.edit (f"Benvenuto {query.message.from_user.mention} nel mio FeedBot, se vuoi inviarmi una feed usa il bottone sottostante!\nBot Creato da @paperego68", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ Mandami una Feed", "inviafeed"), [InlineKeyboardButton("Developer 💻", url="t.me/paperego68")]]
        ]))

@client.on_message(filters.private) # check feed 
async def feed(_, message):
    global check
    if message.from_user.id in check:
        if message.text.find(text_find):
            await client.send_message(UserId, f"Un Utente di nome {message.from_user.mention} Ha inviato una Feed!", reply_markup=InlineKeyboardMarkup([
    ])) 
            await message.forward(UserId)
            await message.reply_text("__**Feedback inoltrato con successo✅**__", reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton("💻 Mandami una nuova Feed", "inviafeed")],
        [InlineKeyboardButton("⏪ Indietro", "startcb")]
    ]))
            check.remove(message.from_user.id)
        else:
            await message.reply_text("""✖️ Format non valido!
Assicurati di aver inviato precisamente ciò che ti è stato richiesto.""", reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton("↪️ Riprova", "inviafeed")],
        [InlineKeyboardButton("⏪ Indietro", "startcb")]
    ]))
        check.remove(message.from_user.id)

idle() # run bot telegram
