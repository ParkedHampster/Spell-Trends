#!/bin/bash

URI=$(curl https://api.scryfall.com/bulk-data/ | jq '.data[3].download_uri' -r)
echo "Downloading Scryfall data from ... $URI"
wget "$URI"

echo "Downloading MtGJSon files ..."

PRINTINGSURI="https://mtgjson.com/api/v5/AllPrintings.json"
echo "Downloading AllPrintings from $PRINTINGSURI"
wget "$PRINTINGSURI"

PRICESURI="https://mtgjson.com/api/v5/AllPrices.json"
echo "Downloading AllPrices from $PRICESURI"
wget "$PRICESURI"

echo "All files successfully downloaded."

