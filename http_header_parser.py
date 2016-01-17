import re


def parse(data):
    header = {}
    raw = data.split('\r\n\r\n')[0]
    header = parse_first_line(raw, header)
    header = parse_attributes(raw, header)
    return header

def parse_first_line(raw, header):
    first_line_end = raw.find('\n')
    first_line = raw[0 : first_line_end]
    parts = first_line.split(' ')
    
    if len(parts) != 3:
        print raw
        print parts
        return None
    
    header['method'] = parts[0].strip()
    header['route'] = parts[1].strip()
    header['protocol'] = parts[2].strip()
    return header

def parse_attributes(raw, header):
    parts = re.findall(r"(?P<name>.*?): (?P<value>.*?)\r\n", raw)
    for (key, value) in parts:
        header[key.strip()] = value.strip()
    return header
