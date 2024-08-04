# Public Office

## Description

The `lobbying.PublicOffice` model defines an office for one or more public officials as part of an
executive, legislative, or judicial branch within a governing body. Some offices are elective, such
as a Governor or member of a State Senate, and others are appointed, such as a Secretary of State
or Solicitor.

This model must be nesting, as many legislatures are bicameral, having multiple houses or chambers,
and it's crucial to account for this. For example, in Pennsylvania, the Pennsylvania General Assembly
is a bicameral legislative body with a State Senate (upper house) and House of Representatives (lower
house).

Law passed require support from both houses, but each house elect their members separately, have their
own leadership, produce and vote on their own versions of bills. In the Executive branch, departments
typically report to the Governor, so they would be nested to model reporting structures there.

core.ContactInfo models can be attached to the office to represent key support staff associated with our targets.

## Fields

