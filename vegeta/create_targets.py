import sys
import random
import uuid

# Generate some random targets for Vegeta to obliterate
if len(sys.argv) > 2:
    num_targets = int(sys.argv[1])
    target_server = sys.argv[2]
    print "Generating {} random targets for server {}...".format(num_targets, target_server)

    random_content = []
    with open('./random_targets.txt', 'w') as targets_file:
      for i in range(0, num_targets):
          with open("./random{}".format(i), 'w') as body_file:
              content = "key={}&value={}".format(uuid.uuid4(), random.randint(-10000, 10000))
              body_file.write(content)
          targets_file.write("POST http://{}:3333/increment\n".format(target_server))
          targets_file.write("@./random{}\n".format(i))
          targets_file.write("\n")

    print "Done."
else:
    print "This program requires <num_targets> followed by <target_server>.  Exiting."

