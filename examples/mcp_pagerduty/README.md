# Generated MCP Server

This is an automatically generated Model Context Protocol (MCP) server based on an OpenAPI specification.

## Setup

1. Copy `.env.example` to `.env` and fill in your API credentials:
```bash
cp .env.example .env
```

2. Install dependencies:
```bash
poetry install
```

3. Run the server:
```bash
poetry run python -m server
```

## Available Tools

The following tools are available through the MCP server:


### POST /{entity_type}/{id}/change_tags
Assign tags

Assign existing or new tags.

A Tag is applied to Escalation Policies, Teams or Users and can be used to filter them.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#tags)

Scoped OAuth requires: `tags.write`



### GET /{entity_type}/{id}/tags
Get tags for entities

Get related tags for Users, Teams or Escalation Policies.

A Tag is applied to Escalation Policies, Teams or Users and can be used to filter them.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#tags)

Scoped OAuth requires: `tags.read`



### GET /abilities
List abilities

List all of your account's abilities, by name.

"Abilities" describes your account's capabilities by feature name. For example `"teams"`.

An ability may be available to your account based on things like your pricing plan or account state.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#abilities)

Scoped OAuth requires: `abilities.read`



### GET /abilities/{id}
Test an ability

Test whether your account has a given ability.

"Abilities" describes your account's capabilities by feature name. For example `"teams"`.

An ability may be available to your account based on things like your pricing plan or account state.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#abilities)

Scoped OAuth requires: `abilities.read`



### GET /addons
List installed Add-ons

List all of the Add-ons installed on your account.

Addon's are pieces of functionality that developers can write to insert new functionality into PagerDuty's UI.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#add-ons)

Scoped OAuth requires: `addons.read`



### POST /addons
Install an Add-on

Install an Add-on for your account.

Addon's are pieces of functionality that developers can write to insert new functionality into PagerDuty's UI.

Given a configuration containing a `src` parameter, that URL will be embedded in an `iframe` on a page that's available to users from a drop-down menu.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#add-ons)

Scoped OAuth requires: `addons.write`



### GET /addons/{id}
Get an Add-on

Get details about an existing Add-on.

Addon's are pieces of functionality that developers can write to insert new functionality into PagerDuty's UI.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#add-ons)

Scoped OAuth requires: `addons.read`



### DELETE /addons/{id}
Delete an Add-on

Remove an existing Add-on.

Addon's are pieces of functionality that developers can write to insert new functionality into PagerDuty's UI.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#add-ons)

Scoped OAuth requires: `addons.write`



### PUT /addons/{id}
Update an Add-on

Update an existing Add-on.

Addon's are pieces of functionality that developers can write to insert new functionality into PagerDuty's UI.

Given a configuration containing a `src` parameter, that URL will be embedded in an `iframe` on a page that's available to users from a drop-down menu.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#add-ons)

Scoped OAuth requires: `addons.write`



### GET /alert_grouping_settings
List alert grouping settings

List all of your alert grouping settings including both single service settings and global content based settings.

The settings part of Alert Grouper service allows us to create Alert Grouping Settings and configs that are required to be used during grouping of the alerts.

Scoped OAuth requires: `services.read`



### POST /alert_grouping_settings
Create an Alert Grouping Setting

Create a new Alert Grouping Setting.

The settings part of Alert Grouper service allows us to create Alert Grouping Settings and configs that are required to be used during grouping of the alerts.

This endpoint will be used to create an instance of AlertGroupingSettings for either one service or many services that are in the alert group setting.

Scoped OAuth requires: `services.write`



### GET /alert_grouping_settings/{id}
Get an Alert Grouping Setting

Get an existing Alert Grouping Setting.

The settings part of Alert Grouper service allows us to create Alert Grouping Settings and configs that are required to be used during grouping of the alerts.

Scoped OAuth requires: `services.read`



### DELETE /alert_grouping_settings/{id}
Delete an Alert Grouping Setting

Delete an existing Alert Grouping Setting.

The settings part of Alert Grouper service allows us to create Alert Grouping Settings and configs that are required to be used during grouping of the alerts.

Scoped OAuth requires: `services.write`



### PUT /alert_grouping_settings/{id}
Update an Alert Grouping Setting

Update an Alert Grouping Setting.

The settings part of Alert Grouper service allows us to create Alert Grouping Settings and configs that are required to be used during grouping of the alerts.

if `services` are not provided in the request, then the existing services will not be removed from the setting.

Scoped OAuth requires: `services.write`



### POST /analytics/metrics/incidents/all
Get aggregated incident data

Provides aggregated enriched metrics for incidents.

The provided metrics are aggregated by day, week, month using the aggregate_unit parameter, or for the entire period if no aggregate_unit is provided.

