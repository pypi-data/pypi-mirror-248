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

## Language customization

Assuming familiarity with spacy:

```py
nlp.tokenizer = customize_tokenizer(nlp, tokenizer_rules)
ruler = nlp.add_pipe("span_ruler",config=span_ruler_cfg)
ruler.add_patterns(span_ruler_patterns) # Loading model with 130k pattern lines takes ~2 min.
nlp.add_pipe("add_cats_from_spans", config={"options": textcat_options})
```

> [!NOTE]
> `tokenizer_rules`, `span_ruler_cfg`, `span_ruler_patterns`, and `textcat_options` is data generated via `create_data_cfg(<corpus-assets-folder-as-str>)`

## Training data

### Concept spans

Uses `q.txt` lines to get results from the database, with results _not_ exceeding `max_segments` per `q.txt` parsed:

```py
for folder in asset_dir.glob("concept/*"):
    if folder.is_dir():
        for doc in apply_concept_q_filter(nlp, db_file, filter_path=folder, max_segments=500):
            yield doc
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

To serialize data to essential `spans` / `cats`:

```py
from pathlib import Path

from lexcorpora import Corpora

crp = Corpora(
    base_model="en_core_web_sm",
    db_file=Path().home().joinpath("code/citelaws-builder/data/main.db"),
    asset_dir=Path("/Users/mv/Code/corpus-assets"),
    output_path=Path("training/spancat-to-textcat-trainer"),
)

_ = crp.nlp # initializes
crp.annotate_artifacts(examples_per_asset=2500, results_per_query=20)
crp.annotate_concepts(examples_per_asset=200, results_per_query=25)
crp.merge_annontations()
```

This will generate .spacy files:

```yml
- corpus-assets:
  - concept
  - artifact
  - text
  - corpus: #  added structure after
    - dev:
      - _dev.spacy # compiled
      - concept-political-bill_of_rights.spacy # 20% of docs generated
    - train:
      - _train.spacy # compiled
      - concept-political-bill_of_rights.spacy # 80% of docs generated
```
