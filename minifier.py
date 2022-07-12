import collections
import json
import re


def encode(text):
    text = text.replace("\\", "\\\\").replace("$", "\\$")
    manifest = []
    for length in range(len(text) // 2, 3, -1):
        fixed = re.sub(r"\$(\d)+;", "", text)

        substrings = (
            fixed[i:i + length]
            for i in range(0, len(fixed) - length + 1)
        )

        counts = collections.Counter(substrings)

        for substring in filter(lambda key: counts[key] > 1, counts):
            if substring in text:
                text = text.replace(substring, f"${len(manifest)};")
                manifest.append(substring)

    return text, manifest


def decode(text, manifest):
    mode = False
    escaped = False
    result = []
    index = []
    for i in text:
        if mode:
            if i == ";":
                result.append(manifest[int("".join(index))])
                index.clear()
                mode = False
                continue
            index.append(i)
        else:
            if i == "$" and escaped is False:
                mode = True
                continue
            if i == "\\" and escaped is False:
                escaped = True
                continue
            escaped = False
            result.append(i)
    return "".join(result)


def decode_string(string):
    data = string.split("\n", maxsplit=1)
    return decode(data[1], json.loads(data[0]))


def encode_string(string):
    text, manifest = encode(string)
    return json.dumps(manifest) + "\n" + text


if __name__ == '__main__':
    sample = "Hello world, world hello, hello, world"
    print(sample)
    minified = encode_string(sample)
    print(minified)
    decoded = decode_string(minified)
    print(decoded)