<!-- theme: info -->
> A `team_ids` or `service_ids` filter is required for [user-level API keys](https://support.pagerduty.com/docs/using-the-api#section-generating-a-personal-rest-api-key) or keys generated through an OAuth flow. Account-level API keys do not have this requirement.
<!-- theme: info -->
> **Note:** Analytics data is updated [periodically](https://support.pagerduty.com/main/docs/insights#:~:text=Data%20Update%20Schedule). It takes up to 24 hours before new incidents appear in the Analytics API.

Scoped OAuth requires: `analytics.read`



### POST /analytics/metrics/incidents/escalation_policies
Get aggregated escalation policy data

Provides aggregated metrics for incidents aggregated into units of time by escalation policy.

Example metrics include Seconds to Resolve, Seconds to Engage, Snoozed Seconds, and Sleep Hour Interruptions. Metric definitions can be found in our [Knowledge Base](https://support.pagerduty.com/docs/insights#escalation-policy-list).

<!-- theme: info -->
> **Note:** Analytics data is updated [periodically](https://support.pagerduty.com/main/docs/insights#:~:text=Data%20Update%20Schedule). It takes up to 24 hours before new incidents appear in the Analytics API.

Scoped OAuth requires: `analytics.read`



### POST /analytics/metrics/incidents/escalation_policies/all
Get aggregated metrics for all escalation policies

Provides aggregated metrics across all escalation policies.

Example metrics include Seconds to Resolve, Seconds to Engage, Snoozed Seconds, and Sleep Hour Interruptions. Metric definitions can be found in our [Knowledge Base](https://support.pagerduty.com/docs/insights#escalation-policy-list).

<!-- theme: info -->
> **Note:** Analytics data is updated [periodically](https://support.pagerduty.com/main/docs/insights#:~:text=Data%20Update%20Schedule). It takes up to 24 hours before new incidents appear in the Analytics API.

Scoped OAuth requires: `analytics.read`



### POST /analytics/metrics/incidents/services
Get aggregated service data

Provides aggregated metrics for incidents aggregated into units of time by service.

Example metrics include Seconds to Resolve, Seconds to Engage, Snoozed Seconds, and Sleep Hour Interruptions. Metric definitions can be found in our [Knowledge Base](https://support.pagerduty.com/docs/insights#services-list).
Data can be aggregated by day, week or month in addition to by service, or provided just as a collection of aggregates for each service in the dataset for the entire period.  If a unit is provided, each row in the returned dataset will include a 'range_start' timestamp.

<!-- theme: info -->
> **Note:** Analytics data is updated [periodically](https://support.pagerduty.com/main/docs/insights#:~:text=Data%20Update%20Schedule). It takes up to 24 hours before new incidents appear in the Analytics API.

Scoped OAuth requires: `analytics.read`



### POST /analytics/metrics/incidents/services/all
Get aggregated metrics for all services

Provides aggregated metrics across all services.

Example metrics include Seconds to Resolve, Seconds to Engage, Snoozed Seconds, and Sleep Hour Interruptions. Metric definitions can be found in our [Knowledge Base](https://support.pagerduty.com/docs/insights#services-list).

<!-- theme: info -->
> A `team_ids` or `service_ids` filter is required for [user-level API keys](https://support.pagerduty.com/docs/using-the-api#section-generating-a-personal-rest-api-key) or keys generated through an OAuth flow. Account-level API keys do not have this requirement.
<!-- theme: info -->
> **Note:** Analytics data is updated [periodically](https://support.pagerduty.com/main/docs/insights#:~:text=Data%20Update%20Schedule). It takes up to 24 hours before new incidents appear in the Analytics API.

Scoped OAuth requires: `analytics.read`



### POST /analytics/metrics/incidents/teams
Get aggregated team data

Provides aggregated metrics for incidents aggregated into units of time by team.

Example metrics include Seconds to Resolve, Seconds to Engage, Snoozed Seconds, and Sleep Hour Interruptions. Metric definitions can be found in our [Knowledge Base](https://support.pagerduty.com/docs/insights#teams-list).
Data can be aggregated by day, week or month in addition to by team, or provided just as a collection of aggregates for each team in the dataset for the entire period.  If a unit is provided, each row in the returned dataset will include a 'range_start' timestamp.

<!-- theme: info -->
> A `team_ids` or `service_ids` filter is required for [user-level API keys](https://support.pagerduty.com/docs/using-the-api#section-generating-a-personal-rest-api-key) or keys generated through an OAuth flow. Account-level API keys do not have this requirement.
<!-- theme: info -->
> **Note:** Analytics data is updated [periodically](https://support.pagerduty.com/main/docs/insights#:~:text=Data%20Update%20Schedule). It takes up to 24 hours before new incidents appear in the Analytics API.

Scoped OAuth requires: `analytics.read`



### POST /analytics/metrics/incidents/teams/all
Get aggregated metrics for all teams

Provides aggregated metrics across all teams.

Example metrics include Seconds to Resolve, Seconds to Engage, Snoozed Seconds, and Sleep Hour Interruptions. Metric definitions can be found in our [Knowledge Base](https://support.pagerduty.com/docs/insights#teams-list).

<!-- theme: info -->
> A `team_ids` or `service_ids` filter is required for [user-level API keys](https://support.pagerduty.com/docs/using-the-api#section-generating-a-personal-rest-api-key) or keys generated through an OAuth flow. Account-level API keys do not have this requirement.
<!-- theme: info -->
> **Note:** Analytics data is updated [periodically](https://support.pagerduty.com/main/docs/insights#:~:text=Data%20Update%20Schedule). It takes up to 24 hours before new incidents appear in the Analytics API.

Scoped OAuth requires: `analytics.read`



### POST /analytics/metrics/pd_advance_usage/features
Get aggregated PD Advance usage data

Provides aggregated metrics for the usage of PD Advance.
<!-- theme: info -->
> **Note:** Analytics data is updated [periodically](https://support.pagerduty.com/main/docs/insights#:~:text=Data%20Update%20Schedule). It takes up to 24 hours before new incidents appear in the Analytics API.

Scoped OAuth requires: `analytics.read`



### POST /analytics/metrics/responders/all
Get aggregated metrics for all responders

Provides aggregated incident metrics for all selected responders.

Example metrics include Seconds to Resolve, Seconds to Engage, Snoozed Seconds, and Sleep Hour Interruptions. Metric definitions can be found in our [Knowledge Base](https://support.pagerduty.com/docs/insights#responders-list).

<!-- theme: info -->
> **Note:** Analytics data is updated [periodically](https://support.pagerduty.com/main/docs/insights#:~:text=Data%20Update%20Schedule). It takes up to 24 hours before new incidents appear in the Analytics API.

Scoped OAuth requires: `analytics.read`



### POST /analytics/metrics/responders/teams
Get responder data aggregated by team

Provides incident metrics aggregated by responder.

Example metrics include Seconds to Resolve, Seconds to Engage, Snoozed Seconds, and Sleep Hour Interruptions. Metric definitions can be found in our [Knowledge Base](https://support.pagerduty.com/docs/insights#responders-list).

<!-- theme: info -->
> **Note:** Analytics data is updated [periodically](https://support.pagerduty.com/main/docs/insights#:~:text=Data%20Update%20Schedule). It takes up to 24 hours before new incidents appear in the Analytics API.

Scoped OAuth requires: `analytics.read`



### POST /analytics/raw/incidents
Get raw data - multiple incidents

Provides enriched incident data and metrics for multiple incidents.

Example metrics include Seconds to Resolve, Seconds to Engage, Snoozed Seconds, and Sleep Hour Interruptions. Metric definitions can be found in our [Knowledge Base](https://support.pagerduty.com/docs/insights#incidents-list).

<!-- theme: info -->
> A `team_ids` or `service_ids` filter is required for [user-level API keys](https://support.pagerduty.com/docs/using-the-api#section-generating-a-personal-rest-api-key) or keys generated through an OAuth flow. Account-level API keys do not have this requirement.
<!-- theme: info -->
> **Note:** Analytics data is updated [periodically](https://support.pagerduty.com/main/docs/insights#:~:text=Data%20Update%20Schedule). It takes up to 24 hours before new incidents appear in the Analytics API.

Scoped OAuth requires: `analytics.read`



### GET /analytics/raw/incidents/{id}
Get raw data - single incident

Provides enriched incident data and metrics for a single incident.

Example metrics include Seconds to Resolve, Seconds to Engage, Snoozed Seconds, and Sleep Hour Interruptions. Metric definitions can be found in our [Knowledge Base](https://support.pagerduty.com/docs/insights#incidents-list).

<!-- theme: info -->
> **Note:** Analytics data is updated [periodically](https://support.pagerduty.com/main/docs/insights#:~:text=Data%20Update%20Schedule). It takes up to 24 hours before new incidents appear in the Analytics API.

Scoped OAuth requires: `analytics.read`



### GET /analytics/raw/incidents/{id}/responses
Get raw responses from a single incident

Provides enriched responder data for a single incident.

Example metrics include Time to Respond, Responder Type, and Response Status. See metric definitions below.

<!-- theme: info -->
> **Note:** Analytics data is updated once per day. It takes up to 24 hours before new incident responses appear in the Analytics API.
Scoped OAuth requires: `analytics.read`



### POST /analytics/raw/responders/{responder_id}/incidents
Get raw incidents for a single responder_id

Provides enriched incident data and metrics for a specific responder.

Example metrics include Mean Seconds to Resolve, Mean Seconds to Engage, Snoozed Seconds, and Sleep Hour Interruptions. Metric definitions can be found in our [Knowledge Base](https://support.pagerduty.com/docs/insights#incidents-list).

<!-- theme: info -->
> **Note:** Analytics data is updated [periodically](https://support.pagerduty.com/main/docs/insights#:~:text=Data%20Update%20Schedule). It takes up to 24 hours before new incidents appear in the Analytics API.

Scoped OAuth requires: `analytics.read`



### GET /audit/records
List audit records

List audit trail records matching provided query params or default criteria.

The returned records are sorted by the `execution_time` from newest to oldest.

See [`Cursor-based pagination`](https://developer.pagerduty.com/docs/rest-api-v2/pagination/) for instructions on how to paginate through the result set.

Only admins, account owners, or global API tokens on PagerDuty account [pricing plans](https://www.pagerduty.com/pricing) with the "Audit Trail" feature can access this endpoint.

For other role based access to audit records by resource ID, see the resource's API documentation.

For more information see the [Audit API Document](https://developer.pagerduty.com/docs/rest-api-v2/audit-records-api/).

Scoped OAuth requires: `audit_records.read`



### POST /automation_actions/actions
Create an Automation Action

Create a Script, Process Automation, or Runbook Automation action



### GET /automation_actions/actions
List Automation Actions

Lists Automation Actions matching provided query params.

The returned records are sorted by action name in alphabetical order.

See [`Cursor-based pagination`](https://developer.pagerduty.com/docs/rest-api-v2/pagination/) for instructions on how to paginate through the result set.



### GET /automation_actions/actions/{id}
Get an Automation Action

Get an Automation Action



### DELETE /automation_actions/actions/{id}
Delete an Automation Action

Delete an Automation Action



### PUT /automation_actions/actions/{id}
Update an Automation Action

Updates an Automation Action



### POST /automation_actions/actions/{id}/invocations
Create an Invocation

Invokes an Action



### GET /automation_actions/actions/{id}/services
Get all service references associated with an Automation Action

Gets all service references associated with an Automation Action


### POST /automation_actions/actions/{id}/services
Associate an Automation Action with a service

Associate an Automation Action with a service



### GET /automation_actions/actions/{id}/services/{service_id}
Get the details of an Automation Action / service relation

Gets the details of a Automation Action / service relation


### DELETE /automation_actions/actions/{id}/services/{service_id}
Disassociate an Automation Action from a service

Disassociate an Automation Action from a service



### POST /automation_actions/actions/{id}/teams
Associate an Automation Action with a team

Associate an Automation Action with a team



### GET /automation_actions/actions/{id}/teams
Get all team references associated with an Automation Action

Gets all team references associated with an Automation Action


### DELETE /automation_actions/actions/{id}/teams/{team_id}
Disassociate an Automation Action from a team

Disassociate an Automation Action from a team



### GET /automation_actions/actions/{id}/teams/{team_id}
Get the details of an Automation Action / team relation

Gets the details of an Automation Action / team relation


### GET /automation_actions/invocations
List Invocations

List Invocations



### GET /automation_actions/invocations/{id}
Get an Invocation

Get an Automation Action Invocation



### POST /automation_actions/runners
Create an Automation Action runner.

Create a Process Automation or a Runbook Automation runner.



### GET /automation_actions/runners
List Automation Action runners

Lists Automation Action runners matching provided query params.
The returned records are sorted by runner name in alphabetical order.

See [`Cursor-based pagination`](https://developer.pagerduty.com/docs/rest-api-v2/pagination/) for instructions on how to paginate through the result set.



### GET /automation_actions/runners/{id}
Get an Automation Action runner

Get an Automation Action runner



### PUT /automation_actions/runners/{id}
Update an Automation Action runner

Update an Automation Action runner



### DELETE /automation_actions/runners/{id}
Delete an Automation Action runner

Delete an Automation Action runner



### POST /automation_actions/runners/{id}/teams
Associate a runner with a team

Associate a runner with a team



### GET /automation_actions/runners/{id}/teams
Get all team references associated with a runner

Gets all team references associated with a runner


### DELETE /automation_actions/runners/{id}/teams/{team_id}
Disassociate a runner from a team

Disassociates a runner from a team



### GET /automation_actions/runners/{id}/teams/{team_id}
Get the details of a runner / team relation

Gets the details of a runner / team relation


### GET /business_services
List Business Services

List existing Business Services.

Business services model capabilities that span multiple technical services and that may be owned by several different teams.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#business-services)

Scoped OAuth requires: `services.read`



### POST /business_services
Create a Business Service

Create a new Business Service.

Business services model capabilities that span multiple technical services and that may be owned by several different teams.

There is a limit of 5,000 business services per account. If the limit is reached, the API will respond with an error.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#business-services)

Scoped OAuth requires: `services.write`



### GET /business_services/{id}
Get a Business Service

Get details about an existing Business Service.

Business services model capabilities that span multiple technical services and that may be owned by several different teams.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#business-services)

Scoped OAuth requires: `services.read`



### DELETE /business_services/{id}
Delete a Business Service

Delete an existing Business Service.

Once the service is deleted, it will not be accessible from the web UI and new incidents won't be able to be created for this service.

Business services model capabilities that span multiple technical services and that may be owned by several different teams.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#business-services)

Scoped OAuth requires: `services.write`



### PUT /business_services/{id}
Update a Business Service

Update an existing Business Service. NOTE that this endpoint also accepts the PATCH verb.

Business services model capabilities that span multiple technical services and that may be owned by several different teams.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#business-services)

Scoped OAuth requires: `services.write`



### POST /business_services/{id}/account_subscription
Create Business Service Account Subscription

Subscribe your Account to a Business Service.

Scoped OAuth requires: `subscribers.write`



### DELETE /business_services/{id}/account_subscription
Delete Business Service Account Subscription

Unsubscribe your Account from a Business Service.

Scoped OAuth requires: `subscribers.write`



### GET /business_services/{id}/subscribers
List Business Service Subscribers

Retrieve a list of Notification Subscribers on the Business Service.

<!-- theme: warning -->
> Users must be added through `POST /business_services/{id}/subscribers` to be returned from this endpoint.
Scoped OAuth requires: `subscribers.read`



### POST /business_services/{id}/subscribers
Create Business Service Subscribers

Subscribe the given entities to the given Business Service.

Scoped OAuth requires: `subscribers.write`



### GET /business_services/{id}/supporting_services/impacts
List the supporting Business Services for the given Business Service Id, sorted by impacted status.

Retrieve of Business Services that support the given Business Service sorted by highest Impact with `status` included.
This endpoint does not return an exhaustive list of Business Services but rather provides access to the most impacted up to the limit of 200.

The returned Business Services are sorted first by Impact, secondarily by most recently impacted, and finally by name.

To get impact information about a specific set of Business Services, use the `ids[]` parameter on the `/business_services/impacts` endpoint.
Scoped OAuth requires: `services.read`



### POST /business_services/{id}/unsubscribe
Remove Business Service Subscribers

Unsubscribes the matching Subscribers from a Business Service.

Scoped OAuth requires: `subscribers.write`



### GET /business_services/impactors
List Impactors affecting Business Services

Retrieve a list of Impactors for the top-level Business Services on the account. Impactors are currently limited to Incidents.

This endpoint does not return an exhaustive list of Impactors but rather provides access to the highest priority Impactors for the Business Services in question up to the limit of 200.

To get Impactors for a specific set of Business Services, use the `ids[]` parameter.

The returned Impactors are sorted first by priority and secondarily by their creation date.
Scoped OAuth requires: `services.read`



### GET /business_services/impacts
List Business Services sorted by impacted status

Retrieve a list top-level Business Services sorted by highest Impact with `status` included.
When called without the `ids[]` parameter, this endpoint does not return an exhaustive list of Business Services but rather provides access to the most impacted up to the limit of 200.

The returned Business Services are sorted first by Impact, secondarily by most recently impacted, and finally by name.

To get impact information about a specific set of Business Services, use the `ids[]` parameter.
Scoped OAuth requires: `services.read`



### GET /business_services/priority_thresholds
Get the global priority threshold for a Business Service to be considered impacted by an Incident

Retrieves the priority threshold information for an account.  Currently, there is a `global_threshold` that can be set for the account.  Incidents that have a priority meeting or exceeding this threshold will be considered impacting on any Business Service that depends on the Service to which the Incident belongs.
Scoped OAuth requires: `services.read`



### DELETE /business_services/priority_thresholds
Deletes the account-level priority threshold for Business Service impact

Clears the Priority Threshold for the account.  If the priority threshold is cleared, any Incident with a Priority set will be able to impact Business Services.
Scoped OAuth requires: `services.write`



### PUT /business_services/priority_thresholds
Set the Account-level priority threshold for Business Service impact.

Set the Account-level priority threshold for Business Service.
Scoped OAuth requires: `services.write`



### GET /change_events
List Change Events

List all of the existing Change Events.

Scoped OAuth requires: `change_events.read`



### POST /change_events
Create a Change Event

Sending Change Events is documented as part of the V2 Events API. See [`Send Change Event`](https://developer.pagerduty.com/api-reference/b3A6Mjc0ODI2Ng-send-change-events-to-the-pager-duty-events-api).



### GET /change_events/{id}
Get a Change Event

Get details about an existing Change Event.

Scoped OAuth requires: `change_events.read`



### PUT /change_events/{id}
Update a Change Event

Update an existing Change Event

Scoped OAuth requires: `change_events.write`



### GET /escalation_policies
List escalation policies

List all of the existing escalation policies.

Escalation policies define which user should be alerted at which time.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#escalation-policies)

Scoped OAuth requires: `escalation_policies.read`



### POST /escalation_policies
Create an escalation policy

Creates a new escalation policy. At least one escalation rule must be provided.

Escalation policies define which user should be alerted at which time.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#escalation-policies)

Scoped OAuth requires: `escalation_policies.write`



### GET /escalation_policies/{id}
Get an escalation policy

Get information about an existing escalation policy and its rules.

Escalation policies define which user should be alerted at which time.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#escalation-policies)

Scoped OAuth requires: `escalation_policies.read`



### DELETE /escalation_policies/{id}
Delete an escalation policy

Deletes an existing escalation policy and rules. The escalation policy must not be in use by any services.

Escalation policies define which user should be alerted at which time.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#escalation-policies)

Scoped OAuth requires: `escalation_policies.write`



### PUT /escalation_policies/{id}
Update an escalation policy

Updates an existing escalation policy and rules.

Escalation policies define which user should be alerted at which time.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#escalation-policies)

Scoped OAuth requires: `escalation_policies.write`



### GET /escalation_policies/{id}/audit/records
List audit records for an escalation policy

The returned records are sorted by the `execution_time` from newest to oldest.

See [`Cursor-based pagination`](https://developer.pagerduty.com/docs/rest-api-v2/pagination/) for instructions on how to paginate through the result set.

For more information see the [Audit API Document](https://developer.pagerduty.com/docs/rest-api-v2/audit-records-api/).

Scoped OAuth requires: `audit_records.read`



### GET /event_orchestrations
List Event Orchestrations

List all Global Event Orchestrations on an Account.

Global Event Orchestrations allow you define a set of Global Rules and Router Rules, so that when you ingest events using the Orchestration's Routing Key your events will have actions applied via the Global Rules & then routed to the correct Service by the Router Rules, based on the event's content.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#event-orchestrations)

Scoped OAuth requires: `event_orchestrations.read`



### POST /event_orchestrations
Create an Orchestration

Create a Global Event Orchestration.

Global Event Orchestrations allow you define a set of Global Rules and Router Rules, so that when you ingest events using the Orchestration's Routing Key your events will have actions applied via the Global Rules & then routed to the correct Service by the Router Rules, based on the event's content.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#event-orchestrations)

Scoped OAuth requires: `event_orchestrations.write`



### GET /event_orchestrations/{id}
Get an Orchestration

Get a Global Event Orchestration.

Global Event Orchestrations allow you define a set of Global Rules and Router Rules, so that when you ingest events using the Orchestration's Routing Key your events will have actions applied via the Global Rules & then routed to the correct Service by the Router Rules, based on the event's content.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#event-orchestrations)

Scoped OAuth requires: `event_orchestrations.read`



### PUT /event_orchestrations/{id}
Update an Orchestration

Update a Global Event Orchestration.

Global Event Orchestrations allow you define a set of Global Rules and Router Rules, so that when you ingest events using the Orchestration's Routing Key your events will have actions applied via the Global Rules & then routed to the correct Service by the Router Rules, based on the event's content.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#event-orchestrations)

Scoped OAuth requires: `event_orchestrations.write`



### DELETE /event_orchestrations/{id}
Delete an Orchestration

Delete a Global Event Orchestration.

Once deleted, you will no longer be able to ingest events into PagerDuty using this Orchestration's Routing Key.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#event-orchestrations)

Scoped OAuth requires: `event_orchestrations.write`



### GET /event_orchestrations/{id}/integrations
List Integrations for an Event Orchestration

List the Integrations associated with this Event Orchestrations.

You can use a Routing Key from these Integrations to send events to PagerDuty!

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#event-orchestrations)

Scoped OAuth requires: `event_orchestrations.read`



### POST /event_orchestrations/{id}/integrations
Create an Integration for an Event Orchestration

Create an Integration associated with this Event Orchestration.

You can then use the Routing Key from this new Integration to send events to PagerDuty!

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#event-orchestrations)

Scoped OAuth requires: `event_orchestrations.write`



### GET /event_orchestrations/{id}/integrations/{integration_id}
Get an Integration for an Event Orchestration

Get an Integration associated with this Event Orchestrations.

You can use the Routing Key from this Integration to send events to PagerDuty!

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#event-orchestrations)

Scoped OAuth requires: `event_orchestrations.read`



### PUT /event_orchestrations/{id}/integrations/{integration_id}
Update an Integration for an Event Orchestration

Update an Integration associated with this Event Orchestrations.

You can use the Routing Key from this Integration to send events to PagerDuty!

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#event-orchestrations)

Scoped OAuth requires: `event_orchestrations.write`



### DELETE /event_orchestrations/{id}/integrations/{integration_id}
Delete an Integration for an Event Orchestration

Delete an Integration and its associated Routing Key.

Once deleted, PagerDuty will drop all future events sent to PagerDuty using the Routing Key.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#event-orchestrations)

Scoped OAuth requires: `event_orchestrations.write`



### POST /event_orchestrations/{id}/integrations/migration
Migrate an Integration from one Event Orchestration to another

Move an Integration and its Routing Key from the Event Orchestration specified in the request payload, to the Event Orchestration specified in the request URL.

Any future events sent to this Integration's Routing Key will be processed by this Event Orchestration's Rules.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#event-orchestrations)

Scoped OAuth requires: `event_orchestrations.write`



### GET /event_orchestrations/{id}/global
Get the Global Orchestration for an Event Orchestration

Get the Global Orchestration for an Event Orchestration.

Global Orchestration Rules allows you to create a set of Event Rules. These rules evaluate against all Events sent to an Event Orchestration. When a matching rule is found, it can modify and enhance the event and can route the event to another set of Global Rules within this Orchestration for further processing.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#event-orchestrations)

Scoped OAuth requires: `event_orchestrations.read`



### PUT /event_orchestrations/{id}/global
Update the Global Orchestration for an Event Orchestration

Update the Global Orchestration for an Event Orchestration.

Global Orchestration Rules allows you to create a set of Event Rules. These rules evaluate against all Events sent to an Event Orchestration. When a matching rule is found, it can modify and enhance the event and can route the event to another set of Global Rules within this Orchestration for further processing.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#event-orchestrations)

Scoped OAuth requires: `event_orchestrations.write`



### GET /event_orchestrations/{id}/router
Get the Router for an Event Orchestration

Get a Global Orchestration's Routing Rules.

An Orchestration Router allows you to create a set of Event Rules. The Router evaluates Events you send to this Global Orchestration against each of its rules, one at a time, and routes the event to a specific Service based on the first rule that matches. If an event doesn't match any rules, it'll be sent to service specified in as the `catch_all` or the "Unrouted" Orchestration if no service is specified.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#event-orchestrations)

Scoped OAuth requires: `event_orchestrations.read`



### PUT /event_orchestrations/{id}/router
Update the Router for an Event Orchestration

Update a Global Orchestration's Routing Rules.

An Orchestration Router allows you to create a set of Event Rules. The Router evaluates Events you send to this Global Orchestration against each of its rules, one at a time, and routes the event to a specific Service based on the first rule that matches. If an event doesn't match any rules, it'll be sent to service specified in as the `catch_all` or the "Unrouted" Orchestration if no service is specified.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#event-orchestrations)

Scoped OAuth requires: `event_orchestrations.write`



### GET /event_orchestrations/{id}/unrouted
Get the Unrouted Orchestration for an Event Orchestration

Get a Global Event Orchestration's Rules for Unrouted events.

An Unrouted Orchestration allows you to create a set of Event Rules that will be evaluated against all events that don't match any rules in the Global Orchestration's Router. Events that reach the Unrouted Orchestration will never be routed to a specific Service.

The Unrouted Orchestration evaluates Events sent to it against each of its rules, beginning with the rules in the "start" set. When a matching rule is found, it can modify and enhance the event and can route the event to another set of rules within this Unrouted Orchestration for further processing.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#event-orchestrations)

Scoped OAuth requires: `event_orchestrations.read`



### PUT /event_orchestrations/{id}/unrouted
Update the Unrouted Orchestration for an Event Orchestration

Update a Global Event Orchestration's Rules for Unrouted events.

An Unrouted Orchestration allows you to create a set of Event Rules that will be evaluated against all events that don't match any rules in the Global Orchestration's Router. Events that reach the Unrouted Orchestration will never be routed to a specific Service.

The Unrouted Orchestration evaluates Events sent to it against each of its rules, beginning with the rules in the "start" set. When a matching rule is found, it can modify and enhance the event and can route the event to another set of rules within this Unrouted Orchestration for further processing.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#event-orchestrations)

Scoped OAuth requires: `event_orchestrations.write`



### GET /event_orchestrations/services/{service_id}
Get the Service Orchestration for a Service

Get a Service Orchestration.

A Service Orchestration allows you to create a set of Event Rules. The Service Orchestration evaluates Events sent to this Service against each of its rules, beginning with the rules in the "start" set. When a matching rule is found, it can modify and enhance the event and can route the event to another set of rules within this Service Orchestration for further processing.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#event-orchestrations)

Scoped OAuth requires: `services.read`



### PUT /event_orchestrations/services/{service_id}
Update the Service Orchestration for a Service

Update a Service Orchestration.

A Service Orchestration allows you to create a set of Event Rules. The Service Orchestration evaluates Events sent to this Service against each of its rules, beginning with the rules in the "start" set. When a matching rule is found, it can modify and enhance the event and can route the event to another set of rules within this Service Orchestration for further processing.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#event-orchestrations)

Scoped OAuth requires: `services.write`



### GET /event_orchestrations/services/{service_id}/active
Get the Service Orchestration active status for a Service

Get a Service Orchestration's active status.

A Service Orchestration allows you to set an active status based on whether an event will be evaluated against a service orchestration path (true) or service ruleset (false).

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#event-orchestrations)

Scoped OAuth requires: `services.read`



### PUT /event_orchestrations/services/{service_id}/active
Update the Service Orchestration active status for a Service

Update a Service Orchestration's active status.

A Service Orchestration allows you to set an active status based on whether an event will be evaluated against a service orchestration path (true) or service ruleset (false).

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#event-orchestrations)

Scoped OAuth requires: `services.write`



### GET /event_orchestrations/{id}/cache_variables
List Cache Variables for a Global Event Orchestration

List Cache Variables for a Global Event Orchestration.

Cache Variables allow you to store event data on an Event Orchestration, which can then be used in Event Orchestration rules as part of conditions or actions.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#event-orchestrations)

Scoped OAuth requires: `event_orchestrations.read`



### POST /event_orchestrations/{id}/cache_variables
Create a Cache Variable for a Global Event Orchestration

Create a Cache Variable for a Global Event Orchestration.

Cache Variables allow you to store event data on an Event Orchestration, which can then be used in Event Orchestration rules as part of conditions or actions.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#event-orchestrations)

Scoped OAuth requires: `event_orchestrations.write`



### GET /event_orchestrations/{id}/cache_variables/{cache_variable_id}
Get a Cache Variable for a Global Event Orchestration

Get a Cache Variable for a Global Event Orchestration.

Cache Variables allow you to store event data on an Event Orchestration, which can then be used in Event Orchestration rules as part of conditions or actions.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#event-orchestrations)

Scoped OAuth requires: `event_orchestrations.read`



### PUT /event_orchestrations/{id}/cache_variables/{cache_variable_id}
Update a Cache Variable for a Global Event Orchestration

Update a Cache Variable for a Global Event Orchestration.

Cache Variables allow you to store event data on an Event Orchestration, which can then be used in Event Orchestration rules as part of conditions or actions.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#event-orchestrations)

Scoped OAuth requires: `event_orchestrations.write`



### DELETE /event_orchestrations/{id}/cache_variables/{cache_variable_id}
Delete a Cache Variable for a Global Event Orchestration

Delete a Cache Variable for a Global Event Orchestration.

Cache Variables allow you to store event data on an Event Orchestration, which can then be used in Event Orchestration rules as part of conditions or actions.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#event-orchestrations)

Scoped OAuth requires: `event_orchestrations.write`



### GET /event_orchestrations/{id}/cache_variables/{cache_variable_id}/data
Get Data for an External Data Cache Variable on a Global Event Orchestration

Get the data for an `external_data` type Cache Variable on a Global Orchestration.

Use External Data type Cache Variables to store string, number, or boolean values via a dedicated API endpoint. These stored values can then be used in conditions or actions in Event Orchestration rules.

For more information see the [Knowledge Base](https://support.pagerduty.com/main/docs/event-orchestration-cache-variables)

Scoped OAuth requires: `event_orchestrations.read`



### PUT /event_orchestrations/{id}/cache_variables/{cache_variable_id}/data
Update Data for an External Data Cache Variable on a Global Event Orchestration

Update data for an `external_data` type Cache Variable on a Global Event Orchestration

Use External Data type Cache Variables to store string, number, or boolean values via a dedicated API endpoint. These stored values can then be used in conditions or actions in Event Orchestration rules.

For more information see the [Knowledge Base](https://support.pagerduty.com/main/docs/event-orchestration-cache-variables)

Scoped OAuth requires: `event_orchestrations.write`



### DELETE /event_orchestrations/{id}/cache_variables/{cache_variable_id}/data
Delete Data for an External Data Cache Variable on a Global Event Orchestration

Delete data for an `external_data` type Cache Variable on a Global Event Orchestration

Use External Data type Cache Variables to store string, number, or boolean values via a dedicated API endpoint. These stored values can then be used in conditions or actions in Event Orchestration rules.

For more information see the [Knowledge Base](https://support.pagerduty.com/main/docs/event-orchestration-cache-variables)

Scoped OAuth requires: `event_orchestrations.write`



### GET /event_orchestrations/services/{service_id}/cache_variables
List Cache Variables for a Service Event Orchestration

List Cache Variables for a Service Event Orchestration.

Cache Variables allow you to store event data on an Event Orchestration, which can then be used in Event Orchestration rules as part of conditions or actions.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#event-orchestrations)

Scoped OAuth requires: `services.read`



### POST /event_orchestrations/services/{service_id}/cache_variables
Create a Cache Variable for a Service Event Orchestration

Create a Cache Variable for a Service Event Orchestration.

Cache Variables allow you to store event data on an Event Orchestration, which can then be used in Event Orchestration rules as part of conditions or actions.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#event-orchestrations)

Scoped OAuth requires: `services.write`



### GET /event_orchestrations/services/{service_id}/cache_variables/{cache_variable_id}
Get a Cache Variable for a Service Event Orchestration

Get a Cache Variable for a Service Event Orchestration.

Cache Variables allow you to store event data on an Event Orchestration, which can then be used in Event Orchestration rules as part of conditions or actions.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#event-orchestrations)

Scoped OAuth requires: `services.read`



### PUT /event_orchestrations/services/{service_id}/cache_variables/{cache_variable_id}
Update a Cache Variable for a Service Event Orchestration

Update a Cache Variable for a Service Event Orchestration.

Cache Variables allow you to store event data on an Event Orchestration, which can then be used in Event Orchestration rules as part of conditions or actions.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#event-orchestrations)

Scoped OAuth requires: `services.write`



### DELETE /event_orchestrations/services/{service_id}/cache_variables/{cache_variable_id}
Delete a Cache Variable for a Service Event Orchestration

Delete a Cache Variable for a Service Event Orchestration.

Cache Variables allow you to store event data on an Event Orchestration, which can then be used in Event Orchestration rules as part of conditions or actions.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#event-orchestrations)

Scoped OAuth requires: `services.write`



### GET /event_orchestrations/services/{service_id}/cache_variables/{cache_variable_id}/data
Get Data for an External Data Cache Variable on a Service Event Orchestration

Get the data for an `external_data` type Cache Variable for a Service Event Orchestration.

Use External Data type Cache Variables to store string, number, or boolean values via a dedicated API endpoint. These stored values can then be used in conditions or actions in Event Orchestration rules.

For more information see the [Knowledge Base](https://support.pagerduty.com/main/docs/event-orchestration-cache-variables)

Scoped OAuth requires: `services.read`



### PUT /event_orchestrations/services/{service_id}/cache_variables/{cache_variable_id}/data
Update Data for an External Data Cache Variable on a Service Event Orchestration

Update the data for an `external_data` type Cache Variable on a Service Event Orchestration.

Use External Data type Cache Variables to store string, number, or boolean values via a dedicated API endpoint. These stored values can then be used in conditions or actions in Event Orchestration rules.

For more information see the [Knowledge Base](https://support.pagerduty.com/main/docs/event-orchestration-cache-variables)

Scoped OAuth requires: `services.write`



### DELETE /event_orchestrations/services/{service_id}/cache_variables/{cache_variable_id}/data
Delete Data for an External Data Cache Variable on a Service Event Orchestration

Delete Data for an `external_data` type Cache Variable on a Service Event Orchestration.

Use External Data type Cache Variables to store string, number, or boolean values via a dedicated API endpoint. These stored values can then be used in conditions or actions in Event Orchestration rules.

For more information see the [Knowledge Base](https://support.pagerduty.com/main/docs/event-orchestration-cache-variables)

Scoped OAuth requires: `services.write`



### GET /extension_schemas
List extension schemas

List all extension schemas.

A PagerDuty extension vendor represents a specific type of outbound extension such as Generic Webhook, Slack, ServiceNow.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#extension-schemas)

Scoped OAuth requires: `extension_schemas.read`



### GET /extension_schemas/{id}
Get an extension vendor

Get details about one specific extension vendor.

A PagerDuty extension vendor represents a specific type of outbound extension such as Generic Webhook, Slack, ServiceNow.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#extension-schemas)

Scoped OAuth requires: `extension_schemas.read`



### GET /extensions
List extensions

List existing extensions.

Extensions are representations of Extension Schema objects that are attached to Services.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#extensions)

Scoped OAuth requires: `extensions.read`



### POST /extensions
Create an extension

Create a new Extension.

Extensions are representations of Extension Schema objects that are attached to Services.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#extensions)

Scoped OAuth requires: `extensions.write`



### GET /extensions/{id}
Get an extension

Get details about an existing extension.

Extensions are representations of Extension Schema objects that are attached to Services.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#extensions)

Scoped OAuth requires: `extensions.read`



### DELETE /extensions/{id}
Delete an extension

Delete an existing extension.

Once the extension is deleted, it will not be accessible from the web UI and new incidents won't be able to be created for this extension.

Extensions are representations of Extension Schema objects that are attached to Services.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#extensions)

Scoped OAuth requires: `extensions.write`



### PUT /extensions/{id}
Update an extension

Update an existing extension.

Extensions are representations of Extension Schema objects that are attached to Services.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#extensions)

Scoped OAuth requires: `extensions.write`



### POST /extensions/{id}/enable
Enable an extension

Enable an extension that is temporarily disabled. (This API does not require a request body.)

Extensions are representations of Extension Schema objects that are attached to Services.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#extensions)

Scoped OAuth requires: `extensions.write`



### GET /incident_workflows
List Incident Workflows

List existing Incident Workflows.

This is the best method to use to list all Incident Workflows in your account. If your use case requires listing Incident Workflows associated with a particular Service, you can use the "List Triggers" method to find Incident Workflows configured to start for Incidents in a given Service.

An Incident Workflow is a sequence of configurable Steps and associated Triggers that can execute automated Actions for a given Incident.

Scoped OAuth requires: `incident_workflows.read`



### POST /incident_workflows
Create an Incident Workflow

Create a new Incident Workflow

An Incident Workflow is a sequence of configurable Steps and associated Triggers that can execute automated Actions for a given Incident.

Scoped OAuth requires: `incident_workflows.write`



### GET /incident_workflows/{id}
Get an Incident Workflow

Get an existing Incident Workflow

An Incident Workflow is a sequence of configurable Steps and associated Triggers that can execute automated Actions for a given Incident.

Scoped OAuth requires: `incident_workflows.read`



### DELETE /incident_workflows/{id}
Delete an Incident Workflow

Delete an existing Incident Workflow

An Incident Workflow is a sequence of configurable Steps and associated Triggers that can execute automated Actions for a given Incident.

Scoped OAuth requires: `incident_workflows.write`



### PUT /incident_workflows/{id}
Update an Incident Workflow

Update an Incident Workflow

An Incident Workflow is a sequence of configurable Steps and associated Triggers that can execute automated Actions for a given Incident.

Scoped OAuth requires: `incident_workflows.write`



### POST /incident_workflows/{id}/instances
Start an Incident Workflow Instance

Start an Instance of an Incident Workflow. Sometimes referred to as "triggering a workflow on an incident."

An Incident Workflow is a sequence of configurable Steps and associated Triggers that can execute automated Actions for a given Incident.

Scoped OAuth requires: `incident_workflows:instances.write`



### GET /incident_workflows/actions
List Actions

List Incident Workflow Actions

Scoped OAuth requires: `incident_workflows.read`



### GET /incident_workflows/actions/{id}
Get an Action

Get an Incident Workflow Action

Scoped OAuth requires: `incident_workflows.read`



### GET /incident_workflows/triggers
List Triggers

List existing Incident Workflow Triggers

Scoped OAuth requires: `incident_workflows.read`



### POST /incident_workflows/triggers
Create a Trigger

Create new Incident Workflow Trigger

Scoped OAuth requires: `incident_workflows.write`



### GET /incident_workflows/triggers/{id}
Get a Trigger

Retrieve an existing Incident Workflows Trigger

Scoped OAuth requires: `incident_workflows.read`



### PUT /incident_workflows/triggers/{id}
Update a Trigger

Update an existing Incident Workflow Trigger

Scoped OAuth requires: `incident_workflows.write`



### DELETE /incident_workflows/triggers/{id}
Delete a Trigger

Delete an existing Incident Workflow Trigger

Scoped OAuth requires: `incident_workflows.write`



### POST /incident_workflows/triggers/{id}/services
Associate a Trigger and Service

Associate a Service with an existing Incident Workflow Trigger

Scoped OAuth requires: `incident_workflows.write`



### DELETE /incident_workflows/triggers/{trigger_id}/services/{service_id}
Dissociate a Trigger and Service

Remove a an existing Service from an Incident Workflow Trigger

Scoped OAuth requires: `incident_workflows.write`



### GET /incidents
List incidents

List existing incidents.

An incident represents a problem or an issue that needs to be addressed and resolved.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#incidents)

Scoped OAuth requires: `incidents.read`



### PUT /incidents
Manage incidents

Acknowledge, resolve, escalate or reassign one or more incidents.

An incident represents a problem or an issue that needs to be addressed and resolved.

A maximum of 250 incidents may be updated at a time. If more than this number of incidents are given, the API will respond with status 413 (Request Entity Too Large).

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#incidents)

Scoped OAuth requires: `incidents.write`

This API operation has operation specific rate limits. See the [Rate Limits](https://developer.pagerduty.com/docs/72d3b724589e3-rest-api-rate-limits) page for more information.



### POST /incidents
Create an Incident

Create an incident synchronously without a corresponding event from a monitoring service.

An incident represents a problem or an issue that needs to be addressed and resolved.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#incidents)

Scoped OAuth requires: `incidents.write`

This API operation has operation specific rate limits. See the [Rate Limits](https://developer.pagerduty.com/docs/72d3b724589e3-rest-api-rate-limits) page for more information.



### GET /incidents/{id}
Get an incident

Show detailed information about an incident. Accepts either an incident id, or an incident number.

An incident represents a problem or an issue that needs to be addressed and resolved.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#incidents)

Scoped OAuth requires: `incidents.read`



### PUT /incidents/{id}
Update an incident

Acknowledge, resolve, escalate or reassign an incident.

An incident represents a problem or an issue that needs to be addressed and resolved.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#incidents)

Scoped OAuth requires: `incidents.write`



### GET /incidents/{id}/alerts
List alerts for an incident

List alerts for the specified incident.

An incident represents a problem or an issue that needs to be addressed and resolved.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#incidents)

Scoped OAuth requires: `incidents.read`



### PUT /incidents/{id}/alerts
Manage alerts

Resolve multiple alerts or associate them with different incidents.

An incident represents a problem or an issue that needs to be addressed and resolved. An alert represents a digital signal that was emitted to PagerDuty by the monitoring systems that detected or identified the issue.

A maximum of 250 alerts may be updated at a time. If more than this number of alerts are given, the API will respond with status 413 (Request Entity Too Large).

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#incidents)

Scoped OAuth requires: `incidents.write`



### GET /incidents/{id}/alerts/{alert_id}
Get an alert

Show detailed information about an alert. Accepts an alert id.

An incident represents a problem or an issue that needs to be addressed and resolved.

When a service sends an event to PagerDuty, an alert and corresponding incident is triggered in PagerDuty.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#incidents)

Scoped OAuth requires: `incidents.read`



### PUT /incidents/{id}/alerts/{alert_id}
Update an alert

Resolve an alert or associate an alert with a new parent incident.

An incident represents a problem or an issue that needs to be addressed and resolved.

When a service sends an event to PagerDuty, an alert and corresponding incident is triggered in PagerDuty.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#incidents)

Scoped OAuth requires: `incidents.write`



### PUT /incidents/{id}/business_services/{business_service_id}/impacts
Manually change an Incident's Impact on a Business Service.

Change Impact of an Incident on a Business Service.
Scoped OAuth requires: `incidents.write`



### GET /incidents/{id}/business_services/impacts
List Business Services impacted by the given Incident

Retrieve a list of Business Services that are being impacted by the given Incident.
Scoped OAuth requires: `incidents.read`



### GET /incidents/{id}/custom_fields/values
Get Custom Field Values

Get custom field values for an incident.

<!-- theme: warning -->

Scoped OAuth requires: `incidents.read`



### PUT /incidents/{id}/custom_fields/values
Update Custom Field Values

Set custom field values for an incident.

Scoped OAuth requires: `incidents.write`



### GET /incidents/{id}/log_entries
List log entries for an incident

List log entries for the specified incident.

An incident represents a problem or an issue that needs to be addressed and resolved.

A Log Entry are a record of all events on your account.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#incidents)

Scoped OAuth requires: `incidents.read`



### PUT /incidents/{id}/merge
Merge incidents

Merge a list of source incidents into the target [incident](https://developer.pagerduty.com/api-reference/a47605517c19a-api-concepts#incidents).

After the merge is performed the target incident will contain the source incidents' [alerts](https://developer.pagerduty.com/api-reference/a47605517c19a-api-concepts#alerts),
and the source incidents will be resolved.

Only incidents that have alerts or incidents that were created manually in the UI can be merged.

Open incidents cannot be merged into a resolved incident.

An incident cannot have more than 1000 alerts. The server will return an error if merging the source incidents
will result in the target incident having more than 1000 alerts.

Scoped OAuth requires: `incidents.write`



### GET /incidents/{id}/notes
List notes for an incident

List existing notes for the specified incident.

An incident represents a problem or an issue that needs to be addressed and resolved.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#incidents)

Scoped OAuth requires: `incidents.read`



### POST /incidents/{id}/notes
Create a note on an incident

Create a new note for the specified incident.

An incident represents a problem or an issue that needs to be addressed and resolved.

A maximum of 2000 notes can be added to an incident.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#incidents)

Scoped OAuth requires: `incidents.write`



### GET /incidents/{id}/outlier_incident
Get Outlier Incident

Gets Outlier Incident information for a given Incident on its Service.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#outlier-incident)

Scoped OAuth requires: `incidents.read`



### GET /incidents/{id}/past_incidents
Get Past Incidents

Past Incidents returns Incidents within the past 6 months that have similar metadata and were generated on the same Service as the parent Incident. By default, 5 Past Incidents are returned. Note: This feature is currently available as part of the Event Intelligence package or Digital Operations plan only.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#past_incidents)

Scoped OAuth requires: `incidents.read`



### GET /incidents/{id}/related_change_events
List related Change Events for an Incident

List related Change Events for an Incident, as well as the reason these changes are correlated with the incident.

Change events represent service changes such as deploys, build completion, and configuration changes, providing information that is critical during incident triage or hypercare. For more information on change events, see [Change Events](https://support.pagerduty.com/docs/change-events).

The Change Correlation feature provides incident responders with recent change events that are most relevant to that incident. Change Correlation informs the responder why a particular change event was surfaced and correlated to an incident based on three key factors which include time, related service, or intelligence (machine learning).

Scoped OAuth requires: `incidents.read`



### GET /incidents/{id}/related_incidents
Get Related Incidents

Returns the 20 most recent Related Incidents that are impacting other Responders and Services. Note: This feature is currently available as part of the Event Intelligence package or Digital Operations plan only.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#related_incidents)

Scoped OAuth requires: `incidents.read`



### POST /incidents/{id}/responder_requests
Create a responder request for an incident

Send a new responder request for the specified incident.

An incident represents a problem or an issue that needs to be addressed and resolved.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#incidents)

Scoped OAuth requires: `incidents.write`



### POST /incidents/{id}/snooze
Snooze an incident

Snooze an incident.

An incident represents a problem or an issue that needs to be addressed and resolved.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#incidents)

Scoped OAuth requires: `incidents.write`



### POST /incidents/{id}/status_updates
Create a status update on an incident

Create a new status update for the specified incident. Optionally pass `subject` and `html_message` properties in the request body to override the email notification that gets sent.

An incident represents a problem or an issue that needs to be addressed and resolved.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#incidents)

Scoped OAuth requires: `incidents.write`



### GET /incidents/{id}/status_updates/subscribers
List Notification Subscribers

Retrieve a list of Notification Subscribers on the Incident.

<!-- theme: warning -->
> Users must be added through `POST /incident/{id}/status_updates/subscribers` to be returned from this endpoint.
Scoped OAuth requires: `subscribers.read`



### POST /incidents/{id}/status_updates/subscribers
Add Notification Subscribers

Subscribe the given entities to Incident Status Update Notifications.

Scoped OAuth requires: `subscribers.write`



### POST /incidents/{id}/status_updates/unsubscribe
Remove Notification Subscriber

Unsubscribes the matching Subscribers from Incident Status Update Notifications.

Scoped OAuth requires: `subscribers.write`



### GET /incidents/types
List incident types

List the available incident types

Incident Types are a feature which will allow customers to categorize incidents, such as a security incident, a major incident, or a fraud incident.
These can be filtered by enabled or disabled types.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#incidentType)

Scoped OAuth requires: `incident_types.read`



### POST /incidents/types
Create an Incident Type

Create a new incident type.

Incident Types are a feature which will allow customers to categorize incidents, such as a security incident, a major incident, or a fraud incident.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#incidentType)

Scoped OAuth requires: `incident_types.write`



### GET /incidents/types/{type_id_or_name}
Get an Incident Type

Get detailed information about a single incident type. Accepts either an incident type id, or an incident type name.

Incident Types are a feature which will allow customers to categorize incidents, such as a security incident, a major incident, or a fraud incident.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#incident)

Scoped OAuth requires: `incident_types.read`



### PUT /incidents/types/{type_id_or_name}
Update an Incident Type

Update an Incident Type.

Incident Types are a feature which will allow customers to categorize incidents, such as a security incident, a major incident, or a fraud incident.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#incident)

Scoped OAuth requires: `incident_types.write`



### GET /incidents/types/{type_id_or_name}/custom_fields
List Incident Type Custom Fields

List the custom fields for an incident type.

Custom Fields (CF) are a feature which will allow customers to extend Incidents with their own custom data,
to provide additional context and support features such as customized filtering, search and analytics.
Custom Fields can be applied to different incident types.

Scoped OAuth requires: `custom_fields.read`



### POST /incidents/types/{type_id_or_name}/custom_fields
Create a Custom Field for an Incident Type

Create a Custom Field for an Incident Type

Custom Fields (CF) are a feature which will allow customers to extend Incidents with their own custom data,
to provide additional context and support features such as customized filtering, search and analytics.
Custom Fields can be applied to different incident types.

Scoped OAuth requires: `custom_fields.write`



### GET /incidents/types/{type_id_or_name}/custom_fields/{field_id}
Get an Incident Type Custom Field

Get a custom field for an incident type.

Custom Fields (CF) are a feature which will allow customers to extend Incidents with their own custom data,
to provide additional context and support features such as customized filtering, search and analytics.
Custom Fields can be applied to different incident types.

Scoped OAuth requires: `custom_fields.read`



### PUT /incidents/types/{type_id_or_name}/custom_fields/{field_id}
Update a Custom Field for an Incident Type

Update a custom field for an incident type. Field Options can also be updated within the same call.

Custom Fields (CF) are a feature which will allow customers to extend Incidents with their own custom data,
to provide additional context and support features such as customized filtering, search and analytics.
Custom Fields can be applied to different incident types.

Scoped OAuth requires: `custom_fields.write`



### DELETE /incidents/types/{type_id_or_name}/custom_fields/{field_id}
Delete a Custom Field for an Incident Type

Delete a custom field for an incident type.

Custom Fields (CF) are a feature which will allow customers to extend Incidents with their own custom data,
to provide additional context and support features such as customized filtering, search and analytics.
Custom Fields can be applied to different incident types.

Scoped OAuth requires: `custom_fields.write`



### GET /incidents/types/{type_id_or_name}/custom_fields/{field_id}/field_options
List Field Options on a Custom Field

List field options for a custom field.

Custom Fields (CF) are a feature which will allow customers to extend Incidents with their own custom data,
to provide additional context and support features such as customized filtering, search and analytics.
Custom Fields can be applied to different incident types.

Scoped OAuth requires: `custom_fields.read`



### POST /incidents/types/{type_id_or_name}/custom_fields/{field_id}/field_options
Create a Field Option for a Custom Field

Create a field option for a custom field.

Custom Fields (CF) are a feature which will allow customers to extend Incidents with their own custom data,
to provide additional context and support features such as customized filtering, search and analytics.
Custom Fields can be applied to different incident types.

Scoped OAuth requires: `custom_fields.write`



### GET /incidents/types/{type_id_or_name}/custom_fields/{field_id}/field_options/{field_option_id}
Get a Field Option on a Custom Field

Get a field option on a custom field

Custom Fields (CF) are a feature which will allow customers to extend Incidents with their own custom data,
to provide additional context and support features such as customized filtering, search and analytics.
Custom Fields can be applied to different incident types.

Scoped OAuth requires: `custom_fields.read`



### PUT /incidents/types/{type_id_or_name}/custom_fields/{field_id}/field_options/{field_option_id}
Update a Field Option for a Custom Field

Update a field option for a custom field.

Custom Fields (CF) are a feature which will allow customers to extend Incidents with their own custom data,
to provide additional context and support features such as customized filtering, search and analytics.
Custom Fields can be applied to different incident types.

Scoped OAuth requires: `custom_fields.write`



### DELETE /incidents/types/{type_id_or_name}/custom_fields/{field_id}/field_options/{field_option_id}
Delete a Field Option for a Custom Field

Delete a field option for a custom field.

Custom Fields (CF) are a feature which will allow customers to extend Incidents with their own custom data,
to provide additional context and support features such as customized filtering, search and analytics.
Custom Fields can be applied to different incident types.

Scoped OAuth requires: `custom_fields.write`



### POST /incidents/custom_fields
Create a Field


<!-- theme: warning -->
> ### Deprecated
> This endpoint is deprecated and only works for fields on the Base Incident Type. \
> For more flexibility, we recommend using the Incident Types endpoint: \
> [/incidents/types/{type_id_or_name}/custom_fields](openapiv3.json/paths/~1incidents~1types~1{type_id_or_name}~1custom_fields/post)

Creates a new Custom Field on the Base Incident Type, along with the Field Options if provided. \
An account may have up to 10 Fields.

Scoped OAuth requires: `custom_fields.write`



### GET /incidents/custom_fields
List Fields


<!-- theme: warning -->
> ### Deprecated
> This endpoint is deprecated and only works for fields on the Base Incident Type. \
> For more flexibility, we recommend using the Incident Types endpoint: \
> [/incidents/types/{type_id_or_name}/custom_fields](openapiv3.json/paths/~1incidents~1types~1{type_id_or_name}~1custom_fields/get)

List Custom Fields on the Base Incident Type.

Scoped OAuth requires: `custom_fields.read`



### GET /incidents/custom_fields/{field_id}
Get a Field


<!-- theme: warning -->
> ### Deprecated
> This endpoint is deprecated and only works for fields on the Base Incident Type. \
> For more flexibility, we recommend using the Incident Types endpoint: \
> [/incidents/types/{type_id_or_name}/custom_fields/{field_id}](openapiv3.json/paths/~1incidents~1types~1{type_id_or_name}~1custom_fields~1{field_id}/get)

Show detailed information about a Custom Field on the Base Incident Type.

Scoped OAuth requires: `custom_fields.read`



### PUT /incidents/custom_fields/{field_id}
Update a Field


<!-- theme: warning -->
> ### Deprecated
> This endpoint is deprecated and only works for fields on the Base Incident Type. \
> For more flexibility, we recommend using the Incident Types endpoint: \
> [/incidents/types/{type_id_or_name}/custom_fields/{field_id}](openapiv3.json/paths/~1incidents~1types~1{type_id_or_name}~1custom_fields~1{field_id}/put)

Update a Custom Field on the Base Incident Type.

Scoped OAuth requires: `custom_fields.write`



### DELETE /incidents/custom_fields/{field_id}
Delete a Field


<!-- theme: warning -->
> ### Deprecated
> This endpoint is deprecated and only works for fields on the Base Incident Type. \
> For more flexibility, we recommend using the Incident Types endpoint: \
> [/incidents/types/{type_id_or_name}/custom_fields/{field_id}](openapiv3.json/paths/~1incidents~1types~1{type_id_or_name}~1custom_fields~1{field_id}/delete)

Delete a Custom Field from the Base Incident Type.

Scoped OAuth requires: `custom_fields.write`



### POST /incidents/custom_fields/{field_id}/field_options
Create a Field Option


<!-- theme: warning -->
> ### Deprecated
> This endpoint is deprecated and only works for fields on the Base Incident Type. \
> For more flexibility, we recommend using the Incident Types endpoint: \
> [/incidents/types/{type_id_or_name}/custom_fields/{field_id}/field_options](openapiv3.json/paths/~1incidents~1types~1{type_id_or_name}~1custom_fields~1{field_id}~1field_options/post)

Create a new Field Option for a Custom Field on the Base Incident Type. Field Options may only be created for Fields that have `field_options`. A Field may have no more than 10 enabled options.

Scoped OAuth requires: `custom_fields.write`



### GET /incidents/custom_fields/{field_id}/field_options
List Field Options


<!-- theme: warning -->
> ### Deprecated
> This endpoint is deprecated and only works for fields on the Base Incident Type. \
> For more flexibility, we recommend using the Incident Types endpoint: \
> [/incidents/types/{type_id_or_name}/custom_fields/{field_id}/field_options](openapiv3.json/paths/~1incidents~1types~1{type_id_or_name}~1custom_fields~1{field_id}~1field_options/get)

List all enabled Field Options for a Custom Field on the Base Incident Type.

Scoped OAuth requires: `custom_fields.read`



### PUT /incidents/custom_fields/{field_id}/field_options/{field_option_id}
Update a Field Option


<!-- theme: warning -->
> ### Deprecated
> This endpoint is deprecated and only works for fields on the Base Incident Type. \
> For more flexibility, we recommend using the Incident Types endpoint: \
> [/incidents/types/{type_id_or_name}/custom_fields/{field_id}/field_options/{field_option_id}](openapiv3.json/paths/~1incidents~1types~1{type_id_or_name}~1custom_fields~1{field_id}~1field_options~1{field_option_id}/put)

Update a Field Option for a Custom Field on the Base Incident Type.

Scoped OAuth requires: `custom_fields.write`



### DELETE /incidents/custom_fields/{field_id}/field_options/{field_option_id}
Delete a Field Option


<!-- theme: warning -->
> ### Deprecated
> This endpoint is deprecated and only works for fields on the Base Incident Type. \
> For more flexibility, we recommend using the Incident Types endpoint: \
> [/incidents/types/{type_id_or_name}/custom_fields/{field_id}/field_options/{field_option_id}](openapiv3.json/paths/~1incidents~1types~1{type_id_or_name}~1custom_fields~1{field_id}~1field_options~1{field_option_id}/delete)

Delete a Field Option for a Custom Field on the Base Incident Type.

Scoped OAuth requires: `custom_fields.write`



### GET /license_allocations
List License Allocations

List the Licenses allocated to Users within your Account

Scoped OAuth requires: `licenses.read`



### GET /licenses
List Licenses

List the Licenses associated with your Account

Scoped OAuth requires: `licenses.read`



### GET /log_entries
List log entries

List all of the incident log entries across the entire account.

A log of all the events that happen to an Incident, and these are exposed as Log Entries.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#log-entries)

Scoped OAuth requires: `incidents.read`



### GET /log_entries/{id}
Get a log entry

Get details for a specific incident log entry. This method provides additional information you can use to get at raw event data.

A log of all the events that happen to an Incident, and these are exposed as Log Entries.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#log-entries)

Scoped OAuth requires: `incidents.read`



### PUT /log_entries/{id}/channel
Update log entry channel information.

Update an existing incident log entry channel.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#log-entries)

Scoped OAuth requires: `incidents.write`



### GET /maintenance_windows
List maintenance windows

List existing maintenance windows, optionally filtered by service and/or team, or whether they are from the past, present or future.

A Maintenance Window is used to temporarily disable one or more Services for a set period of time.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#maintenance-windows)

Scoped OAuth requires: `services.read`



### POST /maintenance_windows
Create a maintenance window

Create a new maintenance window for the specified services. No new incidents will be created for a service that is in maintenance.

A Maintenance Window is used to temporarily disable one or more Services for a set period of time.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#maintenance-windows)

Scoped OAuth requires: `services.write`



### GET /maintenance_windows/{id}
Get a maintenance window

Get an existing maintenance window.

A Maintenance Window is used to temporarily disable one or more Services for a set period of time.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#maintenance-windows)

Scoped OAuth requires: `services.read`



### DELETE /maintenance_windows/{id}
Delete or end a maintenance window

Delete an existing maintenance window if it's in the future, or end it if it's currently on-going. If the maintenance window has already ended it cannot be deleted.

A Maintenance Window is used to temporarily disable one or more Services for a set period of time.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#maintenance-windows)

Scoped OAuth requires: `services.write`



### PUT /maintenance_windows/{id}
Update a maintenance window

Update an existing maintenance window.

A Maintenance Window is used to temporarily disable one or more Services for a set period of time.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#maintenance-windows)

Scoped OAuth requires: `services.write`



### GET /notifications
List notifications

List notifications for a given time range, optionally filtered by type (sms_notification, email_notification, phone_notification, or push_notification).

A Notification is created when an Incident is triggered or escalated.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#notifications)

Scoped OAuth requires: `users:notifications.read`



### DELETE /oauth_delegations
Delete all OAuth delegations

Delete all OAuth delegations as per provided query parameters.

An OAuth delegation represents an instance of a user or account's authorization to an app (via OAuth) to access their PagerDuty account.
Common apps include the PagerDuty mobile app, Slack, Microsoft Teams, and third-party apps.

Deleting an OAuth delegation will revoke that instance of an app's access to that user or account.
To grant access again, reauthorization/reauthentication may be required.

At this time, this endpoint only supports deleting mobile app OAuth delegations for a given user.
This is equivalent to signing users out of the mobile app.

This is an asynchronous API, the deletion request itself will be processed within 24 hours.

Scoped OAuth requires: `oauth_delegations.write`



### GET /oauth_delegations/revocation_requests/status
Get OAuth delegations revocation requests status

Get the status of all OAuth delegations revocation requests for this account, specifically how many requests are still pending.

This endpoint is limited to account owners and admins.

Scoped OAuth requires: `oauth_delegations.read`



### GET /oncalls
List all of the on-calls

List the on-call entries during a given time range.

An on-call represents a contiguous unit of time for which a User will be on call for a given Escalation Policy and Escalation Rules.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#on-calls)

Scoped OAuth requires: `oncalls.read`

This API operation has operation specific rate limits. See the [Rate Limits](https://developer.pagerduty.com/docs/72d3b724589e3-rest-api-rate-limits) page for more information.



### GET /paused_incident_reports/alerts
Get Paused Incident Reporting on Alerts

Returns the 5 most recent alerts that were triggered after being paused and the 5 most recent alerts that were resolved after being paused for a given reporting period (maximum 6 months lookback period).  Note: This feature is currently available as part of the Event Intelligence package or Digital Operations plan only.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#paused-incident-reports)

Scoped OAuth requires: `incidents.read`



### GET /paused_incident_reports/counts
Get Paused Incident Reporting counts

Returns reporting counts for paused Incident usage for a given reporting period (maximum 6 months lookback period).  Note: This feature is currently available as part of the Event Intelligence package or Digital Operations plan only.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#paused-incident-reports)

Scoped OAuth requires: `incidents.read`



### GET /priorities
List priorities

List existing priorities, in order (most to least severe).

A priority is a label representing the importance and impact of an incident. This feature is only available on Standard and Enterprise plans.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#priorities)

Scoped OAuth requires: `priorities.read`



### GET /response_plays
List Response Plays

List all of the existing Response Plays.

Response Plays allow you to create packages of Incident Actions that can be applied during an Incident's life cycle.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#response-plays)

When using a Global API token, the `From` header is required.

Scoped OAuth requires: `response_plays.read`



### POST /response_plays
Create a Response Play

Creates a new Response Plays.

Response Plays allow you to create packages of Incident Actions that can be applied during an Incident's life cycle.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#response-plays)

Scoped OAuth requires: `response_plays.write`



### GET /response_plays/{id}
Get a Response Play

Get details about an existing Response Play.

Response Plays allow you to create packages of Incident Actions that can be applied during an Incident's life cycle.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#response-plays)

When using a Global API token, the `From` header is required.
Scoped OAuth requires: `response_plays.read`



### PUT /response_plays/{id}
Update a Response Play

Updates an existing Response Play.

Response Plays allow you to create packages of Incident Actions that can be applied during an Incident's life cycle.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#response-plays)

Scoped OAuth requires: `response_plays.write`



### DELETE /response_plays/{id}
Delete a Response Play

Delete an existing Response Play. Once the Response Play is deleted, the action cannot be undone.

WARNING: When the Response Play is deleted, it is also removed from any Services that were using it.

Response Plays allow you to create packages of Incident Actions that can be applied to an Incident.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#response-plays)

Scoped OAuth requires: `response_plays.write`



### POST /response_plays/{response_play_id}/run
Run a response play

Run a specified response play on a given incident.

Response Plays are a package of Incident Actions that can be applied during an Incident's life cycle.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#response-plays)

Scoped OAuth requires: `response_plays.write`



### GET /rulesets
List Rulesets

List all Rulesets
<!-- theme: warning -->
> ### End-of-life
> Rulesets and Event Rules will end-of-life soon. We highly recommend that you [migrate to Event Orchestration](https://support.pagerduty.com/docs/migrate-to-event-orchestration) as soon as possible so you can take advantage of the new functionality, such as improved UI, rule creation, APIs and Terraform support, advanced conditions, and rule nesting.

Rulesets allow you to route events to an endpoint and create collections of Event Rules, which define sets of actions to take based on event content.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#rulesets)

Scoped OAuth requires: `event_rules.read`



### POST /rulesets
Create a Ruleset

Create a new Ruleset.
<!-- theme: warning -->
> ### End-of-life
> Rulesets and Event Rules will end-of-life soon. We highly recommend that you [migrate to Event Orchestration](https://support.pagerduty.com/docs/migrate-to-event-orchestration) as soon as possible so you can take advantage of the new functionality, such as improved UI, rule creation, APIs and Terraform support, advanced conditions, and rule nesting.

Rulesets allow you to route events to an endpoint and create collections of Event Rules, which define sets of actions to take based on event content.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#rulesets)

Scoped OAuth requires: `event_rules.write`



### GET /rulesets/{id}
Get a Ruleset

Get a Ruleset.
<!-- theme: warning -->
> ### End-of-life
> Rulesets and Event Rules will end-of-life soon. We highly recommend that you [migrate to Event Orchestration](https://support.pagerduty.com/docs/migrate-to-event-orchestration) as soon as possible so you can take advantage of the new functionality, such as improved UI, rule creation, APIs and Terraform support, advanced conditions, and rule nesting.

Rulesets allow you to route events to an endpoint and create collections of Event Rules, which define sets of actions to take based on event content.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#rulesets)

Scoped OAuth requires: `event_rules.read`



### PUT /rulesets/{id}
Update a Ruleset

Update a Ruleset.
<!-- theme: warning -->
> ### End-of-life
> Rulesets and Event Rules will end-of-life soon. We highly recommend that you [migrate to Event Orchestration](https://support.pagerduty.com/docs/migrate-to-event-orchestration) as soon as possible so you can take advantage of the new functionality, such as improved UI, rule creation, APIs and Terraform support, advanced conditions, and rule nesting.

Rulesets allow you to route events to an endpoint and create collections of Event Rules, which define sets of actions to take based on event content.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#rulesets)

Scoped OAuth requires: `event_rules.write`



### DELETE /rulesets/{id}
Delete a Ruleset

Delete a Ruleset.
<!-- theme: warning -->
> ### End-of-life
> Rulesets and Event Rules will end-of-life soon. We highly recommend that you [migrate to Event Orchestration](https://support.pagerduty.com/docs/migrate-to-event-orchestration) as soon as possible so you can take advantage of the new functionality, such as improved UI, rule creation, APIs and Terraform support, advanced conditions, and rule nesting.

Rulesets allow you to route events to an endpoint and create collections of Event Rules, which define sets of actions to take based on event content.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#rulesets)

Scoped OAuth requires: `event_rules.write`



### GET /rulesets/{id}/rules
List Event Rules

List all Event Rules on a Ruleset.
<!-- theme: warning -->
> ### End-of-life
> Rulesets and Event Rules will end-of-life soon. We highly recommend that you [migrate to Event Orchestration](https://support.pagerduty.com/docs/migrate-to-event-orchestration) as soon as possible so you can take advantage of the new functionality, such as improved UI, rule creation, APIs and Terraform support, advanced conditions, and rule nesting.

Rulesets allow you to route events to an endpoint and create collections of Event Rules, which define sets of actions to take based on event content.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#rulesets)

Note: Create and Update on rules will accept 'description' or 'summary' interchangeably as an extraction action target. Get and List on rules will always return 'summary' as the target. If you are expecting 'description' please change your automation code to expect 'summary' instead.

Scoped OAuth requires: `event_rules.read`



### POST /rulesets/{id}/rules
Create an Event Rule

Create a new Event Rule.
<!-- theme: warning -->
> ### End-of-life
> Rulesets and Event Rules will end-of-life soon. We highly recommend that you [migrate to Event Orchestration](https://support.pagerduty.com/docs/migrate-to-event-orchestration) as soon as possible so you can take advantage of the new functionality, such as improved UI, rule creation, APIs and Terraform support, advanced conditions, and rule nesting.

Rulesets allow you to route events to an endpoint and create collections of Event Rules, which define sets of actions to take based on event content.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#rulesets)

Note: Create and Update on rules will accept 'description' or 'summary' interchangeably as an extraction action target. Get and List on rules will always return 'summary' as the target. If you are expecting 'description' please change your automation code to expect 'summary' instead.

Scoped OAuth requires: `event_rules.write`



### GET /rulesets/{id}/rules/{rule_id}
Get an Event Rule

Get an Event Rule.
<!-- theme: warning -->
> ### End-of-life
> Rulesets and Event Rules will end-of-life soon. We highly recommend that you [migrate to Event Orchestration](https://support.pagerduty.com/docs/migrate-to-event-orchestration) as soon as possible so you can take advantage of the new functionality, such as improved UI, rule creation, APIs and Terraform support, advanced conditions, and rule nesting.

Rulesets allow you to route events to an endpoint and create collections of Event Rules, which define sets of actions to take based on event content.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#rulesets)

Note: Create and Update on rules will accept 'description' or 'summary' interchangeably as an extraction action target. Get and List on rules will always return 'summary' as the target. If you are expecting 'description' please change your automation code to expect 'summary' instead.

Scoped OAuth requires: `event_rules.read`



### PUT /rulesets/{id}/rules/{rule_id}
Update an Event Rule

Update an Event Rule. Note that the endpoint supports partial updates, so any number of the writable fields can be provided.
<!-- theme: warning -->
> ### End-of-life
> Rulesets and Event Rules will end-of-life soon. We highly recommend that you [migrate to Event Orchestration](https://support.pagerduty.com/docs/migrate-to-event-orchestration) as soon as possible so you can take advantage of the new functionality, such as improved UI, rule creation, APIs and Terraform support, advanced conditions, and rule nesting.

Rulesets allow you to route events to an endpoint and create collections of Event Rules, which define sets of actions to take based on event content.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#rulesets)

Note: Create and Update on rules will accept 'description' or 'summary' interchangeably as an extraction action target. Get and List on rules will always return 'summary' as the target. If you are expecting 'description' please change your automation code to expect 'summary' instead.

Scoped OAuth requires: `event_rules.write`



### DELETE /rulesets/{id}/rules/{rule_id}
Delete an Event Rule

Delete an Event Rule.
<!-- theme: warning -->
> ### End-of-life
> Rulesets and Event Rules will end-of-life soon. We highly recommend that you [migrate to Event Orchestration](https://support.pagerduty.com/docs/migrate-to-event-orchestration) as soon as possible so you can take advantage of the new functionality, such as improved UI, rule creation, APIs and Terraform support, advanced conditions, and rule nesting.

Rulesets allow you to route events to an endpoint and create collections of Event Rules, which define sets of actions to take based on event content.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#rulesets)

Scoped OAuth requires: `event_rules.write`



### GET /schedules
List schedules

List the on-call schedules.

A Schedule determines the time periods that users are On-Call.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#schedules)

Scoped OAuth requires: `schedules.read`



### POST /schedules
Create a schedule

Create a new on-call schedule.

A Schedule determines the time periods that users are On-Call.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#schedules)

Scoped OAuth requires: `schedules.write`



### GET /schedules/{id}
Get a schedule

Show detailed information about a schedule, including entries for each layer.
Scoped OAuth requires: `schedules.read`



### DELETE /schedules/{id}
Delete a schedule

Delete an on-call schedule.

A Schedule determines the time periods that users are On-Call.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#schedules)

Scoped OAuth requires: `schedules.write`



### PUT /schedules/{id}
Update a schedule

Update an existing on-call schedule.

A Schedule determines the time periods that users are On-Call.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#schedules)

Scoped OAuth requires: `schedules.write`



### GET /schedules/{id}/audit/records
List audit records for a schedule

The returned records are sorted by the `execution_time` from newest to oldest.

See [`Cursor-based pagination`](https://developer.pagerduty.com/docs/rest-api-v2/pagination/) for instructions on how to paginate through the result set.

For more information see the [Audit API Document](https://developer.pagerduty.com/docs/rest-api-v2/audit-records-api/).

Scoped OAuth requires: `audit_records.read`



### GET /schedules/{id}/overrides
List overrides

List overrides for a given time range.

A Schedule determines the time periods that users are On-Call.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#schedules)

Scoped OAuth requires: `schedules.read`



### POST /schedules/{id}/overrides
Create one or more overrides

Create one or more overrides, each for a specific user covering a specified time range. If you create an override on top of an existing override, the last created override will have priority.

A Schedule determines the time periods that users are On-Call.

Note: An older implementation of this endpoint only supported creating a single ocverride per request. That functionality is still supported, but deprecated and may be removed in the future.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#schedules)

Scoped OAuth requires: `schedules.write`



### DELETE /schedules/{id}/overrides/{override_id}
Delete an override

Remove an override.

You cannot remove a past override.

If the override start time is before the current time, but the end time is after the current time, the override will be truncated to the current time.

If the override is truncated, the status code will be 200 OK, as opposed to a 204 No Content for a successful delete.

A Schedule determines the time periods that users are On-Call.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#schedules)

Scoped OAuth requires: `schedules.write`



### GET /schedules/{id}/users
List users on call.

List all of the users on call in a given schedule for a given time range.

A Schedule determines the time periods that users are On-Call.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#schedules)

Scoped OAuth requires: `users.read`



### POST /schedules/preview
Preview a schedule

Preview what an on-call schedule would look like without saving it.

A Schedule determines the time periods that users are On-Call.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#schedules)

Scoped OAuth requires: `schedules.write`



### POST /service_dependencies/associate
Associate service dependencies

Create new dependencies between two services.

Business services model capabilities that span multiple technical services and that may be owned by several different teams.

A service can have a maximum of 2,000 dependencies with a depth limit of 100. If the limit is reached, the API will respond with an error.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#business-services)

Scoped OAuth requires: `services.write`



### GET /service_dependencies/business_services/{id}
Get Business Service dependencies

Get all immediate dependencies of any Business Service.

Business Services model capabilities that span multiple technical services and that may be owned by several different teams.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#business-services)

Scoped OAuth requires: `services.read`



### POST /service_dependencies/disassociate
Disassociate service dependencies

Disassociate dependencies between two services.

Business services model capabilities that span multiple technical services and that may be owned by several different teams.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#business-services)

Scoped OAuth requires: `services.write`



### GET /service_dependencies/technical_services/{id}
Get technical service dependencies

Get all immediate dependencies of any technical service.
Technical services are also known as `services`.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#services)

Scoped OAuth requires: `services.read`



### GET /services
List services

List existing Services.

A service may represent an application, component, or team you wish to open incidents against.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#services)

Scoped OAuth requires: `services.read`



### POST /services
Create a service

Create a new service.

If `status` is included in the request, it must have a value of `active` when creating a new service. If a different status is required, make a second request to update the service.

A service may represent an application, component, or team you wish to open incidents against.

There is a limit of 25,000 services per account. If the limit is reached, the API will respond with an error. There is also a limit of 100,000 open Incidents per Service. If the limit is reached and `auto_resolve_timeout` is disabled (set to 0 or null), the `auto_resolve_timeout` property will automatically be set to  84600 (1 day).

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#services)

Scoped OAuth requires: `services.write`



### GET /services/{id}
Get a service

Get details about an existing service.

A service may represent an application, component, or team you wish to open incidents against.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#services)

Scoped OAuth requires: `services.read`



### DELETE /services/{id}
Delete a service

Delete an existing service.

Once the service is deleted, it will not be accessible from the web UI and new incidents won't be able to be created for this service.

A service may represent an application, component, or team you wish to open incidents against.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#services)

Scoped OAuth requires: `services.write`



### PUT /services/{id}
Update a service

Update an existing service.

A service may represent an application, component, or team you wish to open incidents against.

There is a limit of 100,000 open Incidents per Service. If the limit is reached and you disable `auto_resolve_timeout` (set to 0 or null), the API will respond with an error.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#services)

Scoped OAuth requires: `services.write`



### GET /services/{id}/audit/records
List audit records for a service

The returned records are sorted by the `execution_time` from newest to oldest.

See [`Cursor-based pagination`](https://developer.pagerduty.com/docs/rest-api-v2/pagination/) for instructions on how to paginate through the result set.

For more information see the [Audit API Document](https://developer.pagerduty.com/docs/rest-api-v2/audit-records-api/).

Scoped OAuth requires: `audit_records.read`



### GET /services/{id}/change_events
List Change Events for a service

List all of the existing Change Events for a service.

Scoped OAuth requires: `services.read`



### POST /services/{id}/integrations
Create a new integration

Create a new integration belonging to a Service.

A service may represent an application, component, or team you wish to open incidents against.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#services)

Scoped OAuth requires: `services.write`



### PUT /services/{id}/integrations/{integration_id}
Update an existing integration

Update an integration belonging to a Service.

A service may represent an application, component, or team you wish to open incidents against.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#services)

Scoped OAuth requires: `services.write`



### GET /services/{id}/integrations/{integration_id}
View an integration

Get details about an integration belonging to a service.

A service may represent an application, component, or team you wish to open incidents against.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#services)

Scoped OAuth requires: `services.read`



### GET /services/{id}/rules
List Service's Event Rules

List Event Rules on a Service.
<!-- theme: warning -->
> ### End-of-life
> Rulesets and Event Rules will end-of-life soon. We highly recommend that you [migrate to Event Orchestration](https://support.pagerduty.com/docs/migrate-to-event-orchestration) as soon as possible so you can take advantage of the new functionality, such as improved UI, rule creation, APIs and Terraform support, advanced conditions, and rule nesting.

Scoped OAuth requires: `services.read`



### POST /services/{id}/rules
Create an Event Rule on a Service

Create a new Event Rule on a Service.
<!-- theme: warning -->
> ### End-of-life
> Rulesets and Event Rules will end-of-life soon. We highly recommend that you [migrate to Event Orchestration](https://support.pagerduty.com/docs/migrate-to-event-orchestration) as soon as possible so you can take advantage of the new functionality, such as improved UI, rule creation, APIs and Terraform support, advanced conditions, and rule nesting.

Scoped OAuth requires: `services.write`



### POST /services/{id}/rules/convert
Convert a Service's Event Rules into Event Orchestration Rules

Convert this Service's Event Rules into functionally equivalent Event Orchestration Rules.

Sending a request to this API endpoint has several effects:

1. Automatically creates Event Orchestration Rules for this Service that will behave identically as this Service's currently configured Event Rules.
2. Makes all existing Event Rules for this Service read-only. All future updates need to be made via the newly created Event Orchestration rules.

Sending a request to this API endpoint will **not** change how future events will be processed. If past events for this Service have been evaluated via Event Rules then new events sent to this Service will also continue to be evaluated via the (now read-only) Event Rules. To change this Service so that new events start being evaluated via the newly created Event Orchestration Rules use the [Update the Service Orchestration active status for a Service API](https://developer.pagerduty.com/api-reference/855659be83d9e-update-the-service-orchestration-active-status-for-a-service).

> ### End-of-life
> Event Rules will end-of-life soon. We highly recommend that you use this API to [migrate to Event Orchestration](https://support.pagerduty.com/docs/migrate-to-event-orchestration) as soon as possible so you can take advantage of the new functionality, such as improved UI, rule creation, APIs and Terraform support, advanced conditions, and rule nesting.

Scoped OAuth requires: `services.write`



### GET /services/{id}/rules/{rule_id}
Get an Event Rule from a Service

Get an Event Rule from a Service.
<!-- theme: warning -->
> ### End-of-life
> Rulesets and Event Rules will end-of-life soon. We highly recommend that you [migrate to Event Orchestration](https://support.pagerduty.com/docs/migrate-to-event-orchestration) as soon as possible so you can take advantage of the new functionality, such as improved UI, rule creation, APIs and Terraform support, advanced conditions, and rule nesting.

Scoped OAuth requires: `services.read`



### PUT /services/{id}/rules/{rule_id}
Update an Event Rule on a Service

Update an Event Rule on a Service. Note that the endpoint supports partial updates, so any number of the writable fields can be provided.
<!-- theme: warning -->
> ### End-of-life
> Rulesets and Event Rules will end-of-life soon. We highly recommend that you [migrate to Event Orchestration](https://support.pagerduty.com/docs/migrate-to-event-orchestration) as soon as possible so you can take advantage of the new functionality, such as improved UI, rule creation, APIs and Terraform support, advanced conditions, and rule nesting.

Scoped OAuth requires: `services.write`



### DELETE /services/{id}/rules/{rule_id}
Delete an Event Rule from a Service

Delete an Event Rule from a Service.
<!-- theme: warning -->
> ### End-of-life
> Rulesets and Event Rules will end-of-life soon. We highly recommend that you [migrate to Event Orchestration](https://support.pagerduty.com/docs/migrate-to-event-orchestration) as soon as possible so you can take advantage of the new functionality, such as improved UI, rule creation, APIs and Terraform support, advanced conditions, and rule nesting.

Scoped OAuth requires: `services.write`



### POST /services/custom_fields
Create a Field

<!-- theme: warning -->
> ### Early Access
> This endpoint is in Early Access and may change at any time. You must pass in the `X-EARLY-ACCESS` header with `service-custom-fields-preview` to access it.

Creates a new Custom Field for Services, along with the Field Options if provided.

Scoped OAuth requires: `custom_fields.write`



### GET /services/custom_fields
List Fields

<!-- theme: warning -->
> ### Early Access
> This endpoint is in Early Access and may change at any time. You must pass in the `X-EARLY-ACCESS` header with `service-custom-fields-preview` to access it.

List Custom Fields available for Services.

Scoped OAuth requires: `custom_fields.read`



### GET /services/custom_fields/{field_id}
Get a Field

<!-- theme: warning -->
> ### Early Access
> This endpoint is in Early Access and may change at any time. You must pass in the `X-EARLY-ACCESS` header with `service-custom-fields-preview` to access it.

Show detailed information about a Custom Field for Services.

Scoped OAuth requires: `custom_fields.read`



### PUT /services/custom_fields/{field_id}
Update a Field

<!-- theme: warning -->
> ### Early Access
> This endpoint is in Early Access and may change at any time. You must pass in the `X-EARLY-ACCESS` header with `service-custom-fields-preview` to access it.

Update a Custom Field for Services.

Scoped OAuth requires: `custom_fields.write`



### DELETE /services/custom_fields/{field_id}
Delete a Field

<!-- theme: warning -->
> ### Early Access
> This endpoint is in Early Access and may change at any time. You must pass in the `X-EARLY-ACCESS` header with `service-custom-fields-preview` to access it.

Delete a Custom Field from Services.

Scoped OAuth requires: `custom_fields.write`



### GET /services/custom_fields/{field_id}/field_options
List Field Options

<!-- theme: warning -->
> ### Early Access
> This endpoint is in Early Access and may change at any time. You must pass in the `X-EARLY-ACCESS` header with `service-custom-fields-preview` to access it.

List all options for a given field.

Scoped OAuth requires: `custom_fields.read`



### POST /services/custom_fields/{field_id}/field_options
Create a Field Option

<!-- theme: warning -->
> ### Early Access
> This endpoint is in Early Access and may change at any time. You must pass in the `X-EARLY-ACCESS` header with `service-custom-fields-preview` to access it.

Create a new option for the given field.

Scoped OAuth requires: `custom_fields.write`



### GET /services/custom_fields/{field_id}/field_options/{field_option_id}
Get a Field Option

<!-- theme: warning -->
> ### Early Access
> This endpoint is in Early Access and may change at any time. You must pass in the `X-EARLY-ACCESS` header with `service-custom-fields-preview` to access it.

Get a field option for a given field.

Scoped OAuth requires: `custom_fields.read`



### PUT /services/custom_fields/{field_id}/field_options/{field_option_id}
Update a Field Option

<!-- theme: warning -->
> ### Early Access
> This endpoint is in Early Access and may change at any time. You must pass in the `X-EARLY-ACCESS` header with `service-custom-fields-preview` to access it.

Update a field option for a given field.

Scoped OAuth requires: `custom_fields.write`



### DELETE /services/custom_fields/{field_id}/field_options/{field_option_id}
Delete a Field Option

<!-- theme: warning -->
> ### Early Access
> This endpoint is in Early Access and may change at any time. You must pass in the `X-EARLY-ACCESS` header with `service-custom-fields-preview` to access it.

Delete a field option.

Scoped OAuth requires: `custom_fields.write`



### GET /services/{id}/custom_fields/values
Get Custom Field Values

<!-- theme: warning -->
> ### Early Access
> This endpoint is in Early Access and may change at any time. You must pass in the `X-EARLY-ACCESS` header with `service-custom-fields-preview` to access it.

Get custom field values for a service.

Scoped OAuth requires: `services.read`



### PUT /services/{id}/custom_fields/values
Update Custom Field Values

<!-- theme: warning -->
> ### Early Access
> This endpoint is in Early Access and may change at any time. You must pass in the `X-EARLY-ACCESS` header with `service-custom-fields-preview` to access it.

Set custom field values for a service.

Scoped OAuth requires: `services.write`



### GET /standards
List Standards

Get all standards of an account.

Scoped OAuth requires: `standards.read`



### PUT /standards/{id}
Update a standard

Updates a standard

Scoped OAuth requires: `standards.write`



### GET /standards/scores/{resource_type}
List resources' standards scores

List standards applied to a set of resources

Scoped OAuth requires: `standards.read`



### GET /standards/scores/{resource_type}/{id}
List a resource's standards scores

List standards applied to a specific resource

Scoped OAuth requires: `standards.read`



### GET /status_dashboards
List Status Dashboards

Get all your account's custom Status Dashboard views.

Scoped OAuth requires: `status_dashboards.read`



### GET /status_dashboards/{id}
Get a single Status Dashboard by `id`

Get a Status Dashboard by its PagerDuty `id`.

Scoped OAuth requires: `status_dashboards.read`



### GET /status_dashboards/{id}/service_impacts
Get impacted Business Services for a Status Dashboard by `id`.

Get impacted Business Services for a Status Dashboard by `id`

This endpoint does not return an exhaustive list of Business Services but rather provides access to the most impacted on the specified Status Dashboard up to the limit of 200.

The returned Business Services are sorted first by Impact, secondarily by most recently impacted, and finally by name.

To get Impact information about a specific Business Service on the Status Dashboard that does not appear in the Impact-sorted response, use the `ids[]` parameter on the `/business_services/impacts` endpoint.

Scoped OAuth requires: `status_dashboards.read`



### GET /status_dashboards/url_slugs/{url_slug}
Get a single Status Dashboard by `url_slug`

Get a Status Dashboard by its PagerDuty `url_slug`.  A `url_slug` is a human-readable reference
for a custom Status Dashboard that may be created or changed in the UI. It will generally be a `dash-separated-string-like-this`.

Scoped OAuth requires: `status_dashboards.read`



### GET /status_dashboards/url_slugs/{url_slug}/service_impacts
Get impacted Business Services for a  Status Dashboard by `url_slug`

Get Business Service Impacts for the Business Services on a Status Dashboard by its `url_slug`. A `url_slug` is a human-readable reference
for a custom Status Dashboard that may be created or changed in the UI. It will generally be a `dash-separated-string-like-this`.

This endpoint does not return an exhaustive list of Business Services but rather provides access to the most impacted on the Status Dashboard up to the limit of 200.

The returned Business Services are sorted first by Impact, secondarily by most recently impacted, and finally by name.

To get impact information about a specific Business Service on the Status Dashboard that does not appear in the Impact-sored response, use the `ids[]` parameter on the `/business_services/impacts` endpoint.

Scoped OAuth requires: `status_dashboards.read`



### GET /status_pages
List Status Pages

List Status Pages.

Scoped OAuth requires: `status_pages.read`



### GET /status_pages/{id}/impacts
List Status Page Impacts

List Impacts for a Status Page by Status Page ID.

Scoped OAuth requires: `status_pages.read`



### GET /status_pages/{id}/impacts/{impact_id}
Get a Status Page Impact

Get an Impact for a Status Page by Status Page ID and Impact ID.

Scoped OAuth requires: `status_pages.read`



### GET /status_pages/{id}/services
List Status Page Services

List Services for a Status Page by Status Page ID.

Scoped OAuth requires: `status_pages.read`



### GET /status_pages/{id}/services/{service_id}
Get a Status Page Service

Get a Service for a Status Page by Status Page ID and Service ID.

Scoped OAuth requires: `status_pages.read`



### GET /status_pages/{id}/severities
List Status Page Severities

List Severities for a Status Page by Status Page ID.

Scoped OAuth requires: `status_pages.read`



### GET /status_pages/{id}/severities/{severity_id}
Get a Status Page Severity

Get a Severity for a Status Page by Status Page ID and Severity ID.

Scoped OAuth requires: `status_pages.read`



### GET /status_pages/{id}/statuses
List Status Page Statuses

List Statuses for a Status Page by Status Page ID.

Scoped OAuth requires: `status_pages.read`



### GET /status_pages/{id}/statuses/{status_id}
Get a Status Page Status

Get a Status for a Status Page by Status Page ID and Status ID.

Scoped OAuth requires: `status_pages.read`



### GET /status_pages/{id}/posts
List Status Page Posts

List Posts for a Status Page by Status Page ID.

Scoped OAuth requires: `status_pages.read`



### POST /status_pages/{id}/posts
Create a Status Page Post

Create a Post for a Status Page by Status Page ID.

Scoped OAuth requires: `status_pages.write`



### GET /status_pages/{id}/posts/{post_id}
Get a Status Page Post

Get a Post for a Status Page by Status Page ID and Post ID.

Scoped OAuth requires: `status_pages.read`



### PUT /status_pages/{id}/posts/{post_id}
Update a Status Page Post

Update a Post for a Status Page by Status Page ID.

Scoped OAuth requires: `status_pages.write`



### DELETE /status_pages/{id}/posts/{post_id}
Delete a Status Page Post

Delete a Post for a Status Page by Status Page ID and Post ID.

Scoped OAuth requires: `status_pages.write`



### GET /status_pages/{id}/posts/{post_id}/post_updates
List Status Page Post Updates

List Post Updates for a Status Page by Status Page ID and Post ID.

Scoped OAuth requires: `status_pages.read`



### POST /status_pages/{id}/posts/{post_id}/post_updates
Create a Status Page Post Update

Create a Post Update for a Post by Post ID.

Scoped OAuth requires: `status_pages.write`



### GET /status_pages/{id}/posts/{post_id}/post_updates/{post_update_id}
Get a Status Page Post Update

Get a Post Update for a Post by Post ID and Post Update ID.

Scoped OAuth requires: `status_pages.read`



### PUT /status_pages/{id}/posts/{post_id}/post_updates/{post_update_id}
Update a Status Page Post Update

Update a Post Update for a Post by Post ID and Post Update ID.

Scoped OAuth requires: `status_pages.write`



### DELETE /status_pages/{id}/posts/{post_id}/post_updates/{post_update_id}
Delete a Status Page Post Update

Delete a Post Update for a Post by Post ID and Post Update ID.

Scoped OAuth requires: `status_pages.write`



### GET /status_pages/{id}/posts/{post_id}/postmortem
Get a Post Postmortem

Get a Postmortem for a Post by Post ID.

Scoped OAuth requires: `status_pages.read`



### POST /status_pages/{id}/posts/{post_id}/postmortem
Create a Post Postmortem

Create a Postmortem for a Post by Post ID.

Scoped OAuth requires: `status_pages.write`



### PUT /status_pages/{id}/posts/{post_id}/postmortem
Update a Post Postmortem

Update a Postmortem for a Post by Post ID.

Scoped OAuth requires: `status_pages.write`



### DELETE /status_pages/{id}/posts/{post_id}/postmortem
Delete a Post Postmortem

Delete a Postmortem for a Post by Post ID.

Scoped OAuth requires: `status_pages.write`



### GET /status_pages/{id}/subscriptions
List Status Page Subscriptions

List Subscriptions for a Status Page by Status Page ID.

Scoped OAuth requires: `status_pages.read`



### POST /status_pages/{id}/subscriptions
Create a Status Page Subscription

Create a Subscription for a Status Page by Status Page ID.

Scoped OAuth requires: `status_pages.write`



### GET /status_pages/{id}/subscriptions/{subscription_id}
Get a Status Page Subscription

Get a Subscription for a Status Page by Status Page ID and Subscription ID.

Scoped OAuth requires: `status_pages.read`



### DELETE /status_pages/{id}/subscriptions/{subscription_id}
Delete a Status Page Subscription

Delete a Subscription for a Status Page by Status Page ID and Subscription ID.

Scoped OAuth requires: `status_pages.write`



### GET /tags
List tags

List all of your account's tags.

A Tag is applied to Escalation Policies, Teams or Users and can be used to filter them.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#tags)

Scoped OAuth requires: `tags.read`



### POST /tags
Create a tag

Create a Tag.

A Tag is applied to Escalation Policies, Teams or Users and can be used to filter them.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#tags)

Scoped OAuth requires: `tags.write`



### GET /tags/{id}
Get a tag

Get details about an existing Tag.

A Tag is applied to Escalation Policies, Teams or Users and can be used to filter them.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#tags)

Scoped OAuth requires: `tags.read`



### DELETE /tags/{id}
Delete a tag

Remove an existing Tag.

A Tag is applied to Escalation Policies, Teams or Users and can be used to filter them.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#tags)

Scoped OAuth requires: `tags.write`



### GET /tags/{id}/{entity_type}
Get connected entities

Get related Users, Teams or Escalation Policies for the Tag.

A Tag is applied to Escalation Policies, Teams or Users and can be used to filter them.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#tags)

Scoped OAuth requires: `tags.read`



### POST /teams
Create a team

Create a new Team.

A team is a collection of Users and Escalation Policies that represent a group of people within an organization.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#teams)

Scoped OAuth requires: `teams.write`



### GET /teams
List teams

List teams of your PagerDuty account, optionally filtered by a search query.

A team is a collection of Users and Escalation Policies that represent a group of people within an organization.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#teams)

Scoped OAuth requires: `teams.read`



### GET /teams/{id}
Get a team

Get details about an existing team.

A team is a collection of Users and Escalation Policies that represent a group of people within an organization.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#teams)

Scoped OAuth requires: `teams.read`



### DELETE /teams/{id}
Delete a team

Remove an existing team.

Succeeds only if the team has no associated Escalation Policies, Services, Schedules and Subteams.

All associated unresovled incidents will be reassigned to another team (if specified) or will loose team association, thus becoming account-level (with visibility implications).

Note that the incidents reassignment process is asynchronous and has no guarantee to complete before the API call return.

A team is a collection of Users and Escalation Policies that represent a group of people within an organization.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#teams)

Scoped OAuth requires: `teams.write`



### PUT /teams/{id}
Update a team

Update an existing team.

A team is a collection of Users and Escalation Policies that represent a group of people within an organization.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#teams)

Scoped OAuth requires: `teams.write`



### GET /teams/{id}/audit/records
List audit records for a team

The returned records are sorted by the `execution_time` from newest to oldest.

See [`Cursor-based pagination`](https://developer.pagerduty.com/docs/rest-api-v2/pagination/) for instructions on how to paginate through the result set.

For more information see the [Audit API Document](https://developer.pagerduty.com/docs/rest-api-v2/audit-records-api/).

Scoped OAuth requires: `audit_records.read`



### DELETE /teams/{id}/escalation_policies/{escalation_policy_id}
Remove an escalation policy from a team

Remove an escalation policy from a team.

A team is a collection of Users and Escalation Policies that represent a group of people within an organization.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#teams)

Scoped OAuth requires: `teams.write`



### PUT /teams/{id}/escalation_policies/{escalation_policy_id}
Add an escalation policy to a team

Add an escalation policy to a team.

A team is a collection of Users and Escalation Policies that represent a group of people within an organization.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#teams)

Scoped OAuth requires: `teams.write`



### GET /teams/{id}/members
List members of a team

Get information about members on a team.

A team is a collection of Users and Escalation Policies that represent a group of people within an organization.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#teams)

Scoped OAuth requires: `teams.read`



### GET /teams/{id}/notification_subscriptions
List Team Notification Subscriptions

Retrieve a list of Notification Subscriptions the given Team has.

<!-- theme: warning -->
> Teams must be added through `POST /teams/{id}/notification_subscriptions` to be returned from this endpoint.

Scoped OAuth requires: `subscribers.read`



### POST /teams/{id}/notification_subscriptions
Create Team Notification Subscriptions

Create new Notification Subscriptions for the given Team.

Scoped OAuth requires: `subscribers.write`



### POST /teams/{id}/notification_subscriptions/unsubscribe


Unsubscribe the given Team from Notifications on the matching Subscribable entities.

Scoped OAuth requires: `subscribers.write`



### DELETE /teams/{id}/users/{user_id}
Remove a user from a team

Remove a user from a team.

A team is a collection of Users and Escalation Policies that represent a group of people within an organization.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#teams)

Scoped OAuth requires: `teams.write`



### PUT /teams/{id}/users/{user_id}
Add a user to a team

Add a user to a team. Attempting to add a user with the `read_only_user` role will return a 400 error.

A team is a collection of Users and Escalation Policies that represent a group of people within an organization.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#teams)

Scoped OAuth requires: `teams.write`



### GET /templates
List templates

Get a list of all the template on an account

Scoped OAuth requires: `templates.read`



### POST /templates
Create a template

Create a new template

Scoped OAuth requires: `templates.write`



### GET /templates/{id}
Get a template

Get a single template on the account

Scoped OAuth requires: `templates.read`



### PUT /templates/{id}
Update a template

Update an existing template

Scoped OAuth requires: `templates.write`



### DELETE /templates/{id}
Delete a template

Delete a specific of templates on the account

Scoped OAuth requires: `templates.write`



### POST /templates/{id}/render
Render a template

Render a template. This endpoint has a variable request body depending on the template type. For the `status_update` template type, the caller will provide the incident id, and a status update message.

Scoped OAuth requires: `templates.read`



### GET /templates/fields
List template fields

Get a list of fields that can be used on the account templates.

Scoped OAuth requires: `templates.read`



### GET /users
List users

List users of your PagerDuty account, optionally filtered by a search query.

Users are members of a PagerDuty account that have the ability to interact with Incidents and other data on the account.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#users)

Scoped OAuth requires: `users.read`



### POST /users
Create a user

Create a new user.

Users are members of a PagerDuty account that have the ability to interact with Incidents and other data on the account.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#users)

Scoped OAuth requires: `users.write`



### GET /users/{id}
Get a user

Get details about an existing user.

Users are members of a PagerDuty account that have the ability to interact with Incidents and other data on the account.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#users)

Scoped OAuth requires: `users.read`



### DELETE /users/{id}
Delete a user

Remove an existing user.

Returns 400 if the user has assigned incidents unless your [pricing plan](https://www.pagerduty.com/pricing) has the `offboarding` feature and the account is [configured](https://support.pagerduty.com/docs/offboarding#section-additional-configurations) appropriately.

Note that the incidents reassignment process is asynchronous and has no guarantee to complete before the api call return.

[*Learn more about `offboarding` feature*](https://support.pagerduty.com/docs/offboarding).

Users are members of a PagerDuty account that have the ability to interact with Incidents and other data on the account.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#users)

Scoped OAuth requires: `users.write`



### PUT /users/{id}
Update a user

Update an existing user.

Users are members of a PagerDuty account that have the ability to interact with Incidents and other data on the account.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#users)

Scoped OAuth requires: `users.write`



### GET /users/{id}/audit/records
List audit records for a user

The response will include audit records with changes that are made to the identified user not changes made by the identified user.


The returned records are sorted by the `execution_time` from newest to oldest.

See [`Cursor-based pagination`](https://developer.pagerduty.com/docs/rest-api-v2/pagination/) for instructions on how to paginate through the result set.

For more information see the [Audit API Document](https://developer.pagerduty.com/docs/rest-api-v2/audit-records-api/).

Scoped OAuth requires: `audit_records.read`



### GET /users/{id}/contact_methods
List a user's contact methods

List contact methods of your PagerDuty user.

Users are members of a PagerDuty account that have the ability to interact with Incidents and other data on the account.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#users)

Scoped OAuth requires: `users:contact_methods.read`



### POST /users/{id}/contact_methods
Create a user contact method

Create a new contact method for the User.

Users are members of a PagerDuty account that have the ability to interact with Incidents and other data on the account.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#users)

Scoped OAuth requires: `users:contact_methods.write`



### GET /users/{id}/contact_methods/{contact_method_id}
Get a user's contact method

Get details about a User's contact method.

Users are members of a PagerDuty account that have the ability to interact with Incidents and other data on the account.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#users)

Scoped OAuth requires: `users:contact_methods.read`



### DELETE /users/{id}/contact_methods/{contact_method_id}
Delete a user's contact method

Remove a user's contact method.

Users are members of a PagerDuty account that have the ability to interact with Incidents and other data on the account.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#users)

Scoped OAuth requires: `users:contact_methods.write`



### PUT /users/{id}/contact_methods/{contact_method_id}
Update a user's contact method

Update a User's contact method.

Users are members of a PagerDuty account that have the ability to interact with Incidents and other data on the account.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#users)

Scoped OAuth requires: `users:contact_methods.write`



### GET /users/{id}/license
Get the License allocated to a User

Get the License allocated to a User

Scoped OAuth requires: `licenses.read`



### GET /users/{id}/notification_rules
List a user's notification rules

List notification rules of your PagerDuty user.

Users are members of a PagerDuty account that have the ability to interact with Incidents and other data on the account.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#users)

Scoped OAuth requires: `users:contact_methods.read`



### POST /users/{id}/notification_rules
Create a user notification rule

Create a new notification rule.

Users are members of a PagerDuty account that have the ability to interact with Incidents and other data on the account.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#users)

Scoped OAuth requires: `users:contact_methods.write`



### GET /users/{id}/notification_rules/{notification_rule_id}
Get a user's notification rule

Get details about a user's notification rule.

Users are members of a PagerDuty account that have the ability to interact with Incidents and other data on the account.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#users)

Scoped OAuth requires: `users:contact_methods.read`



### DELETE /users/{id}/notification_rules/{notification_rule_id}
Delete a user's notification rule

Remove a user's notification rule.

Users are members of a PagerDuty account that have the ability to interact with Incidents and other data on the account.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#users)

Scoped OAuth requires: `users:contact_methods.write`



### PUT /users/{id}/notification_rules/{notification_rule_id}
Update a user's notification rule

Update a user's notification rule.

Users are members of a PagerDuty account that have the ability to interact with Incidents and other data on the account.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#users)

Scoped OAuth requires: `users:contact_methods.write`



### GET /users/{id}/notification_subscriptions
List Notification Subscriptions

Retrieve a list of Notification Subscriptions the given User has.

<!-- theme: warning -->
> Users must be added through `POST /users/{id}/notification_subscriptions` to be returned from this endpoint.

Scoped OAuth requires: `subscribers.read`



### POST /users/{id}/notification_subscriptions
Create Notification Subcriptions

Create new Notification Subscriptions for the given User.

Scoped OAuth requires: `subscribers.write`



### POST /users/{id}/notification_subscriptions/unsubscribe
Remove Notification Subscriptions

Unsubscribe the given User from Notifications on the matching Subscribable entities.

Scoped OAuth requires: `subscribers.write`



### GET /users/{id}/oncall_handoff_notification_rules
List a User's Handoff Notification Rules

List Handoff Notification Rules of your PagerDuty User.
Users are members of a PagerDuty account that have the ability to interact with Incidents and other data on the account.
For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#users)

Scoped OAuth requires: `users.read`



### POST /users/{id}/oncall_handoff_notification_rules
Create a User Handoff Notification Rule

Create a new Handoff Notification Rule.
Users are members of a PagerDuty account that have the ability to interact with Incidents and other data on the account.
For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#users)

Scoped OAuth requires: `users.write`



### GET /users/{id}/oncall_handoff_notification_rules/{oncall_handoff_notification_rule_id}
Get a user's handoff notification rule

Get details about a User's Handoff Notification Rule.
Users are members of a PagerDuty account that have the ability to interact with Incidents and other data on the account.
For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#users)

Scoped OAuth requires: `users.read`



### DELETE /users/{id}/oncall_handoff_notification_rules/{oncall_handoff_notification_rule_id}
Delete a User's Handoff Notification rule

Remove a User's Handoff Notification Rule.
Users are members of a PagerDuty account that have the ability to interact with Incidents and other data on the account.
For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#users)

Scoped OAuth requires: `users.write`



### PUT /users/{id}/oncall_handoff_notification_rules/{oncall_handoff_notification_rule_id}
Update a User's Handoff Notification Rule

Update a User's Handoff Notification Rule.
Users are members of a PagerDuty account that have the ability to interact with Incidents and other data on the account.
For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#users)

Scoped OAuth requires: `users.write`



### GET /users/{id}/sessions
List a user's active sessions

List active sessions of a PagerDuty user.

Beginning November 2021, active sessions no longer includes newly issued OAuth tokens.

Users are members of a PagerDuty account that have the ability to interact with Incidents and other data on the account.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#users)

Scoped OAuth requires: `users:sessions.read`



### DELETE /users/{id}/sessions
Delete all user sessions

Delete all user sessions.

Beginning November 2021, user sessions no longer includes newly issued OAuth tokens.

If you are interested in deleting mobile app sessions, refer to the Delete OAuth Delegations endpoint.

Users are members of a PagerDuty account that have the ability to interact with Incidents and other data on the account.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#users)

Scoped OAuth requires: `users:sessions.write`



### GET /users/{id}/sessions/{type}/{session_id}
Get a user's session

Get details about a user's session.

Beginning November 2021, user sessions no longer includes newly issued OAuth tokens.

Users are members of a PagerDuty account that have the ability to interact with Incidents and other data on the account.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#users)

Scoped OAuth requires: `users:sessions.read`



### DELETE /users/{id}/sessions/{type}/{session_id}
Delete a user's session

Delete a user's session.

Beginning November 2021, user sessions no longer includes newly issued OAuth tokens.

Users are members of a PagerDuty account that have the ability to interact with Incidents and other data on the account.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#users)

Scoped OAuth requires: `users:sessions.write`



### GET /users/{id}/status_update_notification_rules
List a user's status update notification rules

List status update notification rules of your PagerDuty user.

Users are members of a PagerDuty account that have the ability to interact with Incidents and other data on the account.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#users)

Scoped OAuth requires: `users.read`



### POST /users/{id}/status_update_notification_rules
Create a user status update notification rule

Create a new status update notification rule.

Users are members of a PagerDuty account that have the ability to interact with Incidents and other data on the account.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#users)

Scoped OAuth requires: `users.write`



### GET /users/{id}/status_update_notification_rules/{status_update_notification_rule_id}
Get a user's status update notification rule

Get details about a user's status update notification rule.

Users are members of a PagerDuty account that have the ability to interact with Incidents and other data on the account.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#users)

Scoped OAuth requires: `users.read`



### DELETE /users/{id}/status_update_notification_rules/{status_update_notification_rule_id}
Delete a user's status update notification rule

Remove a user's status update notification rule.

Users are members of a PagerDuty account that have the ability to interact with Incidents and other data on the account.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#users)

Scoped OAuth requires: `users.write`



### PUT /users/{id}/status_update_notification_rules/{status_update_notification_rule_id}
Update a user's status update notification rule

Update a user's status update notification rule.

Users are members of a PagerDuty account that have the ability to interact with Incidents and other data on the account.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#users)

Scoped OAuth requires: `users.write`



### GET /users/me
Get the current user

Get details about the current user.

This endpoint can only be used with a [user-level API key](https://support.pagerduty.com/docs/using-the-api#section-generating-a-personal-rest-api-key) or a key generated through an OAuth flow. This will not work if the request is made with an account-level access token.

Users are members of a PagerDuty account that have the ability to interact with Incidents and other data on the account.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#users)



### GET /vendors
List vendors

List all vendors.

A PagerDuty Vendor represents a specific type of integration. AWS Cloudwatch, Splunk, Datadog are all examples of vendors

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#vendors)

Scoped OAuth requires: `vendors.read`



### GET /vendors/{id}
Get a vendor

Get details about one specific vendor.

A PagerDuty Vendor represents a specific type of integration. AWS Cloudwatch, Splunk, Datadog are all examples of vendors

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#vendors)

Scoped OAuth requires: `vendors.read`



### GET /webhook_subscriptions
List webhook subscriptions

List existing webhook subscriptions.

The `filter_type` and `filter_id` query parameters may be used to only show subscriptions
for a particular _service_ or _team_.

For more information on webhook subscriptions and how they are used to configure v3 webhooks
see the [Webhooks v3 Developer Documentation](https://developer.pagerduty.com/docs/webhooks/v3-overview/).

Scoped OAuth requires: `webhook_subscriptions.read`



### POST /webhook_subscriptions
Create a webhook subscription

Creates a new webhook subscription.

For more information on webhook subscriptions and how they are used to configure v3 webhooks
see the [Webhooks v3 Developer Documentation](https://developer.pagerduty.com/docs/webhooks/v3-overview/).

Scoped OAuth requires: `webhook_subscriptions.write`



### GET /webhook_subscriptions/{id}
Get a webhook subscription

Gets details about an existing webhook subscription.

Scoped OAuth requires: `webhook_subscriptions.read`



### PUT /webhook_subscriptions/{id}
Update a webhook subscription

Updates an existing webhook subscription.

Only the fields being updated need to be included on the request.  This operation does not
support updating the `delivery_method` of the webhook subscription.

Scoped OAuth requires: `webhook_subscriptions.write`



### DELETE /webhook_subscriptions/{id}
Delete a webhook subscription

Deletes a webhook subscription.

Scoped OAuth requires: `webhook_subscriptions.write`



### POST /webhook_subscriptions/{id}/enable
Enable a webhook subscription

Enable a webhook subscription that is temporarily disabled. (This API does not require a request body.)

Webhook subscriptions can become temporarily disabled when the subscription's delivery method is repeatedly rejected by the server.

Scoped OAuth requires: `webhook_subscriptions.write`



### POST /webhook_subscriptions/{id}/ping
Test a webhook subscription

Test a webhook subscription.

Fires a test event against the webhook subscription.  If properly configured,
this will deliver the `pagey.ping` webhook event to the destination.

Scoped OAuth requires: `webhook_subscriptions.write`



### GET /workflows/integrations
List Workflow Integrations

List available Workflow Integrations.

Scoped OAuth requires: `workflow_integrations.read`



### GET /workflows/integrations/{id}
Get Workflow Integration

Get details about a Workflow Integration.

Scoped OAuth requires: `workflow_integrations.read`



### GET /workflows/integrations/connections
List all Workflow Integration Connections

List all Workflow Integration Connections.

Scoped OAuth requires: `workflow_integrations:connections.read`



### GET /workflows/integrations/{integration_id}/connections
List Workflow Integration Connections

List all Workflow Integration Connections for a specific Workflow Integration.

Scoped OAuth requires: `workflow_integrations:connections.read`



### POST /workflows/integrations/{integration_id}/connections
Create Workflow Integration Connection

Create a new Workflow Integration Connection.

Scoped OAuth requires: `workflow_integrations:connections.write`



### GET /workflows/integrations/{integration_id}/connections/{id}
Get Workflow Integration Connection

Get details about a Workflow Integration Connection.

Scoped OAuth requires: `workflow_integrations:connections.read`



### DELETE /workflows/integrations/{integration_id}/connections/{id}
Delete Workflow Integration Connection

Delete a Workflow Integration Connection.

Scoped OAuth requires: `workflow_integrations:connections.write`


