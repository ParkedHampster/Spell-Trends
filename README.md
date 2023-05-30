# Spell-Trends

A natural language processing analysis of Magic: the
Gathering abilities as compared to their relative
prices, foil and non-foil.

![Magic: the Gathering logo](./img/MTG_Primary_LL_2c_Black_LG_V12.png)
<sup>Trademarked,
[Wizards of the Coast](https://magic.wizards.com/)
</sup>

## Preface

This project takes place over the course of several
different Jupyter notebooks. While not necessary to
understanding the process and outcomes, they are
available for review at the following locations:

1. The
[Data Preparation notebook](./1_Data_Prep.ipynb)
has all of the processes used to intake, investigate,
and clean the data frome the aforementioned sources.
2. The
[Modeling notebook](./2_Modeling.ipynb)
contains all of the steps for creating and utilizing
a few different types of models.

While the original data sources are too large to be
uploaded to GitHub, a cleaned version of the data is
available in the data folder which is used in the
second notebook.

Because of the extensive and time-consuming nature of
the modeling process, all models produced by the
original data are also provided in the pickles folder.

## Project Scope and Opportunity Potential

This project will be ongoing as new data becomes
available. The initial training data was obtained on
April 25th, 2023 from multiple sources.

This project aims to create pricing predictions for
Magic: the Gathering cards based on their abilities
or "Oracle Text" as provided. The primary benefit of
this project aims to be to inform players looking to
make informed purchasing decisions, game store owners
deciding on sales patterns, and various other
collectors et al that would be interested in the
buying, selling, and/or trading of Magic cards, with a
focus on cards coming from new sets with little to no
pricing data available.

The base understanding that this operates on is that
cards that do similar things with similar payoffs,
costs, and features can be expected to have similar
values.

Magic has a lot of different working parts, so trying
to understand and investigate what goes into the
pricing of the secondary market comes with a lot of
caveats that we'll be making an attempt at detecting.

An ability to reliably predict and work with pricing
can allow drastic improvement to informed purchasing
decisions.

## Data Sources and Authority

The main dataset for this project was obtained from
[ScryFall](https://scryfall.com/)
at
[their bulk data page](https://scryfall.com/docs/api/bulk-data),
specifically the All Cards JSON file.

Data for pricing (and the data to translate back to
Scryfall usability) was obtained from
[MtGJson](https://mtgjson.com/)
at
[their download page here](https://mtgjson.com/downloads/all-files/),
specifically the "AllPrintings" and "AllPrices" files.
This data is maintained and refreshed on a dail basis,
looking back at a 90-day period. At the sources
mentioned, there is not additional data available
retroactively.

[Scryfall](https://scryfall.com)
is one of the most robust search and sorting
databases available for Magic and is used by many
different applications. They have easily and freely
available data for most cases. This data set includes
the vast majority of features that will be utilized in
this project.

While Scryfall is very robust, the pricing data that it
provides isn't quite what we want to look at. It does
feature a price column, but it's only a snapshot of a
single day and wouldn't be insulated from price spikes.
While, in theory, this data could be collected daily
over the course of weeks or months, this also isn't
held historically. Because of this, we'll utilize
[MtGJson](https://mtgjson.com)
and the available "All Prices" data set that is
available there, as it contains prices from a 90-day
period, which should allow us to better insulate from
random spikes in prices.

In order to pair our data sets together, we need to get
the card IDs from the All Prices data set and get the
related Scryfall ID for each card. For this, we need
to use another data set from
[MtGJson](https://mtgjson.com)
that has all of the IDs that may be related to a card.

The prices available in both the Scryfall data and the
MtGJson data that we'll be looking at are prices from
[TCGPlayer](https://tcgplayer.com),
specifically the "Retail" or market prices. These
prices are made up of the mean prices of actual sales
that are made on the platform rather than the prices
that cards are listed at. Since TCGPlayer is the
largest online marketplace for Magic cards in the
United States, this data should be some of the most
accurate available.

The data from
[MtGJson](https://mtgjson.com)
also has prices from Card Kingdom, CardMarket, and some
others, but these prices are usually notoriously
higher, for foreign markets, or otherwise less
available for various reasons.

Additionally, the pricing data we're looking at will
only be for paper Magic, at least for the initial scope
of this project, though MtG:O pricing may be a target
at a later date.

As for my own authority on this data, I've been an avid
Magic player for almost a decade at this point. I've
been consistently buying and trading cards since early
2014 and have had several interpersonal relationships
with people that have made a business of the Magic
market in all categories of it.

## Data Preparation

There are several steps that need to be taken in order
for this project to be at a point where all of our data
sets are in the same format and where all of our data
is able to even be processed.

### The Need to Translate

Data from MtGJson and data from Scryfall are both
stored differently. Scryfall stores their data in a csv
format that is structured more like a standard
database, whereas MtGJson - as the name implies -
stores their data in a json format.

Additionally, MtGJson and Scryfall have different IDs
that each card uses.

Fortunately, MtGJson has Scryfall ID as an item for
each card.

*Un*fortunately, this ID isn't stored with the card
price data.

In order to put this data together, we need to match
every UUID from MtGJson with a Scryfall ID, that's what
the 'AllPrintings' file is for.

While it has a lot of other information, we'll be using
the much more standardized Scryfall data for that. All
we need is the UUID and ScryfallID tags and we can
create a simple translator.

### Pairing Pricing Data

As mentioned

<!-- Throughout this project, the features being used will
be adapted or changed over the project's course. As
these features are added or removed, justification will
be provided either before the relevant code block or
within it. -->

<!-- DATA UNDERSTANDING -->
<!-- +Describe source and properties + why they're useful -->
<!--    +Describe Data Source, why it's a good choice -->
<!--    +Present data set size -->
<!--    +Justify feature inclusions -->
<!--    Identify limitations -->

<!-- DATA PREPARATION -->
<!-- +Show how data was prepared and why -->
<!--   +Instruct on how to recreate -->
<!--   +Comments to explain code -->
<!--   +Provide valid explanations of steps -->

<!-- MODELING -->
<!-- Demonstrate an iterative approach -->
<!--   +Run/interprate a dummy model -->
<!--   -Introduce new models that improve -->
<!--   -Explicitly justify model change w/
        results and context -->
<!--    -Explicitly describe improvements -->

<!-- EVALUATION -->
<!-- +Show how well a model solves the problem -->
<!--    +Justify choice of metrics and 
        consequences -->
<!--    +Identify final model using those
        metrics -->
<!--    Discuss the implications -->

<!-- CONCLUSIONS -->
<!--  -->

<!-- GITHUB REPO -->
<!--    Conclusion summarizes implications -->

<!-- +CODE QUALITY - NOT PART OF README -->
