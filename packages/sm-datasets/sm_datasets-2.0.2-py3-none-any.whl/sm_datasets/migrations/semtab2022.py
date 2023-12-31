"""NOTE: this script is copied from a local folder and hasn't been re-tested. For now it serves as
a reference how semtab2020 dataset is converted
"""

import csv
from collections import defaultdict
from io import StringIO
from pathlib import Path
from typing import List, Mapping, Optional, Tuple, Union, cast
from zipfile import ZipFile

import orjson
import serde.csv
import serde.textline
from kgdata.wikidata.db import get_class_db, get_entity_redirection_db, get_prop_db
from kgdata.wikidata.models import WDClass, WDProperty
from loguru import logger
from rdflib import RDFS
from sm.dataset import Context, FullTable, Link
from sm.inputs.link import EntityId
from sm.misc.matrix import Matrix
from sm.namespaces.utils import KGName
from sm.namespaces.wikidata import WikidataNamespace
from sm.prelude import I, M, O
from tqdm import tqdm

from scripts.config import DATA_DIR, DATASET_DIR

PathOrStr = Union[str, Path]


def normalize_semtab2022(
    indir: PathOrStr,
    outdir: PathOrStr,
    wdredirections: Optional[Mapping[str, str]] = None,
    wdclasses: Optional[Mapping[str, WDClass]] = None,
    wdprops: Optional[Mapping[str, WDProperty]] = None,
):
    """Normalize semtab2022 dataset. This function tested on HardTablesR1.

    The original semtab2022 dataset should have the following format:

    The output will have the following format:
    descriptions
    ├── part-<num>.zip
    │   ├── <table_file_name>.json
    tables
    ├── part-<num>.zip
    │   ├── <table_file_name>.json

    Args:
        indir: the original Round_<num> directory
        outdir: the output directory
    """
    indir = Path(indir) / "Test"
    outdir = Path(outdir)

    # round number
    cea_gt = indir / f"gt/cea_gt.csv"
    cpa_gt = indir / f"gt/cpa_gt.csv"
    cta_gt = indir / f"gt/cta_gt.csv"

    cea = serde.csv.deser(cea_gt)
    cpa = serde.csv.deser(cpa_gt)
    cta = serde.csv.deser(cta_gt)

    # gather links and prop/types
    table2links = defaultdict(list)
    table2sem = defaultdict(lambda: ([], []))

    for row in cea:
        table2links[row[0]].append(row)
    for row in cpa:
        table2sem[row[0]][0].append(row)
    for row in cta:
        table2sem[row[0]][1].append(row)

    wdns = WikidataNamespace.create()
    outputs: List[Tuple[O.SemanticModel, FullTable]] = []

    cea_tables = {row[0] for row in cea}
    cta_tables = {row[0] for row in cta}

    # verifying that the target and ground truth are the same
    for i, row in enumerate(serde.csv.deser(indir / f"target/cea_target.csv")):
        if i >= len(cea) or row != cea[i][:3]:
            assert (
                row[0] not in cea_tables
            ), f"when a target entity is not in ground-truth. the whole table {row[0]} must not be in the ground-truth"
    for i, row in enumerate(serde.csv.deser(indir / f"target/cpa_target.csv")):
        assert row == cpa[i][:3]
    for i, row in enumerate(serde.csv.deser(indir / f"target/cta_target.csv")):
        if i >= len(cta) or row != cta[i][:2]:
            assert (
                row[0] not in cta_tables
            ), f"when a target column is not in ground-truth. the whole table {row[0]} must not be in the ground-truth"

    print("Number of tables:")
    print("- CEA ground-truth:", len(cea_tables))
    print("- CTA ground-truth:", len(set(row[0] for row in cta)))
    print("- CPA ground-truth:", len(cta_tables))

    # extract tables
    print("- # CSV File:", sum(1 for _ in (indir / "tables").glob("*.csv")))
    ignore_logs = []

    for file in tqdm(sorted((indir / "tables").glob("*.csv"))):
        table_id = file.stem
        with open(file, mode="r") as f:
            reader = csv.reader(f, delimiter=",")
            lst = [row for row in reader]
            header, rows = lst[0], lst[1:]
            columns = []
            for ci in range(len(header)):
                columns.append(
                    I.Column(
                        index=ci, name=header[ci], values=[row[ci] for row in rows]
                    )
                )

            table = I.ColumnBasedTable(table_id=table_id, columns=columns)
            shp = table.shape()
            links = [[[] for ci in range(shp[1])] for ri in range(shp[0])]
            for row in table2links[table_id]:
                ri, ci = int(row[1]) - 1, int(row[2])
                ent_uri = row[-1]
                links[ri][ci].append(
                    Link(
                        start=0,
                        end=len(table[ri, ci]),
                        url=None,
                        entities=[EntityId(wdns.uri_to_id(ent_uri), KGName.Wikidata)],
                    )
                )

            sm = O.SemanticModel()
            col2node = {}
            for col in table.columns:
                col2node[col.index] = sm.add_node(
                    O.DataNode(col.index, cast(str, col.name))
                )

            rels, types = table2sem[table_id]
            ignore_table = False

            for row in types:
                cid = int(row[1])
                ent_id = wdns.uri_to_id(row[-1])

                try:
                    label = get_class_readable_label(ent_id, wdredirections, wdclasses)
                except KeyError:
                    logger.error(
                        "Table {} contains unknown class {} in column {}",
                        table_id,
                        ent_id,
                        cid,
                    )
                    label = None
                    if wdclasses is not None and wdredirections is not None:
                        ignore_table = True
                        ignore_logs.append(
                            f"Ignore table {table_id} as it contains unknown class {ent_id} in column {cid}"
                        )
                        break

                class_id = sm.add_node(
                    O.ClassNode(
                        abs_uri=wdns.id_to_uri(ent_id),
                        rel_uri=wdns.get_rel_uri(wdns.id_to_uri(ent_id)),
                        approximation=False,
                        readable_label=label,
                    )
                )
                sm.add_edge(
                    O.Edge(
                        source=class_id,
                        target=col2node[cid],
                        abs_uri=str(RDFS.label),
                        rel_uri=wdns.get_rel_uri(RDFS.label),
                        approximation=False,
                        readable_label=wdns.get_rel_uri(RDFS.label),
                    )
                )
                col2node[cid] = class_id

            if ignore_table:
                continue

            for row in rels:
                pid = wdns.uri_to_id(row[-1])
                c1, c2 = int(row[1]), int(row[2])
                try:
                    label = get_prop_readable_label(pid, wdredirections, wdprops)
                except KeyError:
                    logger.error(
                        "Table {} contains unknown property {} from column {} -> {}",
                        table_id,
                        pid,
                        c1,
                        c2,
                    )
                    label = None
                    if wdprops is not None and wdredirections is not None:
                        ignore_table = True
                        ignore_logs.append(
                            f"Ignore table {table_id} as it contains unknown property {pid} from column {c1} -> {c2}"
                        )
                        break

                source_node = sm.get_node(col2node[c1])
                if not (
                    isinstance(source_node, O.ClassNode)
                    or (
                        isinstance(source_node, O.LiteralNode)
                        and source_node.datatype == O.LiteralNodeDataType.Entity
                    )
                ):
                    ignore_table = True
                    ignore_logs.append(
                        f"Ignore table {table_id} as it contains edge from column {c1} -> {c2} but {c1} is not a class or entity node"
                    )
                    break
                sm.add_edge(
                    O.Edge(
                        source=col2node[c1],
                        target=col2node[c2],
                        abs_uri=(tmp_abs_uri := wdns.id_to_uri(pid)),
                        rel_uri=wdns.get_rel_uri(tmp_abs_uri),
                        approximation=False,
                        readable_label=label,
                    )
                )

            if ignore_table:
                continue

            outputs.append(
                (sm, FullTable(table=table, context=Context(), links=Matrix(links)))
            )

    serde.textline.ser(ignore_logs, outdir / "ignore_tables.log")

    outputs = sorted(outputs, key=lambda x: x[1].table.table_id)
    (outdir / "descriptions").mkdir(exist_ok=True, parents=True)
    (outdir / "tables").mkdir(exist_ok=True, parents=True)

    batch_size = 500

    for name in ["CEA", "CPA", "CTA"]:
        # compress the content to save space, use zless, zcat to browse it
        content = (indir / f"target/{name.lower()}_target.csv").read_bytes()
        (outdir / f"{name}_targets.csv").write_bytes(content)

    counter = 0
    for i in range(0, len(outputs), batch_size):
        batch = outputs[i : i + batch_size]
        filename = f"part-{counter:04d}.zip"
        with ZipFile(outdir / "descriptions" / filename, "w") as zf:
            for sm, table in batch:
                zf.writestr(
                    table.table.table_id + ".json", data=orjson.dumps([sm.to_dict()])
                )
        with ZipFile(outdir / "tables" / filename, "w") as zf:
            for sm, table in batch:
                zf.writestr(
                    table.table.table_id + ".json", data=orjson.dumps(table.to_dict())
                )
        counter += 1


