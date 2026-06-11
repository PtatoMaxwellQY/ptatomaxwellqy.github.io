import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class JobsCareersStaticTest(unittest.TestCase):
    def read_jobs_page(self):
        return (ROOT / "carrers.html").read_text(encoding="utf-8")

    def read_industrial_css(self):
        return (ROOT / "assets" / "css" / "industrial-pages.css").read_text(encoding="utf-8")

    def test_carrers_route_replaces_jobs_route(self):
        self.assertTrue((ROOT / "carrers.html").is_file())
        self.assertFalse((ROOT / "jobs.html").exists())
        for page in ROOT.glob("*.html"):
            with self.subTest(page=page.name):
                self.assertNotIn("jobs.html", page.read_text(encoding="utf-8"))

    def test_jobs_page_is_labeled_as_careers(self):
        html = self.read_jobs_page()
        self.assertIn("<title>OptiHK | Careers</title>", html)
        self.assertIn('<a href="carrers.html" aria-current="page">Careers</a>', html)
        self.assertIn('<a href="carrers.html">Careers</a>', html)
        self.assertNotIn("<title>OptiHK | Jobs</title>", html)
        self.assertNotIn('aria-current="page">Jobs</a>', html)

    def test_jobs_page_removes_intro_focus_cards(self):
        html = self.read_jobs_page()
        self.assertNotIn("Hiring focus", html)
        self.assertNotIn("Team mode", html)
        self.assertNotIn('class="jobs-hero-grid"', html)
        self.assertNotIn("Engineering roles", html)
        self.assertNotIn("Program operations", html)

    def test_jobs_page_groups_roles_by_employment_type(self):
        html = self.read_jobs_page()
        self.assertIn("Full-time positions", html)
        self.assertIn("Part-time positions", html)
        self.assertLess(html.index("Full-time positions"), html.index("Part-time positions"))
        self.assertEqual(html.count('data-employment="full-time"'), 6)
        self.assertEqual(html.count('data-employment="part-time"'), 4)

        full_time_titles = (
            "Senior Engineer / Engineer, Electronic IC Design",
            "Senior Engineer / Engineer, Photonic IC Design",
            "Senior Engineer / Engineer, Embedded Electronics Design",
            "Senior Engineer, Advanced Packaging Engineer",
            "Senior Engineer / Engineer, EDA and Photonic Automation",
            "Staff, Project Coordinator",
        )
        part_time_titles = (
            "Interim Engineer, Electronic IC Design",
            "Interim Engineer, Photonic IC Design",
            "Interim Engineer, Embedded Electronics Design",
            "Interim Engineer, EDA and Photonic Automation",
        )

        for title in full_time_titles + part_time_titles:
            with self.subTest(title=title):
                self.assertIn(title, html)

    def test_jobs_page_salary_bands_and_default_collapsed_cards(self):
        html = self.read_jobs_page()
        self.assertNotIn("<details open", html)
        self.assertNotIn(" open>", html)
        self.assertEqual(html.count("HKD 390k ~ 700k"), 5)
        self.assertEqual(html.count("HKD 300k ~ 600k"), 1)
        self.assertEqual(html.count("HKD 10k ~ 20k/month"), 4)
        self.assertEqual(html.count('<div class="salary-line"><h2>Salary</h2><p>'), 10)
        self.assertNotIn('class="tag">Salary', html)

    def test_salary_label_uses_job_heading_typography(self):
        css = self.read_industrial_css()
        self.assertIn(".jobs-page .job-body h2", css)
        self.assertIn(".salary-line h2", css)
        self.assertIn(".salary-line p", css)


if __name__ == "__main__":
    unittest.main()
