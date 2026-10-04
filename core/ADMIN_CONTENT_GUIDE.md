# Managing website content

Open `/admin/` and choose the matching content section. Images belong to the entry you are editing; uploading an image does not create a product automatically.

| Admin section | Content to add | Category and details |
| --- | --- | --- |
| Products & Vessels → Products | Equipment and products | Product category, sector ID, description, certifications, supply details, specification rows |
| Products & Vessels → Vessels | Vessels | Vessel type, dimensions, performance, features, delivery |
| Projects → Projects | Project case studies | Project category, client, location, year, status, description, highlights, specification rows |
| Consultancy → Consultancy services | Consultancy offerings | Consultancy category, summary, description, scope/deliverables, clients, methodology, standards, duration, advisors |
| Defence & Industry / Sectors → Sectors | Defence, Industry and other sector overviews | Sector ID, headline, description, capabilities, operators, compliance |
| Homepage, Banners & Company → Hero banner slides | Page banners | Target page, image, text, button, display order |
| Homepage, Banners & Company | Company profile, pillars and process steps | Fields specific to each section |

Create product categories under Products & Vessels → Categories and consultancy categories under Consultancy → Consultancy categories. Consultancy services automatically copy the selected category's display name when saved. Project categories and banner destinations use the existing website-supported choices.

Use **Image file** to upload from your computer, then Save. The upload takes priority over the optional image URL. The edit page shows the current image. Company profiles use **Founder image file**.

Enter deliverables, features, certifications and other list fields one item per line. For consultancy methodology, use one step per line in the format `01 | Discovery | Review project requirements`.

Existing identifiers and slugs must remain stable for existing website links. Product sector IDs should match sector records, such as `defence` or `industry`.

These changes organize the backend admin and preserve existing API data formats; they require no database migration. Deployment is required before the live admin changes. Some frontend sections currently use hardcoded data (including sector content); updating those pages to fetch the API is separate from this admin change. Adding a new category does not automatically add a link to the frontend's hardcoded navbar.
