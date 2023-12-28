import os


def deploy():

    cmd1 = "sudo apt update  && sudo apt upgrade -y"
    os.system(cmd1)


    if os.path.isdir('www') == True:
        print('we are installing some ubuntu package for configurations....')
        cmd2 = "sudo apt install openssh-server ufw apache2 libapache2-mod-wsgi-py3 postgresql postgresql-contrib libpq-dev -y"
        os.system(cmd2)

        print(' RE-Configuring internal setiings now.................................................................')

        with open('/etc/ssh/sshd_config', 'r') as fp:
            # read all lines in a list
            lines = fp.readlines()
            count = 0
            

            for line in lines:
                # check if string present on a current line
                if line.find('Protocol 2') != -1:
                    print('status ok .............')

                else:
                     if line.find('#Port 22') != -1:
                         
                        x = lines.index(line) + 1
                        txt = "Protocol 2" \
                            "\n"
                        lines.insert(x, txt)

            f = open('/etc/ssh/sshd_config', 'w')
            text = "".join(lines)
            f.write(text)
            f.close()

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
