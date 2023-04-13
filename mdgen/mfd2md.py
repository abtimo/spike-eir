import argparse
from lxml import etree
from markdowngenerator import MarkdownGenerator


def increment_idx():
    global idx
    global column1h
    global column2h
    global column3h
    idx = idx + 1

    if len(table) <= idx:
        line = {}
        line[column1h] = ""
        line[column2h] = ""
        line[column3h] = ""
        table.append(line)


def main(mapping, mdfile):
    print("Prepare mapping")

    global theroot
    theroot = etree.parse(mapping)

    for node in theroot.xpath("/mapping/component/structure/children/component"):
        print(node.items())
        print(theroot.getpath(node))
    for component14 in theroot.findall(".//*[@kind='14']"):
        print(type(component14))
        print(component14.items())
        if component14.find(".//*[@inpkey]") is None:
            print("inpkey not found")
            global leftmost
            leftmost = component14
        else:
            print("inpkeyfound")
            global rightmost
            rightmost = component14


def find_key(thekey, idx):
    print("find_key " + thekey + " begin")
    print("idx: " + str(idx))

    # search inpkey
    print("going to search inpkey")
    if theroot.find(".//*[@inpkey='" + thekey + "']") is None:
        print("no inpkey")
    else:
        print("inpkey found")
        node_with_inpkey = theroot.find(".//*[@inpkey='" + thekey + "']")
        print(theroot.getpath(node_with_inpkey))
        name = node_with_inpkey.get("name")
        print(name)
        tollar = get_names(node_with_inpkey, "")
        table[idx][column2h] = tollar
        return node_with_inpkey

    # search vertexkey
    print("going to search vertexkey")
    if theroot.find(".//vertex[@vertexkey='" + thekey + "']") is None:
        print("no vertexkey")
    else:
        print("vertexkey found")
        vertex = theroot.find(".//*[@vertexkey='" + thekey + "']")
        edge = vertex.xpath("./edges/edge")
        edge_vertexkey = edge[0].get("vertexkey")
        print(edge_vertexkey)
        tollar = get_names(edge[0], "")
        table[idx][column3h] = table[idx].get(column3h) + tollar
        find_key(edge_vertexkey, idx)

    # search source key
    print("going to search source key")
    if theroot.find(".//sources/datapoint[@key='" + thekey + "']") is None:
        print("no source key")
    else:
        print("source key found")
        source = theroot.find(".//sources/datapoint[@key='" + thekey + "']")
        target = source.xpath(
            "//sources/datapoint[@key='" + thekey + "']/../../targets/datapoint"
        )
        targetkey = target[0].get("key")
        print(targetkey)
        tollar = get_names(target[0], "")
        table[idx][column3h] = tollar
        find_key(targetkey, idx)

    return None


def follow_link(node):
    print("follow_link begin")

    for child in node.getchildren():
        global idx
        increment_idx()
        print(type(child))
        print(child.items())
        print(child.get("outkey"))
        print(theroot.getpath(child))
        tolarr = get_names(child, "")
        table[idx][column1h] = tolarr
        find_key(child.get("outkey"), idx)
        follow_link(child)
    return


def get_names(node, path):
    if node.get("name") is not None:
        node_name = node.get("name")
    else:
        node_name = ""
    if node_name == "document":
        return path
    to_return = "/" + node_name + path
    if node.getparent() is not None:
        to_return = get_names(node.getparent(), to_return)
    return to_return


def produce_md(mdfile, table):
    with MarkdownGenerator(
        # By setting enable_write as False, content of the file is written
        # into buffer at first, instead of writing directly into the file
        # This enables for example the generation of table of contents
        #filename="example.md", enable_write=False
        filename=mdfile, enable_write=False
    ) as doc:
        doc.addHeader(1, " Mapping - " + column2h + " " + column3h )
        #doc.writeTextLine(f'{doc.addBoldedText("This is just a test.")}')
        #doc.addHeader(2, "Second level header.")
        # table = [
        #     {"Column1": "col1row1 data", "Column2": "col2row1 data"},
        #     {"Column1": "col1row2 data", "Column2": "col2row2 data"},
        # ]

        doc.addTable(dictionary_list=table)
        #doc.writeTextLine("Ending the document....")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert .mfd file to Markdown table or validate XML against XSD schema"
    )
    parser.add_argument("--mapping", help="Path to the mapping .mfd file")
    parser.add_argument("--mdfile", help="Path to the output Markdown file")
    args = parser.parse_args()

    print(args)

if args.mapping and args.mdfile:
    # Convert a mapping file to a Markdown table
    main(args.mapping, args.mdfile)

    print("leftmost")
    print(leftmost.items())
    print("rightmost")
    print(rightmost.items())

    global column1h
    column1h = leftmost.get("name")
    global column2h
    column2h = rightmost.get("name")
    global column3h
    column3h = "mapping"

    table = []

    global idx
    idx = -1
    for document_entry in leftmost.xpath("./data/root/entry/entry/entry/entry"):
        document_entry_name = document_entry.get("name")
        tolarr = get_names(document_entry, "")
        increment_idx()
        table[idx][column1h] = tolarr
        find_key(document_entry.get("outkey"), idx)
        follow_link(document_entry)
    print("table:")
    for line in table:
        print(line)

    produce_md(args.mdfile, table)

else:
    print(
        "Error: specify either --mapping and --mdfile for mapping-to-Markdown conversion"
        "Sample: mfd2md --mapping ./MarketingExpenses2ExpReport.mfd --mdfile ./MarketingExpenses2ExpReport.md"
    )
