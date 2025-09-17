from bs4 import BeautifulSoup

def beautify_html(input_file, output_file):
    # Llegeix l'arxiu HTML original
    with open(input_file, "r", encoding="utf-8") as f:
        raw_html = f.read()

    # Parseja i formateja amb BeautifulSoup
    soup = BeautifulSoup(raw_html, "html.parser")
    pretty_html = soup.prettify()

    # Desa el resultat en un altre arxiu
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(pretty_html)

    print(f"Arxiu bonic guardat a: {output_file}")


if __name__ == "__main__":
    # Exemple d'ús
    input_file = "dani_florit_old/kpler/igln_kpler_2.html"
    output_file = "dani_florit_old/kpler/igln_kpler_2_nice.html"
    beautify_html(input_file, output_file)
