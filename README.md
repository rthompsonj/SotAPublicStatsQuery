# SotA Public Stats Query
Examples scripts for accessing [Shroud of the Avatar](https://www.shroudoftheavatar.com/) public event logs.

## Info
Events within Shroud of the Avatar are logged to an internal [Elastic stack](https://www.elastic.co/).  We have taken location based events and sanitized them for public consumption.  Within this repository you will find several examples on how to query and process these events.  

We will keep logged events available for ~30 days after their entry; after which they will be purged.  We also reserve the right to revoke access to the public stack at any time.

## <a name="query"></a>Querying the stack

There are two primary methods for retrieving data from our Elastic stack: *Search* & *Scroll*.  *Search* is the quickest but only return a maximum of 10,0000 entries.  *Scroll* however, will return unlimited entries at the expense of considerably more time.  For this reason it is helpful to narrow down your search based on the event you are interested in.  The current events we have available [listed here](#available_events).

As you can imagine, `PositionUpdate` occurs far more frequently than the `PlayerKilledByPlayer` event.  It is for this reason that you will likely want to specify which term you are most interested in, or terms you would like to exclude.  But before we get into that let us discuss the included example scripts.

### Included scripts
While there are [numerous methods](https://www.elastic.co/guide/en/elasticsearch/guide/current/_talking_to_elasticsearch.html#_restful_api_with_json_over_http) to communicate with an elastic stack; the example scripts included here are written in *python* with the only dependencies being the [*python elasticsearch client*](https://github.com/elastic/elasticsearch-py).  The two primary scripts for using the [above mentioned methods](#query) are:

* `download_quick.py`  (for *search*)
* `download_scroll.py`   (for *scroll*)

Each of these scripts accepts a number of command line arguments which can be seen by passing the `-h` flag:

~~~bash
$> python download_quick.py -h
usage: download_quick.py [-h] [-o OUTPUT] [-st SEARCH_TERM] [-tf TIME_FRAME]

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output file name (default: "output.json")
  -st SEARCH_TERM, --search-term SEARCH_TERM
                        Search term (default: "*")
  -tf TIME_FRAME, --time-frame TIME_FRAME
                        Time frame in days (default: "0.04")
~~~                            
Running either of these scripts should yield a `json` file with the requested events.  The `--search-term` parameter takes a [Lucene query](https://lucene.apache.org/core/2_9_4/queryparsersyntax.html).

### Examples

* Download up to 10,000 position updates from the last 24hr period and dump them to a file called `positionUpdates.json`:

~~~bash
$> python download_quick.py -o positionUpdates.json -tf 1 -st "PositionUpdate"
~~~    

* Download up to 10,000 entries of all events *except* position updates from the last 48hrs:

~~~bash
$> python download_quick.py -o allbutposition.json -tf 2 -st "NOT PositionUpdate"
~~~

* Download all player killed by player and player killed by self events in the last 30 days:

~~~bash
$> python download_scroll.py -o playerkilled.json -tf 30 -st "PlayerKilledByPlayer OR PlayerKilledBySelf"
~~~

* Download all loot generated events in the past 12 hours:

~~~bash
$> python download_scroll.py -o lootGenerated.json -tf 0.5 -st "LootGenerated"
~~~

* Download all loot generated from *The Rise* in the past 12 hours:

~~~bash
$> python download_scroll.py -o riseLoot.json -tf 0.5 -st "SceneName:The Rise"
~~~

## <a name="available_events"></a>Event Reference
Currently there are a number of different location based events. The different types of location events are:

* `LocationEvent`
    * `PositionUpdate`
    * `AdventureExperienceGained`
    * `PlayerDeath`
    * `PlayerKilledByPlayer`
    * `PlayerKilledByMonster`
    * `PlayerKilledBySelf`
    * `MonsterKilledByPlayer`
    * `MonsterKilledByMonster`
    * `MonsterKilledBySelf`
    * `LootGenerated`
    * `ItemGained_Crafting`
    * `ItemGained_CrownMerchant`
    * `ItemGained_ExplodeItem_Merchant`
    * `ItemGained_World`
    * `ItemGained_StartingChar`
    * `ItemGained_Merchant`
    * `ItemGained_LootGold`
    * `ItemGained_Merchant`
    * `ItemGained_StartingChar`
    * `ItemGained_World`
    * `ItemDestroyed_BankUpgrade`
    * `ItemDestroyed_Crafting`
    * `ItemDestroyed_CrownMerchant`
    * `ItemDestroyed_Merchant`
    * `ItemDestroyed_User`

Most share common attributes, but some may vary.  Below are some of the attributes attached to the different event types.  Note that not all event types have all of the listed attributes; a little data exploration will be required to become more familiar with which event contains which attributes.

* Archetype
* EconomyGoldDelta
* ItemId
* LocationEvent
* Price
* PricePerUnit
* Quantity
* SceneName
* timestamp
* xpos
* ypos
* zpos
* PlayerName
* Killer
* Victim