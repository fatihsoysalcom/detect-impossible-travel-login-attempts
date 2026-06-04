# Detect Impossible Travel Login Attempts

This example demonstrates "impossible travel detection" in login flows. It simulates user logins from different geographic locations and timestamps. The script calculates the distance and time between consecutive logins for a user, then determines if the implied travel speed exceeds a plausible maximum (e.g., airplane speed). If the speed is too high, it flags an "impossible travel" event, indicating potential fraudulent activity.

## Language

`python`

## How to Run

Save the code as `main.py`.
Run from your terminal: `python main.py`

## Original Article

This example accompanies the Turkish article: [Olası Sahtekarlık Tespiti: Giriş Akışlarınızı Güvenli Hale Getirin](https://fatihsoysal.com/blog/olasi-sahtekarlik-tespiti-giris-akislarinizi-guvenli-hale-getirin/).

## License

MIT — see [LICENSE](LICENSE).
