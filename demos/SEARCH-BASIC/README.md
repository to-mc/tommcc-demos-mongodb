# Instructions

## Initial setup

1. Add sample dataset to cluster
2. Create "default" index, with support for autocomplete on title, various faceting, and synonyms:
```
{
  "mappings": {
    "dynamic": false,
    "fields": {
      "_id": {
        "type": "ObjectId"
      },
      "directors": {
        "type": "stringFacet"
      },
      "genres": {
        "type": "stringFacet"
      },
      "released": {
        "type": "date"
      },
      "title": [
        {
          "analyzer": "lucene.english",
          "type": "string"
        },
        {
          "foldDiacritics": false,
          "maxGrams": 15,
          "minGrams": 2,
          "tokenization": "edgeGram",
          "type": "autocomplete"
        }
      ],
      "year": {
        "type": "numberFacet"
      },
      "plot": {
        "analyzer": "lucene.english",
        "type": "string"
      }
    }
  },
  "synonyms": [
    {
      "analyzer": "lucene.english",
      "name": "transportSynonyms",
      "source": {
        "collection": "transport_synonyms"
      }
    },
    {
      "analyzer": "lucene.english",
      "name": "attireSynonyms",
      "source": {
        "collection": "attire_synonyms"
      }
    }
  ]
}
```

3. Example queries in `Search Examples.ipynb`.