from fabric.contrib.files import exists
from fabric.api import run, env, local
import re as regex


env.disable_known_hosts = True

env.roledefs.update({
    'nodes': ['nathantrujillo@rooter.local', 'renderhack@renderhack.local', 'raptor@raptor.local', 'raptor@reaktor.local'],
})

authorized_keys = '~/.ssh/authorized_keys' 
myhostname = local("uname -a | awk '{print $2}'", capture=True)
whichbrew = local("which brew", capture=True)

print myhostname




def add_keys():

	print("Executing on %(host)s as %(user)s" % env)
	run_commands("sw_vers && df -h")
	if(not exists('~/.ssh')):
		run('mkdir ~/.ssh')
		run('chmod 700 ~/.ssh && chmod 600 ~/.ssh/*')
	run('touch ' + authorized_keys)
	if(not exists(authorized_keys)):
		local("cat ~/.ssh/id_rsa.pub | ssh %(user)s@%(host)s 'cat - >> ~/.ssh/authorized_keys'" % env)
	else:
		run('cat ' + authorized_keys + ' | grep %(host)s' % env)

	run_commands('chmod 600 ~/.ssh/authorized_keys && chmod 700 ~/.ssh/')


def test_ssh():
	print("I AM:", myhostname, authorized_keys)
	if(myhostname !=  '%(host)s' % env ):
		result = run('cat ' + authorized_keys + ' | grep ' + myhostname, warn_only=True)
		print result


def runner(*args):
	if(myhostname !=  '%(host)s' % env ):
		run(args)
	else:
		local(args)


def run_commands(str):
	commands = regex.split("\s+\&\&\s+", str)
	for command in commands:
		run(command)


def install_brew():
	if(runner('which brew', warn_only=True) != whichbrew):
		runner('ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"', warn_only=True)