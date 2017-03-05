defmodule Web.Router do
  use Web.Web, :router

  pipeline :api do
    plug :accepts, ["json"]
  end

  scope "/increment", Web do
    pipe_through :api
    post "/", IncrementController, :increment
  end
end
