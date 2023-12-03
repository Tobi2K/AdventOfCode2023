import sys
sys.path.insert(0, "")  # noqa

def get_file_as_lines(path):
    with open(path, 'r') as f:
        tmp_lines = f.readlines()
        lines = []
        for line in tmp_lines:
            lines.append(line.replace('\n', ''))
        return lines