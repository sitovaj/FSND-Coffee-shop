/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'dev-p8l4wm2k.eu', // the auth0 domain prefix
    audience: 'CoffeeShopAPI', // the audience set for the auth0 app
    clientId: 'zSAHkIAIxtRz61wmpccbaKNSuY9CAj5L', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:8100/login-results', // the base url of the running ionic application. 
  }
};
