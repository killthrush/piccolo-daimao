defmodule Web.IncrementController do
  use Web.Web, :controller

  def increment(connection, _params) do
    text connection, "a!"
  end
end