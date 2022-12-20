# Development: URL Scheme

The URL scheme for the platform will need to support the following requirements:

## General Website

General website views of platform will be provided in the `www` subdomain, including a registration app for users
and organizations, using the following configuration.

### Website Root

* `/`: Index for the site; welcome page, sign up/sign in forms, updates, etc.


### Account Management

* `/account/user/`: Account management view for authenticated users, always accessible in the UI while logged in.
* `/account/user/create/`: Account creation view for users to sign up with.
* `/account/user/settings/`: Account settings view for existing users to configure their account.
* `/account/user/profile/`: Account profile view for displaying the platform-wide profile of their account.
* `/account/user/delete/`: Account deletion view for existing users to delete their account.
* `/account/user/log-in/`: User log-in view, always accessible in the UI while logged out.
* `/account/user/log-out/`: User log-out view, always accessible in the UI while logged in.
* `/account/user/reset-password/`: Password reset view, accessible in the UI log in form (and while logged out).
* `/account/organization/create/`: Account creation view for organizations to sign up with. Must be
  performed by an existing user.
* `/account/organization/<organization_id>/delete/`: Account deletion view for organizations to delete their account. Must be
  performed by an existing user, with explicit confirmation.

### Contact Management

* `/<organization_id>/contacts/<contact_id>/`:
* `/<organization_id>/contacts/create/`:
* `/<organization_id>/contacts/<contact_id>/update/`:
* `/<organization_id>/contacts/<contact_id>/delete/`:

### Lobbying Management

* `/<organization_id>/

### Organizing Management

* `/<organization_id>/

### Places Management

* `/<organization_id>/

### Social Management

* `/<organization_id>/

### Web Management

* `/<organization_id>/

## API Subdomain

!!! info
    
    This functionality will remain unavailable until the underlying data model stabilizes and the front end is
    functional enough for daily usage.

The platform API will be organized within `api.democracrm.org`, with specific structure and versioning to follow.

## Organization Subdomains

!!! info

    This functionality will remain unavailable until the full multi-tenancy infrastructure is implemented. Until then,
    only one organization may operate in an instance of the platform.

A subdomain for each organization account on the platform, such as `mohpa.democracrm.org`, is planned to shorten and
encapsulate the URLs used for the platform functionality. Within each organizational subdomain, we will
use the following configuration:

* `/`: Index for the organization account; layout TBD, and conditional on if viewed by anonymous or authenticated 
  user.
