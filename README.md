# Piccolo Daimao

An exploration of web app designs used to implement a high-throughput 'incrementor'.  The web app should accept a high number of concurrent POST requests containing key-value pairs.  The values are all integers, and the challenge is to sum those values continuously (and correctly) into a sqlite database without catching fire, and without introducing too much latency between the actual state(s) in the web apps and the state in the database.

I've tried a few different ideas here, at present NodeJS, Phoenix, and Python.  Though I was really impressed with the raw out-of-the box performance of Phoenix, and the simplicity of NodeJS, I've opted to fully implement the Python solution since I could implement and test it faster than the others.  The same general pattern can be applied to the other languages without much effort.

# TL;DR - How do I run this thing?

## Vagrant

If you have Vagrant, you can run `vagrant up` from the root of this repository - it will spin up an Ubuntu 16 VM with a public IP for smashing with load tests.  Feel free to tweak the settings as well (like adding memory).  Please note that it will prompt you to select a network adapter on the host to bind to - the rule of thumb is "pick the one you get your internetz from".

## Manual Install (Ubuntu)

First, copy/clone the repository code to the server in the location `/usr/local/piccolo-daimao`.

Run the following commands:
```
cd /usr/local/piccolo-daimao
sudo bash install_ubuntu.sh
sudo bash install_main.sh
```

This has been tested on Ubuntu 16 and *should* work on 14, but I haven't tested it explicitly.

## Manual Install (Other Linux Flavors)

In order to install on other flavors of Linux, you'll need to work a little bit harder (but not too hard!).  The main thing is you'll need to make sure a few core packages are installed using the package manager of your choice, or for you masochists - build everything from source =)

First, copy/clone the repository code to the server in the location `/usr/local/piccolo-daimao`.

Next, make a copy of `install_ubuntu.sh` and call it something like `install_linux.sh`.  Edit that file to make sure you've accounted for all of the noted dependencies.

Run the following commands from the repository root:
```
sudo bash install_linux.sh
sudo bash install_main.sh
```

## Running the main app

All that remains after installation is to start up two python processes on the host that will be tested.
For the web app:
```
cd /usr/local/piccolo-daimao/apps/python-falcon
python app/incrementor.py pywsgi
```

For the redis consumer:
```
cd /usr/local/piccolo-daimao/apps/python-falcon
python app/consumer.py /var/local/piccolo-daimao/sqlite/numbers.db
```

Then take aim and fire with a load testing tool!  There's some rudimentary console logging available to let you know things are working.  To check results, the database is located by default at `/var/local/piccolo-daimao/sqlite/numbers.db`.  There are a few useful helpers that Vegeta can use as well - see "Load testing with Vegeta" below.

# Design Choices

This problem is fairly trivial to solve *correctly*, however making the solution scale is not so trivial.  I think I've come up with something that works decently for a production web app.  Making it scale ridiculously (e.g. [LMAX](https://martinfowler.com/articles/lmax.html)) is a bit beyond the scope of this project.  

## Picking an appropriate framework

The first order of business is to find a web framework that is known to handle concurrent load really well.  The first thing that popped into my head was NodeJS, so I picked that as a good reference point.  The second thing that popped into my head was Phoenix, since I've read that it's really well suited for this kind of problem - I just don't happen to know much about it.  The third was the Python micro-framework called Falcon, given that I know that stack more than the other two.

