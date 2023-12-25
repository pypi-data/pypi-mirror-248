[![PyPI](https://img.shields.io/pypi/v/hikari-miru)](https://pypi.org/project/hikari-miru)
[![Documentation Status](https://readthedocs.org/projects/hikari-miru/badge/?version=latest)](https://hikari-miru.readthedocs.io/en/latest/?badge=latest)

# hikari-miru

An optional component handler for [hikari](https://github.com/hikari-py/hikari), inspired by discord.py's views.

## Installation

To install miru, run the following command:

```sh
python3 -m pip install -U hikari-miru
```

To check if miru has successfully installed or not, run the following:

```sh
python3 -m miru
```

## Usage

```py
import hikari
import miru


class MyView(miru.View):

    @miru.button(label="Rock", emoji="\N{ROCK}", style=hikari.ButtonStyle.PRIMARY)
    async def rock_button(self, button: miru.Button, ctx: miru.ViewContext) -> None:
        await ctx.respond("Paper!")

    @miru.button(label="Paper", emoji="\N{SCROLL}", style=hikari.ButtonStyle.PRIMARY)
    async def paper_button(self, button: miru.Button, ctx: miru.ViewContext) -> None:
        await ctx.respond("Scissors!")

    @miru.button(label="Scissors", emoji="\N{BLACK SCISSORS}", style=hikari.ButtonStyle.PRIMARY)
    async def scissors_button(self, button: miru.Button, ctx: miru.ViewContext) -> None:
        await ctx.respond("Rock!")

    @miru.button(emoji="\N{BLACK SQUARE FOR STOP}", style=hikari.ButtonStyle.DANGER, row=1)
    async def stop_button(self, button: miru.Button, ctx: miru.ViewContext) -> None:
        self.stop() # Stop listening for interactions


bot = hikari.GatewayBot(token="...")
miru.install(bot) # Load miru and attach it to the bot instance.


@bot.listen()
async def buttons(event: hikari.GuildMessageCreateEvent) -> None:

    # Ignore bots or webhooks pinging us
    if not event.is_human:
        return

    me = bot.get_me()

    # If the bot is mentioned
    if me.id in event.message.user_mentions_ids:
        view = MyView(timeout=60)  # Create a new view
        message = await event.message.respond("Rock Paper Scissors!", components=view)
        await view.start(message)  # Start listening for interactions
        await view.wait() # Optionally, wait until the view times out or gets stopped
        await event.message.respond("Thank you for playing!")

bot.run()
```

For more examples see [examples](https://github.com/hypergonial/hikari-miru/tree/main/examples), or refer to the [documentation](https://hikari-miru.readthedocs.io/en/latest/).

## Extensions

miru has two extensions built-in:

- [`ext.nav`](https://hikari-miru.readthedocs.io/en/latest/guides/navigators.html) - To make it easier to build navigators (sometimes called paginators).
- [`ext.menu`](https://hikari-miru.readthedocs.io/en/latest/guides/menus.html) - To make it easier to create nested menus.

Check the corresponding documentation and the [examples](https://github.com/hypergonial/hikari-miru/tree/main/examples) on how to use them.

## Issues and support

For general usage help or questions, see the `#miru` channel in the [hikari discord](https://discord.gg/hikari), if you have found a bug or have a feature request, feel free to [open an issue](https://github.com/hypergonial/hikari-miru/issues/new)!

## Contributing

See [Contributing](./CONTRIBUTING.md)

## Links

- [**Documentation**](https://hikari-miru.readthedocs.io/en/latest/index.html)
- [**Examples**](https://github.com/hypergonial/hikari-miru/tree/main/examples)
- [**License**](https://github.com/hypergonial/hikari-miru/blob/main/LICENSE)
