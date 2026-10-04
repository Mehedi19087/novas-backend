import json
import os
from django.conf import settings
from django.core.management.base import BaseCommand
from catalog.models import Category, Product, ProductSpecification, Vessel
from consultancy.models import ConsultancyCategory, ConsultancyService
from projects.models import Project, ProjectSpec
from sectors.models import Sector
from site_content.models import CompanyProfile, CompanyPillar, BlueprintStep, HeroBannerSlide


class Command(BaseCommand):
    help = "Seeds initial database records from frontend datasets"

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Starting database seed..."))
        json_path = os.path.join(settings.BASE_DIR, "seed_data.json")
        if not os.path.exists(json_path):
            json_path = "/home/mehedi/Documents/novas/core/seed_data.json"

        if not os.path.exists(json_path):
            self.stdout.write(self.style.ERROR(f"Seed file not found at {json_path}"))
            return

        with open(json_path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)

        # 1. Seed Categories & Products
        self.seed_catalog(raw_data.get("products", []))

        # 2. Seed Vessels
        self.seed_vessels(raw_data.get("vessels", []))

        # 3. Seed Consultancy
        self.seed_consultancy(
            raw_data.get("consultancy_categories", []),
            raw_data.get("consultancy_services", [])
        )

        # 4. Seed Projects
        self.seed_projects(raw_data.get("projects", []))

        # 5. Seed Sectors
        self.seed_sectors(raw_data.get("sectors", []))

        # 6. Seed Site Content (Company Profile, Pillars, Blueprints, Banners)
        self.seed_site_content(raw_data.get("company_info", {}))

        self.stdout.write(self.style.SUCCESS("Database seeding completed successfully!"))

    def seed_catalog(self, products_data):
        self.stdout.write("Seeding Catalog (Categories & Products)...")

        # Map frontend category names to clean slugs
        cat_map = {
            "Defence": ("defense-tactical", "Defense & Tactical", "Shield", 1),
            "Tactical": ("defense-tactical", "Defense & Tactical", "Shield", 1),
            "Maritime": ("maritime-security", "Maritime Security", "Anchor", 2),
            "Medical": ("medical-systems", "Medical Systems", "HeartPulse", 3),
            "Agriculture": ("agriculture", "Agriculture", "Wheat", 4),
            "Agri": ("agriculture", "Agriculture", "Wheat", 4),
            "Vessels": ("marine-vessels", "Marine Vessels & Workboats", "Ship", 5),
            "Oil & Gas": ("oil-gas", "Oil & Gas Infrastructure", "Flame", 6),
            "Telecom & ICT": ("telecom-ict", "Telecom & ICT Systems", "Cpu", 7),
            "Renewable Energy": ("renewable-energy", "Renewable Energy", "Sun", 8),
        }

        # Ensure categories exist
        category_objects = {}
        for cat_name, (slug, display_name, icon, order) in cat_map.items():
            cat_obj, _ = Category.objects.get_or_create(
                slug=slug,
                defaults={
                    "name": display_name,
                    "icon": icon,
                    "sort_order": order,
                    "is_active": True,
                }
            )
            category_objects[cat_name] = cat_obj

        # Explicitly ensure Agriculture category exists
        if "Agriculture" not in category_objects:
            agri_obj, _ = Category.objects.get_or_create(
                slug="agriculture",
                defaults={
                    "name": "Agriculture",
                    "icon": "Wheat",
                    "sort_order": 4,
                    "is_active": True,
                }
            )
            category_objects["Agriculture"] = agri_obj

        # Seed products
        for p in products_data:
            cat_obj = category_objects.get(p.get("category"))
            if not cat_obj:
                cat_obj = Category.objects.first()

            product, created = Product.objects.update_or_create(
                sku=p.get("id"),
                defaults={
                    "slug": p.get("slug", p.get("id")),
                    "name": p.get("name"),
                    "category": cat_obj,
                    "sector_id": p.get("sectorId", "defence"),
                    "tagline": p.get("tagline", ""),
                    "description": p.get("description", ""),
                    "featured": p.get("featured", False),
                    "certifications": p.get("certifications", []),
                    "lead_time": p.get("leadTime", ""),
                    "origin": p.get("origin", ""),
                    "warranty": p.get("warranty", ""),
                    "image_url": p.get("imageUrl", ""),
                }
            )

            # Specs
            ProductSpecification.objects.filter(product=product).delete()
            specs_list = []
            for idx, spec in enumerate(p.get("specs", [])):
                specs_list.append(
                    ProductSpecification(
                        product=product,
                        label=spec.get("label", ""),
                        value=spec.get("value", ""),
                        sort_order=idx,
                    )
                )
            if specs_list:
                ProductSpecification.objects.bulk_create(specs_list)

        self.stdout.write(f"  -> Created/Updated {Product.objects.count()} products across {Category.objects.count()} categories.")

    def seed_vessels(self, vessels_data):
        self.stdout.write("Seeding Vessels...")
        for v in vessels_data:
            Vessel.objects.update_or_create(
                vessel_id=v.get("id"),
                defaults={
                    "slug": v.get("slug", v.get("id")),
                    "name": v.get("name"),
                    "vessel_type": v.get("vesselType", ""),
                    "tagline": v.get("tagline", ""),
                    "description": v.get("description", ""),
                    "length_overall": v.get("lengthOverall", ""),
                    "beam": v.get("beam", ""),
                    "draft": v.get("draft", ""),
                    "max_speed": v.get("maxSpeed", ""),
                    "bollard_pull": v.get("bollardPull", ""),
                    "engine_power": v.get("enginePower", ""),
                    "hull_material": v.get("hullMaterial", ""),
                    "classification_society": v.get("classificationSociety", ""),
                    "crew_capacity": v.get("crewCapacity", 1),
                    "delivery_lead_time": v.get("deliveryLeadTime", ""),
                    "image_url": v.get("imageUrl", ""),
                    "features": v.get("features", []),
                }
            )
        self.stdout.write(f"  -> Seeded {Vessel.objects.count()} vessels.")

    def seed_consultancy(self, categories_data, services_data):
        self.stdout.write("Seeding Consultancy Categories and Services...")
        cat_cache = {}
        for idx, c in enumerate(categories_data):
            cat_obj, _ = ConsultancyCategory.objects.update_or_create(
                category_id=c.get("id"),
                defaults={
                    "slug": c.get("slug", c.get("id")),
                    "name": c.get("name"),
                    "tagline": c.get("tagline", ""),
                    "description": c.get("description", ""),
                    "icon_name": c.get("iconName", "Globe2"),
                    "sort_order": idx,
                }
            )
            cat_cache[c.get("id")] = cat_obj

        for idx, s in enumerate(services_data):
            cat_obj = cat_cache.get(s.get("categoryId"))
            if not cat_obj:
                cat_obj = ConsultancyCategory.objects.first()

            ConsultancyService.objects.update_or_create(
                service_id=s.get("id"),
                defaults={
                    "slug": s.get("slug", s.get("id")),
                    "name": s.get("name"),
                    "category": cat_obj,
                    "category_name": s.get("categoryName", cat_obj.name),
                    "tagline": s.get("tagline", ""),
                    "summary": s.get("summary", ""),
                    "description": s.get("description", ""),
                    "deliverables": s.get("deliverables", []),
                    "target_clients": s.get("targetClients", []),
                    "methodology": s.get("methodology", []),
                    "standards": s.get("standards", []),
                    "duration": s.get("duration", ""),
                    "lead_advisors": s.get("leadAdvisors", ""),
                    "image_url": s.get("imageUrl", ""),
                    "featured": s.get("featured", False),
                    "sort_order": idx,
                }
            )
        self.stdout.write(f"  -> Seeded {ConsultancyCategory.objects.count()} categories and {ConsultancyService.objects.count()} services.")

    def seed_projects(self, projects_data):
        self.stdout.write("Seeding Projects...")
        for idx, prj in enumerate(projects_data):
            p_obj, _ = Project.objects.update_or_create(
                project_id=prj.get("id"),
                defaults={
                    "slug": prj.get("id"),
                    "title": prj.get("title"),
                    "category": prj.get("category", "defence"),
                    "sector_name": prj.get("sectorName", ""),
                    "client": prj.get("client", ""),
                    "location": prj.get("location", ""),
                    "year": prj.get("year", ""),
                    "image": prj.get("image", ""),
                    "summary": prj.get("summary", ""),
                    "description": prj.get("description", ""),
                    "features": prj.get("features", []),
                    "status": prj.get("status", "Delivered"),
                    "sort_order": idx,
                }
            )

            # Specs
            ProjectSpec.objects.filter(project=p_obj).delete()
            specs_list = [
                ProjectSpec(
                    project=p_obj,
                    label=spec.get("label", ""),
                    value=spec.get("value", ""),
                    sort_order=s_idx,
                )
                for s_idx, spec in enumerate(prj.get("specs", []))
            ]
            if specs_list:
                ProjectSpec.objects.bulk_create(specs_list)

        self.stdout.write(f"  -> Seeded {Project.objects.count()} projects.")

    def seed_sectors(self, sectors_data):
        self.stdout.write("Seeding Sectors...")
        for idx, s in enumerate(sectors_data):
            Sector.objects.update_or_create(
                sector_id=s.get("id"),
                defaults={
                    "slug": s.get("slug", s.get("id")),
                    "name": s.get("name"),
                    "headline": s.get("headline", ""),
                    "tagline": s.get("tagline", ""),
                    "description": s.get("description", ""),
                    "icon_name": s.get("iconName", "Shield"),
                    "accent_color": s.get("accentColor", "#f59e0b"),
                    "capabilities": s.get("capabilities", []),
                    "target_operators": s.get("targetOperators", []),
                    "compliance_standards": s.get("complianceStandards", []),
                    "image_url": s.get("imageUrl", ""),
                    "sort_order": idx,
                }
            )
        self.stdout.write(f"  -> Seeded {Sector.objects.count()} sectors.")

    def seed_site_content(self, company_info):
        self.stdout.write("Seeding Site Content...")

        # Company Profile
        CompanyProfile.objects.update_or_create(
            id=1,
            defaults={
                "name": company_info.get("name", "Nova Solutions BD"),
                "short_name": company_info.get("shortName", "NOVAS"),
                "founder": company_info.get("founder", "Mr. Raoson Alom"),
                "founder_title": company_info.get("founderTitle", "Founder & CEO, Novas"),
                "founder_image": company_info.get("founderImage", "/assets/founder.png"),
                "founded_year": company_info.get("foundedYear", "2012"),
                "founded_month": company_info.get("foundedMonth", "July 2012"),
                "team_size": company_info.get("teamSize", "24-member specialized engineering & research team"),
                "tagline": company_info.get("tagline", "Achieving excellence in the field of science, technology and procurement"),
                "subheading": company_info.get("subheading", ""),
                "address": company_info.get("address", ""),
                "phone": company_info.get("phone", "+8801711264822"),
                "landline": company_info.get("landline", "9832552"),
                "email": company_info.get("email", "info@novasbd.com"),
                "corporate_registry": company_info.get("corporateRegistry", "REG-BD-NOVAS-2012"),
                "mission": company_info.get("mission", ""),
                "vision": company_info.get("vision", ""),
                "values": company_info.get("values", []),
                "shipyard_capacity": company_info.get("shipyardCapacity", {}),
                "certifications": company_info.get("certifications", []),
            }
        )

        # Pillars
        for idx, p in enumerate(company_info.get("bestInPillars", [])):
            CompanyPillar.objects.update_or_create(
                pillar_id=p.get("id"),
                defaults={
                    "badge": p.get("badge", "BEST"),
                    "keyword": p.get("keyword", ""),
                    "title": p.get("title", ""),
                    "description": p.get("description", ""),
                    "icon": p.get("icon", ""),
                    "sort_order": idx,
                }
            )

        # Blueprints
        for idx, b in enumerate(company_info.get("blueprintSteps", [])):
            BlueprintStep.objects.update_or_create(
                step=b.get("step"),
                defaults={
                    "title": b.get("title"),
                    "description": b.get("description"),
                    "sort_order": idx,
                }
            )

        # Hero Banner Slides (Default dynamic slides for pages)
        banner_slides = [
            # Projects Page Slides (Left-aligned as desired)
            {
                "page_identifier": "projects",
                "title": "Tactical High-Speed Naval Interceptors",
                "subtitle": "Turnkey delivery and systems integration of high-speed naval interceptor workboats equipped with marine X-band surveillance radar and encrypted VHF.",
                "badge": "MARITIME PLATFORMS // NAVAL SHIPYARD",
                "image_url": "/assets/hero/hero-maritime-Z9Kk4jOd.jpg",
                "alignment": "left",
                "cta_label": "View Naval Project",
                "cta_link": "/projects/naval-interceptor-craft-patrol",
                "sort_order": 0,
            },
            {
                "page_identifier": "projects",
                "title": "Perimeter Border Radar & Optronics",
                "subtitle": "Deployment of tactical perimeter ground-surveillance radar with co-mounted long-range thermal electro-optical tracking cameras for 24/7 border security.",
                "badge": "DEFENCE & BORDER RECONNAISSANCE",
                "image_url": "/assets/hero/hero-defence-CzOJrdZI.jpg",
                "alignment": "left",
                "cta_label": "View Radar Project",
                "cta_link": "/projects/tactical-border-surveillance-radar",
                "sort_order": 1,
            },
            {
                "page_identifier": "projects",
                "title": "Tactical C4I Backbone & Cyber Defense Center",
                "subtitle": "Nationwide military-grade VHF/UHF tactical radio repeaters and encrypted microwave backbone network for inter-agency joint commands.",
                "badge": "DEFENCE COMMUNICATIONS // C4I",
                "image_url": "/assets/hero/hero-cyber-BQaYidYs.jpg",
                "alignment": "left",
                "cta_label": "View C4I Project",
                "cta_link": "/projects/tactical-c4i-network",
                "sort_order": 2,
            },

            # Consultancy Page Slides
            {
                "page_identifier": "consultancy",
                "title": "Foreign OEM Representation & Global Trade Alliances",
                "subtitle": "Accredited local representation connecting European, North American, and Asian defense manufacturers with South Asian sovereign procurement directorates.",
                "badge": "INTERNATIONAL CONSULTANCY // GLOBAL TRADE",
                "image_url": "https://images.unsplash.com/photo-1577962917302-cd874c4e31d2?auto=format&fit=crop&w=1200&q=80",
                "alignment": "left",
                "cta_label": "Explore International Practice",
                "cta_link": "/consultancy/international",
                "sort_order": 0,
            },
            {
                "page_identifier": "consultancy",
                "title": "Tactical Defense Comms & Sovereign Data Infrastructure",
                "subtitle": "Architecting mission-critical tactical radio backbones, Tier-III/IV data centers, encrypted communication systems, and cyber defense operation centers.",
                "badge": "IT & TELECOMMUNICATION // C4ISR & CYBER",
                "image_url": "/assets/hero/hero-cyber-BQaYidYs.jpg",
                "alignment": "left",
                "cta_label": "View IT & Telecom Practice",
                "cta_link": "/consultancy/it-telecom",
                "sort_order": 1,
            },
            {
                "page_identifier": "consultancy",
                "title": "Naval Shipyard Modernization & Industrial EPC Advisory",
                "subtitle": "Feasibility, equipment layout, CNC fabrication cells, dry dock expansion, and high-capital machinery procurement advisory.",
                "badge": "PROJECT CONSULTANCY // HEAVY INDUSTRIAL EPC",
                "image_url": "/assets/hero/hero-maritime-Z9Kk4jOd.jpg",
                "alignment": "left",
                "cta_label": "View Project Consultancy",
                "cta_link": "/consultancy/project",
                "sort_order": 2,
            },

            # Defence Page Slides
            {
                "page_identifier": "defence",
                "title": "Tactical Force Protection & Superiority",
                "subtitle": "Battle-tested ballistic armor, electro-optics, and secure communications engineered for frontline special forces.",
                "badge": "FORCE PROTECTION // BALLISTIC CAPABILITY",
                "image_url": "/assets/hero/hero-defence-CzOJrdZI.jpg",
                "alignment": "left",
                "cta_label": "Explore Defense Systems",
                "cta_link": "/products?sector=defence",
                "sort_order": 0,
            },

            # Industry Page Slides
            {
                "page_identifier": "industry",
                "title": "Industrial Heavy Machinery & Maritime Logistics",
                "subtitle": "Turnkey engineering solutions, shipyard equipment, and industrial automation powering modern heavy industry.",
                "badge": "HEAVY INDUSTRY // MARITIME & EPC",
                "image_url": "/assets/hero/hero-industry-DF_u2f-4.jpg",
                "alignment": "left",
                "cta_label": "Explore Industry Capabilities",
                "cta_link": "/sectors/industry",
                "sort_order": 0,
            },

            # Home Page Slides
            {
                "page_identifier": "home",
                "title": "Engineering Sovereign Defense & Industrial Resilience",
                "subtitle": "Novas BD bridges Tier-1 NATO and global manufacturers with Bangladesh armed forces and heavy industries.",
                "badge": "DEFENSE & INDUSTRIAL PARTNERSHIPS",
                "image_url": "/assets/hero/hero-defence-CzOJrdZI.jpg",
                "alignment": "left",
                "cta_label": "Explore Our Capabilities",
                "cta_link": "/catalog",
                "sort_order": 0,
            },
        ]

        for s in banner_slides:
            HeroBannerSlide.objects.update_or_create(
                page_identifier=s["page_identifier"],
                title=s["title"],
                defaults={
                    "subtitle": s["subtitle"],
                    "badge": s["badge"],
                    "image_url": s["image_url"],
                    "alignment": s["alignment"],
                    "cta_label": s["cta_label"],
                    "cta_link": s["cta_link"],
                    "sort_order": s["sort_order"],
                    "is_active": True,
                }
            )

        self.stdout.write(f"  -> Seeded company profile, {CompanyPillar.objects.count()} pillars, {BlueprintStep.objects.count()} blueprints, and {HeroBannerSlide.objects.count()} banner slides.")
