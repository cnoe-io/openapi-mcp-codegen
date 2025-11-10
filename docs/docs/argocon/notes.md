# Notes

```
2025-11-09T15:48:23.319240Z     info    management::hyper_helpers       listener established    address=[::]:15021 component="readiness"
2025-11-09T15:48:23.325098Z     info    state_manager   Watching config file: argo-agentgateway.yaml
2025-11-09T15:48:23.344004Z     info    agent_core::readiness   Task 'agentgateway' complete (34.102958ms), still awaiting 1 tasks
2025-11-09T15:48:23.344010Z     info    agent_core::readiness   Task 'state manager' complete (34.112ms), marking server ready
2025-11-09T15:48:23.344022Z     info    management::hyper_helpers       listener drained        address=[::]:15021 component="readiness"
Error: binds[0].listeners[0].routes[0].backends[0]: paths: no variant of enum ParameterSchemaOrContent found in flattened data at line 1 column 158490
```