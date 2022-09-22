# Instructions

## Initial setup

1. Add sample dataset to cluster
2. Create "default" index with all defaults on sample_mflix.movies
3. Create autocomplete index:
```
{
  "mappings": {
    "dynamic": true,
    "fields": {
      "title": [
        {
          "foldDiacritics": false,
          "maxGrams": 15,
          "minGrams": 2,
          "tokenization": "edgeGram",
          "type": "autocomplete"
        }
      ]
    }
  }
}
```
4. Create facet index:
```
{
  "mappings": {
    "dynamic": false,
    "fields": {
      "directors": {
        "type": "stringFacet"
      },
      "year": {
        "type": "number"
      },
      "released": {
        "type": "date"
      }
    }
  }
}
```



5. Example queries in `Search Examples.ipynb`.