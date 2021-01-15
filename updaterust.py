from subprocess import run
try:
    run(["/usr/games/steamcmd"," +login anonymous +force_install_dir . +app_update 258550  validate +quit"])
except Exception as err:
    print("Error while updating steam: %s" % err)

