# Semestrální práce BI-PYT 21/22
## Použití
Pro zapnutí hry je třeba se připojit k serveru. Tento server můžete založit lokálně příkazem (za ip je potřeba doplnit vaši lokální adresu):
```
python3 app server [ip]
```
Pro připojení k serveru musíte znát jeho ip adresu. Připojíte se obdobně příkazem:
```
python3 app client [ip]
```
kde ip je adresa, na které běží server, ke kterému se chcete připojit. Po připojení musíte počkat, než hostitel zapne hru.

## Ovládání
### Server
Server je ovládán přes CLI, jakožto hostitel máte k dispozici tyto příkazy:

`start` - zapne hru s momentálně připojenými klienty

`exit` - vypne server

`restart` - po dohrání instance hry lze použít pro restartování serveru do stavu 'lobby'

`help` - vypíše seznam možných příkazů
### Hráč
Hráč se pohybuje pomocí `WASD`, míří a střílí pomocí `myši`. Má navíc dostupnou schopnost `dash`, která hráče krátkodobě zrychlí. Tato schopnost se aktivuje `mezerníkem`.

## Gameplay
Vaším cílem je porazit všechny protivníky dříve než oni porazí vás. Svou postavu rozeznáte podle modré barvy, vaši spojenci jsou zelení a vaši nepřátelé červení.

Protivníky zraníte tím, že na ně vystřelíte (pomocí myši). Dávejte ale pozor, protože kulky se odráží od stěn, takže se může klidně stát, že míříte na protivníka, ale odrazem zraníte spoluhráče.

## Potřebné knihovny
Hra pro svou funkcionalitu vyžaduje knihovnu `pyglet` a tím pádem Python verze 3.6+.

Testy základních funkcionalit spustíte příkazem `pytest`