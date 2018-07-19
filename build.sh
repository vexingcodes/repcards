#!/bin/bash
docker build . -t repcards/gen_cards
mkdir -p cards
docker run -v $(realpath ./cards):/repcards/output repcards/gen_cards
