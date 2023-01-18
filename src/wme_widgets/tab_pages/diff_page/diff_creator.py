from fast_diff_match_patch import diff


class DiffData:
    # where should the diff be inserted (left index)
    start = -1
    # length of the diff in lines
    length = -1
    # operation (+: left, -: right)
    op = ""
    # right_only: fetch index
    right_index = -1

    def __str__(self):
        return "start: " + str(self.start) + " length: " + str(self.length) \
               + " op: " + self.op + " r_index: " + str(self.right_index)


def get_diff(left_file_path: str, right_file_path: str):
    # read files
    left_text = open(left_file_path).read()
    right_text = open(right_file_path).read()

    # run char-based comparison with fast_dmp
    changes = diff(right_text, left_text)

    # keep track of the current char index for both files
    current_char_left = 0
    current_char_right = 0

    # save resulting diffs as list of DiffData objects
    result = []

    # iterate through changes
    for op, chars in changes:
        # ignore same chars
        if op == "=":
            current_char_left += chars
            current_char_right += chars
        # added chars (left)
        elif op == "+":
            data = DiffData()
            data.start = get_line_of_pos(current_char_left + 1, left_text)
            end = get_line_of_pos(current_char_left + chars, left_text)
            data.length = end - data.start + 1
            data.op = "+"
            result.append(data)
            current_char_left += chars
        # removed chars (right)
        elif op == "-":
            data = DiffData()
            data.right_index = get_line_of_pos(current_char_right + 1, right_text)
            end = get_line_of_pos(current_char_right + chars, right_text)
            data.length = end - data.right_index + 1
            data.op = "-"
            data.start = get_line_of_pos(current_char_left + 1, left_text)
            result.append(data)
            current_char_right += chars

    result = cleanup_result(result)
    return create_diff_blocks(result, get_line_of_pos(len(left_text) - 1, left_text))


def get_line_of_pos(char_pos: int, text: str, start: int = 0) -> int:
    return start + text.count("\n", start, char_pos)


def cleanup_result(result: list) -> list:
    i = 0
    while i < len(result) - 1:
        # go through tuples
        data = result[i]
        j = i + 1
        # check if following adjacent tuples with same op exist
        while j < len(result):
            inner_data = result[j]
            # merge adjacent same op tuples
            if data.op == inner_data.op and data.start == inner_data.start - data.length:
                result[i].length += 1
                del result[j]
            # abort loop if next same op tuple has larger start
            elif data.op == inner_data.op and data.start < inner_data.start - data.length:
                break
            else:
                j += 1
        i += 1

    return result


# context lines to be display before and after each diff block
padding = 3
# max lines that can be between to diffs for them to be in the same block
max_distance = 6


# create list of lists of tuples (line_number, op) based on given distance between diffs
def create_diff_blocks(result: list, left_len: int) -> list:
    if len(result) == 0:
        return []
    diff_blocks = []
    i = 0
    while i < len(result):
        diff_block = []
        data = result[i]
        # append forward padding
        padding_start = max(data.start - padding, 0)
        for j in range(data.start - padding_start):
            diff_block.append((padding_start + j, "="))
        append_data_to_block(data, diff_block)
        # check if next block should be appended
        k = i + 1
        while k < len(result):
            next_data = result[k]
            # don't append if block is too far away
            if next_data.start > data.start + data.length + max_distance:
                break
            # add spacing
            spacing_start = data.start + data.length
            spacing = next_data.start - spacing_start
            for l in range(spacing):
                diff_block.append((spacing_start + l, "="))
            # append block
            append_data_to_block(next_data, diff_block)
            # increase block length
            data.length += spacing + next_data.length
            # remove next_data from result
            del result[k]
            k += 1
        # append trailing padding
        padding_end = min(left_len, data.start + data.length + padding)
        for j in range(padding_end - data.start - data.length):
            diff_block.append((data.start + data.length + j, "="))
        # put diff_block in list
        diff_blocks.append(diff_block)
        i += 1
    return diff_blocks


def append_data_to_block(data: DiffData, diff_block: list):
    if data.op == "+":
        for j in range(data.length):
            diff_block.append((data.start + j, "+"))
    elif data.op == "-":
        for j in range(data.length):
            diff_block.append((data.right_index + j, "-"))


# TODO: integrate this into diff_page, fix potential bugs (e.g. incorrect length of diff blocks)
if __name__ == "__main__":
    res = get_diff("left.txt", "right.txt")
    for o in res:
        print(str(o))
