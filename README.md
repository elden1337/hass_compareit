# Compare IT Homeline

Basic integration for the Compare It Homeline to Home Assistant, which controls outlets in your smarthome. 
See https://www.compare-it.se/ for more information on the product.

### Installation

Copy this folder to `<config_dir>/custom_components/compareit/`.

Add the following entry in your `configuration.yaml`:

```yaml
compareit:
    username: youruser@domain.com 
    password: yourAweSOMEPasswOrd!
```

As of version 0.1 Lights should work. Switches and services will come later.