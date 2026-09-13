# App Screen Feature Inventory

## Deploy to Netlify

Open `/canvas` to browse all 30 available screens on a draggable, zoomable
canvas. Scroll or pinch to zoom, drag the background to pan, and drag previews
to arrange them. Double-click / double-tap a preview (or use its Open link) to
open the screen. Keyboard users can Tab to a screen and press Enter; `F` fits
all screens and `+` / `-` zoom. Positions and zoom are saved in this browser.
Use Reset layout to restore the grid. Screen 8 is not present in this project.

Connect this GitHub repository to Netlify and deploy the `main` branch.
The included `netlify.toml` sets the build command to `python build.py` and
the publish directory to `dist`. No Python server runs on the hosted site.

For a manual upload, run `python build.py` locally and upload the `dist`
folder to Netlify Drop. Upload the built folder, not the repository root.

`routes.json` is the shared route map for local development and deployment.
The build generates `dist/_redirects` with explicit rewrites for named routes
such as `/calendar`, numbered routes such as `/7`, and `/screen/7` aliases,
including trailing slashes. Opening or refreshing these URLs serves the
matching screen; query strings remain available to the frontend.
The home URL opens Front Desk. Unknown URLs return Netlify's normal 404.

The static build includes the navigation and screen picker normally injected
by `server.py`, without the local live-reload script. Run `python server.py`
for local development. After changing `routes.json`, restart the local server.

Netlify is recommended for this project because the frontend uses root-relative
links and server-style route aliases. GitHub Pages would need a separate build
for route directories and repository subpath support; this configuration targets
Netlify. Authentication and other prototype actions remain frontend demos.

This README is a feature-focused inventory of the screens in this project. It intentionally ignores layout, styling, spacing, and visual design and focuses only on the functionality, buttons, forms, sections, and actions that exist on each screen.

## Screen 1 — Sign In
Features:
- Email address field
- Password field
- Show/hide password toggle
- Remember me checkbox
- Forgot password link
- Continue button
- Create account link

## Screen 2 — Create New Password
Features:
- New password field
- Confirm password field
- Password strength rules checklist:
  - At least 8 characters
  - One uppercase letter
  - One lowercase letter
  - One number
  - One special character
- Show/hide password option
- Update Password button
- Sign In link for users who remember their password

## Screen 3 — Password Updated
Features:
- Success confirmation message: Password updated
- Continue to Sign In button
- Back to Home button

## Screen 4 — Sales Management
Features:
- Sales overview with total sales and payment status summary
- New Sale button
- Search field
- Filters:
  - All
  - Pending
  - Unpaid
  - Refunded
- Sales table/list with details:
  - Sale
  - Customer
  - Services / Products
- Payment status handling

## Screen 5 — Checkout / Order Summary
Features:
- Order summary for a service/product item
- Item details such as service name, duration, and client name
- Edit item action
- Remove item action
- Add Item button
- Pricing summary:
  - Subtotal
  - Discount
  - Total
- Client selection / new client flow
- Payment section
- Payment methods/actions:
  - Pay By Link
  - Card payment option
  - Alternative payment method placeholder

## Screen 6 — New Appointment
Features:
- New appointment flow
- Client selection area
- New client creation option
- Client details preview (name, phone)
- Change client action
- Scheduling area
- Date navigation
- Available time slot selection
- Appointment booking form logic

## Screen 7 — Calendar
Features:
- Calendar navigation
- Day view and Week view toggle
- Filter button
- New Appointment action
- Availability status view
- Booking schedule visibility

## Screen 9 — Front Desk
Features:
- Front Desk as primary workspace
- Time/date navigation
- Day and Week toggles
- Filter controls
- New Appointment action
- Booking and operations overview for the day
- Daily operational dashboard context

## Screen 10 — Salon Management Hub
Features:
- Workspace selection dashboard
- Navigation categories:
  - Front Desk
  - Calendar
  - Chats
  - Customers
- Core workspaces cards:
  - Services
  - Products
  - Billing
- Service and product management access
- Business operations overview / workspace dashboard

## Screen 11 — Messages
Features:
- Chat inbox / message list
- Search contacts/messages
- Contact list with unread or recent message previews
- Messaging thread selection
- Conversation metadata (time, last message)
- Message communication workflow

## Screen 12 — Service Management
Features:
- Service management workspace
- Add service action
- Category filtering
- Service categories such as:
  - Haircuts
  - Styling
- Service list entries such as:
  - Long Cut
  - Short Cut
  - Bang Trim
  - Signature Haircut
- Add new service or category actions

## Screen 13 — Resource Management
Features:
- Resource management workspace
- Add resource action
- Resource categories:
  - Spaces
  - Treatment Rooms
  - Consultation Rooms
  - Studios
