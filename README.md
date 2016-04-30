# gcloud-letsencrypt-flask
## Aim and assumptions
This quick HOWTO is aimed at gcloud users who are just playing around/getting into the Google App Engine. I'm assuming you completed the tutorial which left you with an initial small flask app that's currently deployed and you now want to secure your connection via custom domain with a [free letsencrypt certificate](https://letsencrypt.org/). The custom domain is already added and serving via an unsecured connection.

You've set up gcloud on your local machine and cloned the repo with the example flask app.

## Acknowledgements
This howto is based almost entirely on Sean Fujiwara's [blog post](http://blog.seafuj.com/lets-encrypt-on-google-app-engine) from November 2015, when, I assume, the Google App Engine did not yet use flask.

## Actual HOWTO
### Step 1
Set up letsencrypt on your local system, either by cloning the repo and using letsencrypt-auto (`git clone https://github.com/letsencrypt/letsencrypt`) or by installing via your distribution's package manager. With Archlinux use `pacman -S letsencrypt`. The advantage of setting up letsencrypt locally is that the /etc/letsencrypt directory will be persistent, allowing for easier updating.

### Step 2
Download the letsencrypt.py from this repo (clone and cp, copy&paste, whatever floats your goat) and add it to your app's main directory.

Add a new handler **above** the `.*` handler in your app.yaml:
```
- url: /\.well-known/acme-challenge/.*
  script: letsencrypt.app
  secure: never
```
If you've changed nothing else yet, you can probably also just download the app.yaml from this repo and overwrite yours.

### Step 3
Generate the challenge-response credentials via letsencrypt.

If you've cloned the repo, you'll have to
```
cd letsencrypt
sudo ./letsencrypt-auto -a manual certonly
```
and let it install some stuff, if you've used your distribution's package manager, you should be able to do
```
sudo letsencrypt -a manual certonly
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
Copy the various challenges and responses into the credentials dict in letsencrypt.py. Don't press enter when you've reached the final CN entry you want in your certificate.

### Step 5
Deploy the app. If you're working locally and have set up gcloud, use
```
gcloud preview app deploy
```
in the app directory. If everything's deployed alright, you can now press enter in the terminal where letsencrypt is running. If you want, you can check the URL in the letsencrypt output above and look if it serves and matches the expected response.

### Step 6
The letsencrypt script should now tell you congratulations and inform you where your certificate is (/etc/letsencrypt/live/). Follow the instructions in Sean Fujiwara's [blog post](http://blog.seafuj.com/lets-encrypt-on-google-app-engine) of how to convert and upload your key and certificate to app engine.

### Step 7
Call up your custom domain with https in front (if you used my app.yaml, the app should serve securely by default) and see if everything's running smoothly.

## Updating your certificates
I'll add to this section once I update mine. Should work exactly like getting your certificates in the first place.
