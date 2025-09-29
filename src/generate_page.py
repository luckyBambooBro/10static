from markdown_to_blocks import markdown_to_html_node
import os, pathlib

def extract_title(markdown):
    title = markdown.split("# ")[1]
    title = title.split("\n\n")[0]
    return title

def generate_page(from_path, template_path, dst_path, basepath):
    print(f"Generating page from {from_path} to {dst_path} using {template_path}")

    with open(template_path, "r") as template_path_f:
        html_template = template_path_f.read()

    with open(from_path, "r") as from_path_f:
        md_text_str = from_path_f.read()
        html_str = markdown_to_html_node(md_text_str).to_html()
        
        html_contents = html_template.replace(
        "{{ Title }}", extract_title(md_text_str)).replace(
        "{{ Content }}", html_str).replace(
        'href="/', f'href="{basepath}'.replace(
        'src="/', f'src="{basepath}') 
        )

    dst_path = pathlib.Path(dst_path).with_suffix(".html")
    dir_path = os.path.dirname(dst_path)
    if dir_path != "":
        os.makedirs(dir_path, exist_ok=True)
    with open(dst_path, "w") as html_f:
        html_f.write(html_contents)
        print("...")
        print(f"{from_path} successfully written to {dst_path} ")

def generate_pages_recursive(dir_path_content, template_path, dst_path, basepath):
    for path in os.listdir(dir_path_content):
        if os.path.isfile(os.path.join(dir_path_content, path)):
            generate_page(
                os.path.join(dir_path_content, path),
                template_path, 
                os.path.join(dst_path, path),
                basepath)
        else:
            generate_pages_recursive(
                os.path.join(dir_path_content, path), 
                template_path, 
                os.path.join(dst_path, path))