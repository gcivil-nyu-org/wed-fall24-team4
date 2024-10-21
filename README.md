[![Build Status](https://app.travis-ci.com/gcivil-nyu-org/wed-fall24-team4.svg?token=jwUNqiGUzS6Hs3vuhjTX&branch=develop)](https://app.travis-ci.com/github/gcivil-nyu-org/wed-fall24-team4)
[![Coverage Status](https://coveralls.io/repos/github/gcivil-nyu-org/wed-fall24-team4/badge.svg?branch=develop)](https://coveralls.io/github/gcivil-nyu-org/wed-fall24-team4?branch=develop)

### Usage

1. **Set up your local environment:**
   - Create a `.env` file in the root directory of your project.
   - Add your Google Maps API key to the `.env` file:
     ```bash
     GOOGLE_MAPS_API_KEY=<your-google-maps-api-key>
     ```

2. **Enable Required APIs in Google Cloud Console:**
   - Go to the [Google Cloud Console](https://console.cloud.google.com/).
   - Enable the **Geolocation API** and **Geocoding API** for your project.

3. **Enable Billing:**
   - Ensure billing is enabled in your Google Cloud project. Certain Google Maps services, like the Geocoding API, require billing to be activated to avoid errors like `REQUEST_DENIED`.

4. **Run the following commands:**
   ```bash
   python manage.py migrate
   python manage.py makemigrations app
   ```
    Then:
    ```bash
    python manage.py runserver 
    ```

Link to website: [http://stepfreemta-env.eba-je3qmwfd.us-west-2.elasticbeanstalk.com/]
