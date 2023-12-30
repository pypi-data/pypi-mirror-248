import os
import shutil
from subprocess import check_output

def deploy():

    cmd1 = "sudo apt update  && sudo apt upgrade -y"
    os.system(cmd1)


    
    print('we are installing some ubuntu package for configurations....')
    cmd2 = "sudo apt install openssh-server ufw apache2 libapache2-mod-wsgi-py3 postgresql postgresql-contrib libpq-dev -y"
    os.system(cmd2)

    print(' RE-Configuring internal setiings now.................................................................')

    # Specify the path of the file you want to copy
    pyversion = check_output('ls /usr/local/lib', shell=True).decode('utf-8').strip()
    file_to_copy = '/usr/local/lib/%s/dist-packages/bigsansar/etc/serve-cgi-bin.conf' % (pyversion)

    # Specify the path of the destination directory you want to copy to
    destination_directory = '/etc/apache2/conf-available/'

    # Use the shutil.copy() method to copy the file to the destination directory
    shutil.copy(file_to_copy, destination_directory)

    # configuring sshd file 
    shutil.copy('/usr/local/lib/%s/dist-packages/bigsansar/etc/sshd_config','/etc/ssh/') % (pyversion)

    # make a chroot environment
    file = open('/etc/ssh/sshd_config', 'a')
    sudo_user = check_output('whoami', shell=True).decode('utf-8').strip()
    chroot_text = 'Match User *,!%s' % (sudo_user)
    file.write(chroot_text)
    file.close()

    print('secure on firewall...................................................')
    ufw = "sudo ufw allow OpenSSH && sudo ufw allow Apache && sudo ufw allow  'Apache Full' && sudo ufw allow 'Apache Secure'"
    os.system(ufw)

    print('restarting all service ...........................................')
    restart = "sudo service ssh restart && sudo service apache2 restart && sudo ufw enable"
    os.system(restart)

    print('checking the service status........................................................ ')

    check = "sudo service ssh status && sudo service apache2 status && sudo service ufw status"
    os.system(check)
