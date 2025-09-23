from markdown_to_blocks import markdown_to_html_node
import pprint

def extract_title(markdown):
    title = markdown.split("# ")[1]
    title = title.split("\n\n")[0]
    return title

def generate_page(from_path, template_path, dst_path):
    print(f"Generating page from {from_path} to {dst_path} using template_path")
    with open(from_path, "r") as from_path_f:
        md_text_str = from_path_f.read()
    with open(template_path, "r") as template_path_f:
        html_template = template_path_f.read()
    html_nodes = markdown_to_html_node(md_text_str)
    html_str = html_nodes.to_html()
    print(html_str)

    






generate_page("./content/index.md", "template.html", "public")