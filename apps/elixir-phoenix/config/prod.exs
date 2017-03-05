use Mix.Config

config :web, Web.Endpoint,
  http: [port: {:system, "PORT"}],
  url: [host: "localhost", port: 80]

# Do not print debug messages in production
config :logger, level: :error