- Resource listing and management
- Ability to create or manage resource availability

## Screen 14 — Service Management (Expanded)
Features:
- Service management screen with category-based listing
- Add service action
- Category groups such as:
  - Haircuts
  - Styling
- Service listing examples:
  - Signature Haircut
  - Buzz Cut
  - Kids Trim
  - Blowout
- Service catalog organization

## Screen 15 — Create Staff Member
Features:
- Staff management dashboard
- Staff list with names and roles
- Add staff member action
- Staff profiles such as:
  - Marcus Thorne - Senior Stylist
  - Elena Rodriguez - Lead Aesthetician
  - Sarah Jenkins - Head Receptionist
  - David Chen - Barber & Men's Specialist
  - Rebecca Miller - Senior Colorist
- Navigation to staff functions

## Screen 16 — Staff Management
Features:
- Staff directory / employee list
- Active staff status display
- Role and employee metadata
- Add staff action
- Employee cards with:
  - Name
  - Position
  - Employment ID
  - Join date
  - Status
- Staff administration workflow

## Screen 17 — Customers
Features:
- Customer workspace
- Customer segment tabs:
  - All Customers
  - VIP Clients
  - Recent Leads
  - Inactive
  - Archived
- New Segment action
- Search/filtering for customers
- Status-based customer organization

## Screen 18 — Add Customer
Features:
- Add customer form flow
- Back navigation
- Customer details entry
- Customer creation workflow
- Data entry fields for customer profile information

## Screen 19 — Customer Reviews
Features:
- Reviews dashboard
- Rating summary (example: 4.8 average)
- Total reviews count
- Review status filters:
  - All Reviews
  - Awaiting Reply
  - Replied
  - With Photos
- Rating breakdown section
- Review management workflow

## Screen 20 — Reports & Analysis
Features:
- Reports workspace
- Overview dashboard
- Search capability
- Report categories:
  - Overview
  - Sales
  - Revenue
- Analytics / business performance reporting

## Screen 21 — Create New Service
Features:
- New service creation form
- Category selection
- Service name field
- Service listing / catalog context
- Add or create new service action
- Service class/category organization such as:
  - Haircuts
  - Styling
- Service examples such as Standard Cut, Fade & Trim, Blow Dry

## Screen 22 — General Settings
Features:
- Settings navigation
- Workspace management
- General settings section
- Appearance section
- Theme customization option
- Workspace preferences and notification settings

## Screen 23 — Subscription & Billing
Features:
- Subscription and billing management
- Current plan details (example: Professional)
- Active plan status
- Billing information section
- Manage package / included features

## Screen 24 — Business Setup
Features:
- Business setup workspace
- General setup section
- Team Access management
- Financials section
- Payments config
- Taxes config
- Branding section
- Business Profile management
- Profile information setup for customer-facing business details

## Screen 25 — Business Hours
Features:
- Business Hours settings
- General setup workflow
- Schedule configuration for shop operating times
- Business profile / admin setup context

## Screen 26 — Contact Details Workspace
Features:
- Contact Details settings
- Business profile configuration
- Business hours management
- Locations management
- Team access settings
- Financial settings and tax configuration
- General business info setup

## Screen 27 — Business Setup / Location Setup
Features:
- Business setup workspace
- Team access controls
- Financial configuration
- Branding preferences
- Add Location action
- Location management context

## Screen 28 — Media Setup
Features:
- Media setup section
- Image/media management for the business
- General setup access
- Team access and business settings context
- Notifications configuration
- Subscription and financial tools options

## High-Level Feature Groups Across the App
These are the main functional areas represented across the screens:
- Authentication
  - Sign in
  - Password reset
  - Password update success flow
- Sales & checkout
  - New sale
  - Payment summary
  - Payment methods
- Appointments & calendar
  - New appointment
  - Schedule management
  - Availability booking
- Customer management
  - Customers list
  - Add customer
  - Reviews
  - Segments
- Staff management
  - Staff directory
  - Add staff
  - Roles and active status
- Service & resource management
  - Service catalog
  - Resource setup
  - Categories
- Business configuration
  - Business setup
  - Contact details
  - Business hours
  - Media setup
  - General settings
  - Subscription & billing
- Messaging and reporting
  - Chat workspace
  - Reports and analytics dashboard

## Suggested Simplification / Things to Remove Later
Since you mentioned you may remove extra screens/features, the likely areas to trim are:
- Duplicate setup flows (general settings, business setup, contact details, media, subscription pages)
- Multiple similar service/resource management screens
- Redundant navigation pages or dashboard hubs
- Extra category pages that do not add unique product value
- Messaging and reports if they are not required in the first version
- Multiple versions of the same management workflow (e.g., service management pages with minor differences)

This is intentionally a feature inventory only; the visual layout, colors, and spacing are not included here.
