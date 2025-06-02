from prometheus_client import Counter, Histogram


REQUEST_COUTNER = Counter(
    "pokebase_requests_total",
    "Total number of requests to the pokebase API",
    ["method", "path", "status"]
)

# A Histogram in Prometheus is used to track the distribution of values, particularly useful for measuring things like request durations, response sizes, or any other continuous values. It automatically creates buckets to count observations that fall into different ranges, allowing you to analyze the distribution of your data.
REQUEST_HISTOGRAM = Histogram(
    "pokebase_request_duration_seconds",
    "Duration of requests to the pokebase API",
)
