# #project - CRUD opration

from  pathlib import Path
import os


def read_file_and_folder():
    try:
        p = Path('')
        item = list(p.rglob('*'))
        for index , file in enumerate(item):
            print(f'{index + 1} - {file}')
    except Exception as e:
        print(e)        



def create_file():
    try:
        read_file_and_folder()
        file_name = input("Enter your file name :- ")                                                                                                                   
        p = Path(file_name)
        if p.exists():
            print('File alredy exist')
        else:    
            with open(file_name,'w') as file:
                content = input("Enter your file content :- ")
                file.write(content)
                print('File Added')
    except Exception as e:
        print(e)      


              
def read_file():
    try:
        read_file_and_folder()
        file_name = input("Enter your file name :- ")
        p = Path(file_name)
        if p.exists():
            with open(file_name,'r') as file:
                print(file.read())
        else:
            print("File not exist")      
    except Exception as e:
        print(e)      

def updete_file():
    try:
        read_file_and_folder()
        file_name = input("Enter your file name to update : ")
        p = Path(file_name)

        if p.exists():
            print("Press 1 for overwrite")
            print("press 2 for append")

            choice = int(input("Enter your choice :- "))

            if choice == 1:
                with open(file_name,'w') as file:
                    content = input("Enter your content:- ")
                    file.write(content)
                print("File overwrite successfully")
                    
            elif choice == 2:
                with open(file_name,'a') as file:
                    content = input("Enter your content :-  ")
                    file.write(content)
                print("content append successfully") 

            else:
                print("Invalid choice")
 
        else:
            print("file not found")               
    except Exception as e:
        print(e)
        


def delete_file():
    try:
        read_file_and_folder()

        file_name = input("enter your file name:- ")
        # p = Path(file_name)

        if os.path.exists(file_name):
            os.remove(file_name)
            print("File deleted successfully")

        else:
            print("File not exist")
    except Exception as e:
        print(e)      



def rename_file():
    try:

        read_file_and_folder()

        old_name = input("Enter current file name:- ")
        p = Path(old_name)

        if p.exists():
            new_name = input("Enter new file name :- ")
            os.rename(old_name,new_name)
            
            print("file rename successfull")
        else:
            print("File not exist")

    except Exception as e:
        print(e)        



def creat_folder():
    try:
        folder_name = input("Enter a folder name :- ")
        p = Path(folder_name)

        # desktop_path = Path.home() / "OneDrive" / "Desktop" # show on Destop
        # p = desktop_path / folder_name

        if p.exists():
            print("Folder alredy exists")
        else:
            p.mkdir()
            print("Folder is created successfuly")   
    except Exception as e:
        print(e)         


def remove_folder():
    try:
        folder_name = input("Enter a folder name to remove :- ")
        p = Path(folder_name)

        if p.exists():
            p.rmdir()
            print("File is deleted successfully")
        else:
            print("Folder not exsist")    
    except Exception as e:
        print(e)        


def creat_file_in_folder():
    try:
        folder_name = input("Enter a folder name :- ")
        file_name = input("Enter file name:- ")
        p = Path(folder_name)/file_name
        if p.exists():
            print('File alredy exist')
        else:    
            with open(p,'w') as file:
                content = input("Enter your file content :- ")
                file.write(content)
                print('File Added')
    except Exception as e:
        print(e)             




while True:
    print("Press 1 for creating a file")
    print("Press 2 for reading a file")
    print("Press 3 for updateing file")
    print("Press 4 for deleting a file")
    print("Press 5 for rename a file")
    print("Press 6 for create folder")
    print("Press 7 for remove folder ")
    print("Press 8 for create file in folder :- ")
    print("Press 0 for break ")

    option = int(input("Enter your choice:- "))

    if option == 1:
        create_file()

    elif option == 2:
        read_file()

    elif  option == 3:
        updete_file()

    elif option == 4:
        delete_file()
    
    elif option == 5:
        rename_file()

    elif option == 6:
        creat_folder()    

    elif option == 7:
        remove_folder()    

    elif option == 8:
        creat_file_in_folder()    

    elif option == 0: 
        break
