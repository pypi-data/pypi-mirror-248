#!/usr/bin/env python
import os, re, json
import openai
import discord
from discord.ext import commands
from math import floor

from .initialize import INIT_BOT_CONFIG, init_structure, init_bot_config, init_bot_prompt
from .conversation import Conversation
from .tokenGPT import TokenGPT
from .message_handlers import handle_greetings, handle_common_queries, handle_url_ask
from .utils import read_yaml, read_text, find_exact_word, log_error

class PFDiscord:
    ######################
    ### INITIALIZATION ###
    ######################
    def __init__(self,
        bot_owner      = INIT_BOT_CONFIG['bot_owner'],
        bot_nickname   = INIT_BOT_CONFIG['bot_nickname'],
        chat_model     = INIT_BOT_CONFIG['chat_model'],
        url_model      = INIT_BOT_CONFIG['url_model'],
        token_limit    = INIT_BOT_CONFIG['token_limit'],
        persona_temp   = INIT_BOT_CONFIG['persona_temp'],
        persona_prompt = INIT_BOT_CONFIG['persona_prompt']
    ):
        # First provide the main structure if not already there
        init_structure()

        # Discord bot configuration
        self.owner = bot_owner.lower()
        self.bot_nickname = bot_nickname
        self.started = False
        self.GPT_online = False
        self.error_log = os.path.join(os.environ['PFDISCORD_APP_PATH'], 'errorlogs', 'error.log')
        self.token_warning = {} # Determines whether user has reached token limit by OpenAI model
        self.conversations = {} # Provides Conversation class per user based on bot response

        # Get our LLM spun up with defaults if not defined by user input
        # Tokens as integers measure the length of conversation messages
        self.chatgpt = {
            'prompt'      : persona_prompt,
            'chat_model'  : chat_model,
            'url_model'   : url_model,
            'token_limit' : token_limit or TokenGPT(chat_model).max_tokens(),
            'temperature' : persona_temp or 1.0,
            'top_p'       : 0.9
        }
        # Set a rounded-down integer to prune a lengthy conversation by 500 tokens
        # Note if the upper limit is below 500, the lower limit is set to 0
        self.chatgpt['prune_threshold'] = floor(0.95 * self.chatgpt['token_limit'])
        self.chatgpt['prune_back_to']   = max(0, self.chatgpt['prune_threshold'] - 500)

        # Use OpenAI API key from environment variable
        openai.api_key = os.environ['PFDISCORD_OPENAI_API_KEY']

    # Sets PFDiscord object based on its YAML configuration and prompt files
    def set(config_file='config.yaml', prompt_file='test_personality.prmpt'):
        # First provide the main structure if not already there
        init_structure()

        # Ensure both bot configuration and prompt files are defined and readable
        config = read_yaml(init_bot_config(config_file))
        prompt = read_text(init_bot_prompt(prompt_file))

        # Check any configuration values missing and apply default values:
        for parameter, value in INIT_BOT_CONFIG.items():
            if parameter == 'persona_prompt':
                # Apply initial prompt if not defined
                if not prompt:
                    prompt = value
                    print(f"File '{prompt_file}' is empty, set default prompt '{prompt}'")
            elif parameter not in config:
                # Apply initial configuration paramter with default if not defined
                config[parameter] = value
                if value: print(f"Configuration '{parameter}' not defined, set to '{value}'")

        # Apply parameters to bot:
        return PFDiscord(
            bot_owner      = config['bot_owner'],
            bot_nickname   = config['bot_nickname'],
            chat_model     = config['chat_model'],
            url_model      = config['url_model'],
            token_limit    = config['token_limit'],
            persona_temp   = config['persona_temp'],
            persona_prompt = prompt
        )

    ###############
    ### DISCORD ###
    ###############
    def run_bot(self):
        # Change only the no_category default string and call command by '!'
        intents = discord.Intents.default()
        intents.message_content = True
        bot = commands.Bot(
            command_prefix=commands.when_mentioned_or('!'),
            description='Hosted by PFDiscord using OpenAI\'s ChatGPT.',
            help_command=commands.DefaultHelpCommand(no_category = 'Commands'),
            intents=intents
        )

        ################
        ### COMMANDS ### > Type !help to show all the commands available, starting below.
        ################
        @bot.command(help='Goes online (Admin only)')
        # Start command only runs by the 'bot_owner' specified in configuration file
        async def start(ctx: commands.Context, *args):
            uname = ctx.author.name
            if uname == self.owner:
                await ctx.send(f"Oh, hello {ctx.author.display_name}! Let me get to work!")
                self.started = True
                self.GPT_online = True
            else:
                await ctx.send("Sorry, but I'm off the clock at the moment.")

        @bot.command(help='Goes offline (Admin only)')
        # Stop command formally closes out the polling loop
        async def stop(ctx: commands.Context, *args):
            uname = ctx.author.name
            if uname == self.owner:
                self.GPT_online = False
                await ctx.send("Sure thing boss, cutting out!")
            else:
                await ctx.send("Sorry, I can't do that for you.")

        @bot.command(help='Sets your nickname (e.g. "!nick B0b #2")')
        # Let bot know to call the user by a different name other than the Discord user name
        # Must follow the format of "/nick <nickname>" using regular expression
        async def nickname(ctx: commands.Context, *args: str):
            nickname = (' '.join(args)).strip()
            if nickname != '':
                prompt = f"Please refer to me by my nickname, {nickname}, rather than my user name."
                await ctx.send(prompt)
            else:
                await ctx.send("Please provide a valid nickname after the command like \"/nick B0b #2\".")

        @bot.command(help='Clears your conversations')
        # Remove the whole conversation including past session logs for peace of mind
        async def forget(ctx: commands.Context, *args):
            uname = ctx.author.name
            if uname in self.conversations:
                self.conversations[uname].clear_interaction()
                del self.conversations[uname] # Delete object as well
                await ctx.send("My memories of all our conversations are wiped!")
            else:
                await ctx.send(
                    "My apologies, but I don't recall any conversations with you, or you"
                    " already asked me to forget about you. Either way, nice to meet you!"
                )

        ##############
        ### EVENTS ###
        ##############
        @bot.event
        # When the Discord bot is up and logged in, do commands
        async def on_ready():
            # Running with API gives us the Discord bot name for free
            self.bot_name = bot.user.name
            self.error_log = self.error_log.replace('error.log', f'PFDiscord-{self.bot_name}-error.log')
            self.bot_initials = ''.join([word[0] for word in self.bot_name.replace(' ', '_').split('_')]).upper()
            print(f"Logged in as {self.bot_name} ({bot.user.id})")

        @bot.event
        # If received a user message, handle command or response
        async def on_message(message):
            # Ignore messages from the bot itself
            if message.author == bot.user:
                return
            # Handle commands (must start with !) or process message
            if re.search(r'^\![\S]+', message.content):
                await bot.process_commands(message)
            else:
                await handle_message(message)

        @bot.event
        # Any Discord-related errors are reported to a file
        async def on_error(error, *args, **kwargs):
            log_error(error, 'Discord', self.error_log)

        @bot.event
        # Any Discord command errors are reported to a file, unless a command was mistyped
        # Source: https://www.pythondiscord.com/pages/guides/python-guides/proper-error-handling/
        async def on_command_error(ctx: commands.Context, error):
            if isinstance(error, commands.CommandNotFound):
                await ctx.send(f"{error}! Type \"!help\" for a list of commands.")
            else:
                log_error(error, 'Discord-Command', self.error_log)

        # Handles the Discord side of the message, discerning between Private and Group conversation
        async def handle_message(message):
            message_type: str = message.channel.type.name # Private or Group Chat
            message_text: str = message.content
            message_print = f"User {message.author.name} in {message_type} channel ID {message.channel.id}"

            # If it's a group text, only reply if the bot is named
            # The real magic of how the bot behaves is in tele_handle_response()
            if message_type == 'text':
                if (
                    find_exact_word(self.bot_name, message_text) or
                    find_exact_word(self.bot_nickname, message_text) or
                    find_exact_word(self.bot_initials, message_text)
                ):
                    print(message_print)
                    message.content = message.content.replace(self.bot_name, '').strip()
                    response: str = await handle_response(message)
                elif bot.user.mentioned_in(message):
                    print(message_print)
                    response: str = await handle_response(message)
                else:
                    return
            elif message_type == 'private':
                print(message_print)
                response: str = await handle_response(message)
            else:
                return
            await message.reply(response, mention_author=True)

        # Provides the appropriate response to the user's message
        async def handle_response(message):
            # Before we handle messages, ensure a user did !start us
            # Starting ensures we get some kind of user account details for logging
            not_started_reply = "I'd love to chat, but please wait as I haven't started up yet!"
            if not self.started:
                return not_started_reply

            # For a new session, track if the user has conversed with the Discord bot before
            # Username is consistent across restarts and different conversation instances
            uname = message.author.name
            if uname not in self.conversations:
                self.conversations[uname] = Conversation(
                    uname,
                    self.bot_name,
                    self.chatgpt['prompt'],
                    self.chatgpt['chat_model']
                )
                # If there are past conversations via logs, load by 50% threshold of tokens
                self.conversations[uname].get_past_interaction(
                    floor(self.chatgpt['prune_threshold'] / 2)
                )

            # Add the user's message to our conversation
            self.conversations[uname].add_user_message(message.content)

            # Check if the user is asking about a [URL]
            url_match = re.search(r'\[http(s)?://\S+]', message.content)

            # Form the assistant's message based on low level easy stuff or send to GPT
            # OpenAI relies on the maximum amount of tokens a ChatGPT model can support
            response = not_started_reply
            if handle_greetings(message.content):
                response = handle_greetings(message.content)
            elif handle_common_queries(message.content):
                response = handle_common_queries(message.content)
            elif url_match:
                # URL content is passed into another model to summarize (GPT-4 preferred)
                await message.reply("Sure, give me a moment to look at that URL...", mention_author=True)
                response = await handle_url_ask(message.content, self.chatgpt['url_model'])
            elif self.GPT_online:
                # This is essentially the transition point between quick Discord replies and GPT
                response = self.gpt_completion(uname)['choices'][0]['message']['content'].strip()

            # Calculate the total token count of our conversation messages via tiktoken
            token_count = self.conversations[uname].get_message_token_count()

            # If the user is getting closer to the bot's token threshold, warn the first time
            if token_count > self.chatgpt['prune_back_to'] and uname not in self.token_warning:
                response += ("\n\n"
                    "By the way, our conversation will soon reach my token limit, so I may"
                    " start forgetting some of our older exchanges. Would you like me to"
                    " summarize our conversation so far to keep the main points alive?"
                )
                self.token_warning[uname] = True

            # Add assistant's message to the user's conversation
            self.conversations[uname].add_assistant_message(response)

            # Truncate older messages if the conversation is above the bot's token threshold
            if token_count > self.chatgpt['prune_threshold']:
                self.conversations[uname].prune_conversation(self.chatgpt['prune_back_to'])

            return response

        #######################
        ### RUN DISCORD BOT ###
        #######################
        print("--- PFDiscord Start ---")
        bot.run(os.environ['PFDISCORD_DISCORD_API_KEY'])
        print("--- PFDiscord Ended ---")

    ##############
    ### OPENAI ###
    ##############
    # Read the GPT Conversation so far
    @staticmethod
    def gpt_read_interactions(file_path: str):
        with open(file_path, 'r') as interaction_log:
            lines = interaction_log.readlines()
        formatted_messages = [json.loads(line) for line in lines]
        return formatted_messages

    # Get the OpenAI Chat Completion response based on bot configuration
    def gpt_completion(self, uname: str):
        try:
            response = openai.ChatCompletion.create(
                model       = self.chatgpt['chat_model'],
                messages    = self.conversations[uname].messages,
                temperature = self.chatgpt['temperature'],
                top_p       = self.chatgpt['top_p']
            )
            return response
        except openai.error.AuthenticationError as e:
            # Handle authentication error
            log_error(e, error_type='OpenAI-Authentication', error_filename=self.error_log)
        except openai.error.InvalidRequestError as e:
            # Handle invalid request error
            if re.search(r'maximum context.+reduce the length', e.user_message):
                # Remove older messages and try again since the model's maximum token limit reached 
                print(f"Response to {uname} reached maximum context length, pruning conversation")
                self.conversations[uname].prune_conversation(self.chatgpt['prune_back_to'])
                return self.gpt_completion(uname)
            else:
                # Another error is actually invalid to investigate 
                log_error(e, error_type='OpenAI-InvalidRequest', error_filename=self.error_log)
        except openai.error.APIConnectionError as e:
            # Handle API connection error
            log_error(e, error_type='OpenAI-APIConnection', error_filename=self.error_log)
        except openai.error.OpenAIError as e:
            # Handle other OpenAI-related errors
            log_error(e, error_type='OpenAI-Other', error_filename=self.error_log)
        except Exception as e:
            # Catch any other unexpected exceptions
            log_error(e, error_type='Other', error_filename=self.error_log)
