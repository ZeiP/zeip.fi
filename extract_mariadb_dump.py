#!/usr/bin/env python3
import csv
import os
import re
import sys
from pathlib import Path


CREATE_RE = re.compile(r"^CREATE TABLE `([^`]+)`")
INSERT_RE = re.compile(r"^INSERT INTO `([^`]+)` VALUES")
STRUCT_RE = re.compile(r"^-- Table structure for table `([^`]+)`")


def mysql_unescape(value):
    out = []
    i = 0
    while i < len(value):
        ch = value[i]
        if ch != "\\":
            out.append(ch)
            i += 1
            continue
        i += 1
        if i >= len(value):
            out.append("\\")
            break
        esc = value[i]
        out.append({
            "0": "\0",
            "'": "'",
            '"': '"',
            "b": "\b",
            "n": "\n",
            "r": "\r",
            "t": "\t",
            "Z": "\x1a",
            "\\": "\\",
            "%": "%",
            "_": "_",
        }.get(esc, esc))
        i += 1
    return "".join(out)


def parse_values(values_sql):
    row = []
    token = []
    in_string = False
    quoted = False
    paren_depth = 0
    i = 0
    while i < len(values_sql):
        ch = values_sql[i]
        if in_string:
            if ch == "\\" and i + 1 < len(values_sql):
                token.append(ch)
                token.append(values_sql[i + 1])
                i += 2
                continue
            if ch == "'":
                in_string = False
                i += 1
                continue
            token.append(ch)
            i += 1
            continue

        if ch == "'":
            in_string = True
            quoted = True
            i += 1
            continue
        if ch == "(":
            paren_depth += 1
            if paren_depth == 1:
                row = []
                token = []
                quoted = False
            else:
                token.append(ch)
            i += 1
            continue
        if ch == "," and paren_depth == 1:
            row.append(finalize_token(token, quoted))
            token = []
            quoted = False
            i += 1
            continue
        if ch == ")":
            paren_depth -= 1
            if paren_depth == 0:
                row.append(finalize_token(token, quoted))
                yield row
                row = []
                token = []
                quoted = False
            else:
                token.append(ch)
            i += 1
            continue
        if ch == ";" and paren_depth == 0:
            break
        if paren_depth >= 1:
            token.append(ch)
        i += 1


def finalize_token(token, quoted):
    raw = "".join(token)
    if quoted:
        return mysql_unescape(raw)
    stripped = raw.strip()
    if stripped.upper() == "NULL":
        return None
    return stripped


def column_names(create_sql):
    cols = []
    for line in create_sql.splitlines():
        stripped = line.lstrip()
        if not stripped.startswith("`"):
            continue
        match = re.match(r"`([^`]+)`", stripped)
        if match:
            cols.append(match.group(1))
    return cols


