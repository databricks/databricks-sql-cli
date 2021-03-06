# -*- coding: utf-8 -*-


def format_status(rows_length=None, cursor=None):
    return rows_status(rows_length) + statistics(cursor)


def rows_status(rows_length):
    if rows_length:
        return "%d row%s in set" % (rows_length, "" if rows_length == 1 else "s")
    else:
        return "Query OK"


def statistics(cursor):
    # if cursor:
    #     return '\nExecution time: %d ms' % (
    #             cursor.engine_execution_time_in_millis)
    # else:
    #     return ''
    # TODO(arikfr): figure if we can bring back some of this somehow
    return ""


def humanize_size(num_bytes):
    suffixes = ["B", "KB", "MB", "GB", "TB"]

    suffix_index = 0
    while num_bytes >= 1024 and suffix_index < len(suffixes) - 1:
        num_bytes /= 1024.0
        suffix_index += 1

    num = ("%.2f" % num_bytes).rstrip("0").rstrip(".")
    return "%s %s" % (num, suffixes[suffix_index])
