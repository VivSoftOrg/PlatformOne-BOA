
dev : Read the LB Name, Create route53 record with ${env}-app.batcave-dev.internal.cms.gov.
test: read the LB name, update route53 record with ${app}.batcave-test.internal.cms.gov
prod: read the LB name and update route53 record with ${app}.batcave.internal.cms.gov
