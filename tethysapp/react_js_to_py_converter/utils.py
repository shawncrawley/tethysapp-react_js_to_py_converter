import re
import black
from pyperclip import copy as copy_to_clipboard

def rreplace(s, old, new):
    return (s[::-1].replace(old[::-1],new[::-1], 1))[::-1]

def do_py_to_js_conversion(reactjs_code, accessor):
    iter_reactpy = str(reactjs_code)
    iter_reactpy = re.sub(r"import .+\n", "", iter_reactpy)
    iter_reactpy = re.sub(r"function ([^(]+)\(([^\)]?)\) ?{", "def \\1(lib):", iter_reactpy)
    iter_reactpy = re.sub(r"export .+\n?", "", iter_reactpy)
    # Convert useState hooks
    iter_reactpy = re.sub(r"const \[([^\]]+)\] = React.useState[^\(]*([^\)]*)\);?", "\\1 = lib.hooks.use_state(\\2)", iter_reactpy)
    # Convert numbers in braces (e.g. spacing={2})
    iter_reactpy = re.sub(r"{([^}]+)}", "\\1,", iter_reactpy)
    iter_reactpy = re.sub(r"<>", "lib.html._(", iter_reactpy)
    iter_reactpy = re.sub(r"</>", ")", iter_reactpy)
    iter_reactpy = re.sub(r"([^\s=]+=\"[^\"]+\")", "\\1,", iter_reactpy)
    # Add underscore to reserved python words
    iter_reactpy = re.sub(r"(\b)as=\"", "\\1as_=\"", iter_reactpy)
    iter_reactpy = re.sub(r"(\b)for=\"", "\\1for_=\"", iter_reactpy)
    iter_reactpy = re.sub(r"(\b)type=\"", "\\1type_=\"", iter_reactpy)
    iter_reactpy = re.sub(r"(\b)id=\"", "\\1id_=\"", iter_reactpy)
    iter_reactpy = re.sub(r"={{([^}]+)}}", "=lib.Props(\\1)", iter_reactpy)
    iter_reactpy = re.sub(r"(\b\w+):", "\\1=", iter_reactpy)
    iter_reactpy = re.sub(r";\s?", "", iter_reactpy)
    iter_reactpy = re.sub(r"}", "", iter_reactpy)
    # iter_reactpy = iter_reactpy.replace("'", '"')
    iter_reactpy = iter_reactpy.replace("= ", '=')
    
    pattern = re.compile(r"<([^\s>/]+)")
    next_match_start_index = 0
    while True:
        component_match = pattern.search(iter_reactpy, next_match_start_index)
        
        if not component_match:
            break
        
        component_name = component_match.group(0)[1:]
        start_index = component_match.start()
        next_match_start_index = component_match.end()
        close_index = None
        end_index = None
        scan_str = component_match.group(0)

        for i, char in enumerate(iter_reactpy[component_match.end():], len(scan_str)):
            scan_str += char
            if ">" not in scan_str:
                # replace_str += char
                continue
            if "/>" in scan_str:
                # replace_str += ")"
                break
            if ">" in scan_str and not close_index:
                # replace_str += ")"
                close_index = i
            if f"</{component_name}" in scan_str:
                # replace_str += ")"
                break
            if "<" in scan_str:
                scan_str = scan_str[:close_index + 1] + "(" + scan_str[close_index + 1:]
                break
        end_index = start_index + i
        iter_reactpy = iter_reactpy[:start_index] + scan_str + iter_reactpy[end_index + 1:]
    iter_reactpy = re.sub(r"<([^\s>/]+)", "lib.xxx.\\1(", iter_reactpy)
    iter_reactpy = re.sub(r"</[^\s>]+>", "),", iter_reactpy)
    iter_reactpy = re.sub(r"/>", "),", iter_reactpy)
    iter_reactpy = re.sub(r">", ")", iter_reactpy)
    iter_reactpy = re.sub(r"\( ", "(", iter_reactpy)
    iter_reactpy = re.sub(r" \)", ")", iter_reactpy)
    iter_reactpy = re.sub(r", ?\)", ")", iter_reactpy)

    if "return (" in iter_reactpy:
        iter_reactpy = rreplace(iter_reactpy, ")", "")
        iter_reactpy = iter_reactpy.replace("return (", "return ")

    iter_reactpy = re.sub(r"^\s*\n", "", iter_reactpy, flags=re.MULTILINE)
    iter_reactpy = re.sub(r"return \s+", "return ", iter_reactpy, flags=re.MULTILINE)
    iter_reactpy = re.sub(r"lib\.xxx\.([^\.\(]+)\.([^\.\(]+)\(", "lib.xxx.\\1\\2(", iter_reactpy)
    iter_reactpy = re.sub(r"\((\s*[^\"\)\(]+\s*)\)", "(\"\"\"\\1\"\"\")", iter_reactpy)  # Convert html strings to python strings
    iter_reactpy = re.sub(r"\"\"\"([^\n\"]+)\"\"\"", "\"\\1\"", iter_reactpy)
    iter_reactpy = re.sub(r"(\w+)\-(\w+)=", "\\1_\\2=", iter_reactpy)
    iter_reactpy = re.sub(r"lib\.xxx\.([a-z]+)", "lib.html.\\1", iter_reactpy)
    # Handle attributes without "=" (e.g. disabled)
    iter_reactpy = re.sub(r"^(\s*)(\w+)(\s*)$", "\\1\\2=True,\\3", iter_reactpy, flags=re.MULTILINE)
    iter_reactpy = re.sub(r"\", (\w+)\)", "\", \\1=True)", iter_reactpy)
    iter_reactpy = re.sub(r"\((\w+)( \w+=\")", "(\\1=True,\\2", iter_reactpy)
    iter_reactpy = re.sub(r"\"([^\"\n\)]*)\(\"([^\"\n]*)\"\)([^\"\n]+)\"", "\"\\1(\\2)\"", iter_reactpy)
    
    iter_reactpy = iter_reactpy.replace('("lib")', "(lib)")
    iter_reactpy = iter_reactpy.replace('.xxx.', f'.{accessor or "xxx"}.')
    if iter_reactpy.strip().endswith(','):
        iter_reactpy = rreplace(iter_reactpy, ",", "")
    
    iter_reactpy = black.format_str(iter_reactpy, mode=black.FileMode())
    
    return iter_reactpy
