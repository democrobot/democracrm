# Campaign

A campaign is a model that represents a specific legislative goal for an organization and is used to track progress
on that effort.

## Fields

### `id` (BigInt)

Object ID

### `org_account` (ForeignKey)

The `lobbying.OrganizationAccount` that this object is owned by.