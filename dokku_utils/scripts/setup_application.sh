dokku apps:create %(app_name_dokku)s;

dokkutils hosts.%(environment)s env.update_envs;

git remote add dokku_%(environment)s dokku@%(host)s:%(app_name_dokku)s;

