from pprint import pprint


def get_asset(symbol, base_asset):
    symbol = symbol.strip()
    base_asset = base_asset.strip()
    if base_asset and symbol.endswith(base_asset):
        asset = symbol[0:-len(base_asset)]
        return asset
    else:
        return symbol


def eprint(data, length=2):
    """
    Formats and prints the given data in a structured way, compatible with both list and dict types in 'data' field.
    Includes "... ..." to indicate more items in the list.

    Args:
    data (dict): The data to be formatted and printed.
    """
    try:
        texts = []
        texts.append("{")
        for key, value in data.items():
            if key == "data":
                texts.append(f" '{key}': [\n")
                # Check if the first item in data is a list or a dict to determine the format
                if isinstance(value[0], dict):
                    # Handling dict format
                    for i, item in enumerate(value):
                        if i == length:  # For the second entry, add ...
                            texts.append("          ... ...\n")
                            break
                        texts.append("          {\n")
                        for sub_key, sub_value in item.items():
                            texts.append(f"           '{sub_key}': {repr(sub_value)},\n")

                        texts.append("          },\n")
                else:
                    # Handling list format
                    for i, item in enumerate(value):
                        if i == length:  # For the second entry, add ...
                            texts.append("          ... ...\n")
                            break
                        texts.append("          [\n")
                        for j, elem in enumerate(item):
                            end_char = "," if j < len(item) - 1 else ""
                            texts.append(f"           {repr(elem)}{end_char}\n")
                        texts.append("          ],\n")
                texts.append("         ]\n")
            else:
                if key == 'code':
                    texts.append(f"'{key}': {repr(value)},\n")
                elif key == 'msg':
                    texts.append(f" '{key}': {repr(value)},")
                else:
                    texts.append(f" '{key}': {repr(value)},\n")

        texts.append("}")
        print(''.join(texts))
    except:
        pprint(data)
