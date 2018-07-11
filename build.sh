#!/bin/bash
docker build . -t repcards/gen_cards
mkdir -p output
docker run -v $(realpath ./output):/repcards/output repcards/gen_cards
