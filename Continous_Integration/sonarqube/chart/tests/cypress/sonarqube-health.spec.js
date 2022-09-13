// needs to be fixed
describe('Basic Sonarqube', function() {
  it('Check Sonarqube is accessible', function() {
    cy.visit(Cypress.env('url'))
    
    cy.wait(2000)
    cy.get("body").then($body => {
      if ($body.find('h1[class="maintenance-title"]').length > 0) {
        cy.visit(Cypress.env('url_setup'))
        cy.get('button[id="start-migration"]').click()
        cy.wait(2000)
        cy.title().should('include', 'SonarQube Is Starting')
      } 
    })

    cy.get('input[name="login"]').type(Cypress.env('user'))
    cy.get('input[name="password"]').type(Cypress.env('password'))
    cy.contains("Log in").click()

    cy.wait(2000)
    cy.get("body").then($body => {
      if ($body.find('div[class="plugin-risk-consent-content boxed-group"]').length > 0) {
        cy.contains("I understand the risk").click()
      }
    })
    cy.wait(2000)
    cy.scrollTo('topRight')
    cy.get('a[class="dropdown-toggle navbar-avatar"]').click()
    cy.contains("My Account").click()
    cy.contains("Security").click()
    cy.get('input[class="input-large spacer-right"]').type(Math.random().toString(36).substring(8))
    cy.get('button[class="button js-generate-token"]').click()
  })
})
