from markdown_to_blocks import markdown_to_html_node
import os

def extract_title(markdown):
    title = markdown.split("# ")[1]
    title = title.split("\n\n")[0]
    return title

def generate_page(from_path, template_path, dst_path):
    print(f"Generating page from {from_path} to {dst_path} using {template_path}")

    with open(template_path, "r") as template_path_f:
        html_template = template_path_f.read()

    with open(from_path, "r") as from_path_f:
        md_text_str = from_path_f.read()
        html_str = markdown_to_html_node(md_text_str).to_html()
        html_contents = html_template.replace(
        "{{ Title }}", extract_title(md_text_str)).replace(
        "{{ Content }}", html_str)

    with open(os.path.join(dst_path, "html_page.html"), "w") as html_f:
        html_file = html_f.write(html_contents)
        print("...")
        print(f"{from_path} successfully written to {dst_path} ")


