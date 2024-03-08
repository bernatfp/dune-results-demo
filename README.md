# Dune Query Results API Demo

The Dune API now supports basic querying functionality on top of its query results endpoint.

Specifically, it supports the following actions:

- Selecting specific columns
- `WHERE` style filters on columns
- Sorting on specific columns
- Sampling results
- Pagination

This functionality makes it much easier, faster and efficient to build interactive data apps on top of the Dune API!

This repository shows how to build a simple interactive webapp with Streamlit leveraging the Dune API.

The use case we build is a finder of the largest trades in the last day for a particular token above a certain $ threshold. The app uses [this query](https://dune.com/queries/3503523) as its backend. The query is scheduled to refresh every hour, which ensures decently fresh results without needing to worry about query refresh logic at the app level.

The app is available at xxxxxPLACEHOLDERxxxxx
