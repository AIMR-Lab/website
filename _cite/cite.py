"""
cite process to convert sources and metasources into full citations
"""

import traceback
from importlib import import_module
from pathlib import Path
from dotenv import load_dotenv
from util import *

# load environment variables
load_dotenv()

# error flag
error = False

# output citations file
output_file = "_data/citations.yaml"

log()

log("Compiling sources")

# compiled list of sources
sources = []

# in-order list of plugins to run
plugins = ["google-scholar", "pubmed", "orcid", "sources"]

# loop through plugins
for plugin in plugins:
    # convert into path object
    plugin = Path(f"plugins/{plugin}.py")

    log(f"Running {plugin.stem} plugin")

    # get all data files to process with current plugin
    files = Path.cwd().glob(f"_data/{plugin.stem}*.*")
    files = list(filter(lambda p: p.suffix in [".yaml", ".yml", ".json"], files))

    log(f"Found {len(files)} {plugin.stem}* data file(s)", 1)

    # loop through data files
    for file in files:
        log(f"Processing data file {file.name}", 1)

        # load data from file
        try:
            data = load_data(file)
            # check if file in correct format
            if not list_of_dicts(data):
                raise Exception("File not a list of dicts")
        except Exception as e:
            log(e, 2, "ERROR")
            error = True
            continue

        # loop through data entries
        for index, entry in enumerate(data):
            log(f"Processing entry {index + 1} of {len(data)}, {label(entry)}", 2)

            # run plugin on data entry to expand into multiple sources
            try:
                expanded = import_module(f"plugins.{plugin.stem}").main(entry)
                # check that plugin returned correct format
                if not list_of_dicts(expanded):
                    raise Exception("Plugin didn't return list of dicts")
            # catch any plugin error
            except Exception as e:
                # log detailed pre-formatted/colored trace
                print(traceback.format_exc())
                # log high-level error
                log(e, 3, "ERROR")
                error = True
                continue

            # loop through sources
            for source in expanded:
                if plugin.stem != "sources":
                    log(label(source), 3)

                # include meta info about source
                source["plugin"] = plugin.name
                source["file"] = file.name

                # add source to compiled list
                sources.append(source)

            if plugin.stem != "sources":
                log(f"{len(expanded)} source(s)", 3)


log("Merging sources by id")

# merge sources with matching (non-blank) ids
for a in range(0, len(sources)):
    a_id = get_safe(sources, f"{a}.id", "")
    if not a_id:
        continue
    for b in range(a + 1, len(sources)):
        b_id = get_safe(sources, f"{b}.id", "")
        if b_id == a_id:
            log(f"Found duplicate {b_id}", 2)
            sources[a].update(sources[b])
            sources[b] = {}
sources = [entry for entry in sources if entry]

log(f"{len(sources)} total source(s) to cite")

log()

log("Generating citations")

# list of new citations
citations = []

# loop through compiled sources
for index, source in enumerate(sources):
    log(f"Processing source {index + 1} of {len(sources)}, {label(source)}")

    # if explicitly flagged, remove/ignore entry
    if get_safe(source, "remove", False) == True:
        continue

    # new citation data for source
    citation = {}

    # source id
    _id = get_safe(source, "id", "").strip()

    # Manubot doesn't work without an id
    if _id:
        log("Using Manubot to generate citation", 1)

        try:
            # run Manubot and set citation
            citation = cite_with_manubot(_id)

        except NotImplementedError as e:
            # Specific handling for unsupported IDs
            log(f"Manubot does not support ID: {_id}. Generating fallback citation.", 3, "WARNING")
            # Fallback: Generate minimal citation metadata
            citation = {
                "id": _id,
                "title": get_safe(source, "title", "Untitled"),
                "authors": get_safe(source, "authors", []),
                "publisher": get_safe(source, "publisher", "Unknown Publisher"),
                "date": get_safe(source, "date", ""),
                "link": get_safe(source, "link", ""),
                "description": "Generated from fallback mechanism due to unsupported ID."
            }

        except Exception as e:
            # Generic handling for all other errors
            if get_safe(source, "plugin", "") == "sources.py":
                log(f"Error generating citation for {_id}: {e}", 3, "ERROR")
                error = True
            else:
                log(f"Warning: Unable to process source ID {_id}: {e}", 3, "WARNING")
            # Skip this source in both cases
            continue

    else:
        # Handle sources without an ID
        log("Source does not have an ID. Generating minimal fallback citation.", 1, "WARNING")
        citation = {
            "title": get_safe(source, "title", "Untitled"),
            "authors": get_safe(source, "authors", []),
            "publisher": get_safe(source, "publisher", "Unknown Publisher"),
            "date": get_safe(source, "date", ""),
            "link": get_safe(source, "link", ""),
            "description": "Generated from fallback mechanism due to missing ID."
        }

    # preserve fields from input source, overriding existing fields
    citation.update(source)

    # ensure date in proper format for correct date sorting
    if get_safe(citation, "date", ""):
        citation["date"] = format_date(get_safe(citation, "date", ""))

    # add new citation to list
    citations.append(citation)

log()

log("Saving updated citations")

# save new citations
try:
    save_data(output_file, citations)
except Exception as e:
    log(e, level="ERROR")
    error = True

# exit at end, so user can see all errors in one run
if error:
    log("Error(s) occurred above", level="ERROR")
    exit(1)
else:
    log("All done!", level="SUCCESS")

log("\n")