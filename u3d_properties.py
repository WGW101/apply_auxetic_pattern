from itertools import groupby


def parse_properties(str_lst):
    typ = str_lst.pop()
    if typ == "bool":
        return bool(str_lst.pop())
    elif typ == "int":
        return int(str_lst.pop())
    elif typ == "double":
        return float(str_lst.pop())
    elif typ == "string":
        return str_lst.pop().strip('"')
    elif typ == "vector3d":
        return tuple(float(str_lst.pop()) for _ in range(3))
    elif typ == "box3d":
        return tuple(float(str_lst.pop()) for _ in range(6))
    elif typ == "ints":
        int_lst = []
        delim = str_lst.pop()
        assert delim == '{'
        s = str_lst.pop()
        while s != '}':
            int_lst.append(int(s))
            s = str_lst.pop()
        return int_lst
    elif typ == "doubles":
        flt_lst = []
        delim = str_lst.pop()
        assert delim == '{'
        s = str_lst.pop()
        repeat = -1
        while s != '}':
            if s == 'r':
                repeat = 0
            elif repeat == 0:
                repeat = int(s)
            elif repeat > 0:
                flt_lst.extend(float(s) for _ in range(repeat))
                repeat = -1
            else:
                flt_lst.append(float(s))
            s = str_lst.pop()
        return flt_lst
    elif typ == "table" or typ == "CSubMeshGroup":
        table = {}
        name = str_lst.pop()
        delim, name = name[0], name[1:]
        assert delim == '{'
        while name != '}':
            table[name] = parse_properties(str_lst)
            name = str_lst.pop()
        return table
    else:
        raise KeyError("Unknown type in U3D properties: '{}'".format(typ))


def format_properties(properties):
    if isinstance(properties, bool):
        return " bool " + str(properties).lower()
    elif isinstance(properties, int):
        return " int " + str(properties)
    elif isinstance(properties, float):
        return " double " + str(properties)
    elif isinstance(properties, str):
        return ' string "' + properties + '"'
    elif isinstance(properties, tuple):
        if len(properties) == 3:
            return " vector3d " + " ".join(str(x) for x in properties)
        elif len(properties) == 6:
            return " box3d " + " ".join(str(i) for i in properties)
    elif isinstance(properties, list):
        if not properties or isinstance(properties[0], int):
            return " ints { " + " ".join(str(i) for i in properties) + " }"
        elif isinstance(properties[0], float):
            grouped = [(k, len(list(g))) for k, g in groupby(properties)]
            return " doubles { " + " ".join(str(v) if l == 1 else "r {} {}".format(l, v) for v, l in grouped) + " }"
    elif isinstance(properties, dict):
        if "Children" in properties:
            typ = " CSubMeshGroup {"
        else:
            typ = " table {"
        return typ + " ".join(name + format_properties(val) for name, val in properties.items()) + " }"

