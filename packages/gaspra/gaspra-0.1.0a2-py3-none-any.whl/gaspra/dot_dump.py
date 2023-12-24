import io
from gaspra.suffix_automaton import build, Node


def dump(node: Node, f: io.TextIOWrapper):
    queue = [node]
    processed = set()

    while queue:
        current = queue.pop()

        if current.id not in processed:
            if current.is_terminal:
                f.write(f" {current.id}[color=red]\n")

            for token, child in current.transitions.items():
                f.write(f' {current.id} -> {child.id} [label="{token}"]\n')
                queue.append(child)

        processed.add(current.id)

    return


def dot_dump(s: str, filename: str):
    root = build(s)

    with open(filename, "w") as f:
        f.write("digraph G {\n")
        f.write("  rankdir=LR\n")
        dump(root, f)
        f.write("}\n")


if __name__ == "__main__":
    dot_dump("abc", "abc.dot")
    dot_dump("ababab", "ababab.dot")
    dot_dump("abc0cdabchi1abcabcxyz", "multiple.dot")
