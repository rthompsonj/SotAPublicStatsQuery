# SotA Public Stats Query
Examples scripts for accessing and processing [Shroud of the Avatar](https://www.shroudoftheavatar.com/) public event logs.

## Info
Events within Shroud of the Avatar are logged to an internal [Elastic stack](https://www.elastic.co/).  We have taken location based events and sanitized them for public consumption.  Within this repository you will find several examples on how to query and process these events.  

We will keep logged events available for ~30 days after their entry; after which they will be purged.  We also reserve the right to revoke access to the public stack at any time.

## <a name="query"></a>Querying the stack
The primary method for retrieving data from our Elastic stack is: *Search* & *Scroll*.  *Search* is the quickest but only returns a maximum of 10,000 entries.  *Scroll* can return all entries but has been disabled for security purposes.  Due to the query limits it is helpful to narrow down your search based on the event you are interested in.  The current events we have available [listed here](#available_events).

As you can imagine, some events occur far more frequently than others.  It is for this reason that you will likely want to specify which event you are most interested in or which events you would like to exclude.  But before we get into that let us discuss the included example scripts.

### Included scripts
While there are [numerous methods](https://www.elastic.co/guide/en/elasticsearch/guide/current/_talking_to_elasticsearch.html#_restful_api_with_json_over_http) to communicate with an elastic stack; the example scripts included here are written in *python* with the only dependencies being the [*python elasticsearch client*](https://github.com/elastic/elasticsearch-py).  The primary script for using the [above mentioned methods](#query) *search* are:

* `download_quick.py`

This script accepts a number of command line arguments which can be seen by passing the `-h` flag (note that `$>` represents a terminal prompt):

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
  -tfs TIME_FRAME_START, --time-frame-start TIME_FRAME_START
                        When to start the time frame (default: "0.0")
~~~                            
Running either of these scripts should yield a `json` file with the requested events in a list.  The `--search-term` parameter takes a [Lucene query](https://lucene.apache.org/core/2_9_4/queryparsersyntax.html).  To better illustrate how this works there are a number of examples in the next section.

### Examples
Each of the following examples will return a maximum of 10,000 entries.

* Download AdventureExperienceGained events from the last 24hr period and dump them to a file called `xpgained.json`:

~~~bash
$> python download_quick.py -o xpgained.json -tf 1 -st "AdventureExperienceGained"
~~~    

* Download all events *except* experience gained from the last 48hrs:

~~~bash
$> python download_quick.py -o allButXP.json -tf 2 -st "NOT AdventureExperienceGained"
~~~

* Download player killed by player and player killed by self events:

~~~bash
$> python download_quick.py -o playerkilled.json -tf 30 -st "PlayerKilledByPlayer OR PlayerKilledBySelf"
~~~

* Download loot generated events in the past 12 hours:

~~~bash
$> python download_quick.py -o lootGenerated.json -tf 0.5 -st "LootGenerated"
~~~

* Download loot generated from *The Rise* in the past 12 hours:

~~~bash
$> python download_quick.py -o riseLoot.json -tf 0.5 -st "LootGenerated AND SceneName:The Rise"
~~~

* Download loot generated from *The Rise* in a 24hr period two days ago:

~~~bash
$> python download_quick.py -o riseLoot.json -tf 1 -tfs 2 -st "LootGenerated AND SceneName:The Rise"
~~~

## Analysis Examples
Under the `SotAPublicStatsQuery/examples` folder you will find two quick examples on how one might read in and or process the data:

1. `read_data.py` is a simple example that illustrates how one can read a json file into a python dictionary.
2. `pvp_stats.py` goes a bit more in depth by reading in `PlayerKilledByPlayer` events, aggregating them into individual kill-to-death ratios, and finally outputting an interactive html that can be displayed on a webpage.  *Note that this script requires the [pandas](http://pandas.pydata.org/) and [bokeh](http://bokeh.pydata.org/en/latest/) python packages.*

## <a name="available_events"></a>Event Reference
Currently there are a number of different location based events:

* `LocationEvent`
    * `AdventureExperienceGained`
    * `PlayerDeath`
    * `PlayerKilledByPlayer`
    * `PlayerKilledByMonster`
    * `PlayerKilledBySelf`
    * `MonsterKilledByPlayer`
    * `MonsterKilledBySelf`
    * `LootGenerated`
    * `ItemGained_Crafting`
    * `ItemGained_CrownMerchant`
    * `ItemGained_ExplodeItem_Merchant`
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

Below are some of the attributes attached to the different event types.  Note that not all event types have all of the listed attributes; a little data exploration is required to become more familiar with which event contains which attributes.

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