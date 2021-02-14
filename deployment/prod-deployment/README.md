# prod-deployment
![Prod Deployment](https://github.com/XAI-Demonstrator/xai-demonstrator/workflows/Prod%20Deployment/badge.svg)
![Monitor Deployment(s)](https://github.com/XAI-Demonstrator/template-service/workflows/Monitor%20Deployment(s)/badge.svg)

_This is the deployment currently at [xai-demonstrator-test.web.app](http://xai-demonstrator-test.web.app/) 
that will soon move to its final home at [https://www.xaidemo.de](https://www.xaidemo.de)._

Production deployment of the XAI demonstrator on [Google Cloud Platform](https://cloud.google.com).
The frontend is served through [Firebase Hosting](https://firebase.google.com/docs/hosting/)
with the backends deployed on [Google Cloud Run](https://cloud.google.com/run/).

## Set Up
To set up the XAI demonstrator on the Google Cloud Platform follow these steps:
1. [Create a GCP project](https://cloud.google.com/resource-manager/docs/creating-managing-projects?hl=en) and [enable billing](https://cloud.google.com/billing/docs/how-to/modify-project?hl=en).
2. [Activate Google's Cloud SDK](https://cloud.google.com/sdk/docs/authorizing?hl=en).
3. [Create a service account](https://cloud.google.com/iam/docs/creating-managing-service-accounts?hl=en) for the GitHub workflows and assign the following roles to it: Service Account User, Cloud Run Admin and Cloud Storage Admin.
4. [Create a key](https://cloud.google.com/iam/docs/creating-managing-service-account-keys?hl=en) for your workflow service account.
5. Create the following [GitHub secrets](https://docs.github.com/en/actions/reference/encrypted-secrets): 
     - GCP_PROD_EMAIL - the email adress of your workflow service account
     - GCP_PROD_PROJECT_ID - your project ID
     - GCP_PROD_REGION - the region you want your project to be hosted in
     - GCP_PROD_SA_KEY - the key your created in step 4
6. Activate [Firebase Hosting](https://console.cloud.google.com/marketplace/details/google-cloud-platform/firebase-hosting) for your GCP project (without Google Analytics)
7. To generate the Firebase token, install the [Firebase CLI](https://firebase.google.com/docs/cli) and log in using your Google account associated with your GCP project with `firebase login:ci`. Store the token as `GCP_PROD_FIREBASE_TOKEN`.
8. Set the project name in [.firebaserc](./frontends/.firebaserc) to the name of your GCP/Firebase project.

Be careful to insert the exact identifiers when creating the GitHub secrets. Common problems are extra spaces, inserting the computing zone (e.g. us-west1-a) instead of the region (us-west1) and copying only parts of the key json.

Now the XAI demonstrator is ready to be deployed to your GCP project by the [Prod Deployment workflow](../../.github/workflows/prod-deployment.yml)!

