import subprocess


map_to_docker_env = {
        'dbname': 'POSTGRES_DB',
        'user': 'POSTGRES_USER',
        'password': 'POSTGRES_PASS',
        }

def get_db_credentials():
    process = subprocess.Popen('heroku pg:credentials:url --app lcs-tracking'.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

    if output:
        split = output.decode().split('\n')[2]
        values = list(filter(lambda x: len(x), split))
        creds = {}
        for x in values:
            x = x.replace('"', '')
            k, v = x.split('=')
            creds[k] = v
        return output

    if error:
        print(error)
