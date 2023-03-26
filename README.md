# Counter Strike: Local Defensive

This game was supposed to be a simple clone of a classic Counter Strike with both client and server side implementation.

## Dependencies

See [requirements](requirements.txt).

## How to run

In order to play the game, you need to start a server:

```python
python3 app server [ip]
```

Where `ip` represents the IP address where the server will run.
The default value can be changed in [config.py](app/utils/config.py)

Afterwards, you need to run a client instance, that will connect to the server:

```python
python3 app client [ip]
```

Where `ip` represents the IP address of your desired server.

After the desired amount of clients has connected, you can start the game from the server by typing `start`.

## Controls

### Server

The server is controlled by a simple CLI with the following commands:

`start` - starts the game with currently connected clients

`exit` - shuts the server down

`restart` - restart to *lobby* after a game is over.

`help` - lists available commands

### Client

While waiting in a lobby, clients cannot do anything.

After the game starts, the client can control his character with:

- `WASD` for movement
- `Mouse` for targetting and shooting
- `Spacebar` for using *dash* - an ability, that increases your speed for a limited amount of time

## Gameplay

Once the game starts, you're randomly assigned either to a Terrorist or a Counter-terrorist team. Your team wins once all of your enemies are dead. You can recognize your character by a blue colour, your allies are green and your enemies are red.

You can kill enemies by shooting them with bullets. However, it's not a good idea to fire as many as you can, because the bullets ricochet from the walls (and friendly fire is on).

You are have 5 lives, you can see how many you currently have in the bottom-right corner. The cooldown on your *dash* ability is represented by a shade on your character.

![screenshots](screenshots/Screenshot%20from%202023-03-26%2015-02-02.png)

## Tests

Tests of basic features can be run using `pytest`.
