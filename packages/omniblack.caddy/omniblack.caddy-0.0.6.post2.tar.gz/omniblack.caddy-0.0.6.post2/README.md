# Omniblack Caddy

Omniblack Caddy offer a pythonic interface
to control a [Caddy](https://caddyserver.com/) server
using caddy's [JSON API](https://caddyserver.com/docs/api).

## Basic Example

```python3
from omniblack.caddy import Caddy

# omniblack.caddy will use the caddy file to find the
# Admin api's address
with Caddy(caddy_file='./caddyfile.json') as caddy:
    caddy.get('/reverse_proxy/upstreams')
```
