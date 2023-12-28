# cmdata 

> A python package to get started with CargoMetrics data products

The main goal of this python package is to get subscribers of the CargoMetrics data products up and running with our 
data as fast as possible. With that in mind we provide functions to quickly access the various datasets and perform 
the first couple of common transformations. After that, the universe is yours...  

## Commodity packs

The 
[Commodity Packs](https://aws.amazon.com/marketplace/search/results?prevFilters=%257B%2522category%2522%3A%2522d5a43d97-558f-4be7-8543-cce265fe6d9d%2522%2C%2522FULFILLMENT_OPTION_TYPE%2522%3A%2522DATA_EXCHANGE%2522%2C%2522filters%2522%3A%2522FULFILLMENT_OPTION_TYPE%2522%257D&searchTerms=cargometrics)
from CargoMetrics contain the data capturing the global maritime imports and exports of a range of commodities. The 
commodity packs come in two varieties:

* a daily point-in-time dataset
* a weekly or monthly "best information" view, derived from the daily point-in-time dataset

### The point-in-time Advanced Commodity packs

