import discord
from config import DISCORD_BOT_TOKEN, DOCUMENTATION_PATH
from utils.loader import load_documents
from utils.vector_store import initialize_vector_store, add_documents_to_store
from utils.langchain import initialize_llm, initialize_embeddings, initialize_prompt
from workflow import build_workflow

llm = initialize_llm()
embeddings = initialize_embeddings()
vector_store = initialize_vector_store(embedding_function=embeddings)
prompt = initialize_prompt()

documents = load_documents(DOCUMENTATION_PATH)
add_documents_to_store(vector_store, documents)

graph = build_workflow(vector_store, llm, prompt)

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if client.user in message.mentions:
        content = message.content.replace(f"<@{client.user.id}>", "").strip()

        if content:
            async with message.channel.typing():
                result = graph.invoke({"question": content})
                answer = result.get(
                    "answer", "Sorry, I could not find an answer to that question :'("
                )

            if answer == "I don't know.":
                await message.channel.send(
                    "Sorry, I could not find an answer to that question :'("
                )

            await message.channel.send(answer)
        else:
            await message.channel.send(
                "Hi friend!!! Ask me a question about Purdue Hackers and I will try to help you!"
            )


client.run(DISCORD_BOT_TOKEN)
