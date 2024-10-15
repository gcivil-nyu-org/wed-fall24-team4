### Usage

1. **Set up your environment:**
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