def main():
    if len(sys.argv) != 3:
        raise SystemExit("Usage: extract_mariadb_dump.py dump.sql output_dir")

    dump_path = Path(sys.argv[1])
    out_dir = Path(sys.argv[2])
    schema_dir = out_dir / "schema"
    sql_dir = out_dir / "tables_sql"
    csv_dir = out_dir / "csv"
    schema_dir.mkdir(parents=True, exist_ok=True)
    sql_dir.mkdir(parents=True, exist_ok=True)
    csv_dir.mkdir(parents=True, exist_ok=True)

    table_sql = {}
    table_schema = {}
    row_counts = {}
    insert_counts = {}
    columns = {}
    current_table = None
    current_schema_lines = []
    pending_insert_table = None
    pending_insert_lines = []

    with dump_path.open("r", encoding="utf-8", errors="replace", newline="") as source:
        for line in source:
            struct = STRUCT_RE.match(line)
            if struct:
                if current_table and current_schema_lines:
                    table_schema[current_table] = "".join(current_schema_lines)
                current_table = struct.group(1)
                current_schema_lines = [line]
            elif current_table is not None:
                current_schema_lines.append(line)
                if line.startswith("/*!40101 SET character_set_client = @saved_cs_client */;"):
                    table_schema[current_table] = "".join(current_schema_lines)
                    current_table = None
                    current_schema_lines = []

            if pending_insert_table is not None:
                pending_insert_lines.append(line)
                if line.rstrip().endswith(";"):
                    statement = "".join(pending_insert_lines)
                    table_sql.setdefault(pending_insert_table, []).append(statement)
                    insert_counts[pending_insert_table] = insert_counts.get(pending_insert_table, 0) + 1
                    values = statement.split(" VALUES", 1)[1].strip()
                    row_counts[pending_insert_table] = row_counts.get(pending_insert_table, 0) + sum(1 for _ in parse_values(values))
                    pending_insert_table = None
                    pending_insert_lines = []
                continue

            insert = INSERT_RE.match(line)
            if insert:
                pending_insert_table = insert.group(1)
                pending_insert_lines = [line]
                if line.rstrip().endswith(";"):
                    statement = "".join(pending_insert_lines)
                    table_sql.setdefault(pending_insert_table, []).append(statement)
                    insert_counts[pending_insert_table] = insert_counts.get(pending_insert_table, 0) + 1
                    values = statement.split(" VALUES", 1)[1].strip()
                    row_counts[pending_insert_table] = row_counts.get(pending_insert_table, 0) + sum(1 for _ in parse_values(values))
                    pending_insert_table = None
                    pending_insert_lines = []

    if current_table and current_schema_lines:
        table_schema[current_table] = "".join(current_schema_lines)

    all_tables = sorted(set(table_schema) | set(table_sql))
    for table in all_tables:
        schema_text = table_schema.get(table, "")
        (schema_dir / f"{table}.schema.sql").write_text(schema_text, encoding="utf-8")
        if schema_text:
            columns[table] = column_names(schema_text)
        if table in table_sql:
            (sql_dir / f"{table}.data.sql").write_text("".join(table_sql[table]), encoding="utf-8")

    with (out_dir / "schema.sql").open("w", encoding="utf-8") as schema_out:
        for table in all_tables:
            schema_out.write(table_schema.get(table, ""))
            if table_schema.get(table):
                schema_out.write("\n")

    csv_handles = {}
    writers = {}
    try:
        for table in all_tables:
            if table not in table_sql:
                continue
            handle = (csv_dir / f"{table}.csv").open("w", encoding="utf-8", newline="")
            csv_handles[table] = handle
            writers[table] = csv.writer(handle)
            if columns.get(table):
                writers[table].writerow(columns[table])

        pending_insert_table = None
        pending_insert_lines = []
        with dump_path.open("r", encoding="utf-8", errors="replace", newline="") as source:
            for line in source:
                if pending_insert_table is not None:
                    pending_insert_lines.append(line)
                    if line.rstrip().endswith(";"):
                        writer = writers.get(pending_insert_table)
                        if writer is not None:
                            statement = "".join(pending_insert_lines)
                            values = statement.split(" VALUES", 1)[1].strip()
                            writer.writerows(parse_values(values))
                        pending_insert_table = None
                        pending_insert_lines = []
                    continue

                insert = INSERT_RE.match(line)
                if insert:
                    pending_insert_table = insert.group(1)
                    pending_insert_lines = [line]
                    if line.rstrip().endswith(";"):
                        writer = writers.get(pending_insert_table)
                        if writer is not None:
                            statement = "".join(pending_insert_lines)
                            values = statement.split(" VALUES", 1)[1].strip()
                            writer.writerows(parse_values(values))
                        pending_insert_table = None
                        pending_insert_lines = []
    finally:
        for handle in csv_handles.values():
            handle.close()

    with (out_dir / "manifest.csv").open("w", encoding="utf-8", newline="") as manifest:
        writer = csv.writer(manifest)
        writer.writerow(["table", "columns", "rows", "insert_statements", "schema_file", "data_sql_file", "csv_file"])
        for table in all_tables:
            writer.writerow([
                table,
                len(columns.get(table, [])),
                row_counts.get(table, 0),
                insert_counts.get(table, 0),
                f"schema/{table}.schema.sql",
                f"tables_sql/{table}.data.sql" if table in table_sql else "",
                f"csv/{table}.csv" if table in table_sql else "",
            ])

    (out_dir / "README.txt").write_text(
        "Extracted from MariaDB/MySQL dump.\n"
        "schema.sql contains all CREATE TABLE statements.\n"
        "schema/ contains one schema file per table.\n"
        "tables_sql/ contains raw INSERT statements per table.\n"
        "csv/ contains parsed table data for tables with INSERT statements.\n"
        "manifest.csv lists tables, column counts, row counts, and artifact paths.\n",
        encoding="utf-8",
    )

    print(f"Extracted {len(all_tables)} tables into {out_dir}")
    print(f"Tables with data: {sum(1 for table in all_tables if table in table_sql)}")
    print(f"Total parsed rows: {sum(row_counts.values())}")


if __name__ == "__main__":
    main()
