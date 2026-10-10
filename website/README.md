# Night Shift Interactive: Website

A single-page studio site with no dependencies. Open `index.html` in a browser, or host the `website/` folder on any static host, such as GitHub Pages, Netlify or Cloudflare Pages.

- Edit the page in `src/page.html`, then run `python3 build.py`. The build inlines the logo SVGs from `branding/` and writes `index.html`.
- The contact address is a placeholder. Set `EMAIL` in `build.py` to the real inbox.
- The clock in the top bar uses the visitor's local time. The "night shift" runs from 20:00 to 06:00.
- Add milestones to the **Shift log** section in `src/page.html` as they happen.
