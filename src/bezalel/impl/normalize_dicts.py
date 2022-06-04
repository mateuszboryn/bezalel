
def normalize_dicts(records_list: list, path: list, separator=".", return_incomplete_records=True):
    """
    Normalize list of nested python dicts to a list of one-level dicts.

    Example input:
    ```
    data = [
        {
            "id": 1, "name": "John Smith",
            "pets": [
                {"id": 101, "type": "cat", "name": "Kitty", "toys": [{"name": "toy1"}, {"name": "toy2"}]},
                {"id": 102, "type": "dog", "name": "Barky", "toys": [{"name": "toy3"}]}
            ]
        },
        {
            "id": 2, "name": "Sue Smith",
            "pets": [
                {"id": 201, "type": "cat", "name": "Kitten", "toys": [{"name": "toy4"}, {"name": "toy5"}, {"name": "toy6"}]},
                {"id": 202, "type": "dog", "name": "Fury", "toys": []}
            ]
        },
    ]
    ```

    then `normalize_dicts(data, ["pets", "toys"])` would return:

    ```
    [{'id': 1, 'name': 'John Smith', 'pets.id': 101, 'pets.type': 'cat', 'pets.name': 'Kitty', 'pets.toys.name': 'toy1'},
     {'id': 1, 'name': 'John Smith', 'pets.id': 101, 'pets.type': 'cat', 'pets.name': 'Kitty', 'pets.toys.name': 'toy2'},
     {'id': 1, 'name': 'John Smith', 'pets.id': 102, 'pets.type': 'dog', 'pets.name': 'Barky', 'pets.toys.name': 'toy3'},
     {'id': 2, 'name': 'Sue Smith', 'pets.id': 201, 'pets.type': 'cat', 'pets.name': 'Kitten', 'pets.toys.name': 'toy4'},
     {'id': 2, 'name': 'Sue Smith', 'pets.id': 201, 'pets.type': 'cat', 'pets.name': 'Kitten', 'pets.toys.name': 'toy5'},
     {'id': 2, 'name': 'Sue Smith', 'pets.id': 201, 'pets.type': 'cat', 'pets.name': 'Kitten', 'pets.toys.name': 'toy6'},
     {'id': 2, 'name': 'Sue Smith', 'pets.id': 202, 'pets.type': 'dog', 'pets.name': 'Fury'}]
    ```

    :param records_list: list of dicts to be normalized
    :param path: list of str, name of objects in nested dicts to follow when normalizing
    :param separator: str, (defaults to "."), it will be put in names of fields of resulting dicts.
    :param return_incomplete_records: bool (defaults to True), if following the `path` fails because there is no object
        at some level, this flag indicates if that incomplete record should be returned in result list.
    :return: list of normalized dicts.
    """
    def normalize_dicts_rec(records_list: list, path: list, prefix: str = "") -> list:
        if records_list is None or len(records_list) == 0:
            records_list = [{}] if return_incomplete_records else []
        if type(records_list) != list:
            raise Exception(f"records_list is not a list at [{prefix}]")
        if len(path) == 0:
            if records_list is None:
                return []
            return [{f"{prefix}{k}": v for k,v in record.items()} for record in records_list]
        records_denormalized = []
        path_head = path[0]
        path_tail = path[1:]
        for record in records_list:
            if type(record) != dict:
                raise Exception(f"record is not a dict at [{prefix}]")
            keys_to_repeat = list(record.keys())
            if path_head in keys_to_repeat:
                keys_to_repeat.remove(path_head)
            obj_to_repeat = {f"{prefix}{k}": record[k] for k in keys_to_repeat}
            records2 = normalize_dicts_rec(record.get(path_head), path_tail, prefix=f"{prefix}{path_head}{separator}")
            for rec2 in records2:
                records_denormalized.append({**obj_to_repeat, **rec2})
        return records_denormalized
    return normalize_dicts_rec(records_list, path)
