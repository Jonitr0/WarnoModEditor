from fast_diff_match_patch import diff


def get_diff(left_file_path: str, right_file_path: str):
    # read files
    left_text = open(left_file_path).read()
    right_text = open(right_file_path).read()

    # run char-based comparison with fast_dmp
    changes = diff(right_text, left_text)

    # keep track of the current char index for both files
    current_char_left = 0
    current_char_right = 0

    # save resulting diffs as list of tuples: (start_line, length, operation)
    result = []

    # iterate through changes
    for op, chars in changes:
        # ignore same chars
        if op == "=":
            current_char_left += chars
            current_char_right += chars
        # added chars (left)
        elif op == "+":
            start = get_line_of_pos(current_char_left + 1, left_text)
            end = get_line_of_pos(current_char_left + chars, left_text)
            length = end - start + 1
            result.append((start, length, "+"))
            current_char_left += chars
        # removed chars (right)
        elif op == "-":
            start = get_line_of_pos(current_char_right + 1, right_text)
            end = get_line_of_pos(current_char_right + chars, right_text)
            length = end - start + 1
            # TODO: is this the right start index? might have to take left index
            result.append((start, length, "-"))
            current_char_right += chars

    # cleanup results
    i = 0
    while i < len(result) - 1:
        # go through tuples
        block = result[i]
        j = i + 1
        # check if following adjacent tuples with same op exist
        while j < len(result):
            inner_block = result[j]
            # merge adjacent same op tuples
            if block[2] == inner_block[2] and block[0] == inner_block[0] - block[1]:
                result[i] = (block[0], block[1] + 1, block[2])
                block = result[i]
                del result[j]
            else:
                j += 1
        i += 1

    return result


def get_line_of_pos(char_pos: int, text: str, start: int = 0) -> int:
    return start + text.count("\n", start, char_pos)


if __name__ == "__main__":
    get_diff(
        "D:\\SteamLibrary\\steamapps\\common\\WARNO\\Mods\\NitroMod\\GameData\\Generated\\Gameplay\\Gfx\\UniteDescriptor.ndf",
        "D:\\SteamLibrary\\steamapps\\common\\WARNO\\Mods\\CompareTarget\\GameData\\Generated\\Gameplay\\Gfx\\UniteDescriptor.ndf")
