# lexcorpora

![Github CI](https://github.com/justmars/lexcorpora/actions/workflows/main.yml/badge.svg)

Dependency to preprocess Phil. 🇵🇭  legal corpus via [weasel](https://github.com/explosion/weasel)-based flows:

1. [lexcat-proj](https://github.com/justmars/lexcat-proj); and
2. [lexcat-multi](https://github.com/justmars/lexcat-multi)

> [!IMPORTANT]
> Requires private [corpus-assets](https://github.com/justmars/corpus-assets) folder and sqlite3 db in [citelaws-data](https://github.com/justmars/citelaws-data) to be cloned locally.

```yml
- corpus-assets: # folder structure
  - concept: # must be two-level nested patterns.json + q.txt
  - artifact: # single folder patterns.json + q.txt
  - text: # each file is a .txt
```

Each concept_dir contains subtopics:

```yml
- corpus-assets: # folder structure
  - concept: # must be two-level nested
    - political: # main subject category
        - bill_of_rights: # sub-topic
            - patterns.json # contains matcher files
            - q.txt # contains lines which can be used to query the database
```

Because of structure, it's possible to:

1. train dedicated `spancat` just for one concept for terms and patterns found in the `political` directory
2. train `textcat_multilabel` component where different concept directories are options

## Span data structures

Each `Asset` object has correlated resources found in the corpus-assets folder. There are two types of assets considered for purposes of generating rule-based span patterns:

asset | desc | resources | e.g.
-- | -- | -- | --
**concept** | arbitrary spans consisting of Philippine legal terms associated with a topic | many files stored in subtopics that need to be compiled, see folder structure |"actus reus" is a criminal law concept
**artifact** | ordinarily these would be considered entities rather, e.g. legal names and titles, but since they also overlap with other artifacts, they also need to be spans | simpler file structure, only 2 (optional) files need to be considered | "RA 1234" ought to be labeled a `STATUTE` entity and 1995, a `DATE` but it is often included in a longer entity where the spans are connected to each other, e.g. "Implementing Rules of RA 1234 of 1995"

## Prerequisite db and asset folder

This is **not included** in the package:

```py
import sqlite3
from pathlib import Path

conn = sqlite3.connect("/Users/mv/code/citelaws-builder/data/main.db")
asset_dir = Path("/Users/mv/Code/corpus-assets")
```

## Concept train data

```py
train_path, dev_path = create_corpus_dirs()
concepts = create_concept_collection(asset_dir=asset_dir)
nlp = compile_concepts_nlp(asset_dir=asset_dir)
```

This creates the following structure:

```yml
- corpus:
  - dev: # where .spacy files will be stored
    - concept-civil-contract_clauses.spacy
    - concept-civil-contract_defects.spacy
  - train:  # where .spacy files will be stored
    - concept-civil-contract_clauses.spacy
    - concept-civil-contract_defects.spacy
- lexcorpora # the /src
```

For each concept asset, generate 500 example Doc structures (if possible).

This uses an sql statement where each query consists of chunks of 3 terms (from a terminology list, see `chunk_limit`) and extracts at least 20 text fragments (see `results per query`):

```py
concepts = create_concept_collection(asset_dir=asset_dir)
nlp = compile_concepts_nlp(asset_dir=asset_dir)
for concept in concepts:
    asset: Asset = concept.value
    asset.data_to_spacy(
        nlp=nlp,
        conn=conn,
        examples_per_asset=5000,
        chunk_limit=3,
        results_per_query=100,
        train_output_dir=train_path,
        dev_output_dir=dev_path,
    )
```

## Artifact train data

Instead of compiling all Artifact assets into a single collection (see note below), can instantiate isolated nlp object and patterns and use this to create training data:

```py
for artifact in Artifact:
    asset: Asset = artifact.value  # each artifact.value is an Asset
    nlp = asset.create_asset_nlp(asset_dir=asset_dir)
    asset.data_to_spacy(
        nlp=nlp,
        conn=conn,
        examples_per_asset=10000,
        chunk_limit=1,
        results_per_query=100,
        train_output_dir=train_path,
        dev_output_dir=dev_path,
    )
```

> [!NOTE]
> Originally tried to combine artifacts with concepts but this experiment proved inaccurate. The training process was able to detect the following artifacts `title`, `money` but unable to detect `ref` and `axiom`. I can't seem to pin point the discrepancy so at this time, may be better to just use an asset-based approach for Artifacts in the meantime.
