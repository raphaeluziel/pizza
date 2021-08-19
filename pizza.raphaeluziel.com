server {
    listen 80;
    listen [::]:80;

    server_name pizza.raphaeluziel.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/raphaeluziel/pizza;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/pizza.sock;
    }
}
