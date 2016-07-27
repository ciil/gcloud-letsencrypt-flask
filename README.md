# gcloud-letsencrypt-flask
## Aim and assumptions
This quick HOWTO is aimed at gcloud users who are just playing around/getting into the Google App Engine. I'm assuming you completed the tutorial which left you with an initial small flask app that's currently deployed and you now want to secure your connection via custom domain with a [free letsencrypt certificate](https://letsencrypt.org/). The custom domain is already added and serving via an unsecured connection.

You've set up gcloud on your local machine and cloned the repo with the example flask app.

## Acknowledgements
This howto is based almost entirely on Sean Fujiwara's [blog post](http://blog.seafuj.com/lets-encrypt-on-google-app-engine) from November 2015, when, I assume, the Google App Engine did not yet use flask (at least not as the preferred python App Engine tutorial framework).

## Actual HOWTO
### Step 1
Set up certbot on your local system, either by getting the self-updating script from the [EFF](https://certbot.eff.org/)
```
wget https://dl.eff.org/certbot-auto
chmod a+x certbot-auto
```
or by installing certbot with your distribution's package manager. With Archlinux use `pacman -S certbot`. The advantage of setting up certbot locally is that the /etc/letsencrypt directory will be persistent, allowing for easier updating.

### Step 2
Download the letsencrypt.py from this repo (clone and cp, copy&paste, whatever floats your goat) and add it to your app's main directory.

Add a new handler **above** the `.*` handler in your app.yaml:
```
- url: /\.well-known/acme-challenge/.*
  script: letsencrypt.app
  secure: never
```
If you've changed nothing else from the Google tutorial yet, you can probably also just download the app.yaml from this repo and overwrite yours.

### Step 3
Generate the challenge-response credentials with certbot.

If you've downloaded the file, you'll have to do
```
./certbot-auto -a manual certonly
```
and let it install some stuff, if you've used your distribution's package manager, you should be able to do
```
sudo certbot -a manual certonly
```
The script will then ask for an email address and for all the domains you want to secure. Put in the domains you've previously entered via custom domains in your app's settings.

### Step 4
The script will ask you to set up the challenge-response pairs for each domain individually like so:
```
Make sure your web server displays the following content at
http://www.example.com/.well-known/acme-challenge/[challenge] before continuing:
[response]
Content-Type header MUST be set to text/plain.
...
Press ENTER to continue
```
Copy the various challenges and responses into the credentials dict in letsencrypt.py. Don't press enter yet when you've reached the final CN entry you want in your certificate! That immediately starts the auth process and you need to deploy the app first.

### Step 5
Deploy the app. If you're working locally and have set up gcloud, check if you're in the correct project, otherwise change with
```
gcloud config set project <project-name>
```
and then use
```
gcloud app deploy
```
in the app directory to deploy your app. If you want, you can check the URL in the output above and look if it serves and matches the expected response. If everything's deployed alright, you can now press enter in the terminal where certbot is running.

### Step 6
The certbot script should now tell you congratulations and inform you where your certificate is (it should be `/etc/letsencrypt/live/`). Follow the instructions in Sean Fujiwara's [blog post](http://blog.seafuj.com/lets-encrypt-on-google-app-engine) and convert your private key with
```
sudo openssl rsa -inform pem -in /etc/letsencrypt/live/www.example.com/privkey.pem -outform pem | less
```
Then get your public certificate with
```
sudo less /etc/letsencrypt/live/www.example.com/fullchain.pem
```
and upload your key and certificate to app engine (App Engine -> Settings -> SSL Certificates -> Upload a new certificate).

### Step 7
Call up your custom domain with https in front (if you used my app.yaml, the app should serve securely by default - that means it will automatically forward to a secure connection no matter what) and see if everything's running smoothly.

## Updating your certificates
To update your certificates, just follow the above howto again from Step 3. Be sure to keep your system updated.
