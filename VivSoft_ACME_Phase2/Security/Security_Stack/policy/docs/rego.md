# Rego

[Rego](https://www.openpolicyagent.org/docs/latest/policy-language/) is Open Policy Agent's native query language that inspects the data published by services and users. Its creation was influenced by [Datalog](https://en.wikipedia.org/wiki/Datalog), a declarative logic programming query language used for deductive databases. Rego goes well beyond Datalog to support structured document models. Its queries help define policies identify data violations. Rego can be a steep learning curve for users.

Some benefits of Rego are:

- Simplistic reading and writing of policies.
- Powerful support of referenced nested documents.
- Queries that accurate and unambiguous.
- Declarative

## Best Practices

Best practices tips for [Rego](https://www.openpolicyagent.org/docs/latest/policy-language/) are:

- Rules are evaluated as logical AND statements.
- The order of rule statements does not matter.
- "true" and defined are usually synonymous. "false" is also usually synonymous with undefined.
- Rule evaluation short-circuits on reaching a statement that evaluates to undefined.

For additional information click [here](https://www.kubermatic.com/blog/opa-rego-in-a-nutshell/).
