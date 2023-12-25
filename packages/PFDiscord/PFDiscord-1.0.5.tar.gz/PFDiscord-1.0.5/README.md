# Persona Forge Discord (PFDiscord)
The basic goal of this project is to create a bridge between a Discord Bot and a Large Langage Model (LLM), like ChatGPT. The interface stems from [TeLLMgramBot](https://github.com/Digital-Heresy/TeLLMgramBot), but for Discord.
* To use this library, you must have a Discord account. If you don't have one, [create one online](https://discord.com/).
* To set up a new Discord bot with "Manage Server" permissions, see this [HowToGeek link](https://www.howtogeek.com/364225/how-to-make-your-own-discord-bot/).
  * This requires priveliged message intents, which can be enabled in the Discord Developer Portal under **Bot Settings**.

## Discord Bot + LLM Encapsulation
* The Discord interface handles special commands, especially on some basic "chatty" prompts and responses that don't require LLM like "Hello".
* Tokens are used to measure the length of all conversation messages between the Discord bot assistant and the user. This is useful to:
  * Ensure the length does not go over the ChatGPT model limit. If it does, prune oldest messages to fit within the limit.
  * Remember 50% of the past conversations when starting up PFDiscord again.
* Users can also clear their conversation history for privacy.
* A URL in [square brackets] can be mentioned for interpretation.
  * Example: "What do you think of this article? [https://some_site/article]"
  * This uses another ChatGPT model, preferrably GPT-4, to support more URL content by OpenAI tokens.

## Directories
When initializing PFDiscord, the following directories get created:
* `configs` - Contains bot conifguration files.
  * `config.yaml` (can be a different name)
    * This file sets parameters for the Discord bot (its user name is given by API) and OpenAI's ChatGPT to process.
    * The parameter `url_model` is to read URL content, different than `chat_model` that the bot normally uses to interact with the user.
    * An empty `token_limit` would do the maximum amount of tokens supported by the `chat_model` (e.g. 4097 for `gpt-3.5-turbo`).
  * `tokenGPT.yaml`
    * This important YAML file contains token size parameters for every ChatGPT model possible supported by OpenAI.
    * If the first time, only `gpt-3.5-turbo` and `gpt-4` get populated, but the user can specify more models with token size parameters as needed.
* `prompts` - Contains prompt files for how the bot interacts with any user.
    * `test_personality.prmpt`
      * This is a sample prompt file as a basis to test this library.
      * The user can create more prompt files as needed for different personalities. See [OpenAI Playground](https://platform.openai.com/playground) to test some ideas.
    * `url_analysis.prmpt`
      * This is a crucial prompt file to analysis URL content in brackets `[]` in a different ChatGPT model (likely `gpt-4` or higher).
* `errorlogs`
   * Contains error log files to investigate if there are problems during the interaction.
   * User will also get notified to contact the owner.
* `sessionlogs`
  * Every conversation is stored between the Discord bot assistant and each user.
  * If a user types `!forget`, any session log files between the bot and the user will all be removed.

## API Keys
Three API keys are required for operation:
* [OpenAI](https://platform.openai.com/overview) - Drives the actual GPT AI.
* [Discord](https://discord.com/developers/applications/) - Found by creating a new bot application.
* [VirusTotal](https://www.virustotal.com/gui/home/) - Performs safety checks on URLs.

There are two ways to populate each API key: environment variables or `.key` files.

### Environment Variables
PFDiscord uses the following environment variables that can be pre-loaded with the three API keys respectively:
1. `PFDISCORD_OPENAI_API_KEY`
2. `PFDISCORD_DISCORD_API_KEY`
3. `PFDISCORD_VIRUSTOTAL_API_KEY`

During spin-up time, a user can call out `os.environ[env_var]` to set those variables, like the following example:
```
my_keys = Some_Vault_Fetch_Function()

os.environ['PFDISCORD_OPENAI_API_KEY']     = my_keys['GPTKey']
os.environ['PFDISCORD_DISCORD_API_KEY']    = my_keys['DiscordApplicationToken']
os.environ['PFDISCORD_VIRUSTOTAL_API_KEY'] = my_keys['VirusTotalToken']
```

This means the user can implement whatever key vault they want to fetch the keys at runtime, without needing key files.

### API Key Files
By default, three files are created for the user to input each API key, unless its respective environment variable is defined already as discussed before:
1. `openai.key`
2. `discord.key`
3. `virustotal.key`

## Bot Setup
This library includes an example script `test_local.py`, which uses files from the folders `configs` and `prompts` to process.
1. Ensure the previous sections are followed with the proper API keys and your Discord bot set.
2. Install this library via PIP (`pip install PFDiscord`) and then import into your project.
3. Instantiate the bot by passing in various configuration pieces needed below:
   ```
   discord_bot = PFDiscord.PFDiscord(
       bot_owner      = <Bot owner's Discord username>,
       bot_nickname   = <Bot nickname like 'Botty'>,
       chat_model     = <Conversation ChatGPT model like 'gpt-3.5-turbo'>,
       url_model      = <URL contents ChatGPT model like 'gpt-4'>,
       token_limit    = <Maximum token count set, by default chat_model max>,
       persona_temp   = <LLM factual to creative value [0-2], by default 1.0>,
       persona_prompt = <System prompt summarizing bot personality>
   )
   ```
4. Turn on PFDiscord by calling:
   ```
   discord_bot.run_bot()
   ```
5. Typing `!help` shows all available commands.
6. Only as owner, type `!start` directly to the bot to initiate user conversations.

## Resources
* See documentation from [discord.py](https://discordpy.readthedocs.io/en/stable/) for the Discord API.
* For more information on ChatGPT models like `gpt-3.5-turbo` and tokens, see the following:
  * [OpenAI model overview and maximum tokens](https://platform.openai.com/docs/models/overview).
  * [OpenAI message conversion to tokens](https://github.com/openai/openai-python/blob/main/chatml.md).
  * [OpenAI custom fine-tuning](https://platform.openai.com/docs/guides/fine-tuning).
  * [OpenAI's tiktoken library, including some helpful guides](https://github.com/openai/tiktoken/tree/main).
* [OpenAI Playground](https://platform.openai.com/playground) is a great place to test out prompts and responses.
