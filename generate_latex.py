import json
from pathlib import Path

# =============================
# CONFIG
# =============================

INPUT_JSON = "data/main.json"
OUTPUT_TEX = "cv.tex"


# =============================
# LATEX TEMPLATE COMPONENTS
# =============================


def latex_preamble():
    return r"""\documentclass[11pt,a4paper]{article}

% ---------- Packages ----------
\usepackage[a4paper,margin=1.8cm]{geometry}
\usepackage{enumitem}
\usepackage{titlesec}
\usepackage{hyperref}
\usepackage{xcolor}
\usepackage{parskip}

\hypersetup{
    colorlinks=true,
    urlcolor=blue
}

\setlist[itemize]{noitemsep, topsep=2pt, leftmargin=1.2em}

% ---------- Section Formatting ----------
\titleformat{\section}
{\Large\bfseries}
{}{0em}{}

\titlespacing*{\section}{0pt}{14pt}{6pt}

\newcommand{\sectionline}{
    \vspace{6pt}
    \hrule
    \vspace{10pt}
}

\newcommand{\subline}{
    \vspace{4pt}
    \hrule height 0.4pt
    \vspace{6pt}
}

\begin{document}
"""


def latex_closing():
    return r"\end{document}"


# =============================
# HELPERS
# =============================


def esc(text):
    """
    Escape LaTeX special characters.
    """
    replacements = {
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text


def header_section(meta, socials):
    name = esc(meta["name"])
    title = esc(meta["title"])

    email = socials[0]["url"]
    github = socials[1]["url"]
    linkedin = socials[2]["url"]

    return f"""
{{\\Huge \\textbf{{{name}}}}} \\\\
\\textit{{{title}}}

\\href{{{email}}}{{{esc(socials[0]["handle"])}}} \\quad
\\href{{{github}}}{{{esc(socials[1]["handle"])}}} \\quad
\\href{{{linkedin}}}{{{esc(socials[2]["handle"])}}}

\\sectionline
"""


# =============================
# SECTIONS
# =============================


def education_section(data):
    out = "\\section*{Education}\n\n"
    for i, edu in enumerate(data["academics"]["education"]):
        degree = esc(edu["degree"])
        institution = esc(edu["institution"].split(",")[0])
        years = esc(edu["years"])

        out += f"""\\textbf{{{degree}}} \\hfill {years} \\\\
{institution}
"""

        if "tag" in edu:
            out += f"\\\\\n\\textit{{{esc(edu['tag'])}}}\n"

        if i != len(data["academics"]["education"]) - 1:
            out += "\n\\subline\n\n"

    out += "\n\\sectionline\n"
    return out


def publications_section(data):
    pubs = data["academics"].get("publications", [])
    if not pubs:
        return ""

    out = "\\section*{Publications}\n\n"

    for pub in pubs:
        title = esc(pub["title"])
        venue = esc(pub["venue"])
        year = esc(pub["year_doi"])

        out += f"""\\textbf{{Journal Article}} \\\\
{title} \\\\
\\textit{{{venue}}} \\\\
{year}
"""

    out += "\n\\sectionline\n"
    return out


def conferences_section(data):
    confs = data["academics"].get("conferences", [])
    if not confs:
        return ""

    out = "\\section*{Conference Presentations}\n\n"

    for i, c in enumerate(confs):
        venue = esc(c["venue"].split("·")[0].strip())
        title = esc(c["title"])
        year = esc(c["year"])
        ctype = esc(c["type"])

        out += f"""\\textbf{{{venue}}} ({ctype}, {year}) \\\\
{title}
"""

        if i != len(confs) - 1:
            out += "\n\\subline\n\n"

    out += "\n\\sectionline\n"
    return out


def experience_section(data):
    exps = data.get("experience", [])
    if not exps:
        return ""

    out = "\\section*{Professional Experience}\n\n"

    for i, e in enumerate(exps):
        role = esc(e["role"])
        company = esc(e["company"])
        date = esc(e["date"])

        out += f"""\\textbf{{{role}}} \\hfill {date} \\\\
{company}
"""

        if e.get("highlights"):
            out += "\n\\begin{itemize}\n"
            for h in e["highlights"]:
                out += f"    \\item {esc(h)}\n"
            out += "\\end{itemize}\n"

        if i != len(exps) - 1:
            out += "\n\\subline\n\n"

    out += "\n\\sectionline\n"
    return out


def projects_section(data):
    projects = data.get("projects", [])
    if not projects:
        return ""

    out = "\\section*{Selected Projects}\n\n"

    for i, p in enumerate(projects):
        name = esc(p["name"])
        desc = esc(p["description"])
        tech = esc(p["tech"])

        out += f"""\\textbf{{{name}}} \\\\
{desc} \\\\
{tech}
"""

        if i != len(projects) - 1:
            out += "\n\\subline\n\n"

    out += "\n\\sectionline\n"
    return out


def skills_section(data):
    skills = data.get("skills", {})
    out = "\\section*{Technical Skills}\n\n"

    languages = ", ".join([esc(l["name"]) for l in skills.get("languages", [])])
    libraries = ", ".join([esc(l["name"]) for l in skills.get("libraries", [])])
    tools = ", ".join([esc(t) for t in skills.get("tools", [])])
    domains = ", ".join([esc(d) for d in skills.get("domains", [])])

    out += f"""\\textbf{{Programming:}} {languages}

\\subline

\\textbf{{Libraries:}} {libraries}

\\subline

\\textbf{{Tools:}} {tools}

\\subline

\\textbf{{Domains:}} {domains}

"""

    return out


# =============================
# MAIN
# =============================


def main():
    with open(INPUT_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    tex = ""
    tex += latex_preamble()
    tex += header_section(data["meta"], data["about"]["socials"])
    tex += education_section(data)
    tex += publications_section(data)
    tex += conferences_section(data)
    tex += experience_section(data)
    tex += skills_section(data)
    tex += latex_closing()

    Path(OUTPUT_TEX).write_text(tex, encoding="utf-8")
    print(f"Generated {OUTPUT_TEX}")


if __name__ == "__main__":
    main()