def get_prop_readable_label(
    pid: str,
    wdredirections: Optional[Mapping[str, str]] = None,
    wdprops: Optional[Mapping[str, WDProperty]] = None,
):
    if wdprops is None:
        return None

    if wdredirections is not None and pid in wdredirections:
        pid = wdredirections[pid]

    return f"{wdprops[pid].label} ({pid})"


def get_class_readable_label(
    eid: str,
    wdredirections: Optional[Mapping[str, str]] = None,
    wdclasses: Optional[Mapping[str, WDClass]] = None,
):
    if wdclasses is None:
        return None

    if wdredirections is not None and eid in wdredirections:
        eid = wdredirections[eid]

    return f"{wdclasses[eid].label} ({eid})"


if __name__ == "__main__":
    wdredirections = get_entity_redirection_db(
        DATA_DIR / "home/databases/wdentity_redirections.db", read_only=True
    )
    wdclasses = get_class_db(DATA_DIR / "home/databases/wdclasses.db", read_only=True)
    wdprops = get_prop_db(DATA_DIR / "home/databases/wdprops.db", read_only=True)

    wdclasses = wdclasses.cache()
    wdprops = wdprops.cache()
    wdredirections = wdredirections.cache()

    normalize_semtab2022(
        DATASET_DIR / "semtab2022_round1/HardTablesR1/DataSets/HardTablesR1",
        DATASET_DIR / "semtab2022_hardtable_r1",
        wdredirections,
        wdclasses,
        wdprops,
    )
