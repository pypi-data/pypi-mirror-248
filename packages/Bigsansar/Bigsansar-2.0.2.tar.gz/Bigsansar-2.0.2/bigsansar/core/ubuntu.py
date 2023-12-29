import os
import shutil

def deploy():

    cmd1 = "sudo apt update  && sudo apt upgrade -y"
    os.system(cmd1)


    if os.path.isdir('www') == True:
        print('we are installing some ubuntu package for configurations....')
        cmd2 = "sudo apt install openssh-server ufw apache2 libapache2-mod-wsgi-py3 postgresql postgresql-contrib libpq-dev -y"
        os.system(cmd2)

        print(' RE-Configuring internal setiings now.................................................................')

        # Specify the path of the file you want to copy
        file_to_copy = '/usr/local/lib/*/dist-packages/bigsansar/etc/serve-cgi-bin.conf'

        # Specify the path of the destination directory you want to copy to
        destination_directory = '/etc/apache2/conf-available/'

        # Use the shutil.copy() method to copy the file to the destination directory
        shutil.copy(file_to_copy, destination_directory)

        print('secure on firewall...................................................')
        ufw = "sudo ufw allow ssh && sudo ufw allow openssh"

        print('restarting all service ...........................................')
        restart = "sudo service ssh restart"
        os.system(restart)

        print('checking the service status........................................................ ')

        check = "sudo service ssh status"
        os.system(check)



    else:
        print("you have no any configurations file and folder . use 'bigsansar init' command line for internal configurations. then , type 'sudo bigsansar setup_server' again . ")
