import argparse
from datetime import datetime
import sys

# ------------------- Constants -------------------

FILETYPES = [
    'p12', 'bmp', 'xml', 'wml', 'htm', 'jar', 'odp', 'csv', 'properties', 'cs', 'sql', 'conf', 'py', 'mp4', 'js',
    'key', 'aac', 'xps', 'ppt', 'pem', 'pub', 'bak', 'cc', 'msg', 'flac', 'cer', 'cpp', '3gp', 'xlsx', 'csv.gz',
    'tar.bz2', 'kmz', 'jsp', 'tif', 'txt', 'avi', 'ods', 'html', 'asp', 'sh', 'tar', 'markdown', 'dotx', 'bash', 'h',
    'wav', 'java', 'cpl', 'ott', 'bat', 'eml', 'sql.zip', 'class', 'webp', 'zsh', 'chm', 'ps', 'c', 'shtml', 'tex',
    'pl', 'm4a', 'txt.gz', 'xltx', 'pdf', 'doc', 'epub', 'epub.zip', 'aspx', 'rb', 'log.gz', 'cxx', 'yaml', 'gz',
    'hpp', 'zip', 'xml.gz', 'md', 'text', 'dot', 'json', 'cfg', 'wps', 'mht', 'rtf', 'mp3', 'cab', 'dmg', 'svg', 'hwp',
    'yml', 'tiff', 'mov', 'sql.gz', 'wap', 'xls', 'vsdx', 'wmv', 'kml', 'docx', 'docm', 'gpx', 'pfx', 'dox', 'iso',
    'xlsm', 'apk', 'xlt', 'odt', 'tar.gz', 'bas', 'backup', 'pptx', 'php', 'exe', 'log'
]

IMAGES = ['BMP', 'GIF', 'JPEG', 'PNG', 'WebP', 'SVG', 'AVIF']

VIDEOS = [
    '3GP', '3G2', 'ASF', 'AVI', 'DivX', 'M2V', 'M3U', 'M3U8', 'M4V', 'MKV', 'MOV', 'MP4', 'MPEG', 'OGV',
    'QVT', 'RAM', 'RM', 'VOB', 'WebM', 'WMV', 'XAP'
]

ADVANCED_DORKS = [
    'intitle:"index of"', 'inurl:login', 'ext:sql', 'ext:xml', 'ext:conf', 'intitle:"admin login"', 'inurl:wp-content',
    'inurl:config', 'intext:"password"', 'inurl:dashboard'
]

# ------------------- Dork Generator -------------------

def generate_dorks(domains, category):
    targets = {
        "filetypes": FILETYPES,
        "images": IMAGES,
        "videos": VIDEOS,
        "advanced": ADVANCED_DORKS
    }

    if category not in targets:
        raise ValueError("Invalid category selected.")

    dorks = []
    for domain in domains:
        for dork in targets[category]:
            if category == "advanced":
                query = f'site:{domain} {dork}'
            else:
                query = f'site:{domain} filetype:{dork}'
            dorks.append(query)

    return dorks

# ------------------- Save Output -------------------

def save_output(dorks, output_path, html=False):
    timestamp = f"Dork list generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    if not html:
        with open(output_path, "w") as f:
            f.write(f"# {timestamp}\n\n")
            for d in dorks:
                f.write(d + "\n")
    else:
        with open(output_path, "w") as f:
            f.write(f"<html><body><h2>{timestamp}</h2><ul>")
            for d in dorks:
                link = f"https://www.google.com/search?q={d}"
                f.write(f'<li><a href="{link}" target="_blank">{d}</a></li>\n')
            f.write("</ul></body></html>")

# ------------------- Main Function -------------------

def main():
    parser = argparse.ArgumentParser(description="🔍 AutoDork - Google Dork Generator Tool")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--domain", help="Target domain")
    group.add_argument("--input-file", help="File containing multiple domains (one per line)")

    parser.add_argument("--category", choices=["filetypes", "images", "videos", "advanced"], required=True,
                        help="Dork category to generate")
    parser.add_argument("--output", default="dorks.txt", help="Output file path")
    parser.add_argument("--html", action="store_true", help="Generate HTML with clickable links")

    try:
        args = parser.parse_args()
    except SystemExit as e:
        print("\n❗ Error: Missing or incorrect arguments.\n")
        parser.print_help()
        sys.exit(1)

    # Read domain(s)
    if args.input_file:
        try:
            with open(args.input_file, "r") as f:
                domains = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"❗ Error: File '{args.input_file}' not found.")
            sys.exit(1)
    else:
        domains = [args.domain]

    # Generate and save
    try:
        dorks = generate_dorks(domains, args.category)
        save_output(dorks, args.output, html=args.html)
        print(f"\n✅ Generated {len(dorks)} dorks for {len(domains)} domain(s). Output saved to: {args.output}")
    except Exception as e:
        print(f"❗ Error: {e}")
        sys.exit(1)

# ------------------- Run -------------------

if __name__ == "__main__":
    main()
