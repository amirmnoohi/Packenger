from lib import *
import subprocess

__MAIN_DIR__ = os.getcwd()
__RUNNING_DIR__ = os.path.dirname(os.path.realpath(__file__))


def check_module_loaded():
    lsmod_proc = subprocess.Popen(['lsmod'], stdout=subprocess.PIPE)
    grep_proc = subprocess.Popen(['grep', "netmap"], stdin=lsmod_proc.stdout)
    grep_proc.communicate()  # Block until finished
    os.system("clear")
    return grep_proc.returncode == 0


def check_internet():
    import socket
    try:
        host = socket.gethostbyname("one.one.one.one")
        s = socket.create_connection((host, 80), 2)
        s.close()
        return True
    except OSError:
        pass
    return False


def download_files():
    os.system("clear")
    print(bcolors.OKBLUE + "[*] Downloading Dependencies" + bcolors.ENDC)
    os.system("sudo apt install git gcc g++ make python-dev -y")
    os.system("sudo rm -rf lib/netmap")
    os.system("sudo git clone https://git.noohi.org/amirmnoohi/netmap lib/netmap")
    os.system("clear")
    if not os.path.exists("lib/netmap"):
        print(bcolors.OKGREEN + "[+] Changed to Sudo Successfully" + bcolors.ENDC)
        print(bcolors.FAIL + "[-] Failed to Download Dependencies" + bcolors.ENDC)
        exit(0)
    print(bcolors.OKGREEN + "[+] Changed to Sudo Successfully" + bcolors.ENDC)
    print(bcolors.OKGREEN + "[+] Dependencies Downloaded successfully" + bcolors.ENDC)


def configure_files():
    print(bcolors.OKBLUE + "[*] Configuring Dependencies" + bcolors.ENDC)
    os.chdir("lib/netmap")
    os.system("sudo ./lib/netmap/LINUX/configure --select-version=ixgbe:5.7.1,i40e:2.11.29,e1000e:3.8.4")
    os.chdir(__RUNNING_DIR__)
    os.system("clear")
    print(bcolors.OKGREEN + "[+] Changed to Sudo Successfully" + bcolors.ENDC)
    print(bcolors.OKGREEN + "[+] Dependencies Downloaded successfully" + bcolors.ENDC)
    print(bcolors.OKGREEN + "[+] Dependencies Configured successfully" + bcolors.ENDC)


def install_files():
    print(bcolors.OKBLUE + "[*] Installing Dependencies" + bcolors.ENDC)
    os.chdir("lib/netmap/LINUX")
    os.system("make && sudo make install")
    os.chdir("../extra/python")
    os.system("make && sudo make install")
    os.chdir(__RUNNING_DIR__)
    os.system("clear")
    print(bcolors.OKGREEN + "[+] Changed to Sudo Successfully" + bcolors.ENDC)
    print(bcolors.OKGREEN + "[+] Dependencies Downloaded successfully" + bcolors.ENDC)
    print(bcolors.OKGREEN + "[+] Dependencies Configured successfully" + bcolors.ENDC)
    print(bcolors.OKGREEN + "[+] Dependencies Installed successfully" + bcolors.ENDC)


def load_kernel_module():
    print(bcolors.OKBLUE + "[*] Loading Kernel Module" + bcolors.ENDC)
    os.system("sudo insmod lib/netmap/LINUX/netmap.ko")
    # os.system("clear")
    print(bcolors.OKGREEN + "[+] Dependencies Downloaded successfully" + bcolors.ENDC)
    print(bcolors.OKGREEN + "[+] Dependencies Configured successfully" + bcolors.ENDC)
    print(bcolors.OKGREEN + "[+] Dependencies Installed successfully" + bcolors.ENDC)
    print(bcolors.OKGREEN + "[+] Kernel Module Loaded Successfully" + bcolors.ENDC)


def clearing():
    os.system("sudo cp lib/netmap/LINUX/netmap.ko .")
    os.system("sudo rm -rf lib/netmap")


def main():
    if __name__ == "__main__":
        if check_module_loaded():
            print(bcolors.WARNING + "[-] Module Netmap has already been loaded"
                                    " try to unload it then rerun the script again" + bcolors.ENDC)
            exit(0)
        check_internet()
        os.chdir(__RUNNING_DIR__)
        change_sudo()
        print(bcolors.OKGREEN + "[+] Changed to Sudo Successfully" + bcolors.ENDC)
        download_files()
        configure_files()
        install_files()
        load_kernel_module()
        clearing()
        os.chdir(__MAIN_DIR__)


main()
