# [Monero](https://getmonero.org) metrics plugin for [mkdocs](https://www.mkdocs.org)
using [monerod stats exporter](https://github.com/DiosDelRayo/monerod_stats_exporter) endpoints which are [Prometheus](https://prometheus.io) [exporter endpoints](https://prometheus.io/docs/instrumenting/clientlibs/)

## Install

```sh
pip install git+https://github.com/DiosDelRayo/mkdocs_monero_metrics_plugin.git
```

or add into your requirement.txt:
```
git+https://github.com/DiosDelRayo/mkdocs_monero_metrics_plugin.git
```

## Config

Add in `mkdocs.yml` the following:
```yaml
plugins:
  - monero-metrics:
      endpoints:
        - 'http://localhost:9123/metrics'
        - 'http://localhost:9124/metrics'
      time_format: '%d-%m-%Y %H:%M:%S'
      defaults:
        monero_main_file_size: "203.24 GB"
        monero_main_file_last_update: "2024-09-09 11:51:28"
        monero_main_block_height: 3233846
        monero_main_block_timestamp: "2024-09-09 11:50:21"
```

- endpoints: You add as may endpoints as needed or preferred.
- time_format: (optional) How to convert unix timestamps
- defaults: set defaults for your used metrics, you can also abuse it to set static values, but
  they need to be prefixed with `monero_`. So you can set e.g. `monero_url: "https://getmonero.org"`
  and then use in you markdown files `{{ monero_url }}`

## What in the plugin happens:

1. On `__init__` of the plugin it will load the defaults as metrics
2. On `on_pre_build` it tries to connect to all declared endpoints and add the metrics.
   If various endpoints share the same metrics, the later will override the previous metrics.
   Various endpoints are implemented for the purpose of different metrics for {main,test,stage}
   networks and {pruned,full} blockchain, so it can be distributed, or also used as fallback in
   case an endpoint is not reachable at that moment.
3. On `on_env` the metrics get injected into the jinja2 template so that now the metrics can be
   used like `{{ monero_main_file_size }}` which represents the size of the blockchain of mainnet
   without prunning. For pruned size use `{{ monero_main_pruned_file_size }}`, and for testnet use
   `{{ monero_test_file_size }}` or pruned `{{ monero_test_pruned_file_size }}`. Of course you need
   first to collect the mtrics from some endpoints.

## Where to find metrics

If not somebody else will provide the metrics I will soon provide metrics for:

- main full
- main pruned
- test full
- test pruned
- stage full
- stage pruned

Maybe later in time for stressnet, but for now it is too stressful for me :D
If you want to provide metrics, let me know and I will add it here.

## License

I don't give a crap as long no criminal organization a.k.a. governmental organization or employee uses it,
only for that purpose I add the [BipCot NoGov Software](https://www.bipcot.org) [License](LICENSE.txt). So
if you don't initiate aggression feel free to use this piece of source for whatever you want.
