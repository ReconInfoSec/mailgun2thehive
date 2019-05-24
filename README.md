# mailgun2thehive

Create alerts in [The Hive](https://github.com/TheHive-Project/TheHive) from emails sent to your Mailgun account, to be turned into Hive cases.

Simple Python flask app that runs as a web server, and accepts POST requests from your Mailgun routes.

```
git clone https://github.com/ReconInfoSec/mailgun2thehive.git /opt/mailgun2thehive
```

Get up and running:
* Configure SSL certificate paths in `app.py`, or remove all context lines if not using SSL
* Copy `init.d/mailgun2thehive.service` to `/etc/systemd/system/mailgun2thehive.service`
* Set your Hive API key in `/etc/systemd/system/mailgun2thehive.service` for the `HIVE_SECRET_KEY`
* Set your Hive URL in `config.py`

```
pip install -r requirements.txt
cp init.d/mailgun2thehive.service /etc/systemd/system/mailgun2thehive.service
systemctl enable mailgun2thehive
systemctl start mailgun2thehive
```

* Runs at https://0.0.0.0:5000, accepts POST requests at `/create_alert`
* Point your Mailgun route to forward to `https://[YOURSERVER]:5000/create_alert`
