"""Write a Playwright script that uploads every file changed between origin/main and HEAD
through GitHub's web upload page, one commit per folder (used when git push cannot authenticate).

  python _i18n/make_upload.py OUT.js "commit message"
"""
import json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace("\\", "/")
out, msg = sys.argv[1], sys.argv[2]
files = subprocess.check_output(["git", "diff", "--name-only", "--diff-filter=AM", "origin/main", "HEAD"],
                                cwd=ROOT, text=True).split()
groups = {}
for f in files:
    groups.setdefault(os.path.dirname(f), []).append(f)
# translated folders first, English root last, so hreflang never points at a missing page
order = sorted(groups, key=lambda d: (d == "", d == "blog", d))
jobs = []
for d in order:
    lst = groups[d]
    for i in range(0, len(lst), 20):  # GitHub rejects very large single uploads
        jobs.append([d, [ROOT + "/" + f for f in lst[i:i + 20]], "%s (%s)" % (msg, d or "root")])
js = """async (page) => {
  const jobs = %s;
  const res = [];
  for (const [dir, list, msg] of jobs) {
    await page.goto('https://github.com/kamranarshad24/kamranarshad24.github.io/upload/main' + (dir ? '/' + dir : ''), {waitUntil: 'domcontentloaded'});
    await page.waitForTimeout(2500);
    await page.locator('#upload-manifest-files-input').setInputFiles(list);
    for (let i = 0; i < 90; i++) { if (await page.locator('.js-manifest-file-entry').count() > list.length) break; await page.waitForTimeout(1000); }
    await page.waitForTimeout(2500);
    await page.fill('#commit-summary-input', msg);
    await page.locator('button[type=submit]:has-text("Commit changes")').first().evaluate(b => b.click());
    for (let i = 0; i < 45; i++) { await page.waitForTimeout(2000); if (!(await page.title()).includes('Processing') && !page.url().includes('/upload')) break; }
    res.push([dir || 'root', list.length, page.url()]);
  }
  return res;
}""" % json.dumps(jobs)
open(out, "w", encoding="utf-8", newline="\n").write(js)
print(len(files), "files in", len(jobs), "uploads")
