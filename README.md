# Porkbun Dynamic DNS

1. `git clone https://github.com/borroot/porkbun-ddns`
2. `sudo apt install python3 python3-pip`
3. `pip install requests`
4. Create `config.json` from `config.json.example`, also see [Porkbun DDNS.](https://kb.porkbun.com/article/190-getting-started-with-the-porkbun-dns-api)
5. `sudo touch /etc/cron.d/porkbun`
6. Add the following line to `/etc/cron.d/porkbun`: `*/5 * * * * pi bash -c 'python3 /path/to/porkbun-ddns.py /path/to/config.json example.com www'`
