from prometheus_client import Counter, Histogram


REQUEST_COUTNER = Counter(
    "pokebase_requests_total",
    "Total number of requests to the pokebase API",
    ["method", "path", "status"]
)

REQUEST_HISTOGRAM = Histogram(
    "pokebase_request_duration_seconds",
    "Duration of requests to the pokebase API",
)
