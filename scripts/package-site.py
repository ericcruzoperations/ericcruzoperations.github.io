"""Stage only public site assets for GitHub Pages."""
from pathlib import Path
import shutil
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'_site'
OUT.mkdir(exist_ok=True)
for item in ['index.html','work.html','resume.html','styles.css','favicon.svg','sitemap.xml','robots.txt','.nojekyll','assets','samples','downloads']:
 source=ROOT/item
 if source.is_dir(): shutil.copytree(source,OUT/item,dirs_exist_ok=True)
 else: shutil.copy2(source,OUT/item)
print('Public site staged in _site')
