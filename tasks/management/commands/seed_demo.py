from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from tasks.models import Project, Task
from datetime import date, timedelta


PROJECTS = [
    {"name": "Website Redesign", "description": "Full redesign of the company website with new branding and improved UX."},
    {"name": "Mobile App v2", "description": "Second version of the mobile app with new features and performance improvements."},
    {"name": "API Integration", "description": "Integrate third-party payment and analytics APIs into the platform."},
]

TASKS = [
    # Website Redesign
    {"title": "Design new homepage layout", "description": "Create wireframes and high-fidelity mockups for the new homepage.", "status": "done", "priority": "high", "project": 0, "due": 10},
    {"title": "Implement responsive navigation", "description": "Build mobile-first navigation with hamburger menu.", "status": "done", "priority": "high", "project": 0, "due": 5},
    {"title": "Migrate content to new CMS", "description": "Move all existing content and blog posts to the new CMS.", "status": "in_progress", "priority": "medium", "project": 0, "due": 7},
    {"title": "SEO audit and optimization", "description": "Audit current SEO and implement meta tags, schema markup.", "status": "in_progress", "priority": "medium", "project": 0, "due": 14},
    {"title": "Performance optimization", "description": "Achieve 90+ Lighthouse score. Optimize images and lazy loading.", "status": "todo", "priority": "high", "project": 0, "due": 20},
    {"title": "Cross-browser testing", "description": "Test on Chrome, Firefox, Safari, and Edge.", "status": "todo", "priority": "low", "project": 0, "due": 25},
    # Mobile App v2
    {"title": "Set up React Native project", "description": "Initialize project with Expo and configure navigation.", "status": "done", "priority": "high", "project": 1, "due": -5},
    {"title": "Design onboarding screens", "description": "Create 4-step onboarding flow with animations.", "status": "done", "priority": "medium", "project": 1, "due": -2},
    {"title": "Implement authentication flow", "description": "Login, register, forgot password with JWT tokens.", "status": "in_progress", "priority": "high", "project": 1, "due": 3},
    {"title": "Build dashboard screen", "description": "Main dashboard with stats, recent activity, and quick actions.", "status": "in_progress", "priority": "high", "project": 1, "due": 6},
    {"title": "Push notifications setup", "description": "Integrate Expo push notifications for task reminders.", "status": "todo", "priority": "medium", "project": 1, "due": 15},
    {"title": "App Store submission", "description": "Prepare screenshots, description, and submit to App Store.", "status": "todo", "priority": "low", "project": 1, "due": 30},
    # API Integration
    {"title": "Stripe payment integration", "description": "Implement checkout, subscriptions, and webhook handling.", "status": "done", "priority": "high", "project": 2, "due": -3},
    {"title": "Set up Mixpanel analytics", "description": "Track user events and funnels with Mixpanel SDK.", "status": "in_progress", "priority": "medium", "project": 2, "due": 4},
    {"title": "SendGrid email integration", "description": "Transactional emails for welcome, password reset, invoices.", "status": "todo", "priority": "medium", "project": 2, "due": 10},
    {"title": "Rate limiting and API security", "description": "Add throttling, API key management, and audit logs.", "status": "todo", "priority": "high", "project": 2, "due": 12},
    # Standalone tasks
    {"title": "Write technical documentation", "description": "Document all API endpoints with examples and error codes.", "status": "todo", "priority": "medium", "project": None, "due": 18},
    {"title": "Set up CI/CD pipeline", "description": "GitHub Actions for automated testing and Railway deployment.", "status": "done", "priority": "high", "project": None, "due": -8},
    {"title": "Security audit", "description": "Review auth flows, input validation, and OWASP checklist.", "status": "in_progress", "priority": "high", "project": None, "due": 8},
    {"title": "Team onboarding guide", "description": "Write onboarding doc for new developers joining the team.", "status": "todo", "priority": "low", "project": None, "due": 21},
]


class Command(BaseCommand):
    help = "Seed demo user with realistic projects and tasks"

    def handle(self, *args, **options):
        # Create demo user
        user, created = User.objects.get_or_create(username="demo")
        if created or not user.has_usable_password():
            user.set_password("demo1234")
            user.first_name = "Alex"
            user.last_name = "Morgan"
            user.email = "demo@taskflow.app"
            user.save()
            self.stdout.write(self.style.SUCCESS("Demo user created: demo / demo1234"))
        else:
            self.stdout.write("Demo user already exists — refreshing data...")
            Project.objects.filter(owner=user).delete()

        today = date.today()

        # Create projects
        projects = []
        for p in PROJECTS:
            proj = Project.objects.create(owner=user, **p)
            projects.append(proj)

        # Create tasks
        for t in TASKS:
            project = projects[t["project"]] if t["project"] is not None else None
            Task.objects.create(
                owner=user,
                title=t["title"],
                description=t["description"],
                status=t["status"],
                priority=t["priority"],
                project=project,
                due_date=today + timedelta(days=t["due"]),
            )

        self.stdout.write(self.style.SUCCESS(
            f"Seeded {len(PROJECTS)} projects and {len(TASKS)} tasks for demo user."
        ))
        self.stdout.write(self.style.WARNING("Login: demo / demo1234"))