I first built trivial "hello world" endpoints using Node, Phoenix, and Falcon and punished them with "attacks" from the [Vegeta](https://github.com/tsenart/vegeta) framework.  Based on this, it looked like something on the order of thousands of requests/second was feasible.  Not surprisingly, Elixir/Phoenix right out of the box was some 3-4X faster than Node/Express.  Falcon was faster or slower depending on what kind of WSGI server was being used.  The best-performing ones I tried (Bjoern and gevents.pywsgi) were faster than Node, though not by an order of magnitude.

Given this information, I decided to choose a Python implementation as a reference since I would be able to build and test it fastest, and the performance would be competitive.  Once built, it would be easy to port to other languages in the future.

## Reducing the "Gear Ratio"

Once we are able to accept large numbers of connections, the next step is to design an algorithm that could quickly aggregate all those requests and slow things down enough so that sqlite is not overwhelmed.  The observation that makes this work is that we do not need to know the current value of a given key at the rate requests come in - we can queue them, reduce them, and sum them without changing the final answer.  In other words, key 'foo'=10 after a sequence of updates 10+1+1+1+1+1+1+1+1 is the same as 10+8.  That's primarily what drives the "gear ratio slowdown" effect - after a configurable time interval, all observed increments from new requests are set aside, summed, and the sums are pushed to redis lists, and then summed again by a second single-threaded process (more on this in the next section).

## Designing for scale-out

The choice to introduce Redis into the equation might seem a bit gratuitous.  Based on cursory testing, it seems feasible that a single web process with the "gear ratio" algorithm in place could slow things down enough to keep sqlite from running hot.  But there were two things that concerned me about this - 1) sqlite is writing to disk and essentially doing a fair amount of work relative to one of the super-lightweight web requests, and even with an event loop, I suspect this would reduce the throughput unacceptably.  2) If we added more servers or web processes, we would potentially have to deal with concurrent writes in sqlite and that doesn't sound fun.  I would much rather deal with that elsewhere and redis seems like a perfect intermediary.  We could push values atomically and very quickly to redis without requiring synchronization constructs, and then a separate single-threaded process (the Consumer) can pop values and write to sqlite without database contention.  If we really wanted to get fancy and add lots of web workers, we could ensure that redis doesn't fill up by adding more Consumers, and partition/shard the keyspace that each Consumer looks at.

# Dependencies

As mentioned in the setup scripts, this project depends on the following, some of which are installed on the system and some are installed by framework-specific package managers:
* Python 2.7 (installed by default on many distros)
* NTP util - allows clock syncing when vagrant VMs drift off (a common problem, and totally optional)
* Erlang VM and Elixir
* Python 2.7's pip package manager
* NPM - Node package manager - allows us to bootstrap a NodeJS environment
* Redis
* SQLite

# Load testing with Vegeta

Vegeta is not really necessary for testing but it *is* really useful. Installing it and running the following command from the repository's `vegeta` directory on a separate host will perform a simple load test, useful for checking the math.  It's recommended that you empty the database and restart the python processes before testing.:
```
cd vegeta
echo "POST http://<yourserver>:3333/increment" | vegeta attack -rate 1100 -output out.bin -header "Content-Type: application/x-www-form-urlencoded" -body "./testbody"
```

You can also run the insane mode profile, which really piles on the hurt:
```
python create_targets.py 9000 <yourserver> && vegeta attack -rate 9000 -output out.bin -header "Content-Type: application/x-www-form-urlencoded" -targets random_targets.txt 
```

After a test, you can run the following to see a simple report:
```
vegeta report -inputs out.bin -reporter text
```

See the Vegeta docs for more details on testing options and reporting output.

# Extra stuff

You *can* run the Phoenix and Node projects and fire requests at them - they just don't do any actual work and exist merely to see roughly how fast each framework *could* be.

To run the Node project:
```
cd /usr/local/piccolo-daimao/apps/node-express
nodemon
```

To run the Phoenix project:
```
cd /usr/local/piccolo-daimao/apps/elixir-phoenix
MIX_ENV=prod mix compile.protocols
MIX_ENV=prod PORT=3333 elixir -pa _build/prod/consolidated -S mix phoenix.server
```

# Future work

* I really would like to finish up the Node/Express and Elixir/Phoenix implementations now that I know the basic pattern works
* Some unit tests would be nice.  I did most of my testing using Vegeta because load was so important to proper functioning of the app.  Also the app code itself was extremely simple, so simple in fact that Vegeta covered most of the code.
* I really really wish I could have found a way to make the Bjoern WSGI server solve this problem because it's so blazing fast, comparable to Phoenix.  Its event loop is opaque to the application, though, which means if traffic stops suddenly, we could end up where some state is not flushed to the database in a guaranteed amount of time.
* This is a really good test project for trying out various logging/monitoring tools.  I personally like to be able to peeer into the innards of my applications and see what's going on - especially in production


 
