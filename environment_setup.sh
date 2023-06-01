#!/bin/bash                                      

cd ./data/

URI=$(curl https://api.scryfall.com/bulk-data/ | jq '.data[3].download_uri' -r)
echo "Downloading Scryfall data from ... $URI"
wget "$URI"

echo "Renaming Scryfall data"
mv all-cards-*.json ScryfallData.json

echo "Downloading MtGJSon files ..."

PRINTINGSURI="https://mtgjson.com/api/v5/AllPrintings.json"
echo "Downloading AllPrintings from $PRINTINGSURI"
wget "$PRINTINGSURI"

PRICESURI="https://mtgjson.com/api/v5/AllPrices.json"
echo "Downloading AllPrices from $PRICESURI"
wget "$PRICESURI"

cd -

echo "All files successfully downloaded. Creating Conda ENV"

conda env create -f environment.yml

